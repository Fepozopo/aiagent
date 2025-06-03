import os

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)

    # If file_path is absolute, use as is; if relative, join with working_directory
    if os.path.isabs(file_path):
        abs_file_path = os.path.abspath(file_path)
        display_file_path = file_path
    else:
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        display_file_path = os.path.join(working_directory, file_path)

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file_path, 'r') as file:
            content = file.read()
        if len(content) > 10000:
            content = content[:10000] + f"\n[...File \"{file_path}\" truncated at 10000 characters]"
        return f"File: {display_file_path}\nContent:\n{content}"
    except Exception as e:
        return f"Error: Unable to read file: {str(e)}"