from Business_logic.Models.Note import Note
from datetime import date as d

class TxtStorage:
    def __init__(self):
        self.filename = "tasks_for_days.txt"

    def read_day(self, date):
        notes = []
        printing = False

        with open(self.filename, "r", encoding="utf-8") as file:
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
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(f"{date}\n")
            file.write("\n")

    def read_all_file(self):
        with open(self.filename, "r", encoding="utf-8") as file:
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
        with open(self.filename, "w", encoding="utf-8") as file:
            file.writelines(convert_from_dict)

