class _BaseMenu:
    @classmethod
    def return_attrs(cls):
        values = list()
        for attr_name, value in cls.__dict__.items():
            if not attr_name.startswith("_"):
                values.append(value)
        return values

class MainCommand(_BaseMenu):
    OPEN = '1'
    READ_TODAY = '2'
    WRITE_TODAY = '3'
    CLOSE = '4'

class NotesCommand(_BaseMenu):
    WRITE = '1'
    BACK = '2'
