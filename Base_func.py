from datetime import datetime
from copy import copy
from UI_Console.Console_func import Console
from UI_Console.menu_choices import MainCommand, NotesCommand
from UI_Console.UserInputErrors import InvalidChoice
from Business_logic.Buisness_logic_txt import TxtLogic
from Business_logic.LogicErrors import TimeOverlapseError, InputFormatError
from flows.day_flow import handle_day

logic = TxtLogic()
Console = Console()
filename = "tasks_for_days.txt"
Console.print_hello_line()
Console.print_user_main_choice()
command = Console.ask_valid_input(MainCommand.return_attrs())
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
            handle_day(Console, logic, date, filename)
            Console.print_user_main_choice()
            command = Console.ask_valid_input(MainCommand.return_attrs())
        case MainCommand.READ_TODAY:
            today = logic.return_today_date()
            notes = logic.chose_or_create_day(today, filename)
            Console.print_notes(notes)
            Console.print_user_main_choice()
            command = Console.ask_valid_input(MainCommand.return_attrs())
        case MainCommand.WRITE_TODAY:
            today = logic.return_today_date()
            handle_day(Console, logic, today, filename)
            Console.print_user_main_choice()
            command = Console.ask_valid_input(MainCommand.return_attrs())