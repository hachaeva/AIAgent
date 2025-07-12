import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python files given the specified file_path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to run, relative to the working directory. If it doesn't exist, print an error message.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path):
    try:
        relative_path = os.path.join(working_directory, file_path)
        if not os.path.isfile(relative_path):
            return f'Error: File "{file_path}" not found.'
        if not os.path.abspath(relative_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        run_result = subprocess.run(["python", relative_path], text=True, capture_output = True, timeout=30)
        first_return_line = f"Executing {relative_path}: "
        stdout_string = "STDOUT:"
        if run_result.stdout:
            stdout_string = stdout_string + " " +  run_result.stdout
        stderr_string = "STDERR:"
        if run_result.stderr:
            stderr_string = stderr_string + " " + run_result.stderr
        else:
            stderr_string = stderr_string + " "
        return_string = stdout_string + " " + stderr_string
        if run_result.returncode != 0:
            return first_return_line + return_string + " " + f"Process exited with code {run_result.returncode}."
        if not run_result.stdout and not run_result.stderr:
            return first_return_line + "No output produced."
        else:
            return first_return_line + return_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    return