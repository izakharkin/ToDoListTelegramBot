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

    def get_day(self):
        return self.day

    def get_month(self):
        return self.month

    def get_year(self):
        return self.year

    def __gt__(self, other):
        return self.year > other.get_year() \
               or self.year == other.get_year() and self.month > other.get_month() \
               or self.year == other.get_year() and self.month == other.get_month() and self.day > other.get_day()

    def __str__(self):
        return '.'.join([str(self.day), str(self.month), str(self.year)])


class TooMuchTimeArgumentsException(Exception):
    def __init__(self):
        super().__init__()


class TimeType:
    NUM_OF_HOURS_IN_A_DAY = 24

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

    def get_minute(self):
        return self.minute

    def get_hour(self):
        return self.hour

    def __gt__(self, other):
        return self.hour > other.get_hour() \
               or self.hour == other.get_hour() and self.minute > other.get_minute()

    def __str__(self):
        return ':'.join([str(self.hour), str(self.minute)])

    @staticmethod
    def correct_time(time_hh_mm):
        hour = time_hh_mm[0]
        minute = time_hh_mm[1]

        hour += TimeType.NUM_OF_HOURS_IN_A_DAY
        hour %= TimeType.NUM_OF_HOURS_IN_A_DAY

        minute += TimeType.NUM_OF_MINUTES_IN_AN_HOUR
        minute %= TimeType.NUM_OF_MINUTES_IN_AN_HOUR

        return hour, minute

    @staticmethod
    def is_time_string(string):
        return ':' in string
