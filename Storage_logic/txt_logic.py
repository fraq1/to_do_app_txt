import os
from datetime import date as d
from Business_logic.Models.Note import Note
from Storage_logic.Storage import Storage


class TxtStorage(Storage):
    def __init__(self):
        super().__init__("tasks_for_days.txt")
        if not os.path.exists(self._filename):
            with open(self._filename, "w", encoding="utf-8") as file:
                file.write("")
        self.check_changes()

    def read_day(self, date: str) -> list[Note]:
        notes = []
        printing = False
        with open(self._filename, "r", encoding="utf-8") as file:
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

    def create_new_day(self, date: str):
        with open(self._filename, "a", encoding="utf-8") as file:
            file.write(f"{date}\n\n")

    def read_all_file(self) -> dict[str, list[Note]]:
        with open(self._filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
        result = {}
        note_date = None
        for line in lines:
            line = line.rstrip("\n")
            parts = line.split('-')
            if len(parts) == 3 and all(p.isdigit() for p in parts):
                try:
                    year, month, day = map(int, parts)
                    d(year, month, day)
                    note_date = f"{year}-{month:02d}-{day:02d}"
                    result[note_date] = []
                    continue
                except ValueError:
                    pass
            if line and note_date is not None:
                result[note_date].append(Note.from_str(line))
        return result

    def write_all_lines(self, all_file: dict[str, list[Note]]):
        lines = []
        for note_date in sorted(all_file.keys()):
            lines.append(f"{note_date}\n")
            for note in all_file[note_date]:
                lines.append(note.to_str() + "\n")
            lines.append("\n")
        with open(self._filename, "w", encoding="utf-8") as file:
            file.writelines(lines)
        self.save_to_backup_file(lines)

    def check_changes(self):
        if self._hash_changed():
            backup = self._get_backup([])
            with open(self._filename, "w", encoding="utf-8") as file:
                file.writelines(backup)
            self.save_to_backup_file(backup)
