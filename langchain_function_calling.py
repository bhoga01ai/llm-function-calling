
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Ensure the GOOGLE_API_KEY is set
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# --- 1. Define the Python Functions ---

def add(a, b):
    """Adds two numbers."""
    return a + b

def multiply(a, b):
    """Multiplies two numbers."""
    return a * b

# --- 2. Set up the Model and Tools ---

# Wrap the functions into LangChain tools
tools = [
    StructuredTool.from_function(
        func=add,
        name="add",
        description="Adds two numbers."
    ),
    StructuredTool.from_function(
        func=multiply,
        name="multiply",
        description="Multiplies two numbers."
    ),
]

# Initialize the Google Generative AI model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
# Bind the tools to the model
llm_with_tools = llm.bind_tools(tools)

# Create a mapping from tool name to the actual tool object
tool_map = {tool.name: tool for tool in tools}
print(tool_map)
# --- 3. Create the Agent/Chain Logic ---

def run_conversation(query):
    """
    Runs a conversation with the model, handling tool calls as they arise.
    """
    print("User: {}".format(query))

    # Start the conversation with the user's query
    messages = [HumanMessage(query)]

    # Invoke the model
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

    # --- 4. Handle Tool Calls ---
    if ai_msg.tool_calls:
        for tool_call in ai_msg.tool_calls:
            print("Model wants to call tool '{}' with args {}".format(tool_call['name'], tool_call['args']))
            selected_tool = tool_map.get(tool_call["name"])
            if selected_tool:
                tool_output = selected_tool.invoke(tool_call["args"])
                print("Tool Output: {}".format(tool_output))
                messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))
            else:
                print("Error: Tool '{}' not found.".format(tool_call['name']))

        # --- 5. Get Final Response ---
        print("Sending tool output back to the model for final response...")
        final_response = llm_with_tools.invoke(messages)
        print("LLM with tools response: {}".format(final_response.content))
    else:
        # If no tool calls, the first response is the final one
        print("LLM with no tools response: {}".format(ai_msg.content))


# --- Example Usage ---
if __name__ == "__main__":
    run_conversation("What is 5 + 3?")
    print("-" * 30)
    run_conversation("What is 4 multiplied by 7?")
    print("-" * 30)
    run_conversation("What is 12 * 5 and then add 10 to the result?")
    print("-" * 30)
    run_conversation("What is 12 plus 5 ?")
    print("-" * 30)
    run_conversation("Hi, Who are you?")
