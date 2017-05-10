import datetime
import re


class TooMuchDateArgumentsException(Exception):
    def __init__(self):
        super().__init__()


class DateType:
    def __init__(self, date_string):
        now = datetime.datetime.now()
        day = now.day
        month = now.month
        year = now.year

        tokens = re.split('[.\/]', date_string)

        if len(tokens) > 3:
            raise TooMuchDateArgumentsException()

        if len(tokens) >= 1:
            day = tokens[0]
            if len(tokens) >= 2:
                month = tokens[1]
                if len(tokens) == 3:
                    year = tokens[2]
        # try:
        #     datetime.check(year, month, day)
        # except Exception:
        #     print('Wrong day, month or year. Event is not added :(')

        self.day = day
        self.month = month
        self.year = year

    def __str__(self):
        return '.'.join([str(self.day), str(self.month), str(self.year)])


class TooMuchTimeArgumentsException(Exception):
    def __init__(self):
        super().__init__()


class TimeType:
    def __init__(self, time_string):
        hour = 0
        minute = 0

        tokens = re.split(':', time_string)

        if len(tokens) > 2:
            raise TooMuchTimeArgumentsException()

        if len(tokens) >= 1:
            hour = tokens[0]
            if len(tokens) == 2:
                minute = tokens[1]

        # check correctness of time

        self.hour = hour
        self.minute = minute

    def __str__(self):
        return ':'.join([str(self.hour), str(self.minute)])

    @staticmethod
    def is_time_string(string):
        return ':' in string
