import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Runs python files given the specified file_path, constrained to the working directory. and the content to write to the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory. If it doesn't exist, print an error message.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        relative_path = os.path.join(working_directory, file_path)
        if not os.path.abspath(relative_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        with open(relative_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return e
    
    return