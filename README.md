# Gemini Function Calling with LangChain

This project is a demonstration of how to implement function calling (also known as tool use) using Google's Gemini Pro model within the LangChain framework. It provides a clear, minimal example of how to equip a large language model with custom Python functions to perform specific tasks.

## Core Concept

The fundamental idea is to give an LLM access to external tools. When the model receives a user query, it can determine if it needs to use one of its tools to provide an accurate answer. 

This script follows a simple agent-like loop:
1.  The user provides a prompt (e.g., "What is 5 times 12?").
2.  The model, recognizing the need for a calculation, responds with a request to call the `multiply` function with the arguments `{'a': 5, 'b': 12}`.
3.  The script executes the actual Python `multiply` function.
4.  The result (`60`) is sent back to the model.
5.  The model uses this result to formulate the final, human-readable answer.

## Project Structure

```
.llm-function-calling/
├── .env                # Stores the Google API Key
├── langchain_function_calling.py # The main script
├── requirements.txt    # Project dependencies
└── README.md           # This file
```

## Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites

- A modern version of Python (3.7+ recommended).
- A Google API Key. You can obtain one from the [Google AI Studio](https://aistudio.google.com/app/apikey).

### 1. Set Up Your Environment

Create a `.env` file in the root of the project directory to store your API key:

```.env
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

### 2. Install Dependencies

This project uses `uv` for fast dependency management. If you don't have `uv`, you can install it or use `pip`.

```bash
# Create and activate a virtual environment
uv venv
source .venv/bin/activate

# Install the required packages
uv pip install -r requirements.txt
```

### 3. Run the Script

Execute the script from your terminal:

```bash
python langchain_function_calling.py
```

## Example Execution

The script will run through a few examples, demonstrating how the model uses the `add` and `multiply` tools.

```
User: What is 5 + 3?
Model wants to call tool 'add' with args {'a': 5, 'b': 3}
Tool Output: 8
Sending tool output back to the model for final response...
LLM: 8
------------------------------
User: What is 12 * 5 and then add 10 to the result?
Model wants to call tool 'multiply' with args {'a': 12, 'b': 5}
Tool Output: 60
Sending tool output back to the model for final response...
Model wants to call tool 'add' with args {'a': 60, 'b': 10}
Tool Output: 70
Sending tool output back to the model for final response...
LLM: 70
------------------------------
User: Hi, Who are you?
LLM: I am a large language model, trained by Google.
```
