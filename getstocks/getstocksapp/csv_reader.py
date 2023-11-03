from glob import glob
import csv
from .models import Ticker

class FileCSV:
    def __init__(
            self,
            id,
            filepath,
            filename = None,

        ):
        self.id = id
        self.filepath = filepath
        self.filename = filename
        if self.filename is None:
            self.filename = filepath.rsplit("\\", 1)[-1]
        self.filecontent = None


    def open_file(self):
        with open(self.filepath, encoding='utf-8') as stream:
            self.filecontent = csv.DictReader(stream)
    

    def get_list(self):
        if self.filecontent:
            return [position for position in self.filecontent]
        else:
            print ("No content")
    

    def open_and_get(self):
        with open(self.filepath, encoding='utf-8') as stream:
            self.filecontent = csv.DictReader(stream)
            tickers = [position for position in self.filecontent]
        return tickers


def select_id(files: FileCSV):
    ids = [file.id for file in files]
    while True:
        selected_id = input("Please select number of file you need to operate on: ")
        if selected_id in ids:
            return selected_id
        else:
            print ("ID incorrect, try again.")

def create_filecsv_objects(files: list[str]) -> list[FileCSV]:
    objects = []
    counter = 0
    for position in files:
        counter += 1
        file = FileCSV(id=counter, filepath=position)
        objects.append(file)


def search_for_csv_files() -> list[str]:
    filelist = glob("getstocks\\getstocksapp\\csv_files\\*.csv")
    return filelist


def open_csv_file(filename: str) -> list[dict]:
    with open(filename,encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        tickers = [position for position in reader]
    return tickers


def form_filename(filename: str, suffix: str) -> str:
    pure_name, extension = filename.rsplit(".")
    new_name = f"{pure_name}_{suffix.lower()}.{extension}"
    return new_name


def main():
    files = search_for_csv_files()

    print ("Following files has been found:")
    counter = 0
    for position in files:
        counter += 1
        file = FileCSV(counter, position)
        print (f"{file.id}. {file.filename}")

    choosen_id = select_id(files)

if __name__ == "__main__":
    main()