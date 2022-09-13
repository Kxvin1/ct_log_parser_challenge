from user_agents import parse
from collections import defaultdict

import re
import requests
import csv


def extract_useragent(s):
    """Parses the user agent string into a list of strings

    Args:
        s (str): the string to be parsed

    Returns:
        list: A list of strings
    """

    row = []
    qe = qp = None  # quote end character (qe) and quote parts (qp)
    for s in s.replace("\r", "").replace("\n", "").split(" "):
        if qp:
            qp.append(s)
        elif "" == s:  # blanks
            row.append("")
        elif '"' == s[0]:  # begin " quote "
            qp = [s]
            qe = '"'
        elif "[" == s[0]:  # begin [ quote ]
            qp = [s]
            qe = "]"
        else:
            row.append(s)

        l = len(s)
        if l and qe == s[-1]:  # end quote
            if l == 1 or s[-2] != "\\":  # don't end on escaped quotes
                row.append(" ".join(qp)[1:-1].replace("\\" + qe, qe))
                qp = qe = None
    return row


def get_useragent_info(ua_str):
    """The get_useragent_info function takes a user agent (ua) string and returns a tuple of browser, device type, and operating system

    Args:
        ua_str (str): The user agent string to parse

    Returns:
        tuple: A tuple of the browser, device type, and operating system
    """

    user_agent = parse(ua_str)
    browser = user_agent.browser.family
    os = "{}".format(user_agent.os.family)

    device_type = ""

    if user_agent.is_mobile:
        device_type = "Mobile"
    if user_agent.is_tablet:
        device_type = "Tablet"
    if user_agent.is_pc:
        device_type = "Desktop"
    if user_agent.is_bot:
        device_type = "Robot"

    device_type = "{}".format(device_type)

    return browser, device_type, os


def get_ips(filename):
    """Read the log file and extract all the IP addresses

    Args:
        filename (file): the name of the file that contains the log

    Returns:
        list: A list of strings containing IP addresses
    """

    with open(filename) as f:
        log = f.read()

        ip_address_regexp = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
        ip_address_list = re.findall(ip_address_regexp, log)

        return ip_address_list


def convert_user_agent_to_list(filename):
    """Read the log file and extracts all user agent info, specifically device and browser

    Args:
        filename (file): the name of the file that contains the log

    Returns:
        list: A list of strings containing the user agent info
    """

    user_agent_info = []

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            s = line
            result = extract_useragent(s)
            ua_string = result[8]
            user_agent = get_useragent_info(ua_string)
            user_agent_info.append(user_agent)

    return user_agent_info


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


def find_user_info(ips_list, filename):
    """Takes in a list of IP addresses and a file (expects a log file).
    It then iterates through the list of IP addresses and uses the user_agent_info list to find the device and browser used.
    Then it uses the ips_list list to find the country name and state of the IP address.
    Uses helper functions to add data to the final dictionary output.

    Args:
        ips_list (list): the list of IP addresses we want to track
        filename (file): the name of the file that contains the logs

    Returns:
        dictionary: A dictionary with the key being the index of the IP address in the list of IP addresses.
        The value is a list of tuples. Each tuple contains the IP address, country name, state, and user agent info (device and browser)
    """

    user_agent_info = convert_user_agent_to_list(filename)
    method_info = get_method_header(filename)
    api_status_info = get_api_status(filename)
    get_date_and_time_info = get_date_and_time(filename)
    get_url_info = get_url(filename)

    output = defaultdict(list)
    temp_list = []

    for index, ip in enumerate(ips_list):
        response = requests.get(f"https://geolocation-db.com/json/{ip}").json()
        country_name = response["country_name"]
        state = response["state"]

        if state == None:
            state = "Not Found"

        temp_list.append(
            (
                ip,
                country_name,
                state,
                user_agent_info[index - 1],
                method_info[index - 1],
                api_status_info[index - 1],
                get_date_and_time_info[index - 1],
                get_url_info[index - 1],
            )
        )

    for index, info in enumerate(temp_list):
        output[index].append(info)

    return output


def export_to_csv(dict):
    """Takes a dictionary and their associated information and exports it to a CSV file

    Args:
        dict (dictionary): the dictionary to be exported to csv
    """

    with open("output.csv", "w") as csvfile:
        writer = csv.writer(csvfile)

        headers = [
            "IP",
            "Country Name",
            "State",
            "Browser",
            "Device",
            "Method",
            "Status Code",
            "Date and Time",
            "URL",
        ]

        writer.writerow(headers)

        for item in dict.items():
            ip = item[1][0][0]
            country_name = item[1][0][1]
            state = item[1][0][2]
            user_agent_browser = item[1][0][3][0]
            user_agent_device = item[1][0][3][1]
            method = item[1][0][4]
            status_code = item[1][0][5]
            date_and_time = item[1][0][6]
            url = item[1][0][7]

            writer.writerow(
                (
                    ip,
                    country_name,
                    state,
                    user_agent_browser,
                    user_agent_device,
                    method,
                    status_code,
                    date_and_time,
                    url,
                )
            )


# runs file
if __name__ == "__main__":
    export_to_csv(find_user_info(get_ips("log2.log"), "log2.log"))