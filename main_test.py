import pytest
import csv
import os
from main import Handle_Csv

@pytest.fixture(autouse=True)
def create_test_file():
    with open("data_test.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "brand", "price", "rating"])
        writer.writerow(["iphone 15 pro", "apple", "999", "4.9"])
        writer.writerow(["galaxy s23 ultra", "samsung", "1199", "4.8"])
        writer.writerow(["redmi note 12", "xiaomi", "199", "4.6"])
        writer.writerow(["poco x5 pro", "xiaomi", "299", "4.4"])
        writer.writerow(["poco x5 pro", "xiaomi", "299", "4.5"])
    with open("data_test_2.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "brand", "price", "rating"])
        writer.writerow(["iphone 15 pro", "apple", "999", "4.9"])
        writer.writerow(["galaxy s23 ultra", "samsung", "1199", "4.8"])
    with open("data_test_error.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "price", "rating"])
        writer.writerow(["iphone 15 pro", "apple", "999", "4.9"])
        writer.writerow(["galaxy s23 ultra", "samsung", "1199", "4.8"])
    with open("data_test_error_2.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow("")
    yield
    os.remove("data_test.csv")
    os.remove("data_test_2.csv")
    os.remove("data_test_error.csv")
    os.remove("data_test_error_2.csv")
    
    
@pytest.mark.parametrize("file, report, expected",
                        [
                            ([], "", False),
                            (["data_test.csv"], "", False),
                            ([],"average-rating", False),
                            (["data_test.csv"], "average-rating", True)
                        ])
def test_start(file, report, expected):
    pars = Handle_Csv(file, report)
    result = pars.start_main()
    assert result == expected
    
    
@pytest.mark.parametrize("file, report, expected",
                        [
                            (["sfsafas.csv"], "average-rating", False),
                            (["data_test_error.csv, data_test_2.csv,"], "average-rating", False),
                            (["data_test.csv", "data_test_2.csv"], "average-rating", True)
                        ])    
def test_check_file_exists(file, report, expected):
    pars = Handle_Csv(file, report)
    result = pars.check_file_exists()
    assert result == expected
    
    
@pytest.mark.parametrize("file, report, file_data, columns, expected",
                        [
                            ("data_test.csv", "average-rating", [], [], False),
                            ("data_test.csv", "average-rating", ["name", "brand", "price", "rating"], ["name", "brand", "price", "rating"], False),
                        ])
def test_check_rows(file, report, file_data, columns, expected):
    pars = Handle_Csv(file, report)
    pars.data_file = file_data
    pars.columns = columns
    result = pars.check_rows("data_test.csv")
    assert result == expected
@pytest.mark.parametrize("file, report, columns, expected",
                        [
                            ("data_test.csv", "average-rating", [], False),
                            ("data_test.csv", "average-rating", ["name", "brand", "price"], False),
                            ("data_test.csv", "average-rating", ["name", "brand", "price", "rating"], True)
                        ])
def test_check_column(file, report, columns, expected):
    pars = Handle_Csv(file, report)
    pars.columns = columns
    result = pars.check_column("data_test.csv")
    assert result == expected