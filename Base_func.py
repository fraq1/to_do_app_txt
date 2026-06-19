from Business_logic.Business_logic import BusinessLogic
from Storage_logic.Json_logic import JsonStorage
from Storage_logic.txt_logic import TxtStorage
from Storage_logic_v2.SQLite_logic import SQLiteDB
from UI_Console.Console_func import Console
from UI_Console.menu_choices import MainCommand, StorageCommand
from flows.day_flow import handle_day,get_valid_date

Console = Console()
Console.print_hello_line()
storage = SQLiteDB()
logic = BusinessLogic(storage)
Console.print_user_main_choice()
command = Console.ask_valid_input(MainCommand.return_attrs())
while command != MainCommand.CLOSE:
    match command:
        case MainCommand.OPEN:
            date = get_valid_date(Console, logic)
            handle_day(Console, logic, date)
            Console.print_user_main_choice()
            command = Console.ask_valid_input(MainCommand.return_attrs())
        case MainCommand.READ_TODAY:
            today = logic.return_today_date()
            notes = logic.chose_or_create_day(today)
            Console.print_notes(notes, today)
            Console.print_user_main_choice()
            command = Console.ask_valid_input(MainCommand.return_attrs())
        case MainCommand.WRITE_TODAY:
            today = logic.return_today_date()
            handle_day(Console, logic, today)
            Console.print_user_main_choice()
            command = Console.ask_valid_input(MainCommand.return_attrs())

storage.close()

