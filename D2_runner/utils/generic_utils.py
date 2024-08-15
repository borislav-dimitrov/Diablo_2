import math
import shortuuid
from datetime import timedelta


def timedelta_to_str(time_delta: timedelta) -> str:
    '''Convert datetime.timedelta object to string'''
    total_seconds = math.ceil(time_delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)


def generate_uniq_id() -> str:
    '''Generate an unique id'''
    return shortuuid.uuid()
