"""Usage:
  suggest new <block_name>
  suggest remove <block_name>
  suggest unlock <block_name>
  suggest set <block_name> random <length>
  suggest set <block_name> timerange <start_time> <end_time> -u
  suggest set <block_name> restart [--no-unlock]
  suggest set <block_name> password
  suggest lock <block_name> random
  suggest lock <block_name> timerange 
  suggest lock <block_name> restart
  suggest lock <block_name> password
  suggest pomodoro <block_name> <block_time> <break_time>
  suggest allowance <block_name> <duration>
  suggest settings <block_name>
  suggest done
Options:
  --no-unlock       Does not automatically unlock block after a restart
  -u --unlocked     Block is unlocked between time ranged (default is locked)
"""

from docopt import docopt
import json
from getpass import getpass

DEFAULT_STR = """{"enabled":"false","type":"continuous","startTime":"","lock":"none","lockUnblock":"true","restartUnblock":"true","break":"none","password":"","randomTextLength":"30","window":"lock@9,0@17,0","users":"all","web":[],"exceptions":[],"apps":[],"schedule":[],"customUsers":[]}}"""

DEFAULT_SETTINGS = {
    "enabled": False,
    "type": "continuous",
    "timer": "",
    "startTime": "",
    "lock": "none",
    "lockUnblock": True,
    "restartUnblock": True,
    "break": "none",
    "password": "",
    "randomTextLength": 30,
    "window": "lock@9,0@17,0",
    "users": "all",
    "web": [],
    "exceptions": [],
    "apps": [],
    "schedule": [],
    "customUsers": [],
}


def main():
    dict_suggestions = dict()

    # print(DEFAULT_SETTINGS)

    while True:
        try:
            stdin_args = input("> suggest ")
            stdin_args = stdin_args.split(" ")
            dict_args = docopt(__doc__, argv=stdin_args, help=False)

            block_name = dict_args["<block_name>"]

            if dict_args["new"]:
                if dict_suggestions.get(block_name):
                    print(f"Block {block_name} already exists")
                else:
                    dict_suggestions[block_name] = DEFAULT_SETTINGS
                    print(f"Block {block_name} added")

            if dict_suggestions.get(block_name) == None:
                print(f"Block {block_name} doesn't exist")
                continue
            else:
                block_dict = dict_suggestions[block_name]

            if dict_args["remove"]:
                dict_suggestions.pop(block_name)
                print(f"Block {block_name} deleted")

            if dict_args["settings"]:
                print(json.dumps(block_dict, indent=2))

            set_mode = dict_args["set"]
            lock_mode = dict_args["lock"]

            if dict_args["random"]:
                # block_dict["lock"] = "randomText"

                length = dict_args["<length>"]  # should it be int?
                block_dict["randomTextLength"] = length
                print(
                    f"Block {block_name} set to be locked with {length} random characters"
                )
            elif dict_args["timerange"]:
                # block_dict["lock"] = "window"

                start_time = dict_args["<start_time>"]
                end_time = dict_args["<end_time>"]
                un = "un" if dict_args["--unlocked"] else ""

                # convert 9:00 to 9,00 somehow

                block_dict["window"] = f"{un}lock@{start_time}@{end_time}"
            elif dict_args["restart"]:
                # block_dict["lock"] = "restart"
                no_unlock = dict_args["--no-unlock"]  # should it be bool?
                block_dict["restartUnblock"] = no_unlock
                out = "out" if no_unlock else ""
                print(
                    f"Block {block_name} set to be locked until restart, with{out} auto-unlock"
                )
            elif dict_args["password"]:
                # block_dict["lock"] = "password"
                password = getpass("Password: ")
                block_dict["password"] = password
                print(f"Block {block_name} set to be locked with password")

        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    main()
