#!/usr/bin/env python3
"""This program tries to experiment with running Cold Turkey with Python."""

import subprocess
import time
import datetime
import math
from typing import List, Tuple
import copy

_COLD_TURKEY = r'"C:\Program Files\Cold Turkey\Cold Turkey Blocker.exe"'
_START = 'start'
_STOP = 'stop'
_ADD = 'add'
_TOGGLE = 'toggle'

_LOCK = '-lock'
_WEB = 'web'
_EXCEPTION = 'exception'

SEC_PER_MIN = 60
MIN_PER_HOUR = 60

FROZEN_TURKEY = "Frozen Turkey"

# Method / function aliases
now = datetime.datetime.now  
today = datetime.date.today  

# "datetime.time" constants
TEN_THIRTY = datetime.time(22, 30, 0)
MILLISEC_BEFORE_MIDNIGHT = datetime.time(23, 59, 59, 999999)
MIDNIGHT = datetime.time(0, 0, 0, 0)
ONE_THIRTY = datetime.time(1, 30, 0)

"""
WISHLIST:
- Implement a "make-shift" pomodoro timer (DONE!)
- Implement a night Frozen Turkey block that runs to 1:30AM next day. (DONE!)
- Implement scheduling via Python. (DONE!?)
- Make a "mealbreak" Frozen Turkey block for 1.5h, like lunch or dinner. (DONE!?)
- Find a way to block applications via Python.
- Notifications, on-screen timers, etc.
- What is Git? What's GitHub? yada. (Learned to use Git now.)
- Implement a "start block until certain time" function (DONE!)
"""

# These are the "starter" PyTurkey functions.

def start_block(block_name: str, minutes: int = 0, lock: bool = True):
    """Blocks a given block_name"""
    LOCK_STATUS = _LOCK if lock else ''
    TIME_STATUS = str(minutes) if minutes > 0 else ''
    subprocess.run(f'{_COLD_TURKEY} -{_START} "{block_name}" {LOCK_STATUS} {TIME_STATUS}')

def stop_block(block_name: str):
    """Ends the block of a given block_name"""
    subprocess.run(f'{_COLD_TURKEY} -{_STOP} "{block_name}"')

def toggle_block(block_name: str):
    """Starts or stops an unlocked block"""
    subprocess.run(f'{_COLD_TURKEY} -{_TOGGLE} "{block_name}"')

def add_url(block_name: str, url: str, exception: bool = False):
    """Adds the URL into the block, either as a blocked site or exception"""
    where_add = _EXCEPTION if exception else _WEB
    subprocess.run(f'{_COLD_TURKEY} -{_ADD} "{block_name}" -{where_add} "{url}"')

"""
These will then be the pomodoro functions implemented by Python, because
Cold Turkey will only do that in PRO. For now, I don't know how to activate
these functions other than use the Python REPL "command line".
"""

def pomodoro(block_name: str, block_min: int, break_min: int, \
             block_first: bool = True, loops: int = 1, lock: bool = True):
    """This emulates the pomodoro timer, blocking the block_name for a few minutes and 
    unlocks it for a few minutes. You can also choose to have the block unlocked first
    and loop over and over.
    
    By default, the block is blocked first and looped once."""

    block_sec = block_min * SEC_PER_MIN
    break_sec = break_min * SEC_PER_MIN

    if block_first:
        for i in range(loops):
            start_block(block_name, block_min, lock)
            time.sleep(block_sec)
            stop_block(block_name)
            time.sleep(break_sec)
    else:
        for i in range(loops):
            stop_block(block_name)
            time.sleep(break_sec)
            start_block(block_name, block_min, lock)
            time.sleep(block_sec)

def frozen_pomodoro(work_min: int, frozen_min: int, loops: int = 1):
    """Loops between using the computer and Frozen Turkey, given the minutes
    NOTE: This considers work as non-Frozen and it starts first."""
    for i in range(loops):
        time.sleep(work_min * SEC_PER_MIN)  # sleep takes in secs
        start_block(FROZEN_TURKEY, minutes = frozen_min)  # block takes mins
        time.sleep(frozen_min * SEC_PER_MIN)

# Secret convert to time object functions.

def _convert_to_datetime(given_datetime) -> datetime.datetime:
    """Returns the datetime object telling the date and time given
from either ISO format or existing datetime object."""
    if isinstance(given_datetime, str):
        return datetime.datetime.fromisoformat(given_datetime)
    elif isinstance(given_datetime, datetime.datetime):
        return given_datetime
    else:
        raise Exception("given_datetime not in ISO format or datetime.datetime object")

def _convert_to_time(given_time) -> datetime.time: 
    """Returns the time object telling the time from ISO format or existing time
object."""
    # convert given_time into a datetime.time object.
    if isinstance(given_time, str):
        return datetime.time.fromisoformat(given_time)
    elif isinstance(given_time, datetime.time):
        return given_time
    else:
        raise Exception("given_time not in ISO format or datetime.time object")

# This is my implementation of blocking up to a certain time, like Cold Turkey
    
def start_block_until(block_name: str, end_time: datetime.datetime, \
                      start_time: datetime.datetime = now()):
    """Blocks a given block_name from the optional start_time to end_time.
    end_time and start_time can be either in ISO format or datetime object. """
    working_end_time = _convert_to_datetime(end_time)
    working_start_time = _convert_to_datetime(start_time)
    
    while now() < working_start_time:
        time.sleep(1)

    block_duration = working_end_time - now()
    block_min_duration = math.ceil(block_duration.total_seconds() / SEC_PER_MIN)

    start_block(block_name, block_min_duration)

# These will be called the night Frozen block functions.
def frozen_at_night(set_time):
    """Activates Frozen Turkey from specified set_time to 1:30:00AM next day.
    requires: 10:30PM <= set_time <= 11:59PM"""

    """heads-up: I DID NOT take into account Daylight Savings, so..., for me
    I'd just use Task Scheduler and set it on 10:30PM every day.
              Also, if set_time is 11:59PM, weird things happen. no recommend."""

    # !: I did remember someone say whatever you do, NO programming time

    start_block_time = _convert_to_time(set_time)

    if TEN_THIRTY <= start_block_time <= MILLISEC_BEFORE_MIDNIGHT:
        today_date = today()
        if MIDNIGHT <= now() < ONE_THIRTY:
            one_thirty_today = datetime.datetime.combine(today_date, ONE_THIRTY)
            start_block_until(FROZEN_TURKEY, one_thirty_today)
        else:
            tomorrow = today_date + datetime.timedelta(days = 1)
            one_thirty_tomorrow = datetime.datetime.combine(tomorrow, ONE_THIRTY)
            set_datetime = datetime.datetime.combine(today, start_block_time)
            start_block_until(FROZEN_TURKEY, one_thirty_tomorrow, set_datetime)
    else:
        raise ValueError("set_time not between 22:30:00 and 23:59:59 next day")

def frozen_at_midnight():
    """Activates Frozen Turkey at midnight for 1.5h
    note: this while loop is just preemptive if Task Scheduler doesn't program
    it to run at midnight."""

    """
    while (ONE_THIRTY <= now().time() <= MILLISEC_BEFORE_MIDNIGHT):
        time.sleep(1)
    # if you're here after the while loop, 12:00AM < now < 1:30AM
    today_date = today()
    one_thirty_today = datetime.datetime.combine(today_date, ONE_THIRTY)
    remaining_time = one_thirty_today - now()
    min_remains = round(remaining_time.total_seconds() / SEC_PER_MIN)
    start_block(FROZEN_TURKEY, min_remains)  
    """

    today_date = today()
    if (MIDNIGHT <= now().time() < ONE_THIRTY):
        working_date = today_date
    else:
        tomorrow = today_date + datetime.timedelta(days = 1)
        working_date = tomorrow
    start_midnight = datetime.datetime.combine(working_date, MIDNIGHT)
    end_one_thirty = datetime.datetime.combine(working_date, ONE_THIRTY)
    start_block_until(FROZEN_TURKEY, end_one_thirty, start_midnight)
        
    
# This is my "catch-all" scheduling function, first version.
def schedule_blocks(schedule):
    """Schedules a series of blocks to block, given what start time
    until what end time.
    
    requires: - schedule is a sequence (list, tuple, whatever?) of 
    [block name string, start time, end time] triplets. (for now anyway.)"""

    today_date = today()

    working_schedule = copy.deepcopy(schedule)
    for scheduled_block in working_schedule:
        for i in range(1, 3):
            # converts start and end time to time object
            working_time = _convert_to_time(scheduled_block[i])
            scheduled_block[i] = datetime.datetime.combine(today_date, working_time)

    working_schedule.sort(key = lambda sch: sch[1])

    for block_name, start_time, end_time in working_schedule:
        if now() > start_time:
            if now() < end_time:
                start_block_until(block_name, end_time)
            else:
                continue
        else:
            start_block_until(block_name, end_time, start_time)
