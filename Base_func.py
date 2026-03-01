from Business_logic.Business_logic import BusinessLogic
from Storage_logic.Json_logic import JsonStorage
from Storage_logic.txt_logic import TxtStorage
from UI_Console.Console_func import Console
from UI_Console.menu_choices import MainCommand, StorageCommand
from flows.day_flow import handle_day,get_valid_date

def ask_storage(console):
    choice = console.ask_storage_choice()
    if choice == StorageCommand.JSON:
        storage = JsonStorage()
        old_storage = TxtStorage()
    else:
        storage = TxtStorage()
        old_storage = JsonStorage()
    return storage, old_storage

Console = Console()
Console.print_hello_line()
storage, old_storage = ask_storage(Console)
logic = BusinessLogic(storage)
log_for_migrated = logic.migrate_notes(old_storage, storage)
Console.print_log_migrated(log_for_migrated)
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




