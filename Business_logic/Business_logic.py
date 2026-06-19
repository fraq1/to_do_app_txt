from datetime import datetime, date, time
from Storage_logic.Json_logic import JsonStorage
from Storage_logic.txt_logic import TxtStorage
from copy import copy
from Business_logic.Models.Note import Note
from Business_logic.Models.User import User
from Business_logic.LogicErrors import TimeOverlapseError, InputFormatError
from Storage_logic_v2.SQLite_logic import SQLiteDB

class BusinessLogic:
    def __init__(self, storage) -> None:
        self.storage = storage

    @staticmethod
    def parse_time(value:str) -> time:
        value = value.strip()
        value = value.replace(" ", ":")
        value = value.replace(";", ":")
        value = value.replace("-", ":")
        fmt = "%H:%M"
        try:
            parsed_time = datetime.strptime(value, fmt).time()
        except ValueError:
            raise InputFormatError(f"{value}", "\nThe correct format is HH:MM. For example 10:00 or 10 00\n")
        return parsed_time

    @staticmethod
    def check_time_order(start_time: time, end_time: time) -> None:
        if start_time >= end_time:
            raise InputFormatError(f"{start_time}-{end_time}", "\nStart time must be earlier than end time\n")

    @staticmethod
    def validate_date(raw_date: str) -> date:
        try:
            parts = raw_date.split()
            if len(parts) != 3:
                raise InputFormatError(raw_date, "\nThe correct format is YYYY MM DD. For example 2026 10 10\n")
            year, month, day = map(int, parts)
            if len(str(year)) != 4:
                raise InputFormatError(raw_date, "\nThe year must be 4 digits\n")
            return date(year, month, day)
        except ValueError:
            raise InputFormatError(raw_date, "\nThe correct format is YYYY MM DD. For example 2026 10 10.\n")

    def chose_or_create_day(self, day_date: date, telegram_id) -> list[Note]:
        user_id = self.storage.get_user_id(telegram_id)
        date_id = self.storage.get_or_create_date(day_date, user_id)
        notes = self.storage.get_notes_by_date_id(date_id)
        return notes

    @staticmethod
    def return_today_date() -> date:
        today = datetime.date(datetime.now())
        return today

    def check_valid_time(self, day_notes: list[Note], start_time: time, end_time: time, exclude_note_id=None):
        for i in range(0, len(day_notes)):
            if exclude_note_id and day_notes[i].note_id == exclude_note_id:
                continue
            if self.check_overlaps(start_time, day_notes[i].end_time, end_time, day_notes[i].start_time):
                raise TimeOverlapseError(f"{start_time}-{end_time}", f"{day_notes[i].start_time}-{day_notes[i].end_time}")

    @staticmethod
    def check_overlaps(user_start_time: time, notes_end_time: time, user_end_time: time, notes_start_time: time) -> bool:
        overlaps = not (user_start_time >= notes_end_time or user_end_time <= notes_start_time)
        return overlaps

    def write_notes(self, new_text: str, start_time: time, end_time: time, day_date: str, telegram_id) -> None:
        new_note = Note(None, start_time, end_time, new_text)
        user_id = self.storage.get_user_id(telegram_id)
        date_id = self.storage.get_or_create_date(day_date, user_id)
        self.storage.create_note(date_id, new_note)


    def edit_notes_text(self, note_id: int, new_note: str) -> None:
        self.storage.update_note_text(note_id, new_note)

    def edit_notes_time(self, note_id: int, start_time: time, end_time: time) -> None:
        self.storage.update_note_time(note_id, start_time, end_time)

    def delete_note(self, note_id) -> None:
        self.storage.delete_note(note_id)

    def register_or_ignore_user(self, telegram_id, username):
        new_user = User(username, telegram_id)
        self.storage.register_user(new_user)

    def find_user_id(self, telegram_id):
        return self.storage.get_user_id(telegram_id)

