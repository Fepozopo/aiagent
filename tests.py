from functions.overwrite_file import overwrite_file

if __name__ == "__main__":
    result1 = overwrite_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result1)

    result2 = overwrite_file(
        "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
    )
    print(result2)

    result3 = overwrite_file(
        "calculator", "/tmp/temp.txt", "this should not be allowed"
    )
    print(result3)
