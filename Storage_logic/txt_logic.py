from Business_logic.Models.Note import Note
from datetime import date as d
from hashlib import sha256
import pickle
import os

class TxtStorage:
    def __init__(self):
        self.__filename = "tasks_for_days.txt"
        self.__filename_hash = self.__filename + '.hash'
        self.__filename_bac = self.__filename + '.bac'
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as file:
                file.write("")
        self.check_changes()

    def read_day(self, date):
        notes = []
        printing = False

        with open(self.__filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.rstrip("\n")
                if line == "" and printing:
                    break
                if line == date:
                    printing = True
                    continue
                if printing:
                    notes.append(Note.from_str(line))

        return notes

    def create_new_day(self, date):
        with open(self.__filename, "a", encoding="utf-8") as file:
            file.write(f"{date}\n")
            file.write("\n")

    def read_all_file(self):
        with open(self.__filename, "r", encoding="utf-8") as file:
            all_file = file.readlines()
            converted_file = dict()
            note_date = None
            for i in all_file:
                i = i.rstrip("\n")
                parts = i.split('-')
                if len(parts) == 3 and all(p.isdigit() for p in parts):
                    try:
                        year,month,day = map(int, i.split('-'))
                        d(year, month, day)
                        note_date = f"{str(int(year))}-{int(month):02d}-{int(day):02d}"
                        converted_file[note_date] = []
                        continue
                    except ValueError:
                        pass
                if not i:
                    continue
                if note_date is not None:
                    converted_file[note_date].append(Note.from_str(i))


            return converted_file

    def write_all_lines(self, all_file):
        convert_from_dict = list()
        for note_date in sorted(all_file.keys()):
            convert_from_dict.append(f"{note_date}\n")
            for note in all_file[note_date]:
                convert_from_dict.append(note.to_str() + "\n")
            convert_from_dict.append("\n")
        with open(self.__filename, "w", encoding="utf-8") as file:
            file.writelines(convert_from_dict)
        self.save_to_backup_file(convert_from_dict)

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
            self.save_to_backup_file([])
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
                    notes_from_backup = []
            with open(self.__filename, "w", encoding="utf-8") as file:
                file.writelines(notes_from_backup)

