

class UserCache:
    def __init__(self):
        self._storage = {}

    def set(self, user_id, key, value):
        self._storage.setdefault(user_id, {})
        self._storage[user_id][key] = value

    def get(self, user_id, key):
        return self._storage.get(user_id, {}).get(key, None)

    def delete_user(self, user_id):
        self._storage.pop(user_id, None)

    def clear_key(self, user_id, key):
        if user_id in self._storage:
            self._storage[user_id].pop(key,None)
