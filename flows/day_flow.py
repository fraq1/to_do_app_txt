from UI_Console.menu_choices import NotesCommand
from Business_logic.LogicErrors import TimeOverlapseError, InputFormatError
from UI_Console.Console_func import Console
from Business_logic.Business_logic import BusinessLogic
from Business_logic.Models.Note import Note

def handle_day(console: Console, logic: BusinessLogic, date: str):
    notes = logic.chose_or_create_day(date)
    console.print_notes(notes, date)
    option = console.choose_note_action(notes)
    while option != NotesCommand.BACK:

        if option == NotesCommand.EDIT_TEXT:
            notes = logic.chose_or_create_day(date)
            console.print_user_note_text_for_edit(notes)
            user_note_edit = int(console.ask_valid_input(list(range(1,len(notes)+1)))) - 1
            console.print_user_note()
            new_note = console.ask_user_command()
            logic.edit_notes_text(notes[user_note_edit].note_id, new_note)
            option = console.choose_note_action(notes)

        elif option == NotesCommand.WRITE:
            notes = logic.chose_or_create_day(date)
            user_time = get_valid_time(console, logic, notes)
            console.print_user_note()
            new_note = console.ask_user_command()
            logic.write_notes(new_note, user_time, date)
            notes = logic.chose_or_create_day(date)
            option = console.choose_note_action(notes)

        elif option == NotesCommand.EDIT_TIME:
            notes = logic.chose_or_create_day(date)
            console.print_user_note_time_for_edit(notes)
            user_note_edit = int(console.ask_valid_input(list(range(1,len(notes)+1)))) - 1
            notes_without_edited = notes[:user_note_edit] + notes[user_note_edit + 1:]
            user_time = get_valid_time(console, logic, notes_without_edited)
            logic.edit_notes_time(notes[user_note_edit].note_id, user_time)
            option = console.choose_note_action(notes)

        elif option == NotesCommand.DELETE:
            notes = logic.chose_or_create_day(date)
            console.print_user_note_for_delete(notes)
            user_note_delete = int(console.ask_valid_input(list(range(1,len(notes)+1)))) - 1
            logic.delete_note(notes[user_note_delete].note_id)
            notes = logic.chose_or_create_day(date)
            option = console.choose_note_action(notes)


def get_valid_date(console: Console, logic: BusinessLogic):
    while True:
        try:
            console.ask_date()
            date = console.ask_user_command()
            date = logic.validate_date(date)
            return date
        except InputFormatError as e:
            console.write_error(str(e))

def get_valid_time(console: Console, logic: BusinessLogic, notes: list[Note]):
    while True:
        console.print_ask_time()
        user_time = console.ask_user_command()
        try:
            valid_user_time = logic.validate_time(user_time)
            logic.check_valid_time(notes, user_time)
            return valid_user_time
        except TimeOverlapseError as e:
            console.write_overlaps_error(e.new_note_time, e.existed_note_time)
        except InputFormatError as e:
            console.write_error(str(e))