import os
import pickle
from hashlib import sha256


class Storage:
    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._filename_hash = filename + '.hash'
        self._filename_bac = filename + '.bac'

    def save_to_backup_file(self, data: list | dict) -> None:
        with open(self._filename_bac, "wb") as file:
            pickle.dump(data, file)
        with open(self._filename, "rb") as file:
            file_hash = sha256(file.read()).hexdigest()
        with open(self._filename_hash, "w") as file:
            file.write(file_hash)

    def _get_backup(self, default: list | dict) -> list | dict:
        if not os.path.exists(self._filename_bac):
            return default
        with open(self._filename_bac, "rb") as file:
            try:
                return pickle.load(file)
            except Exception:
                return default

    def _hash_changed(self) -> bool:
        if not os.path.exists(self._filename_hash):
            return True
        with open(self._filename, "rb") as file:
            current_hash = sha256(file.read()).hexdigest()
        with open(self._filename_hash, "r") as file:
            saved_hash = file.read()
        return current_hash != saved_hash
