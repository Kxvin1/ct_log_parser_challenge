def get_ips(filename):
    ip_address_list = []

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            ip_address = line.split()[0]
            ip_address_list.append(ip_address)

        return ip_address_list
