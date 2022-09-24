# fmt: off

from timeit import default_timer as timer
from datetime import timedelta
from requests import get
from csv import writer as csv_writer
from json import dumps

from log_parser.file_checker import is_valid_file
from log_parser.read_file import read_file

STATE = "Not Found"

class CreateCSV:
    def __init__(self, filename):
        self.filename = filename

    def get_log_data(self) -> dict:
        dict_with_info = read_file(self.filename)

        ip = dict_with_info["ip"]
        ua_browser = dict_with_info["browser"]
        ua_device = dict_with_info["device"]
        method_info = dict_with_info["method"]
        api_status_info = dict_with_info["api_status_code"]
        get_date_and_time_info = dict_with_info["date_and_time"]
        get_url_info = dict_with_info["url"]

        output = {
            "browser": ua_browser,
            "device": ua_device,
            "method": method_info,
            "api_status_code": api_status_info,
            "date_and_time":get_date_and_time_info,
            "url": get_url_info,
            "ip": ip,
        }

        return output


    def find_user_info(self) -> list:

        is_valid_file(self.filename)
        log_data = self.get_log_data()

        user_info_output = []
        user_info_storage = []

        print(f"########################")
        print("Starting fetches...")
        print(f"########################\n")
        start = timer()

        ips_list = log_data["ip"]
        for index in range(len(ips_list)):
            ip = log_data["ip"][index]
            browser = log_data["browser"][index]
            device = log_data["device"][index]
            method = log_data["method"][index]
            api_status = log_data["api_status_code"][index]
            date_and_time = log_data["date_and_time"][index]
            url = log_data["url"][index]

            try:
                response = get(f"https://geolocation-db.com/json/{ip}").json()
            except:
                raise Exception(f'Error 500: Data for "{ip}" not able to be retrieved at https://geolocation-db.com/json/{ip} \nExiting program...')

            formatted_response = dumps(response, indent=4)

            country_name = response["country_name"]
            STATE = response["state"]
            print(f"Fetched Response: \n {formatted_response} \n-- Progress: {index + 1}/{len(ips_list)}")

            user_info_storage.append(
                (
                    ip,
                    country_name,
                    STATE,
                    browser,
                    device,
                    method,
                    api_status,
                    date_and_time,
                    url,
                )
            )
            print(f"\nAdded to output.\n")

        end = timer()
        print(f"########################")
        print(f"Finished fetching and storing data after {timedelta(seconds=end-start)}")
        print(f"########################\n")

        print(f"########################")
        print(f"Starting list creation...")
        print(f"########################\n")

        start = timer()
        for user_info in user_info_storage:
            user_info_output.append(user_info)
        end = timer()

        print(f"########################")
        print(f"Finished creating list after {timedelta(seconds=end-start)}.")
        print(f"########################\n")

        return user_info_output


    def main(self):
        user_info_list = self.find_user_info()

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
log_file = "./log_files/log2.log"
new_csv = CreateCSV(log_file)

if __name__ == "__main__":
    new_csv.main()
