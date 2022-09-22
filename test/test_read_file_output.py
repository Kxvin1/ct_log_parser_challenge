from ..log_parser.read_file import read_file


def test_read_file_output():
    log_input = {
        "ip": ["207.114.153.6"],
        "browser": ["Chrome"],
        "device": ["Desktop"],
        "method": ["GET"],
        "api_status_code": ["200"],
        "date_and_time": ["10/Jun/2015:18:14:56"],
        "url": ["http://www.gobankingrates.com/banking/find-cds-now/"],
    }
    assert read_file("./log_files/log-test.log") == log_input
