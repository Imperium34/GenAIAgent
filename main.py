import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
from functions import function_call
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_file
from functions.function_call import call_function



def main():
    load_dotenv()
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_file,
    ]
    )
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read files content
    - Write or overwrite files
    - Run python files with optional arguments

    If there is non-text parts in your response don't anounce it. instead put this at the start of your text response '0_0'
    When you are done with users original request say '\nFinal Result:\n' at the very start and give user your final answer regarding their question.
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    When asked to do anything in the current directory isntead of 'None' make the directory variable '.'
    """
    if len(sys.argv) < 2:
        print("no argument given. exiting with code 1")
        exit(1)
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]

    i = 0
    while i <= 20:
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),
        )
        if not response.candidates == None:
            if len(response.candidates) > 0:
                for candidate in response.candidates:
                    for part in candidate.content.parts:
                        print(part)
                        if not (part, "function_call") == None:
                            messages.append(candidate.content)


        verbose = False
        if "--verbose" in sys.argv:

            verbose = True
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
            print("User prompt:", sys.argv[1])

        response_calls = response.function_calls
        if not response_calls == None:
            if len(response_calls) > 0:
                for call in response_calls:
                    func = call.name
                    print(f"Calling function: {func}({call.args})")
                    funct = call_function(call)
                    result_obj = funct.parts[0].function_response.response

                    result_str = funct.parts[0].function_response.response.get("result", "")
                    user_function_call = types.Content(role="user", parts=[types.Part(function_response={"name": func, "response": result_obj,})])
                    messages.append(user_function_call)

                    if verbose == True:
                        print("-->", result_str)
        if not response.text == None:
            if "Final Result:" in response.text:
                print(response.text)
                break

        i += 1
    if i == 20:
        print("STDERR: Max depth reached or encountered an error. \nplease try again with a diffirent prompt")

if __name__ == "__main__":
    main()  