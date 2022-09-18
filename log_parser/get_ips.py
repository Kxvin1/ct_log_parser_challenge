from .confirm_file_type import confirm_file_type as cft


def get_ips(filename):
    """Read the log file and extract all the IP addresses

    Args:
        filename (file): the name of the file that contains the log

    Returns:
        list: A list of strings containing IP addresses
    """
    cft(filename)

    ip_address_list = []

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            ip_address = line.split()[0]
            ip_address_list.append(ip_address)

        return ip_address_list
