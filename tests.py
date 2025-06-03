

from functions.get_file_content import get_file_content

if __name__ == "__main__":
    print("get_file_content('calculator', 'main.py'):")
    content_main = get_file_content("calculator", "main.py")
    print(content_main)
    print("\nget_file_content('calculator', 'pkg/calculator.py'):")
    content_pkg = get_file_content("calculator", "pkg/calculator.py")
    print(content_pkg)
    print("\nget_file_content('calculator', '/bin/cat'):")
    content_error = get_file_content("calculator", "/bin/cat")
    print(content_error)
