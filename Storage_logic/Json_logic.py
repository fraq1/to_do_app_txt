import json
import os
from json import JSONDecodeError
from Business_logic.Models.Note import Note
from Storage_logic.Storage import Storage


class JsonStorage(Storage):
    def __init__(self):
        super().__init__("tasks_for_days.json")
        if not os.path.exists(self._filename):
            with open(self._filename, "w", encoding="utf-8") as file:
                json.dump({}, file, indent=4, ensure_ascii=False)
        self.check_changes()

    def read_day(self, date: str) -> list[Note]:
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except JSONDecodeError:
                    data = {}
            return [Note.from_dict(i) for i in data.get(date, [])]
        except FileNotFoundError:
            with open(self._filename, "w", encoding="utf-8") as file:
                json.dump({}, file, indent=4, ensure_ascii=False)
            return []

    def create_new_day(self, date: str):
        all_file = self.read_all_file()
        all_file[date] = []
        self.write_all_lines(all_file)

    def read_all_file(self) -> dict[str, list[Note]]:
        with open(self._filename, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except JSONDecodeError:
                data = {}
        return {key: [Note.from_dict(n) for n in value] for key, value in data.items()}

    def write_all_lines(self, all_file: dict[str, list[Note]]):
        all_file_dict = {key: [n.to_dict() for n in value] for key, value in all_file.items()}
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(all_file_dict, file, indent=4, ensure_ascii=False)
        self.save_to_backup_file(all_file_dict)

    def check_changes(self):
        if self._hash_changed():
            backup = self._get_backup({})
            with open(self._filename, "w", encoding="utf-8") as file:
                json.dump(backup, file, indent=4, ensure_ascii=False)
            self.save_to_backup_file(backup)
