
class TimeOverlapseError(Exception):
    def __init__(self, new_note_time, existed_note_time):
        self.new_note_time = new_note_time
        self.existed_note_time = existed_note_time
        super().__init__(f"{new_note_time} overlaps with {existed_note_time}")
        
class InputFormatError(Exception):
    def __init__(self, user_input, expected_format):
        self.user_input = user_input
        self.expected_format = expected_format
        super().__init__(f"{user_input} - user input, but a string in the format was expected - {expected_format}")