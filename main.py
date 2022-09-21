# fmt: off

from collections import defaultdict
from timeit import default_timer as timer
from datetime import timedelta
from requests import get as ip_fetch
from csv import writer as csv_writer
from csv import DictWriter as dict_writer
from json import dumps

from log_parser.get_user_agent import convert_user_agent_to_dict
from log_parser.other_headers import (
    get_api_status,
    get_date_and_time,
    get_method_header,
    get_url,
)
from log_parser.get_ips import get_ips
from log_parser.confirm_file_type import confirm_file_type

STATE = "Not Found"

def get_log_info(filename: str) -> list:
    user_agent_info = convert_user_agent_to_dict(filename)
    method_info = get_method_header(filename)
    api_status_info = get_api_status(filename)
    get_date_and_time_info = get_date_and_time(filename)
    get_url_info = get_url(filename)

    output = [user_agent_info, method_info, api_status_info, get_date_and_time_info, get_url_info]
    return output

def find_user_info(ips_dict: dict[str, str], filename: str) -> dict:

    confirm_file_type(filename)
    log_data = get_log_info(filename)

    output = {}
    temp_list = []

    print(f"########################")
    print("Starting fetches...")
    print(f"########################\n")
    start = timer()

    for index, ip in enumerate(ips_dict):
        try:
            response = ip_fetch(f"https://geolocation-db.com/json/{ips_dict[ip]}").json()
        except:
            raise Exception(f"Could not fetch from https://geolocation-db.com/json/{ips_dict[ip]}")

        formatted_response = dumps(response, indent=4)

        country_name = response["country_name"]
        STATE = response["state"]
        print(f"Fetched Response: \n {formatted_response} \n-- Progress: {index + 1}/{len(ips_dict)}")

        temp_list.append(
            (
                ips_dict[ip],
                country_name,
                STATE,
                log_data[0][index],
                log_data[1][index],
                log_data[2][index],
                log_data[3][index],
                log_data[4][index],
            )
        )
        print(f"\nAdded to list.\n")

    end = timer()
    print(f"########################")
    print(f"Finished fetching and storing data after {timedelta(seconds=end-start)}")
    print(f"########################\n")

    print(f"########################")
    print(f"Starting dictionary creation...")
    print(f"########################\n")

    start = timer()
    for index, info in enumerate(temp_list):
        if index not in output:
            output[index] = []
        output[index].append(info)
    end = timer()

    print(f"########################")
    print(f"Finished creating dictionary after {timedelta(seconds=end-start)}.")
    print(f"########################\n")

    return output


def main():
    dict = find_user_info(get_ips(log_file), log_file)

    with open("output.csv", "w") as csvfile:
        writer = csv_writer(csvfile)

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

        print(f"########################")
        print(f"Starting writes to csv...")
        print(f"########################\n")
        start = timer()


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
    end = timer()
    print(f"########################")
    print(f"Finished writing to csv after {timedelta(seconds=end-start)}.")
    print(f"########################")


### EDIT LOG FILE HERE
log_file = "./log_files/log2.log"


if __name__ == "__main__":
    main()
