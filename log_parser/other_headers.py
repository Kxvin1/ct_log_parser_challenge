def get_method_header(filename):
    """Read the log file and extract all the methods (get/post)

    Args:
        filename (file): the name of the file that contains the log

    Returns:
        list: A list of strings containing methods
    """

    method_list = []

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            method = line.split()[5][1:]  # slice [1:] to remove the " at the front
            method_list.append(method)

    return method_list


def get_api_status(filename):
    """Read the log file and extract all the api status codes (200, 204, etc)

    Args:
        filename (file): the name of the file that contains the log

    Returns:
        list: A list of strings containing the status codes
    """
    api_status_list = []

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            api_status_code = line.split()[8]
            api_status_list.append(api_status_code)

    return api_status_list


def get_date_and_time(filename):
    """Read the log file and extract all the dates and times

    Args:
        filename (file): the name of the file that contains the log

    Returns:
        list: A list of strings containing the dates and times
    """

    date_and_time_list = []

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            date_and_time = line.split()[3][
                1:
            ]  # slice [1:] to remove the [ at the front
            date_and_time_list.append(date_and_time)

    return date_and_time_list


def get_url(filename):
    """Read the log file and extracts all the urls

    Args:
        filename (file): the name of the file that contains the log

    Returns:
        list: A list of strings containing the urls
    """

    url_list = []

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            url = line.split()[10][
                1:-1
            ]  # slice [1:-1] to remove quotes from start and end
            if url == "-":
                url_list.append("Empty URL")
            else:
                url_list.append(url)

    return url_list
