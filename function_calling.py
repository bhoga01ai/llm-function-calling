import yfinance as yf
from dotenv import load_dotenv
load_dotenv()
import os
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

# import vertexai
# gcp_access_token=os.getenv('gcp_access_token')
# from google.oauth2 import credentials
# cred=credentials.Credentials(token=gcp_access_token)
# print(cred)
# vertexai.init(project='applied-shade-440515-d2',credentials=cred)

from google.genai import types
from google import genai

client = genai.Client()
MODEL='gemini-2.5-flash'

# Function to Get Stock Price
def get_stock_price(parameters: dict) -> dict:
    ticker = parameters['ticker']
    print(ticker)
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d")
    if not hist.empty:
        return {"price": str(hist['Close'].iloc[-1])}
    else:
        return {"error": "No data available"}

# Function to get temperature
def get_temperature(parameters:dict) -> str:
    city=parameters['city']
    return "It's always Sunny in " + city

# Function declaration 
stocks_function_declaration = {
    "name": "get_stock_price",
    "description": "Get the current stock price of a given company",
    "parameters": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "Stock ticker symbol"
            }
        }
    }
}
temperature_function_declaration = {
    "name": "get_temperature",
    "description": "Get the current temperature in a given city",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name"
            }
        }
    }
}

# Map function names to their actual function objects
available_functions = {
    "get_stock_price": get_stock_price,
    "get_temperature": get_temperature,
}


tools = types.Tool(function_declarations=[stocks_function_declaration, temperature_function_declaration])
config = types.GenerateContentConfig(tools=[tools],temperature=0.5)

while True:
    query=input("user:")
    if not query.lower()=='exit':
        # first LLM call
        response = client.models.generate_content(
            model=MODEL,
            contents=query,
            config=config
        )

        # Check for a function call
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            print(f"Function to call: {function_call.name}")
            print(f"Arguments: {function_call.args}")
            #  In a real app, you would call your function here:
            args = {key: value for key, value in function_call.args.items()}
            print(args)
            if args:
                # Look up the function in the dictionary and call it
                function_to_call = available_functions.get(function_call.name)
                if function_to_call:
                    function_response = function_to_call(args) # Call with the dictionary of arguments
                    print(function_response)
                    if function_response:
                        ## Final LLM call
                        response = client.models.generate_content(
                            model=MODEL,
                            contents=query + str(function_response)
                        )
                else:
                    print(f"Function '{function_call.name}' not found in available functions.")

            else:
                print("No arguments found for the function.")

        else:
            print("No function call found in the response.")
            print(response.text)
    else:
        break
