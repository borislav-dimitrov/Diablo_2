import shortuuid
from datetime import timedelta, datetime


def get_time_obj_delta_timestamp(time_1: datetime, time_2: datetime) -> str:
    '''Get timestamp from the difference of two datetime objects.'''
    return timedelta_to_timestmap(max([time_1, time_2]) - min([time_1, time_2]))

def timedelta_to_timestmap(time_delta: timedelta) -> str:
    '''Convert datetime.timedelta object to string'''
    total_seconds = time_delta.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    stringified = '{:02}:{:02}:{:02}'.format(
        int(hours), int(minutes), int(seconds)
    )
    return stringified


def time_stamp_to_time(time_stamp: str, format: str = '%H:%M:%S') -> str:
    '''Convert a string timestamp to time object.'''
    return datetime.strptime(time_stamp, format)


def seconds_to_time_stamp(seconds: int, format: str = '%H:%M:%S') -> str:
    '''Create a timestamp from the given seconds.'''
    delta_obj = timedelta(seconds=seconds)
    return timedelta_to_timestmap(delta_obj)


def smaller_time_stamp(stamp_1: str, stamp_2: str) -> str:
    '''Compare two timestamps and return the smaller smaller(faster) one.'''
    hours1, minutes1, seconds1 = [int(i) for i in stamp_1.split(':')]
    hours2, minutes2, seconds2 = [int(i) for i in stamp_2.split(':')]

    if hours1 < hours2:
        return stamp_1
    elif hours2 < hours1:
        return stamp_2

    if minutes1 < minutes2:
        return stamp_1
    elif minutes2 < minutes1:
        return stamp_2

    if seconds1 < seconds2:
        return stamp_1
    elif seconds2 < seconds1:
        return stamp_2


def generate_uniq_id() -> str:
    '''Generate an unique id'''
    return shortuuid.uuid()
