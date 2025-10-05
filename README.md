# Gemini Function Calling

This project demonstrates function calling (tool use) with Google's Gemini Pro model. It shows how to give a large language model access to custom Python functions to perform tasks.

## Core Concept

The main idea is to let an LLM use external tools. When the model gets a user query, it can decide if it needs a tool to answer.

The script follows an agent-like loop:
1.  The user gives a prompt (e.g., "What is 5 times 12?").
2.  The model sees it needs to calculate and asks to call the `multiply` function with `{'a': 5, 'b': 12}`.
3.  The script runs the Python `multiply` function.
4.  The result (`60`) is sent back to the model.
5.  The model uses this result to give a final, human-readable answer.

## Project Structure

```
.llm-function-calling/
├── main.py             # The main script
├── requirements.txt    # Project dependencies
└── README.md           # This file
```

## Getting Started

Follow these instructions to get the project running.

### Prerequisites

- A modern version of Python (3.7+ recommended).
- A Google API Key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 1. Set Up Your Environment

Set your Google API key as an environment variable:

```bash
export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

### 2. Install Dependencies

This project uses `uv` for fast dependency management. If you don't have `uv`, you can use `pip`.

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
python main.py
```

## Example Execution

The script will run examples showing how the model uses the `add` and `multiply` tools.

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