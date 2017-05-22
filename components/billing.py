import pickle
import weakref
from collections import defaultdict

from components.parser import WrongIdException
from utils.singleton import Singleton


class EmptyStorageException(Exception):
    def __init__(self):
        super().__init__()


class DBMS(metaclass=Singleton):
    """
    Database Management System class - to add and remove users data
    """

    ID = 0
    DB_FILENAME = 'common_database.pickle'

    def __init__(self):
        try:
            with open(self.DB_FILENAME, 'rb') as dbfile:
                database = pickle.load(dbfile)
        except Exception:
            database = defaultdict(dict)
        self.db = database
        self._finalizer = weakref.finalize(self, self.dump)

    class Entry:
        def __init__(self, list_of_fields):
            self.name = list_of_fields[0]
            self.date = list_of_fields[1]
            self.time = list_of_fields[2]

        def __str__(self):
            return '\n'.join([self.name, str(self.date), str(self.time)])

    def insert(self, chat_id, name, date, time_):
        event_id = self.ID
        self.ID += 1
        self.db[chat_id][event_id] = self.Entry([name, date, time_])
        return event_id

    def remove(self, chat_id, event_id):
        if len(self.db) == 0:
            raise EmptyStorageException()
        try:
            ret_value = self.db[chat_id].pop(event_id)
        except Exception:
            raise WrongIdException()
        return event_id

    def get_all_events(self, chat_id):
        events = []
        id_text = '(ID={})\n'
        if len(self.db) != 0:
            events = [id_text.format(entry_id) + str(self.db[chat_id][entry_id]) for entry_id in
                      self.db[chat_id].keys()]  # !!!
        return '\n'.join(events)

    def dump(self):
        print(10)
        with open(self.DB_FILENAME, 'wb') as dbfile:
            pickle.dump(self.db, dbfile)
