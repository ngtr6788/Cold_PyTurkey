import argparse
import cold_pyturkey as pyturkey

_FROZEN = "frozen"

def main():
    # TODO: Make a help string later. I just need it to work first.

    # I made the top-level parser for the function type only.
    parser = argparse.ArgumentParser()
    func_parser = parser.add_subparsers(title="function")

    # subparser for start command
    def parse_start(args):
        pyturkey.start_block(args.blockname, args.minutes, args.lock)
    pstart = func_parser.add_parser("start")
    pstart.add_argument("blockname", type=str)
    pstart.add_argument("-l", "--lock", action="store_true")
    pstart.add_argument("minutes", type=int)
    pstart.set_defaults(func=parse_start)

    # subparser for stop command
    def parse_stop(args):
        pyturkey.stop_block(args.blockname)
    ptoggle = func_parser.add_parser("stop")
    ptoggle.add_argument("blockname", type=str)
    ptoggle.set_defaults(func=parse_stop)

    # subparser for toggle command
    def parse_toggle(args):
        pyturkey.toggle_block(args.blockname)
    ptoggle = func_parser.add_parser("toggle")
    ptoggle.add_argument("blockname", type=str)
    ptoggle.set_defaults(func=parse_toggle)

    # subparser for add command

    # subparser for pomodoro command
    def parse_pomodoro(args):
        pyturkey.pomodoro(args.blockname, args.blockmin, args.breakmin, args.breakf, args.loops, args.lock)

    pmdr = func_parser.add_parser("pomodoro")
    pmdr.add_argument("blockname", type=str)
    pmdr.add_argument("blockmin", type=int)
    pmdr.add_argument("breakmin", type=int)
    pmdr.add_argument("loops", type=int)
    pmdr.add_argument("-l", "--lock", action='store_true')
    pmdr.add_argument("--breakf", action='store_false')
    pmdr.set_defaults(func=parse_pomodoro)

    # subparser for frozen (start frozen) command

    # what else?
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()