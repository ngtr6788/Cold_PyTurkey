# This program demonstrates the function schedule_blocks from pyturkey

import pyturkey
from pyturkey import FROZEN_TURKEY

def main():
    # day_sched = [[FROZEN_TURKEY, "00:00", "01:30"],
                 # [FROZEN_TURKEY, "23:00", "23:59:59"]]  # Bedtime

    # pyturkey.schedule_blocks(day_sched)

    pyturkey.pomodoro(FROZEN_TURKEY, 15, 90, False, 1, True)

if __name__ == "__main__":
    main()