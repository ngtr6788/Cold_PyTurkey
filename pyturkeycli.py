import subprocess
import sys
import datetime
import cold_pyturkey as pyturkey
from cold_pyturkey import _COLD_TURKEY

_FROZEN = "frozen"

"""How to type in the commands

To open Cold Turkey
$ pyturkey

To start a block:
$ pyturkey start <block_name> [for <minutes> | until <time> [<date>]] 

To stop a block:
$ pyturkey stop <block_name>

To add a URL to a block:
$ pyturkey add <block_name> <url> [-e | --except]

To toggle a block:
$ pyturkey toggle <block_name>

To start a pomodoro block
$ pyturkey pomodoro <block_name> <block_minutes> <break_minutes> <loops> [-r | --break-first] 

Options:
    -e --except Add a url in the exceptions list
    -r --break-first For the pomodoro, you don't block first.
"""


def main(argv):
    if len(argv) == 0:
        # if just pyturkey, it opens Cold Turkey
        subprocess.Popen(_COLD_TURKEY)
    else:
        blockName = argv[1]
        if argv[0] == "start":
            # pyturkey start <blockname> [for|until]
            if len(argv) == 2:
                # pyturkey start <blockname>
                pyturkey.start_block(blockName)
            elif argv[2] == "for":
                # pyturkey start <blockname> for <duration>
                time = int(argv[3])
                pyturkey.start_block(blockName, time)
            elif argv[2] == "until":
                # Parameter for until looks like
                # pyturkey start <blockname> until <time> [<date>]
                # if date is not mentioned, it's assumed to be today
                time_end = datetime.time.fromisoformat(argv[3])
                if len(argv) == 5:
                    date_end = datetime.date.fromisoformat(argv[4])
                else:
                    date_end = datetime.date.today()

                datetime_end = datetime.datetime.combine(date_end, time_end)
                pyturkey.start_block_until(blockName, datetime_end)

        elif argv[0] == "stop":
            # pyturkey stop <blockname>
            pyturkey.stop_block(blockName)
        elif argv[0] == "toggle":
            # pyturkey toggle <blockname>
            pyturkey.toggle_block(blockName)
        elif argv[0] == "add":
            # pyturkey add <blockname> <url> [except]
            exception = True if ("-e" in argv or "--except" in argv) else False

            tagless_argv = list(filter(
                lambda x: not (x in ["-e", "--except"]), argv))

            url = tagless_argv[2]

            pyturkey.add_url(blockName, url, exception)
        elif argv[0] == "pomodoro":
            # Arguments for pomodoro
            # pyturkey pomodoro <block_name> <block_duration> <break_duration> <loops> [-r|--break-first]

            break_first = True if (
                "-r" in argv or "--break-first" in argv) else False

            tagless_argv = list(filter(
                lambda x: not (x in ["-r", "--break-first"]), argv))

            block_duration = int(tagless_argv[2])
            break_duration = int(tagless_argv[3])
            loops = int(tagless_argv[4])

            pyturkey.pomodoro(blockName, block_duration,
                              break_duration, loops, break_first)


if __name__ == "__main__":
    main(sys.argv[1:])
