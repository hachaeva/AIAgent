import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

MODEL = "gemini-2.0-flash-001"
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    args = sys.argv
    user_prompt = ""

    if len(args) > 1:
        user_prompt = str(args[1])
    else:
        print ("Error: prompt message must be provided")
        exit(1)
    if len(args) > 2 and "--verbose" in args[2:]:
        verbose_flag = True
    else:
        verbose_flag = False
    print (f"verbose flag: {verbose_flag}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,schema_get_file_content,schema_run_python_file,schema_write_file
    ]
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    function_calls = response.function_calls
    if len(function_calls) > 0:
        for function_call in function_calls:
            #print (f"Calling function: {function_call.name}({function_call.args})")    
            function_call_result = call_function(function_call, verbose_flag)
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Expected a function call response")
            elif verbose_flag:
                print(f"-> {function_call_result.parts[0].function_response.response})")

    else:
        print (response.text)

    if (verbose_flag):
        print (f"User prompt: {user_prompt}")
        print (f"Prompt tokens: {prompt_tokens}")
        print (f"Response tokens: {response_tokens}")



if __name__ == "__main__":
    main()
    