from sortedcontainers import SortedDict
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
        remind_dates.append((event_date.get_day() - d_diff[0],
                            event_date.get_month() - d_diff[1],
                            event_date.get_year() - d_diff[2]))
    remind_dates = map(DateType.correct_date, remind_dates)

    remind_times = []
    for t_diff in time_diffs:
        remind_dates.append((event_date.get_hour() - t_diff[0],
                            event_date.get_minute() - t_diff[1]))

    return zip(remind_dates, remind_times)


class Tracker(metaclass=Singleton):
    def __init__(self, events_dict=SortedDict()):
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
            current_event = self.events_queue.items()[0]  # the frontal event
            curr_date = current_event[0][0]
            curr_time = current_event[0][1]
            now = datetime.datetime.now()
            if now.year == curr_date[0] and now.month == curr_date[1] and now.day == curr_date[2] \
                    and now.hour == curr_time[0]:
                yield current_event[1]  # return the chat_id and event_id

