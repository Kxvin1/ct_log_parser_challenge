def is_valid_file(filename: str) -> bool:
    if not isinstance(filename, str):
        print("------------------------------------")
        print(f"Filetype of {type(filename)} not accepted.")
        print("------------------------------------")
        raise TypeError("The file must be of type string")

    check_extension = filename.split(".")[-1]

    if check_extension != "log":
        print("------------------------------------")
        print(f'".{check_extension}" extension not accepted.')
        print("------------------------------------")
        raise TypeError("The file must have an extension of .log")
