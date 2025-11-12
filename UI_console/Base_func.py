import io
from datetime import datetime
from copy import copy


class Command:
    OPEN = '1'
    READ_TODAY = '2'
    WRITE_TODAY = '3'
    CLOSE = '4'


def chose_day(date, filename):
    date_str = f"=== {date[0]}-{date[1]}-{date[2]} ==="
    notes = list()
    printing = False
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip("\n")
            if line.startswith("===") and printing:
                print(line)
                break
            if line == date_str:
                printing = True
            if printing:
                print(line)
                notes.append(line)
    return notes

def write_task(day_notes, filename, new_note, time, date):
    date_str = f"=== {date[0]}-{date[1]}-{date[2]} ==="
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
        overlaps = not (user_start_time >= notes_end_time or user_end_time <= notes_start_time)
        if overlaps:
            print("The new time overlaps with the existing record:")
            print(day_notes[i])
            return

        if notes_start_time_next >= user_end_time and user_start_time >= notes_end_time:
            insert_pos = i + 1
            break
        elif i == 1 and user_end_time<=notes_start_time_next:
            insert_pos = i
            break
    new_day_notes.insert(insert_pos, f"{time[0]}-{time[1]} {new_note}")
    all_file = []
    with open(filename, "r", encoding="utf-8") as file:
        all_file = file.readlines()
        start_index = None
        end_index = None
        for index,line in enumerate(all_file):
            if line.rstrip("\n") == date_str:
                start_index = index
            elif line.startswith("===") and start_index is not None:
                end_index = index
                break

        all_file[start_index:end_index] = [i + "\n" for i in new_day_notes]
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(all_file)

filename = "tasks_for_days.txt"
print("Hello! This is to-do-app!\nPlease chose option:")
print("1 - chose day to open or add.\n2 - open to do list for today.\n3 - write task for today.\n4 - close app")
print(datetime.now())
command = input()
while command != Command.CLOSE:
    match command:
        case Command.OPEN:
            print("Enter the date you want to open or create in the format (YYYY MM DD)")
            date = input().split()
            notes = chose_day(date, filename)
            print("Choose what you want to do\n1 - Write a new note\n2 - Сome back")
            option = input()
            while option != '2':
                if option == "1":
                    print("Write what time to add a note (HH:MM - HH:MM)")
                    user_time = input().split("-")
                    print("Write your note for this time")
                    new_note = input()
                    write_task(notes, filename, new_note, user_time,date)
                    print("Choose what you want to do\n1 - Write a new note\n2 - Сome back")
                    option = input()
                else:
                    print("Wrong command")
                    print("Choose what you want to do\n1 - Write a new note\n2 - Сome back")
                    option = input()
            print("1 - chose day to open or add.\n2 - open to do list for today.\n3 - write task for today.\n4 - close app")
            command = input()
        case Command.READ_TODAY:
            print(2)
            print("1 - chose day to open or add.\n2 - open to do list for today.\n3 - write task for today.\n4 - close app")
            command = input()
        case Command.WRITE_TODAY:
            print(3)
            print("1 - chose day to open or add.\n2 - open to do list for today.\n3 - write task for today.\n4 - close app")
            command = input()