import os

def get_files_info(working_directory, directory=None):
    try:
        relative_path = os.path.join(working_directory, directory)
        if not os.path.isdir(relative_path):
            return f'Error: "{directory}" is not a directory'
        if not os.path.abspath(relative_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        return "\n".join(sorted(list(map(lambda x: f"- {x}: file_size={str(os.path.getsize(relative_path+"/"+x))}, is_dir={str(os.path.isdir(relative_path+"/"+x))})",os.listdir(relative_path)))))
    
    except Exception as e:
        return e
