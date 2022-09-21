import unittest

from log_parser.get_ips import get_ips
from log_parser.other_headers import (
    get_method_header,
    get_api_status,
    get_date_and_time,
    get_url,
)

from log_parser.get_user_agent import (
    convert_user_agent_to_list,
    extract_useragent,
    get_useragent_info,
)


class TestFilename(unittest.TestCase):
    """
    Test the functions:
    1. get_ips
    2. get_method_header
    3. get_api_status
    4. get_date_and_time
    5. get_url
    6. convert_user_agent_to_list
    7. extract_useragent
    8. get_useragent_info
    """

    def test_get_ips(self):
        res = get_ips("./log_files/log-test.log")
        self.assertEqual(res, ["207.114.153.6"])

    def test_get_method_header(self):
        res = get_method_header("./log_files/log-test.log")
        self.assertEqual(res, ["GET"])

    def test_get_api_status(self):
        res = get_api_status("./log_files/log-test.log")
        self.assertEqual(res, ["200"])

    def test_get_date_and_time(self):
        res = get_date_and_time("./log_files/log-test.log")
        self.assertEqual(res, ["10/Jun/2015:18:14:56"])

    def test_get_url(self):
        res = get_url("./log_files/log-test.log")
        self.assertEqual(res, ["http://www.gobankingrates.com/banking/find-cds-now/"])

    def test_convert_user_agent_to_list(self):
        res = convert_user_agent_to_list("./log_files/log-test.log")
        self.assertEqual(res, [("Chrome", "Desktop", "Windows")])

    def test_extract_useragent(self):
        test_string = '207.114.153.6 - - [10/Jun/2015:18:14:56 +0000] "GET /favicon.ico HTTP/1.1" 200 0 "http://www.gobankingrates.com/banking/find-cds-now/" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"'
        res = extract_useragent(test_string)
        self.assertEqual(
            res,
            [
                "207.114.153.6",
                "-",
                "-",
                "10/Jun/2015:18:14:56 +0000",
                "GET /favicon.ico HTTP/1.1",
                "200",
                "0",
                "http://www.gobankingrates.com/banking/find-cds-now/",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/43.0.2357.81 Safari/537.36",
            ],
        )

    def test_get_useragent_info(self):
        test_ua_string = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"
        res = get_useragent_info(test_ua_string)
        self.assertEqual(res, ("Chrome", "Desktop", "Windows"))


if __name__ == "__main__":
    unittest.main()
