import csv
import argparse
from tabulate import tabulate

class Handle_Csv():
    
    def __init__(self, files_list, repor):
        self.files_list = files_list
        self.repor = repor
        self.columns = None
        self.error_files = []
        self.all_data = []
        self.data_file = []
        self.response = {}

    def print_table(self):
        count = 1
        rows = []
        for key, val in self.response.items():
            rows.append((count, key, (sum(val) / len(val))))
            count += 1
        sorted_by_brand = sorted(rows, key=lambda x: x[0])
        print(f"Files error {self.error_files}")
        print(tabulate(sorted_by_brand, headers=(["id", "brand", "rating"]), tablefmt="grid"))
        return
    
    def report(self):
        for val in self.all_data:
            if val.get("brand") in self.response:
                self.response[val.get("brand")].append(float(val.get("rating")))
            else:
                self.response[val.get("brand")] = [float(val.get("rating"))]
        return
                
    def add_data(self):
        for val in self.data_file:
            self.all_data.append(val)                
        return
    
    def check_column(self, file: str) -> bool: 
        if "rating" in self.columns and "brand" in self.columns:
            return True
        self.error_files.append(file)
        return False

    def check_rows(self, file: str) -> bool:
        if not self.data_file:
            print("No rows found in the CSV file.")
            self.error_files.append(file)
            return False
        self.columns = [o for o in self.data_file[0]]
        status = self.check_column(file)
        if not status:
            return False
        return True
        
    def check_file_exists(self) -> bool:
        for file in self.files_list:
            try:
                with open(file, 'r') as file:
                    reader = csv.DictReader(file)
                    self.data_file = []
                    for row in reader:
                        self.data_file.append(row)
            except FileNotFoundError:
                print(f"File '{file}' not found.")
                return False
            except Exception as e:
                print(f"Error reading file: {e}")
                return False
            status = self.check_rows(file)
            if status:
                self.add_data()
        if len(self.error_files) == len(self.files_list):
            print("No valid CSV files found.")
            return False
        self.report()
        self.print_table()
        return True

    def start_main(self) -> bool:
        if not self.files_list:
            print("No CSV files provided.")
            return False
        if not self.repor or self.repor != "average-rating":
            print("No report file provided.")
            return False
        self.check_file_exists()
        return True
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="*")
    parser.add_argument("--report")
    args = parser.parse_args()
    pars = Handle_Csv(args.files, args.report)
    pars.start_main()