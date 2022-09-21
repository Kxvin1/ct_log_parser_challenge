# fmt: off
def get_method_header(filename):
    method_dict = {}

    with open(filename) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            method = line.split()[5][1:]  # slice [1:] to remove the " at the front
            method_dict[index] = method

    return method_dict


def get_api_status(filename):
    api_status_dict = {}

    with open(filename) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            api_status_code = line.split()[8]
            api_status_dict[index] = api_status_code

    return api_status_dict


def get_date_and_time(filename):
    date_and_time_dict = {}

    with open(filename) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            date_and_time = line.split()[3][1:]  # slice [1:] to remove the [ at the front
            date_and_time_dict[index] = date_and_time

    return date_and_time_dict


def get_url(filename):
    url_dict = {}

    with open(filename) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            url = line.split()[10][1:-1]  # slice [1:-1] to remove quotes from start and end
            if url == "-":
                url_dict[index] = "Empty URL"
            else:
                url_dict[index] = url

    return url_dict
