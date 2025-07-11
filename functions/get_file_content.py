import os
from google.genai import types

MAX_CHARS = 10000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of files given the working directory and file name, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory. If it doesn't exist, print an error message.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        relative_path = os.path.join(working_directory, file_path)
        if not os.path.isfile(relative_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        if not os.path.abspath(relative_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        with open(relative_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                file_content_string = file_content_string + f'...File "{file_path}" truncated at {MAX_CHARS} characters'
        return file_content_string
    except Exception as e:
        return e