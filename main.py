import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

MODEL = "gemini-2.0-flash-001"

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

    response = client.models.generate_content(model=MODEL, contents=messages)
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    print (response.text)

    if (verbose_flag):
        print (f"User prompt: {user_prompt}")
        print (f"Prompt tokens: {prompt_tokens}")
        print (f"Response tokens: {response_tokens}")



if __name__ == "__main__":
    main()
    