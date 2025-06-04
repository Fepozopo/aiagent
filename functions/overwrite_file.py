import os


def overwrite_file(working_directory, file_path, content):
    try:
        abs_working_directory = os.path.abspath(working_directory)

        # If file_path is absolute, use as is; if relative, join with working_directory
        if os.path.isabs(file_path):
            abs_file_path = os.path.abspath(file_path)
        else:
            abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Ensure parent directory exists
        parent_dir = os.path.dirname(abs_file_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        # Write content to file (overwrite)
        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} bytes written)'

    except Exception as e:
        return f"Error: {str(e)}"
