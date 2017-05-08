from utils.special_types import DateType, TimeType


class TooFewParseArgumentsException(Exception):
    def __init__(self):
        super.__init__()


# TODO: raise when wronf ID entered (with chars or not existing)
class WrongIdException(Exception):
    def __init__(self):
        super.__init__()


class Parser:
    @staticmethod
    def parse_event(self, event_string):
        tokens = event_string.split(' ')

        if (len(tokens) < 2):
            raise TooFewParseArgumentsException()

        name = ' '.join(tokens[:-2])
        date = DateType(tokens[-2])
        time = TimeType(tokens[-1])

        return name, date, time

    @staticmethod
    def parse_id(self, event_id):
        tokens = int(event_id)
        return tokens[0]
