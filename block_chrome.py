import datetime, time
import subprocess
from typing import Sequence, Union

now = datetime.datetime.now

def block_chrome():
    rn = now()
    two_min = datetime.timedelta(minutes = 2)
    while now() < (rn + two_min):
        subprocess.Popen("taskkill /im chrome.exe /t /f", stdout = None, stderr = None, shell = False)
        time.sleep(1)

def taskkill(task: Union[int, str], sec_duration = 0):
    rn = now()
    delta_duration = datetime.timedelta(seconds = sec_duration)
    while now() < (rn + delta_duration):
        if isinstance(task, int):
            subprocess.Popen(f"taskkill /pid {task} /t /f", shell = True)
        elif isinstance(task, str):
            subprocess.Popen(f"taskkill /im {task} /t /f", shell = True)
        else:
            raise TypeError("task is not either an integer (ID number) or str (task name)")
        time.sleep(0.5)
        
def taskkill_list(task_list: Sequence[str], sec_duration = 0):
    rn = now()
    delta_duration = datetime.timedelta(seconds=sec_duration)
    while now() < (rn + delta_duration):
        for task in task_list:
            subprocess.Popen(f"taskkill /im {task} /t /f")
        time.sleep(0.5)

if __name__ == "__main__":
    pass
    # taskkill_list(["chrome.exe", "Notion.exe", "notepad.exe", "msedge.exe"], sec_duration=30)