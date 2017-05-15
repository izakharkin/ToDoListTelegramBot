from collections import OrderedDict
import datetime
import time

from utils.singleton import Singleton
from utils.special_types import DateType


# moments in which we should remind user about his deadline
def get_remind_moments(event_date, event_time):
    date_diffs = [(1, 0, 0), (0, 0, 0)]  # one day to deadline
    time_diffs = [(0, 0), (1, 0)]  # one hour to deadline

    remind_dates = []
    for d_diff in date_diffs:
        remind_dates.append(event_date.get_day() - d_diff[0], \
                            event_date.get_month() - d_diff[1], \
                            event_date.get_year() - date_diffs[2])
    remind_dates = map(DateType.correct_date, remind_dates)
    remind_times = []
    for d_diff in date_diffs:
        remind_dates.append(event_date.get_day() - d_diff[0], \
                            event_date.get_month() - d_diff[1], \
                            event_date.get_year() - date_diffs[2])

    return zip(remind_dates, remind_times)


class Reminder(metaclass=Singleton):
    def __init__(self, events_dict=OrderedDict()):
        self.events_queue = events_dict  # ordered by ((1)date, (2)time)

    def insert_event(self, event_date, event_time, event_chat_id, event_id):
        remind_moments = get_remind_moments(event_date, event_time)

        now_date = datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year
        now_time = datetime.time.hour, datetime.time.minute

        actual_moments = filter(lambda moment: moment[0] >= now_date and moment[1] >= now_time, remind_moments)
        for moment in actual_moments:
            self.events_queue[moment] = (event_chat_id, event_id)

    def start_tracking(self):
        while True:
            current = self.events_queue.front()
            current_date = datetime.GET_DATE
            current_time = time.GET_TIME
