# fmt: off

from timeit import default_timer as timer
from datetime import timedelta
from requests import get as ip_fetch
from csv import writer as csv_writer
from json import dumps

from log_parser.get_user_agent import convert_user_agent_to_dict_device, convert_user_agent_to_dict_browser
from log_parser.other_headers import (
    get_api_status,
    get_date_and_time,
    get_method_header,
    get_url,
)
from log_parser.get_ips import get_ips
from log_parser.confirm_file_type import confirm_file_type

STATE = "Not Found"


def get_log_data(filename: str) -> list:
    ua_browser = convert_user_agent_to_dict_browser(filename)
    ua_device = convert_user_agent_to_dict_device(filename)
    method_info = get_method_header(filename)
    api_status_info = get_api_status(filename)
    get_date_and_time_info = get_date_and_time(filename)
    get_url_info = get_url(filename)

    output = [
        ua_browser,
        ua_device,
        method_info,
        api_status_info,
        get_date_and_time_info,
        get_url_info,
    ]

    return output


def find_user_info(ips_dict: dict[str, str], filename: str) -> list:

    confirm_file_type(filename)
    log_data = get_log_data(filename)

    user_info_output = []
    user_info_storage = []

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

        user_info_storage.append(
            (
                ips_dict[ip],
                country_name,
                STATE,
                log_data[0][index],
                log_data[1][index],
                log_data[2][index],
                log_data[3][index],
                log_data[4][index],
                log_data[5][index],
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
    for index, user_info in enumerate(user_info_storage):
        user_info_output.append(user_info)
    end = timer()

    print(f"########################")
    print(f"Finished creating dictionary after {timedelta(seconds=end-start)}.")
    print(f"########################\n")

    return user_info_output


def main():
    user_info_list = find_user_info(get_ips(log_file), log_file)

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

        for user_info in user_info_list:
            writer.writerow(user_info)

        end = timer()
        print(f"########################")
        print(f"Finished writing to csv after {timedelta(seconds=end-start)}.")
        print(f"########################")


### EDIT LOG FILE HERE
log_file = "./log_files/log-test.log"


if __name__ == "__main__":
    main()
