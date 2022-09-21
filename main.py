# fmt: off

from collections import defaultdict
from logging import raiseExceptions
from timeit import default_timer as timer
from datetime import timedelta
from requests import get as ip_fetch
from csv import writer as csv_writer
from json import dumps

from log_parser.get_user_agent import convert_user_agent_to_list
from log_parser.other_headers import (
    get_api_status,
    get_date_and_time,
    get_method_header,
    get_url,
)
from log_parser.get_ips import get_ips
from log_parser.confirm_file_type import confirm_file_type


def find_user_info(ips_list, filename):
    confirm_file_type(filename)

    user_agent_info = convert_user_agent_to_list(filename)
    method_info = get_method_header(filename)
    api_status_info = get_api_status(filename)
    get_date_and_time_info = get_date_and_time(filename)
    get_url_info = get_url(filename)

    output = defaultdict(list)
    temp_list = []

    print(f"########################")
    print("Starting fetches...")
    print(f"########################\n")
    start = timer()

    for index, ip in enumerate(ips_list):
        try:
            response = ip_fetch(f"https://geolocation-db.com/json/{ip}").json()
        except:
            raise Exception(f"Could not fetch from https://geolocation-db.com/json/{ip}")

        formatted_response = dumps(response, indent=4)

        country_name = response["country_name"]
        state = response["state"]
        print(
            f"Fetched Response: \n {formatted_response} \n-- Progress: {index + 1}/{len(ips_list)}"
        )

        if state == None:
            state = "Not Found"

        temp_list.append(
            (
                ip,
                country_name,
                state,
                user_agent_info[index - 1],
                method_info[index - 1],
                api_status_info[index - 1],
                get_date_and_time_info[index - 1],
                get_url_info[index - 1],
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
        output[index].append(info)
    end = timer()

    print(f"########################")
    print(f"Finished creating dictionary after {timedelta(seconds=end-start)}.")
    print(f"########################\n")

    return output


def main(dict):
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
    main(find_user_info(get_ips(log_file), log_file))
