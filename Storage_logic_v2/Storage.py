import abc

class Storage(abc.ABC):

    @abc.abstractmethod
    def get_notes_by_date_id(self, date):
        pass

    @abc.abstractmethod
    def create_note(self, date, note):
        pass

    @abc.abstractmethod
    def update_note(
            self,
            note_id,
            text=None,
            start_time=None,
            end_time=None
    ):
        pass

    @abc.abstractmethod
    def delete_note(self, note_id):
        pass
