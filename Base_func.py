from datetime import datetime
from copy import copy
from UI_Console.Console_func import Console
from UI_Console.menu_choices import MainCommand, NotesCommand
from UI_Console.UserInputErrors import InvalidChoice
from Business_logic.Buisness_logic_txt import TxtLogic
from Business_logic.LogicErrors import TimeOverlapseError, InputFormatError

logic = TxtLogic()
Console = Console()
filename = "tasks_for_days.txt"
Console.print_hello_line()
Console.print_user_main_choice()
command = Console.ask_valid_command(MainCommand)
while command != MainCommand.CLOSE:
    match command:
        case MainCommand.OPEN:
            while True:
                try:
                    Console.ask_date()
                    date = Console.ask_user_command()
                    date = logic.validate_date(date)
                    break
                except InputFormatError as e:
                    Console.write_error(str(e))
            notes = logic.chose_or_create_day(date, filename)
            Console.print_notes(notes)
            Console.print_user_choice_notes()
            option = Console.ask_valid_command(NotesCommand)
            while option != NotesCommand.BACK:
                if option == NotesCommand.WRITE:
                    while True:
                        Console.print_ask_time()
                        user_time = Console.ask_user_command()
                        Console.print_user_note()
                        new_note = Console.ask_user_command()
                        try:
                            insert_pos = logic.find_insert_index(notes, user_time)
                            break
                        except TimeOverlapseError as e:
                            Console.write_overlaps_error(e.new_note_time, e.existed_note_time)
                        except InputFormatError as e:
                            Console.write_error(str(e))
                    logic.write_notes(insert_pos, filename, new_note, user_time, date, notes)
                    Console.print_user_choice_notes()
                    option = Console.ask_valid_command(NotesCommand)
            Console.print_user_main_choice()
            command = Console.ask_valid_command(MainCommand)
        case MainCommand.READ_TODAY:
            today = logic.return_today_date()
            notes = logic.chose_or_create_day(today, filename)
            Console.print_notes(notes)
            Console.print_user_main_choice()
            command = Console.ask_valid_command(MainCommand)
        case MainCommand.WRITE_TODAY:
            today = logic.return_today_date()
            notes = logic.chose_or_create_day(today, filename)
            Console.print_notes(notes)
            while True:
                Console.print_ask_time()
                user_time = Console.ask_user_command()
                Console.print_user_note()
                new_note = Console.ask_user_command()
                try:
                    insert_pos = logic.find_insert_index(notes, user_time)
                    break
                except TimeOverlapseError as e:
                    Console.write_overlaps_error(e.new_note_time, e.existed_note_time)
                except InputFormatError as e:
                    Console.write_error(str(e))
            logic.write_notes(insert_pos, filename, new_note, user_time, today, notes)
            Console.print_user_main_choice()
            command = Console.ask_valid_command(MainCommand)