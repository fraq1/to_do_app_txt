from UI_Console.menu_choices import NotesCommand
from Business_logic.LogicErrors import TimeOverlapseError, InputFormatError

def handle_day(console, logic, date, filename):
    notes = logic.chose_or_create_day(date, filename)
    console.print_notes(notes)
    commands = console.print_user_choice_notes(notes)
    choice = console.ask_valid_input(list(commands.keys()))
    option = commands[choice]
    while option != NotesCommand.BACK:

        if option == NotesCommand.EDIT_TEXT:
            notes = logic.chose_or_create_day(date, filename)
            console.print_user_note_text_for_edit(notes)
            user_note_edit = int(console.ask_valid_input(list(range(1,len(notes)))))
            console.print_user_note()
            new_note = console.ask_user_command()
            logic.edit_notes_text(user_note_edit, filename, new_note, date)
            commands = console.print_user_choice_notes(notes)
            choice = console.ask_valid_input(list(commands.keys()))
            option = commands[choice]

        if option == NotesCommand.WRITE:
            notes = logic.chose_or_create_day(date, filename)
            while True:
                console.print_ask_time()
                user_time = console.ask_user_command()
                try:
                    logic.validate_time(user_time)
                    insert_pos = logic.find_insert_index(notes, user_time)
                    break
                except TimeOverlapseError as e:
                    console.write_overlaps_error(e.new_note_time, e.existed_note_time)
                except InputFormatError as e:
                    console.write_error(str(e))
            console.print_user_note()
            new_note = console.ask_user_command()
            logic.write_notes(insert_pos, filename, new_note, user_time, date, notes)
            notes = logic.chose_or_create_day(date, filename)
            commands = console.print_user_choice_notes(notes)
            choice = console.ask_valid_input(list(commands.keys()))
            option = commands[choice]

        if option == NotesCommand.EDIT_TIME:
            notes = logic.chose_or_create_day(date, filename)
            console.print_user_note_time_for_edit(notes)
            user_note_edit = int(console.ask_valid_input(list(range(1,len(notes)))))
            notes_without_edited = notes[:user_note_edit] + notes[user_note_edit + 1:]
            while True:
                console.print_ask_time()
                user_time = console.ask_user_command()
                try:
                    logic.validate_time(user_time)
                    insert_pos = logic.find_insert_index(notes_without_edited, user_time)
                    break
                except TimeOverlapseError as e:
                    console.write_overlaps_error(e.new_note_time, e.existed_note_time)
                except InputFormatError as e:
                    console.write_error(str(e))
            logic.edit_notes_time(user_note_edit, filename, user_time, date, insert_pos, notes_without_edited)
            commands = console.print_user_choice_notes(notes)
            choice = console.ask_valid_input(list(commands.keys()))
            option = commands[choice]

        if option == NotesCommand.DELETE:
            notes = logic.chose_or_create_day(date, filename)
            console.print_user_note_for_delete(notes)
            user_note_delete = int(console.ask_valid_input(list(range(1,len(notes)))))
            logic.delete_note(user_note_delete, filename, date)
            notes = logic.chose_or_create_day(date, filename)
            commands = console.print_user_choice_notes(notes)
            choice = console.ask_valid_input(list(commands.keys()))
            option = commands[choice]

