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


def get_useragent_info(ua_str: str) -> tuple:
    user_agent = parse(ua_str)
    browser = user_agent.browser.family
    os = str(user_agent.os.family)

    device_type = ""
    if user_agent.is_mobile:
        device_type = "Mobile"
    elif user_agent.is_tablet:
        device_type = "Tablet"
    elif user_agent.is_pc:
        device_type = "Desktop"
    elif user_agent.is_bot:
        device_type = "Robot"

    device_type = str(device_type)

    return browser, device_type, os


def read_file(filename: str) -> dict:
    output = {
        "browser": [],
        "device": [],
        "method": [],
        "api_status_code": [],
        "date_and_time": [],
        "url": [],
        "ip": [],
    }

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            ip = line.split()[0]
            output["ip"].append(ip)

            method = line.split()[5][1:]
            output["method"].append(method)

            api_status_code = line.split()[8]
            output["api_status_code"].append(api_status_code)

            date_and_time = line.split()[3][1:]
            output["date_and_time"].append(date_and_time)

            url = line.split()[10][1:-1]
            if url == "-":
                url = "Empty URL"
            else:
                url = url
            output["url"].append(url)

            ua_result = extract_useragent(line)
            ua_string = ua_result[8]
            user_agent = get_useragent_info(ua_string)
            user_agent_browser = user_agent[0]
            output["browser"].append(user_agent_browser)
            user_agent_device = user_agent[1]
            output["device"].append(user_agent_device)

    return output
