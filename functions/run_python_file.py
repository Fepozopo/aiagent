import os


def run_python_file(working_directory, file_path):
    import subprocess

    try:
        abs_working_directory = os.path.abspath(working_directory)

        # If file_path is absolute, use as is; if relative, join with working_directory
        if os.path.isabs(file_path):
            abs_file_path = os.path.abspath(file_path)
        else:
            abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if the file exists
        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        # Check if the file is a Python file
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        try:
            result = subprocess.run(
                ["python", abs_file_path],
                cwd=abs_working_directory,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            return "Error: executing Python file: Process timed out after 30 seconds."
        except Exception as e:
            return f"Error: executing Python file: {e}"

        output_lines = []
        if result.stdout:
            output_lines.append(f"STDOUT:\n{result.stdout.strip()}")
        if result.stderr:
            output_lines.append(f"STDERR:\n{result.stderr.strip()}")
        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")
        if not output_lines:
            return "No output produced."
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error: executing Python file: {e}"
