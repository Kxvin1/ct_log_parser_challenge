from log_parser.get_ips import get_ips


def test_get_ips():
    res = get_ips("log-test.log")
    print(res)


test_get_ips()
