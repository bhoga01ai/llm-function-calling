# create a simple bot with geminin model
from dotenv import load_dotenv
load_dotenv()

from google import genai
client= genai.Client()
#prompt ='who are you?'
while(True):
    prompt = input('user: ')
    if prompt == 'exit':
        break
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[prompt]
    )
    print(response.text)

# using Langchain.