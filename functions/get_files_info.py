import os

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = working_directory

    abs_working_directory = os.path.abspath(working_directory)

    # If directory is absolute, use as is; if relative, join with working_directory
    if os.path.isabs(directory):
        abs_directory = os.path.abspath(directory)
        display_directory = directory
    else:
        abs_directory = os.path.abspath(os.path.join(working_directory, directory))
        display_directory = os.path.join(working_directory, directory)

    if not abs_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'

    directory_contents = list_directory_contents(abs_directory)
    return f"Directory: {display_directory}\nContents:\n{directory_contents}"
    

def list_directory_contents(directory_path):
    try:
        entries = os.listdir(directory_path)
        result_lines = []

        for entry in entries:
            entry_path = os.path.join(directory_path, entry)
            is_dir = os.path.isdir(entry_path)
            try:
                file_size = os.path.getsize(entry_path) if not is_dir else 0
            except Exception as e:
                file_size = "unknown"
            result_lines.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(result_lines)
    
    except Exception as e:
        return f"Error: {str(e)}"