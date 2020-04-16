import random
import time

def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date_time(start, end, prop):
    randDateTime = str_time_prop(start, end, '%d/%m/%Y %I:%M %p', prop)
    return '\''+randDateTime+'\''

def random_date(start, end, prop):
    randDate = str_time_prop(start, end, '%d/%m/%Y', prop)
    return '\''+randDate+'\''


#print(random_date("1/1/2008 1:30 PM", "1/1/2009 4:50 AM", random.random()))