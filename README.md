# GenAIAgent

This project is a powerful, conversational AI agent built on Google's Generative AI API. It's designed to function as an "agent" by not only generating text but also by interacting with your local file system and executing code to solve complex, multi-step tasks.

The agent is equipped with a set of tools and a reasoning loop, allowing it to:

* Read and write files.

* List the contents of directories.

* Execute Python scripts.

* Chain these actions together to fulfill a single, complex user request.

🚀 Key Features

* File System Interaction: Read the contents of existing files or write new content to files (e.g., write_file('output.txt', 'Hello World')).

* Directory Navigation: List all files and folders within a specified directory to understand the project structure (list_directory('.')).

* Python Code Execution: Run Python (.py) files and receive their stdout and stderr output, enabling dynamic scripting and data processing (run_python_file('process_data.py')).

* Multi-Step Reasoning: The agent's core is its "feedback loop." It can receive a complex prompt (e.g., "Read 'data.txt', create a Python script to process it, run the script, and save the result to 'output.txt'"), plan a series of tool calls, execute them one by one, and use the results of each step to inform the next, until the final goal is achieved.

🛠️ How It Works

This agent uses the tool-calling (or function-calling) capabilities of the Google Generative AI API.

  * Prompt: The user provides a high-level goal.

  * Plan: The GenAI model analyzes the prompt and identifies the tools needed. It generates a "plan" which is a sequence of tool calls.

  * Execute: The agent's Python code executes the first tool call recommended by the model (e.g., read_file('data.txt')).

  * Feedback: The output of that tool (e.g., the content of data.txt) is sent back to the model as part of the ongoing conversation.

  * Re-plan: The model receives the tool's output, re-evaluates the original goal, and decides on the next step. This might be calling another tool (e.g., write_file('temp_script.py', ...)), or it might be a final response to the user.

  * Loop: Steps 3-5 repeat until the user's objective is fully accomplished.

**Warning**

Genai can sometimes misunderstand what you mean and change your code in unwanted ways. be sure to backup any file that it will be given access to. for security reasons I have constrained it's working directory to "[the folder Agent is installed]/calculator". you can easily change or completely remove it by changing it in the function_call.py.
