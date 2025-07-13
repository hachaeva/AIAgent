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

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,schema_get_file_content,schema_run_python_file,schema_write_file
    ]
    )

    num_responses = 0
    prompt_tokens = 0
    response_tokens = 0

    done = False
    
    response = []

    while num_responses < 20 and not done:
        try:
            response.append(
                client.models.generate_content(
                    model=MODEL,
                    contents=messages,
                    config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
                )
            )
            
            prompt_tokens = prompt_tokens + response[num_responses].usage_metadata.prompt_token_count
            response_tokens = response_tokens + response[num_responses].usage_metadata.candidates_token_count

            for candidate in response[num_responses].candidates:
                for part in candidate.content.parts:
                    if part.text:
                        print(part.text)
                if candidate.content:
                    messages.append(candidate.content)

            function_calls = response[num_responses].function_calls
            if function_calls:
                for function_call in function_calls:  
                    function_call_result = call_function(function_call, verbose_flag)
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception("Expected a function call response")
                    else:
                        messages.append(types.Content(role="tool", parts=function_call_result.parts)) 
                        if verbose_flag: 
                            print(f"-> {function_call_result.parts[0].function_response.response})")
            else:
                break

            num_responses = num_responses + 1

        except Exception as e:
            print(f"Error: function call failed")
            return f"Error: function call failed"

    if (verbose_flag):
        print (f"User prompt: {user_prompt}")
        print (f"Prompt tokens: {prompt_tokens}")
        print (f"Response tokens: {response_tokens}")

if __name__ == "__main__":
    main()
    