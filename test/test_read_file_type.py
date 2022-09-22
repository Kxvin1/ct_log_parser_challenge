def test_read_file_type():
    log_input = "./log_files/log-test.log"
    test_for_str_log_input = {"str": "str input is valid"}

    assert type(log_input) == type(test_for_str_log_input["str"])
