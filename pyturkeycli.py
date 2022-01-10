"""pyturkey, a better CLI interface for Cold Turkey, written in Python

Usage:
  pyturkey
  pyturkey start <block_name>
  pyturkey start <block_name> for <minutes>
  pyturkey start <block_name> until <time> [<date>]
  pyturkey stop <block_name>
  pyturkey add <block_name> <url> [-e]
  pyturkey toggle <block_name>
  pyturkey pomodoro <block_name> <block_minutes> <break_minutes> --loops=LOOPS [-bt]
  pyturkey suggest

Options:
  -h --help         Show this screen.
  -e --except       Adds <url> as an exception
  -b --break-first  Starts the pomodoro with the block name unblocked first
  -t --timer        Displays a countdown pomodoro timer 
  --loops=LOOPS     Number of loops in a pomodoro session
"""

# Thanks to the docopt library provided by Vladimir Keleshev (check out https://github.com/docopt/docopt), I can simply rewrite pyturkeycli.py in a much, much simpler way, not to mention a free help thing

# UPDATE: Apparently, this library is not maintained for a few years now. However, it's a personal project for myself, I'm not TOO worried about it right now. If I will need to display it to the world, I will really need to fix it.

import pyturkey
from pyturkey import FROZEN_TURKEY

from docopt import docopt
import sys
import time, datetime
import math
import turkeysuggest
from typing import Dict, Union

DocoptDict = Dict[str, Union[str, bool, None]]

def display_pomodoro_timer(
    block_name: str,
    block_duration: int,
    break_duration: int,
    loops: int,
    break_first: bool,
):
    block_session = not break_first

    now_func = datetime.datetime.now

    for i in range(2 * loops):
        if block_session:
            pyturkey.start_block(block_name, block_duration)
            duration = block_duration
            session_type = "Block session"
        else:
            pyturkey.stop_block(block_name)
            duration = break_duration
            session_type = "Break session"

        now = now_func()
        later = now + datetime.timedelta(minutes=duration)

        while now_func() < later:
            sys.stdout.write("\r")
            remaining = (later - now_func()).total_seconds()

            min_remain = math.floor(remaining / 60)
            sec_remain = math.floor(remaining % 60)

            sys.stdout.write(f"Loop #{i // 2 + 1} ")
            sys.stdout.write(session_type)
            sys.stdout.write(f" {min_remain} min {sec_remain} s remaining   ")
            sys.stdout.flush()
            time.sleep(1)

        block_session = not block_session


def main():
    args_dict: DocoptDict = docopt(__doc__)

    block_name = args_dict["<block_name>"]
    block_name = FROZEN_TURKEY if block_name == "frozen" else block_name

    if args_dict["start"]:
        if args_dict["for"]:
            block_duration = int(args_dict["<minutes>"])
            pyturkey.start_block(block_name, block_duration)
        elif args_dict["until"]:
            # if date is not mentioned, assume today
            time_end = datetime.time.fromisoformat(args_dict["<time>"])
            if not args_dict["<date>"] is None:
                date_end = datetime.date.fromisoformat(args_dict["<date>"])
            else:
                date_end = datetime.date.today()

            # create a datetime to pass into start_block_until
            datetime_end = datetime.datetime.combine(date_end, time_end)

            pyturkey.start_block_until(block_name, datetime_end)
        else:
            pyturkey.start_block(block_name)
    elif args_dict["stop"]:
        pyturkey.stop_block(block_name)
    elif args_dict["toggle"]:
        pyturkey.toggle_block(block_name)
    elif args_dict["add"]:
        exception = args_dict["--except"]
        url = args_dict["<url>"]
        pyturkey.add_url(block_name, url, exception)
    elif args_dict["pomodoro"]:
        try:
            break_first = args_dict["--break-first"]

            block_duration = int(args_dict["<block_minutes>"])
            break_duration = int(args_dict["<break_minutes>"])
            loops = int(args_dict["--loops"])

            if args_dict["--timer"]:
                display_pomodoro_timer(
                    block_name, block_duration, break_duration, loops, break_first
                )
            else:
                pyturkey.pomodoro(
                    block_name, block_duration, break_duration, loops, break_first
                )

        except KeyboardInterrupt:
            print(
                "\n\nPomodoro timer has stopped. However, be aware of any unfinished blocks as pyturkey is unable to stop it."
            )
    elif args_dict["suggest"]:
        turkeysuggest.main()
    else:
        pyturkey.open_cold_turkey()


if __name__ == "__main__":
    main()
