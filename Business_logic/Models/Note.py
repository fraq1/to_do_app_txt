class Note:
    def __init__(self, start_time: str, end_time: str, text: str) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

    def to_dict(self) -> dict[str, str]:
        return {"start_time": self.start_time, "end_time": self.end_time, "text": self.text}

    @staticmethod
    def from_dict(dict_note: dict[str, str]) -> "Note":
        return Note(dict_note["start_time"], dict_note["end_time"], dict_note["text"])

    def to_str(self) -> str:
        return f"{self.start_time}-{self.end_time} {self.text}"

    @staticmethod
    def from_str(str_note: str) -> "Note":
        note_time, note_text = str_note.split(maxsplit=1)
        note_time_start, note_time_end = note_time.split('-')
        return Note(note_time_start, note_time_end, note_text)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Note):
            return False
        return (self.start_time == other.start_time and
                self.end_time == other.end_time and
                self.text == other.text)