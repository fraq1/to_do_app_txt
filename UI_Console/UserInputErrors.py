class InvalidChoice(Exception):
    def __init__(self, user_choice, valid_choices):
        self.user_choice = user_choice
        self.valid_choices = valid_choices
        super().__init__(f"Input {user_choice} not correct, correct inputs: {valid_choices}")