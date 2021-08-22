# This program demonstrates the function schedule_blocks from pyturkey

import cold_pyturkey as pyturkey
from cold_pyturkey import FROZEN_TURKEY

def main():
    day_sched = [[FROZEN_TURKEY, "00:00", "01:30"],
                 [FROZEN_TURKEY, "13:00", "14:30"],
                 [FROZEN_TURKEY, "19:00", "20:30"],
                 [FROZEN_TURKEY, "22:30", "23:59:59"]]

    pyturkey.schedule_blocks(day_sched)

if __name__ == "__main__":
    main()