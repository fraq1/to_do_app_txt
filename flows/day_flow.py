from UI_Console.menu_choices import NotesCommand
from Business_logic.LogicErrors import TimeOverlapseError, InputFormatError

def handle_day(console, logic, date):
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
            logic.edit_notes_text(user_note_edit, new_note, date)
            option = console.choose_note_action(notes)

        elif option == NotesCommand.WRITE:
            notes = logic.chose_or_create_day(date)
            insert_pos, user_time = get_valid_time(console, logic, notes)
            console.print_user_note()
            new_note = console.ask_user_command()
            logic.write_notes(insert_pos, new_note, user_time, date, notes)
            notes = logic.chose_or_create_day(date)
            option = console.choose_note_action(notes)

        elif option == NotesCommand.EDIT_TIME:
            notes = logic.chose_or_create_day(date)
            console.print_user_note_time_for_edit(notes)
            user_note_edit = int(console.ask_valid_input(list(range(1,len(notes)+1)))) - 1
            notes_without_edited = notes[:user_note_edit] + notes[user_note_edit + 1:]
            insert_pos, user_time = get_valid_time(console, logic, notes_without_edited)
            logic.edit_notes_time(user_note_edit, user_time, date, notes_without_edited)
            option = console.choose_note_action(notes)

        elif option == NotesCommand.DELETE:
            notes = logic.chose_or_create_day(date)
            console.print_user_note_for_delete(notes)
            user_note_delete = int(console.ask_valid_input(list(range(1,len(notes)+1)))) - 1
            logic.delete_note(user_note_delete, date)
            notes = logic.chose_or_create_day(date)
            option = console.choose_note_action(notes)


def get_valid_date(console, logic):
    while True:
        try:
            console.ask_date()
            date = console.ask_user_command()
            date = logic.validate_date(date)
            return date
        except InputFormatError as e:
            console.write_error(str(e))

def get_valid_time(console, logic, notes):
    while True:
        console.print_ask_time()
        user_time = console.ask_user_command()
        try:
            logic.validate_time(user_time)
            insert_pos = logic.find_insert_index(notes, user_time)
            return insert_pos, user_time
        except TimeOverlapseError as e:
            console.write_overlaps_error(e.new_note_time, e.existed_note_time)
        except InputFormatError as e:
            console.write_error(str(e))