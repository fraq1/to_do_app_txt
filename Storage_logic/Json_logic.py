import hashlib
import json
from json import JSONDecodeError

from Business_logic.Models.Note import Note
from hashlib import sha256
import pickle
import os

class JsonStorage:
    def __init__(self):
        self.__filename = "tasks_for_days.json"
        self.__filename_hash = self.__filename + '.hash'
        self.__filename_bac = self.__filename + '.bac'
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump({}, file, indent=4, ensure_ascii=False)
        self.check_changes()

    def read_day(self, date):
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except JSONDecodeError:
                    data = []
                notes = [Note.from_dict(i) for i in data.get(date, [])]
        except FileNotFoundError:
            data = {}
            notes = []
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        return notes

    def create_new_day(self, date):
        all_file = self.read_all_file()
        all_file[date] = []
        self.write_all_lines(all_file)


    def read_all_file(self):
        with open(self.__filename, "r", encoding="utf-8") as file:
            try:
                all_file = json.load(file)
            except JSONDecodeError:
                all_file = {}
        all_file_obj = {key: [Note.from_dict(n) for n in value] for key, value in all_file.items()}
        return all_file_obj

    def write_all_lines(self, all_file):
        with open(self.__filename, "w", encoding="utf-8") as file:
            all_file_dict = {key: [n.to_dict() for n in value] for key, value in all_file.items()}
            json.dump(all_file_dict, file, indent=4, ensure_ascii=False)
        self.save_to_backup_file(all_file_dict)

    def save_to_backup_file(self, notes):
        with open(self.__filename_bac, "wb") as file:
            pickle.dump(notes, file)
        with open(self.__filename, "rb") as file:
            file_bytes = file.read()
        notes_file_hash = sha256(file_bytes).hexdigest()
        with open(self.__filename_hash, "w") as file:
            file.write(notes_file_hash)


    def check_changes(self):
        if not os.path.exists(self.__filename_hash):
            self.save_to_backup_file({})
            return
        with open(self.__filename, "rb") as file:
            tested_file_bytes = file.read()
        tested_file_hash = sha256(tested_file_bytes).hexdigest()
        with open(self.__filename_hash, "r") as file:
            notes_file_hash = file.read()
        if notes_file_hash != tested_file_hash:
            with open(self.__filename_bac, "rb") as file:
                try:
                    notes_from_backup = pickle.load(file)
                except Exception:
                    notes_from_backup = {}
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump(notes_from_backup, file, indent=4, ensure_ascii=False)





