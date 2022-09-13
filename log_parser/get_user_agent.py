from user_agents import parse


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
