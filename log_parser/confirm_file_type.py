def confirm_file_type(filename):
    if not isinstance(filename, str):
        raise TypeError("The file must be of type string")

    if filename.split(".")[-1] != "log":
        raise TypeError("The file must have an extension of .log")
