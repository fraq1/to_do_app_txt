from datetime import datetime, date
from Storage_logic.txt_logic import TxtStorage
from copy import copy
from Business_logic.LogicErrors import TimeOverlapseError, InputFormatError

class TxtLogic:
    storage = TxtStorage()

    def validate_date(self, raw_date):
        try:
            year,month,day = map(int, raw_date.split())
            date(year, month, day)
            return [str(int(year)), f"{int(month):02d}", f"{int(day):02d}"]
        except Exception:
            raise InputFormatError(raw_date, "YYYY MM DD")

    def chose_or_create_day(self, date, filename):
        date_str = f"=== {date[0]}-{date[1]}-{date[2]} ==="
        notes = self.storage.read_day(filename, date_str)
        if  len(notes) == 0:
            self.storage.create_new_day(filename, date)
            notes.append(date_str)
        return notes

    def return_today_date(self):
        today = str(datetime.date(datetime.now())).split('-')
        return today

    @staticmethod
    def find_indexes(all_file, date_str):
        start_index = None
        end_index = None
        for index,line in enumerate(all_file):
            if line.rstrip("\n") == date_str:
                start_index = index
            elif line.startswith("===") and start_index is not None:
                end_index = index
                return start_index, end_index

    def find_insert_index(self, day_notes, time):
        fmt = "%H:%M"
        parse_time = time.split("-")
        if len(parse_time) != 2:
            raise InputFormatError(time, "HH:MM-HH:MM")
        try:
            user_start_time = datetime.strptime(parse_time[0], fmt).time()
            user_end_time = datetime.strptime(parse_time[1], fmt).time()
        except Exception:
            raise InputFormatError(time, "HH:MM-HH:MM")
        if user_start_time >= user_end_time:
            raise InputFormatError(f"{parse_time[0]}-{parse_time[1]}", "start time must be earlier than end time")

        for i in range(1, len(day_notes)):
            time_notes = day_notes[i].split()[0].split("-")
            notes_end_time = datetime.strptime(time_notes[1], fmt).time()
            notes_start_time = datetime.strptime(time_notes[0], fmt).time()
            if self.check_overlaps(user_start_time, notes_end_time, user_end_time, notes_start_time):
                raise TimeOverlapseError(time, time_notes)
            if user_end_time <= notes_start_time:
                return i

        return len(day_notes)

    @staticmethod
    def check_overlaps(user_start_time, notes_end_time, user_end_time, notes_start_time):
        overlaps = not (user_start_time >= notes_end_time or user_end_time <= notes_start_time)
        return overlaps

    def write_notes(self, insert_pos, filename, new_note, time, date, day_notes):
        time = time.split("-")
        new_day_notes = copy(day_notes)
        date_str = f"=== {date[0]}-{date[1]}-{date[2]} ==="
        new_day_notes.insert(insert_pos, f"{time[0]}-{time[1]} {new_note}")
        all_file = self.storage.read_all_file(filename)
        start_index, end_index = self.find_indexes(all_file, date_str)
        all_file[start_index:end_index] = [i + "\n" for i in new_day_notes]
        self.storage.write_all_lines(filename, all_file)