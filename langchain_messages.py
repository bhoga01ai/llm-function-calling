# STEP1 : LOAD ENV variables
from dotenv import load_dotenv
load_dotenv()


# step 2 : import required modules
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from langchain.tools import StructuredTool
from langchain.chat_models import init_chat_model

# step 3 : initialize the model
model = init_chat_model(model='gemini-2.5-flash-lite',model_provider='google-genai',temperature=.6)

# step4 : create the conversation
messages=[]
sys_msg = SystemMessage(content="You are a helpful assistant.")
messages.append(sys_msg)

# hum_msg=HumanMessage(content="what is the meaning of life.")
# messages.append(hum_msg)

# ai_msg = model.invoke(messages)
# messages.append(AIMessage(content=ai_msg.content))
# #print(ai_msg.content)
# print(messages)

#step 5. define tools
def add(a:float, b:float):
    """Adds two numbers."""
    return a*3 + b*3

def sub(a:float, b:float):
    """Subtracts two numbers."""
    return a*3 - b*3

tools = [
    StructuredTool.from_function(
        func=add,
        name="add",
        description="Adds two numbers."
    ),
    StructuredTool.from_function(
        func=sub,
        name="sub",
        description="Subtracts two numbers."
    )
]

# step 6 : bind the tools to the model
model_with_tools = model.bind_tools(tools)

# step 7 : 1ST llm call 
prompt="what is two + three"
respone=model_with_tools.invoke(prompt)
messages.append(respone)
print(messages)

# step 8 : tool execution
print("---------------")
print(messages[-1].tool_calls)

fun_name=messages[-1].tool_calls[0]['name']
print(fun_name)
fun_args=messages[-1].tool_calls[0]['args']
print(fun_args)

# We need to use the actual function implementation, not the decorated tool
# Extract the values from the arguments
a_value = float(fun_args['a'])
b_value = float(fun_args['b'])

print(a_value,b_value)
# Call the function implementation directly
if fun_name == 'add':
    # The implementation of add is: return a*3 + b*3
    fun_response = add(a_value, b_value)
    print(fun_response)
    messages.append(ToolMessage(content=str(fun_response), tool_call_id=messages[-1].tool_calls[0]['id']))
    print(messages)
    #step 9 : 2ND llm cal
   
    final_prompt=prompt + " and the result is " + str(fun_response)
    respone=model.invoke(final_prompt)
    messages.append(respone)
    print("----output from tool and not from lLM pre-training----")
    print(respone.content)
    # print(messages[-1])
else:
    print(f"Unknown funtcion:{fun_name} ")