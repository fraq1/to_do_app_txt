from UI_Console.UserInputErrors import InvalidChoice
from UI_Console.menu_choices import NotesCommand
from UI_Console.menu_choices import StorageCommand

class Console:

    def ask_storage_choice(self):
        print("Please select the format in which you want to store the data.\n1 - Json file\n2 - Txt file")
        choice = self.ask_valid_input(map(str,list(range(1,3))))
        return choice

    def choose_note_action(self, notes):
        commands = self.print_user_choice_notes(notes)
        choice = self.ask_valid_input(list(commands.keys()))
        return commands[choice]

    def ask_valid_input(self, valid_commands):
        while True:
            try:
                command = self.ask_user_command()
                return self.check_user_input(command, valid_commands)
            except InvalidChoice as e:
                self.write_error(str(e))

    def print_log_migrated(self, log):
        for date_str, notes_for_date in log.items():
            print(f"=== {date_str} ===")
            for note in notes_for_date:
                print(note.to_str())
            print("==================\n")
        print("Transferred from another storage type, if there were overlaps in time, the notes were not transferred")


    def check_user_input(self,user_input, valid_inputs) -> str:
        user_input = user_input.strip()
        if user_input not in map(str,valid_inputs):
            raise InvalidChoice(user_input, valid_inputs)
        return user_input

    def print_hello_line(self):
        print("Hello! This is to-do-app!\nPlease chose option:")

    def print_user_main_choice(self):
        print("1 - chose day to open or add.\n2 - open to do list for today.\n3 - write task for today.\n4 - close app")

    def ask_user_command(self) -> str:
        return input("> ")

    def ask_date(self):
        print("Enter the date you want to open or create in the format (YYYY MM DD)")

    def print_user_choice_notes(self, notes):
        commands = {}
        commands["1"] = NotesCommand.WRITE
        if len(notes) >= 1:
            print("Choose what you want to do\n1 - Write a new note\n2 - Edit note text\n3 - Edit note time\n4 - Delete note\n5 - Come back")
            commands["2"] = NotesCommand.EDIT_TEXT
            commands["3"] = NotesCommand.EDIT_TIME
            commands["4"] = NotesCommand.DELETE
            commands["5"] = NotesCommand.BACK
        else:
            print("Choose what you want to do\n1 - Write a new note\n2 - Сome back")
            commands["2"] = NotesCommand.BACK
        return commands

    def print_ask_time(self):
        print("Write what time to add a note (HH:MM-HH:MM)")

    def print_user_note(self):
        print("Write your note for this time")

    def print_date_not_found(self):
        print("Date not found, was added")

    def print_time_overlaps(self):
        print("The new time overlaps with the existing record:")

    #def print_day_notes(self, day_notes):
       # print(day_notes)

    def print_notes(self, notes, date):
        print(f"=== {date} ===")
        for line in notes:
            print(line.to_str())
        print("==================\n")

    def write_overlaps_error(self, user_note_time, existed_note_time):
        print(f"{user_note_time} overlaps with {existed_note_time}")

    def write_error(self, error_text):
        print(error_text)

    def print_user_note_text_for_edit(self, notes):
        print("Select the note whose text you want to change")
        for i in range(0,len(notes)):
            print(f"{i+1} - {notes[i].to_str()}")

    def print_user_note_time_for_edit(self, notes):
        print("Select the note whose time you want to change")
        for i in range(0,len(notes)):
            print(f"{i+1} - {notes[i].to_str()}")

    def print_user_note_for_delete(self, notes):
        print("Select the note you want to delete")
        for i in range(0,len(notes)):
            print(f"{i+1} - {notes[i].to_str()}")