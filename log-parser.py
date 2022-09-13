# fmt: off

# 1. open log file, read content, and find the following:
# -- ip addresses
# -- useragent
# 2. find country and state using the ip addresses
# 3. translate the useragent to device type (mobile, tablet, desktop) and browser (safari, chrome, etc)
# 4. combine new geo field (country/state) and device field with existing fields on access log file and output/export as a CSV

from collections import defaultdict
import re
import requests
import csv


def reader(filename):
    with open(filename) as f:
        log = f.read()

        ip_address_regexp = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
        ip_address_list = re.findall(ip_address_regexp, log)

        return ip_address_list


def find_country_state(ips_list):
    output = defaultdict(list)
    temp_list = []

    for ip in ips_list:
        response = requests.get(f"https://geolocation-db.com/json/{ip}").json()
        country_name = response["country_name"]
        state = response["state"]

        if state == None:
            state = "Not Found"

        temp_list.append( (ip, country_name, state) )


    for index, info in enumerate(temp_list):
        output[index].append(info)


    return output


def useragent_converter(useragent):
    pass

def export_to_csv(dict):
    with open('output.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)

        header = ["IP", "Country Name", "State"]

        writer.writerow(header)

        for item in dict.items():
            ip = item[1][0][0]
            country_name = item[1][0][1]
            state = item[1][0][2]

            writer.writerow( (ip, country_name, state) )


# run file
if __name__ == "__main__":
    export_to_csv(find_country_state(reader("log2.log")))
