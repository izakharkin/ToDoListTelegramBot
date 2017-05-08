import datetime


class TooMuchDateArgumentsException(Exception):
    def __init__(self):
        super().__init__()


class DateType:
    def __init__(self, date_string):
        now = datetime.datetime.now()
        day = now.day
        month = now.month
        year = now.year

        tokens = date_string.split('.\/')

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
        return '.'.join([self.day, self.month, self.year])


class TooMuchTimeArgumentsException(Exception):
    def __init__(self):
        super().__init__()


class TimeType:
    def __init__(self, time_string):
        hour = 0
        minute = 0

        tokens = time_string.split(':')

        if len(tokens) > 2:
            raise TooMuchTimeArgumentsException()

        if len(tokens) >= 1:
            hour = tokens[0]
            if len(tokens) == 2:
                minute = tokens[1]

        # check correctness of time

        self.hour = hour
        self.minute = minute
