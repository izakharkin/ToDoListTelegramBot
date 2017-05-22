from utils.special_types import DateType, TimeType


class TooFewParseArgumentsException(Exception):
    def __init__(self):
        super().__init__()


class WrongIdException(Exception):
    def __init__(self):
        super().__init__()


class Parser:
    @staticmethod
    def parse_event(event_string):
        tokens = event_string.split(' ')[1:]

        if (len(tokens) < 2):
            raise TooFewParseArgumentsException()

        with_time = TimeType.is_time_string(tokens[-1])

        name = ' '.join(tokens[:(-2 if with_time else -1)])  # match the name
        date = DateType(tokens[(-2 if with_time else -1)])
        time = TimeType((tokens[-1] if with_time else '00:00'))

        return name, date, time

    @staticmethod
    def parse_id(event_id_text):
        tokens = event_id_text.split(' ')[1:]
        if len(tokens) > 1:
            raise WrongIdException()
        return int(tokens[0])
