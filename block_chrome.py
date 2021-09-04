import datetime, time
import subprocess
from typing import Sequence, Union

"""This program *TRIES* to implement blocking applications. Crossing my fingers."""

now = datetime.datetime.now

def taskkill(task: Union[int, str]) -> None:
    """This kills a task either by its name (str) or its ID (int). 
    Raises TypeError if task is neither str or int"""
    if isinstance(task, int):
        flag = "/pid"
    elif isinstance(task, str):
        flag = "/im"
    else:
        raise TypeError("task is not either an integer (ID number) or str (task name)")
    subprocess.Popen(f"taskkill {flag} {task} /t /f", shell = True)

"""
def timed_kill_task(task: Union[int, str], sec_duration = 0):
    # Call taskkill on a certain task for given amount of seconds
    rn = now()
    delta_duration = datetime.timedelta(seconds = sec_duration)
    while now() < (rn + delta_duration):
        taskkill(task)
        time.sleep(0.5)
"""
        
def timed_kill_tasklist(*args: Sequence[Union[int, str]], sec_duration = 0):
    """Calls taskkill on a list of tasks for a given amount of seconds"""
    rn = now()
    delta_duration = datetime.timedelta(seconds=sec_duration)
    while now() < (rn + delta_duration):
        for task in args:
            taskkill(task)
        time.sleep(0.5)

