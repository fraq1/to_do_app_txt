from datetime import datetime, date
from Storage_logic.Json_logic import JsonStorage
from Storage_logic.txt_logic import TxtStorage
from copy import copy
from Business_logic.Models.Note import Note
from Business_logic.LogicErrors import TimeOverlapseError, InputFormatError

class JsonLogic:
    def __init__(self, storage):
        self.storage = storage

    def validate_time(self, raw_time):
        fmt = "%H:%M"
        parse_time = raw_time.split("-")
        if len(parse_time) != 2:
            raise InputFormatError(raw_time, "HH:MM-HH:MM")
        try:
            user_start_time = datetime.strptime(parse_time[0], fmt).time()
            user_end_time = datetime.strptime(parse_time[1], fmt).time()
        except Exception:
            raise InputFormatError(raw_time, "HH:MM-HH:MM")
        if user_start_time >= user_end_time:
            raise InputFormatError(f"{parse_time[0]}-{parse_time[1]}", "start time must be earlier than end time")

    def validate_date(self, raw_date):
        try:
            year,month,day = map(int, raw_date.split())
            date(year, month, day)
            return f"{str(int(year))}-{int(month):02d}-{int(day):02d}"
        except Exception:
            raise InputFormatError(raw_date, "YYYY MM DD")

    def chose_or_create_day(self, day_date):
        notes = self.storage.read_day(day_date)
        if  len(notes) == 0:
            self.storage.create_new_day(day_date)
            notes = []
        return notes

    def return_today_date(self):
        today = str(datetime.date(datetime.now()))
        return today

    def find_insert_index(self, day_notes, time):
        fmt = "%H:%M"
        parse_time = time.split("-")
        user_start_time = datetime.strptime(parse_time[0], fmt).time()
        user_end_time = datetime.strptime(parse_time[1], fmt).time()
        for i in range(0, len(day_notes)):
            notes_start_time = datetime.strptime(day_notes[i].start_time, fmt).time()
            notes_end_time = datetime.strptime(day_notes[i].end_time, fmt).time()
            if self.check_overlaps(user_start_time, notes_end_time, user_end_time, notes_start_time):
                raise TimeOverlapseError(time, f"{notes_start_time}-{notes_end_time}")
            if user_end_time <= notes_start_time:
                return i

        return len(day_notes)

    @staticmethod
    def check_overlaps(user_start_time, notes_end_time, user_end_time, notes_start_time):
        overlaps = not (user_start_time >= notes_end_time or user_end_time <= notes_start_time)
        return overlaps

    def write_notes(self, insert_pos, new_note, time, day_date, day_notes):
        time = time.split("-")
        new_day_notes = copy(day_notes)
        new_day_notes.insert(insert_pos, Note(time[0], time[1], new_note))
        all_file = self.storage.read_all_file()
        all_file[day_date] = new_day_notes
        self.storage.write_all_lines(all_file)

    def edit_notes_text(self, note_index, new_note, day_date):
        notes =self.storage.read_day(day_date)
        notes[note_index].text = new_note
        all_file = self.storage.read_all_file()
        all_file[day_date] = notes
        self.storage.write_all_lines(all_file)

    def edit_notes_time(self, note_index, new_time, day_date, insert_pose, day_notes):
        notes =self.storage.read_day(day_date)
        old_note_text = notes[note_index].text
        insert_pose = self.find_insert_index(day_notes, new_time)
        self.write_notes(insert_pose, old_note_text, new_time, day_date, day_notes)


    def delete_note(self, note_index, day_date):
        notes = self.storage.read_day(day_date)
        notes.pop(note_index)
        all_file = self.storage.read_all_file()
        all_file[day_date] = notes
        self.storage.write_all_lines(all_file)

    def migrate_notes(self, old_storage: JsonStorage | TxtStorage, new_storage: JsonStorage | TxtStorage):
        log_for_migrated_notes = {}
        old_notes = old_storage.read_all_file()
        new_notes = new_storage.read_all_file()
        for date_str, notes_for_date in old_notes.items():
            if date_str not in new_notes.keys():
                new_notes[date_str] = notes_for_date
                log_for_migrated_notes[date_str] = notes_for_date
            else:
                for old_note in notes_for_date:
                    if old_note not in new_notes[date_str]:

                        try:
                            insert_index = self.find_insert_index(new_notes[date_str], f"{old_note.start_time}-{old_note.end_time}")
                            new_notes[date_str].insert(insert_index, old_note)
                            if date_str not in log_for_migrated_notes:
                                log_for_migrated_notes[date_str] = []
                            log_for_migrated_notes[date_str].append(old_note)
                        except TimeOverlapseError:
                            continue
        new_storage.write_all_lines(new_notes)
        return log_for_migrated_notes

