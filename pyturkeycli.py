import subprocess
import sys
import time
import datetime
import cold_pyturkey as pyturkey
from cold_pyturkey import _COLD_TURKEY
import json
from pathlib import Path
import math

_FROZEN = "frozen"

"""How to type in the commands

To open Cold Turkey
$ pyturkey

To start a block:
$ pyturkey start <block_name> [for <minutes> | until <time> [<date>]] 
If <date> is not written, it is assumed to be today, 

To stop a block:
$ pyturkey stop <block_name>

To add a URL to a block:
$ pyturkey add <block_name> <url> [-e | --except]

To toggle a block:
$ pyturkey toggle <block_name>

To start a pomodoro block
$ pyturkey pomodoro <block_name> <block_minutes> <break_minutes> <loops> [-b | --break-first] 

Options:
    -e --except Add a url in the exceptions list
    -b --break-first For the pomodoro, you don't block first.
"""


def main(argv):
    # Here, we're looking for one single .ctbbl file, primarily
    # so we can assist the client with whether or not
    # the block name exists in Cold Turkey or not
    all_ctbbl_files = list(Path(".").glob("**/*.ctbbl"))

    len_ctbbl = len(all_ctbbl_files)
    if len_ctbbl == 1:
        with all_ctbbl_files[0].open() as block_json:
            block_info = json.load(block_json)
    elif len_ctbbl == 0:
        block_info = None
    else:
        print("There are too many .ctbbl files in there, but not to fret. Just provide one .ctbbl file that best reflects the actual blocks in Cold Turkey")
        block_info = None

    # This is where we read the arguments
    if len(argv) == 0:
        # if just pyturkey, it opens Cold Turkey
        subprocess.Popen(_COLD_TURKEY)
    else:
        # This section deals with parsing the tags and non-tags
        def is_tag(arg):
            return arg[0] == "-"

        # Find all tags
        tags = list(filter(is_tag, argv))

        # Find all arguments that aren't tags, hence the special lambda function
        tagless_argv = list(filter(lambda x: not is_tag(x), argv))
        print(tags)
        print(tagless_argv)

        blockName = tagless_argv[1]

        # Here, we use the information from the .ctbbl to aid
        # us a little whether the block name is in Cold Turkey GUI or not
        if (not block_info is None):
            isNot = " " if blockName in block_info else " not "
            print(
                f"The block name you provided is probably{isNot}in your Cold Turkey app.\n")

            print("Your .ctbbl does not always reflect the actual blocks in your Cold Turkey. For best results, make sure that your .ctbbl is updated so pyturkey can better help you.")

        if tagless_argv[0] == "start":
            # pyturkey start <blockname> [for|until]
            if len(tagless_argv) == 2:
                # pyturkey start <blockname>
                pyturkey.start_block(blockName)
            elif tagless_argv[2] == "for":
                # pyturkey start <blockname> for <duration>
                duration = int(tagless_argv[3])
                pyturkey.start_block(blockName, duration)
            elif tagless_argv[2] == "until":
                # pyturkey start <blockname> until <time> [<date>]

                # if date is not mentioned, it's assumed to be today
                time_end = datetime.time.fromisoformat(tagless_argv[3])
                if len(tagless_argv) == 5:
                    date_end = datetime.date.fromisoformat(tagless_argv[4])
                else:
                    date_end = datetime.date.today()

                # create a datetime to pass into start_block_until
                datetime_end = datetime.datetime.combine(date_end, time_end)

                pyturkey.start_block_until(blockName, datetime_end)

        elif tagless_argv[0] == "stop":
            # pyturkey stop <blockname>
            pyturkey.stop_block(blockName)
        elif tagless_argv[0] == "toggle":
            # pyturkey toggle <blockname>
            pyturkey.toggle_block(blockName)
        elif tagless_argv[0] == "add":
            # pyturkey add <blockname> <url> [-e | except]
            exception = True if ("-e" in tags or "--except" in tags) else False

            url = tagless_argv[2]

            pyturkey.add_url(blockName, url, exception)
        elif tagless_argv[0] == "pomodoro":
            # Arguments for pomodoro
            # pyturkey pomodoro <block_name> <block_duration> <break_duration> <loops> [-r|--break-first]

            break_first = True if (
                "-b" in tags or "--break-first" in tags) else False

            block_duration = int(tagless_argv[2])
            break_duration = int(tagless_argv[3])
            loops = int(tagless_argv[4])

            # pyturkey.pomodoro(blockName, block_duration,
            #                   break_duration, loops, break_first)

            block_session = not break_first

            now_func = datetime.datetime.now

            for i in range(2 * loops):
                if block_session:
                    pyturkey.start_block(blockName, block_duration)
                    duration = block_duration
                    session_type = "Block session"
                else:
                    pyturkey.stop_block(blockName)
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
                    sys.stdout.write(
                        f" {min_remain} min {sec_remain} s remaining   ")
                    sys.stdout.flush()
                    time.sleep(1)

                block_session = not block_session


if __name__ == "__main__":
    main(sys.argv[1:])
