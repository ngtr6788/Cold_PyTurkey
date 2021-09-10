import argparse
import datetime
import cold_pyturkey as pyturkey

_FROZEN = "frozen"

def main():
    # TODO: Make a help string later. I just need it to work first.
    def _blockprocess(blockname):
        if _FROZEN == blockname:
            return pyturkey.FROZEN_TURKEY
        else:
            return blockname

    # I made the top-level parser for the function type only.
    parser = argparse.ArgumentParser()
    func_parser = parser.add_subparsers(prog="pyturkey", title="function")

    # subparser for start command
    """
    ROUGH DRAFT OF HOW start WOULD WORK.
    you could either call
    start "Block Name"
    start "Block Name" minutes (number) (-l)
    start "Block Name" until (endtime) (enddate) --at (startdatetime)
    if (date) is not mentioned, it's assumed to be today.
    """
    pstart = func_parser.add_parser("start")
    pstart.add_argument("blockname", type=str)
    start_options = pstart.add_subparsers(title="options")
    
    # subparser for start for
    def parse_start(args):
        pyturkey.start_block(_blockprocess(args.blockname), args.minutes, args.lock)
    pminutes = start_options.add_parser("for")
    pminutes.add_argument("minutes", type=int, default=0)
    pminutes.add_argument("-l", "--lock", action="store_true")
    pminutes.set_defaults(func=parse_start)

    # subparser for start until
    def parse_start_until(args):
        endtimeobj = datetime.time.fromisoformat(args.endtime)
        enddateobj = pyturkey.today() if (args.enddate is None) else datetime.date.fromisoformat(args.enddate)
        enddatetime = datetime.datetime.combine(enddateobj, endtimeobj)
        startdatetime = pyturkey.now() if (args.startat is None) else datetime.datetime.fromisoformat(args.startat)

        pyturkey.start_block_until(_blockprocess(args.blockname), enddatetime, startdatetime)

    puntil = start_options.add_parser("until")   
    puntil.add_argument("endtime", type=str)
    puntil.add_argument("--enddate", type=str, default=None)
    puntil.add_argument("--startat", type=str, required=False, default=None)
    puntil.set_defaults(func=parse_start_until)

    # subparser for stop command
    def parse_stop(args):
        pyturkey.stop_block(_blockprocess(args.blockname))

    ptoggle = func_parser.add_parser("stop")
    ptoggle.add_argument("blockname", type=str)
    ptoggle.set_defaults(func=parse_stop)

    # subparser for toggle command
    def parse_toggle(args):
        pyturkey.toggle_block(_blockprocess(args.blockname))

    ptoggle = func_parser.add_parser("toggle")
    ptoggle.add_argument("blockname", type=str)
    ptoggle.set_defaults(func=parse_toggle)

    # subparser for add command
    def parse_add(args):
        pyturkey.add_url(_blockprocess(args.blockname), args.url, args.exception)

    padd = func_parser.add_parser("add")
    padd.add_argument("blockname", type=str)
    padd.add_argument("url", type=str)
    padd.add_argument("--exception", action="store_true")
    padd.set_defaults(func = parse_add)

    # subparser for pomodoro command
    def parse_pomodoro(args):
        pyturkey.pomodoro(_blockprocess(args.blockname), args.blockmin, args.breakmin, args.breakf, args.loops, args.lock)

    pmdr = func_parser.add_parser("pomodoro")
    pmdr.add_argument("blockname", type=str)
    pmdr.add_argument("blockmin", type=int)
    pmdr.add_argument("breakmin", type=int)
    pmdr.add_argument("loops", type=int, default=1)
    pmdr.add_argument("-l", "--lock", action='store_true')
    pmdr.add_argument("--breakf", action='store_false')
    pmdr.set_defaults(func=parse_pomodoro)

    # subparser for frozen (start frozen) command

    # what else?
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()