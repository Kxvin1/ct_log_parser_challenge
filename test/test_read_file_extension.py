def test_read_file_extension() -> bool:
    log_input = "./log_files/log-test.log"
    test_for_log_extension = ".log"

    assert log_input[-4:] == test_for_log_extension
