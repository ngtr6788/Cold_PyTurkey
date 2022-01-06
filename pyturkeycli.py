import subprocess
import sys
import datetime
import cold_pyturkey as pyturkey
from cold_pyturkey import _COLD_TURKEY

_FROZEN = "frozen"

def main(argv):
    if len(argv) == 0:
        # if just pyturkey, it opens Cold Turkey
        subprocess.Popen(_COLD_TURKEY)
    else: 
        blockName = argv[1]
        # parameters: pyturkey [start|stop|toggle|add|pomodoro]
        if argv[0] == "start":
            # pyturkey start [ (nothing) |for|until] 
            if len(argv) == 2:
                pyturkey.start_block(blockName, lock = False)
            elif argv[2] == "for":
                # pyturkey start blockname for duration
                time = int(argv[3])
                pyturkey.start_block(blockName, time)
            elif argv[2] == "until":
                # Parameter for until looks like
                # pyturkey start blockname until time [date]
                # if date is not mentioned, it's assumed to be today
                time_end = datetime.time.fromisoformat(argv[3])
                if len(argv) == 5:
                    date_end = datetime.date.fromisoformat(argv[4])
                else:
                    date_end = datetime.date.today()
                
                datetime_end = datetime.datetime.combine(date_end, time_end)
                pyturkey.start_block_until(blockName, datetime_end)

        elif argv[0] == "stop":
            # pyturkey stop blockname
            pyturkey.stop_block(blockName)
        elif argv[0] == "toggle":
            # pyturkey toggle blockname
            pyturkey.toggle_block(blockName)
        elif argv[0] == "add":
            # pyturkey add blockname url (except)
            url = argv[2]
            exception = True if argv[3] == "except" else False
            pyturkey.add_url(blockName, url, exception)
        elif argv[0] == "pomodoro":
            # Arguments for pomodoro
            # pyturkey pomodoro block_name block_duration break_duration loops [-l|--lock] [-r|--break-first]
            block_duration = int(argv[2])
            break_duration = int(argv[3])
            loops = int(argv[4])

            lock = True if ("-l" in argv or "--lock" in argv) else False
            block_first = False if ("-r" in argv or "--break-first" in argv) else True

            pyturkey.pomodoro(blockName, block_duration, break_duration, block_first, loops, lock)

if __name__ == "__main__":
    main(sys.argv[1:])