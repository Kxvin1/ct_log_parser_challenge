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
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def get_log_data(self) -> dict[str, str]:
        dict_with_info = read_file(self.filename)

        output = {
            "browser": dict_with_info.get("browser", "Not Found"),
            "device": dict_with_info.get("device", "Not Found"),
            "method": dict_with_info.get("method", "Not Found"),
            "api_status_code": dict_with_info.get("api_status_code", "Not Found"),
            "date_and_time":dict_with_info.get("date_and_time", "Not Found"),
            "url": dict_with_info.get("url", "Not Found"),
            "ip": dict_with_info.get("ip", "Not Found"),
        }

        return output


    def find_user_info(self) -> list[str]:
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

            response = get(f"https://geolocation-db.com/json/{ip}").json()

            formatted_response = dumps(response, indent=4)
            print(f"Fetched Response: \n {formatted_response} \n-- Progress: {index + 1}/{len(ips_list)}")

            country_name = response["country_name"]
            STATE = response["state"]

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


    def main(self) -> None:
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
