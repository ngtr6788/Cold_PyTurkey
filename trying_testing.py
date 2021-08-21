# This program demonstrates the function schedule_blocks from pyturkey

import cold_pyturkey as pyturkey
from cold_pyturkey import FROZEN_TURKEY

def main():
    day_sched = [[FROZEN_TURKEY, "00:00", "01:30"],
                 [FROZEN_TURKEY, "22:30", "23:59:59"],
                 [FROZEN_TURKEY, "16:00", "16:30"],
                 ["Netflix", "17:00", "17:30"]]

    print(pyturkey.schedule_blocks(day_sched))

if __name__ == "__main__":
    main()