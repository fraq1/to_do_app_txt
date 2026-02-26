import json
from Business_logic.Models.Note import Note

class JsonStorage:
    def __init__(self):
        self.filename = "tasks_for_days.json"


    def read_day(self, date):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
                    with open(self.filename, "w", encoding="utf-8") as file:
                        json.dump(data, file, indent=4, ensure_ascii=False)
                notes = [Note.from_dict(i) for i in data.get(date, [])]
        except FileNotFoundError:
            data = {}
            notes = []
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        return notes

    def create_new_day(self, date):
        all_file = self.read_all_file()
        all_file[date] = []
        self.write_all_lines(all_file)


    def read_all_file(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            all_file = json.load(file)
            all_file_obj = {key: [Note.from_dict(n) for n in value] for key, value in all_file.items()}
            return all_file_obj

    def write_all_lines(self, all_file):
        with open(self.filename, "w", encoding="utf-8") as file:
            all_file_dict = {key: [n.to_dict() for n in value] for key, value in all_file.items()}
            json.dump(all_file_dict, file, indent=4, ensure_ascii=False)