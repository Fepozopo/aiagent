from functions.run_python_file import run_python_file

if __name__ == "__main__":
    result1 = run_python_file("calculator", "main.py")
    print("run_python_file('calculator', 'main.py') result:")
    print(result1)
    print()

    result2 = run_python_file("calculator", "tests.py")
    print("run_python_file('calculator', 'tests.py') result:")
    print(result2)
    print()

    result3 = run_python_file("calculator", "../main.py")
    print("run_python_file('calculator', '../main.py') result:")
    print(result3)
    print()

    result4 = run_python_file("calculator", "empty.py")
    print("run_python_file('calculator', 'empty.py') result:")
    print(result4)
