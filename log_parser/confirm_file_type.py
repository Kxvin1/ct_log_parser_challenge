def confirm_file_type(filename):
    confirm_file_type = filename.split(".")

    if confirm_file_type[-1] != "log":
        raise TypeError("The file must have an extension of .log")
