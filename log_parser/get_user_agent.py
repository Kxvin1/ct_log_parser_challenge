# fmt: off
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
                useragent_row.append(" ".join(quote_part)[1:-1].replace("\\" + quote_end, quote_end))
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


def convert_user_agent_to_dict_browser(filename: str) -> dict:
    user_agent_browser = {}

    with open(filename) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            result = extract_useragent(line)
            ua_string = result[8]
            user_agent = get_useragent_info(ua_string)
            user_agent_browser[index] = user_agent[0]

    return user_agent_browser



def convert_user_agent_to_dict_device(filename: str) -> dict:
    user_agent_device = {}

    with open(filename) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            result = extract_useragent(line)
            ua_string = result[8]
            user_agent = get_useragent_info(ua_string)
            user_agent_device[index] = user_agent[1]

    return user_agent_device
