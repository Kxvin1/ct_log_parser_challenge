from user_agents import parse


def extract_useragent(ua_string: str) -> list:
    useragent_row = []
    quote_end = None
    quote_part = None

    for ua_string in ua_string.replace("\r", "").replace("\n", "").split(" "):
        if quote_part:
            quote_part.append(ua_string)
        elif "" == ua_string:  # blanks
            useragent_row.append("")
        elif '"' == ua_string[0]:  # begin " quote "
            quote_part = [ua_string]
            quote_end = '"'
        elif "[" == ua_string[0]:  # begin [ quote ]
            quote_part = [ua_string]
            quote_end = "]"
        else:
            useragent_row.append(ua_string)

        len_of_string = len(ua_string)

        if len_of_string and quote_end == ua_string[-1]:
            if len_of_string == 1 or ua_string[-2] != "\\":
                useragent_row.append(
                    " ".join(quote_part)[1:-1].replace("\\" + quote_end, quote_end)
                )
                quote_end = None
                quote_part = None
    return useragent_row


def get_useragent_info(ua_str: str) -> tuple[str, str, str]:
    # parse the user agent string
    user_agent = parse(ua_str)
    # get the browser family
    browser = user_agent.browser.family
    # get the device type
    device_type = ""
    if user_agent.is_mobile:
        device_type = "Mobile"
    elif user_agent.is_tablet:
        device_type = "Tablet"
    elif user_agent.is_pc:
        device_type = "Desktop"
    elif user_agent.is_bot:
        device_type = "Robot"
    # get the operating system
    os = str(user_agent.os.family)
    device_type = str(device_type)
    # return a tuple of the three values
    return browser, device_type, os


# Read the data from the file and store in dictionary
def read_file(filename: str) -> dict[str, list]:
    output = {
        "ip": [],
        "browser": [],
        "device": [],
        "method": [],
        "api_status_code": [],
        "date_and_time": [],
        "url": [],
    }

    # Open the file in read mode
    with open(filename) as file:
        # Loop through each line in the file
        for line in file:
            # Extract the user agent string from each line
            ua_result = extract_useragent(line)
            ua_string = ua_result[8]
            # Get the user agent info from the user agent string
            user_agent = get_useragent_info(ua_string)

            # Add the IP to the output dictionary
            output["ip"].append(line.split()[0])
            # Add the browser to the output dictionary
            output["browser"].append(user_agent[0])
            # Add the device to the output dictionary
            output["device"].append(user_agent[1])
            # Add the method to the output dictionary
            output["method"].append(line.split()[5][1:])
            # Add the API status code to the output dictionary
            output["api_status_code"].append(line.split()[8])
            # Add the date and time to the output dictionary
            output["date_and_time"].append(line.split()[3][1:])
            # Add the URL to the output dictionary
            url = line.split()[10][1:-1]
            if url == "-":
                url = "Empty URL"
            else:
                url = url
            output["url"].append(url)

    return output
