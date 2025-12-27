from datetime import datetime
from Storage_logic.txt_logic import TxtStorage
from copy import copy

class TxtLogic:
    storage = TxtStorage()

    def chose_or_create_day(self, date, filename):
        date_str = f"=== {date[0]}-{date[1]}-{date[2]} ==="
        notes = self.storage.read_day(filename, date_str)
        #Console.print_day(date_str)
        if  len(notes) == 0:
            self.storage.create_new_day(filename, date)
            #Console.print_date_not_found()
            notes.append(date_str)
        return notes

    def return_today_date(self):
        today = str(datetime.date(datetime.now())).split('-')
        return today

    def find_indexes(self, all_file, date_str):
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
        user_start_time = datetime.strptime(time[0], fmt).time()
        user_end_time = datetime.strptime(time[1], fmt).time()
        new_day_notes = copy(day_notes)
        insert_pos = len(new_day_notes)
        for i in range(1, len(day_notes)-1):
            time_notes = day_notes[i].split()[0].split("-")
            time_notes_next = day_notes[i+1].split()[0].split("-")
            notes_start_time_next = datetime.strptime(time_notes_next[0], fmt).time()
            notes_end_time = datetime.strptime(time_notes[1], fmt).time()
            notes_start_time = datetime.strptime(time_notes[0], fmt).time()
            check = self.check_overlaps(user_start_time, notes_end_time, user_end_time, notes_start_time)
            if check:
                return
            if notes_start_time_next >= user_end_time and user_start_time >= notes_end_time:
                insert_pos = i + 1
                return insert_pos
            elif i == 1 and user_end_time<=notes_start_time_next:
                insert_pos = i
                return insert_pos
        return insert_pos

    def check_overlaps(self, user_start_time, notes_end_time, user_end_time, notes_start_time):
        overlaps = not (user_start_time >= notes_end_time or user_end_time <= notes_start_time)
        return overlaps

    def write_notes(self, insert_pos, filename, new_note, time, date, day_notes):
        new_day_notes = copy(day_notes)
        date_str = f"=== {date[0]}-{date[1]}-{date[2]} ==="
        new_day_notes.insert(insert_pos, f"{time[0]}-{time[1]} {new_note}")
        all_file = self.storage.read_all_file(filename)
        start_index, end_index = self.find_indexes(all_file, date_str)
        all_file[start_index:end_index] = [i + "\n" for i in new_day_notes]
        self.storage.write_all_lines(filename, all_file)