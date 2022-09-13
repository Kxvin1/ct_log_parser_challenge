import re

from .confirm_file_type import confirm_file_type as cft


def get_ips(filename):
    """Read the log file and extract all the IP addresses

    Args:
        filename (file): the name of the file that contains the log

    Returns:
        list: A list of strings containing IP addresses
    """
    cft(filename)

    with open(filename) as f:
        log = f.read()

        ip_address_regexp = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
        ip_address_list = re.findall(ip_address_regexp, log)

        return ip_address_list
