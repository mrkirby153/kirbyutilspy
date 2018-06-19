from enum import Enum
import re

DATE_FORMAT_NOW = "YYYYY-mm-dd HH:MM:ss"
DATE_FORMAT_DAY = "YYYY-mm-dd"


class TimeUnit(Enum):
    FIT = (-1, 'FIT', 'FIT', 'F')
    SECOND = (1, 'Second', 'Seconds', 's')
    MINUTE = (60, 'Minute', 'Minutes', 'm')
    HOUR = (3600, 'Hour', 'Hours', 'h')
    DAY = (86400, 'Day', 'Days', 'd')
    WEEK = (604800, 'Week', 'Weeks', 'w')
    YEAR = (3.154e7, 'Year', 'Years', 'y')

    def __init__(self, time, singular, plural, short):
        self.time = time
        self.singular = singular
        self.plural = plural
        self.short = short

    def __gt__(self, other):
        if isinstance(other, TimeUnit):
            return self.time > other.time
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, TimeUnit):
            return self.time < other.time
        else:
            return False


time_dict = {
    # Shorthand
    "s": TimeUnit.SECOND.time,
    "m": TimeUnit.MINUTE.time,
    "h": TimeUnit.HOUR.time,
    "d": TimeUnit.DAY.time,
    "w": TimeUnit.WEEK.time,
    "y": TimeUnit.YEAR.time,

    # Longhand
    "seconds": TimeUnit.SECOND.time,
    "minutes": TimeUnit.MINUTE.time,
    "hours": TimeUnit.HOUR.time,
    "days": TimeUnit.DAY.time,
    "weeks": TimeUnit.WEEK.time,
    "years": TimeUnit.YEAR.time
}


def fit_time(time, largest=TimeUnit.SECOND):
    determined = largest
    time_list = list(TimeUnit)
    del time_list[0]  # Remove the "FIT" enum
    for t in time_list:
        if time >= t.time:
            determined = t
    if determined > largest:
        return largest
    else:
        return determined


def format_time(trim, time, time_unit=TimeUnit.FIT, largest=TimeUnit.YEAR):
    if time == -1:
        return "Permanent"

    if time_unit == TimeUnit.FIT:
        time_unit = fit_time(time, largest)

    t = time / float(time_unit.time)

    if trim == 0:
        t = int(round(t))
    else:
        t = round(t, trim)

    return '{} {}'.format(t, time_unit.plural)


def format_time_long(time, smallest=TimeUnit.SECOND, short=False):
    time_string = ''
    time_units = list(TimeUnit)
    del time_units[0]
    time_units.reverse()
    map = dict()
    for t in time_units:
        if t < smallest:
            continue
        count = time // t.time
        if count > 0:
            map[t] = count
            time -= t.time * count

    for i in range(0, len(map)):
        key, val = list(map.items())[i]
        time_string += str(val)
        if short:
            time_string += key.short
        else:
            time_string += " {}".format(key.singular if val == 1 else key.plural)

            if i + 1 < len(map):
                time_string += ", "

    return time_string


def parse_time(time):
    if not isinstance(time, str):
        raise TypeError('Must pass a string')
    time = time.lower()
    match = re.findall('(\d+\s?)(\D+)', time)
    time = 0
    for unit, delimiter in match:
        delimiter = delimiter.strip() # Trim whitespace

        if delimiter not in time_dict:
            delimiter = delimiter + 's'
            if delimiter not in time_dict:
                raise AttributeError('Key {} not found'.format(delimiter[0:-1]))

        time += int(unit) * time_dict[delimiter]
    return time
