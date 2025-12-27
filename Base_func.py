import io
from datetime import datetime
from copy import copy
from UI_Console.Console_func import Console
from Buisness_logic.Buisness_logic_txt import TxtLogic

class Command:
    OPEN = '1'
    READ_TODAY = '2'
    WRITE_TODAY = '3'
    CLOSE = '4'


logic = TxtLogic()
Console = Console()
filename = "tasks_for_days.txt"
Console.print_hello_line()
Console.print_user_main_choice()
command = Console.ask_user_command()

while command != Command.CLOSE:
    match command:
        case Command.OPEN:
            Console.ask_date()
            date = Console.ask_user_command().split()
            notes = logic.chose_or_create_day(date, filename)
            Console.print_notes(notes)
            Console.print_user_choice_notes()
            option = Console.ask_user_command()
            while option != '2':
                if option == "1":
                    Console.print_ask_time()
                    user_time = Console.ask_user_command().split("-")
                    Console.print_user_note()
                    new_note = Console.ask_user_command()
                    insert_pos = logic.find_insert_index(notes, user_time)
                    logic.write_notes(insert_pos, filename, new_note, user_time, date, notes)
                    Console.print_user_choice_notes()
                    option = Console.ask_user_command()
                else:
                    Console.print_user_choice_notes()
                    option = Console.ask_user_command()
            Console.print_user_main_choice()
            command = Console.ask_user_command()
        case Command.READ_TODAY:
            today = logic.return_today_date()
            notes = logic.chose_or_create_day(today, filename)
            Console.print_notes(notes)
            Console.print_user_main_choice()
            command = Console.ask_user_command()
        case Command.WRITE_TODAY:
            today = logic.return_today_date()
            notes = logic.chose_or_create_day(today, filename)
            Console.print_notes(notes)
            Console.print_ask_time()
            user_time = Console.ask_user_command().split("-")
            Console.print_user_note()
            new_note = Console.ask_user_command()
            insert_pos = logic.find_insert_index(notes, user_time)
            logic.write_notes(insert_pos, filename, new_note, user_time, today, notes)
            Console.print_user_main_choice()
            command = Console.ask_user_command()