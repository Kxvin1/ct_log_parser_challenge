def get_ips(filename):
    ip_address_list = {}

    with open(filename) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            ip_address = line.split()[0]
            ip_address_list[index] = ip_address

        return ip_address_list
