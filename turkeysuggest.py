"""Usage:
  suggest new <block_name>
  suggest remove <block_name>
  suggest unlock <block_name>
  suggest lock <block_name> (random | range | restart | password)
  suggest config <block_name> random <length> [-l]
  suggest config <block_name> range <start_time> <end_time> [-ul]
  suggest config <block_name> restart [--no-unlock] [-l]
  suggest config <block_name> password [-l]
  suggest nobreak <block_name>
  suggest pomodoro <block_name> <block_minutes> <break_minutes>
  suggest allowance <block_name> <minutes>
  suggest add <block_name> web <url> [-e]
  suggest add <block_name> file <path>
  suggest add <block_name> folder <path>
  suggest add <block_name> win10 <path>
  suggest add <block_name> title <path>
  suggest settings <block_name>
  suggest blocks [-v]
  suggest save
  suggest (q | quit)
Options:
  --no-unlock       Does not automatically unlock block after a restart
  -u --unlocked     Block is unlocked between time range (default is locked)
  -l --lock         Simultaneously locks with that type and configures it
  -v --verbose      Displays all blocks as well as each block's settings
  -e --except       Adds a URL as an exception
"""

import re
from docopt import docopt
import json
from getpass import getpass
import random
from pathlib import Path
from copy import deepcopy
import shlex

DEFAULT_SETTINGS = {
    "enabled": "false",
    "type": "continuous",
    "timer": "",
    "startTime": "",
    "lock": "none",
    "lockUnblock": "true",
    "restartUnblock": "true",
    "break": "none",
    "password": "",
    "randomTextLength": "30",
    "window": "lock@9,0@17,0",
    "users": "all",
    "web": [],
    "exceptions": ["file://*"],
    "apps": [],
    "schedule": [],
    "customUsers": [],
}


def main():
    dict_suggestions = dict()

    def print_keys(verbose):
        if verbose:
            print(json.dumps(dict_suggestions, indent=2))
        else:
            for key in dict_suggestions.keys():
                print(key)

    def save_to_ctbbl():

        # This is to avoid naming conflicts.
        maximum = 10 ** 10
        all_ctbbl_files = list(Path(".").glob("**/*.ctbbl"))

        random_no = random.randint(1, maximum)
        file_name = f"suggestions_{random_no}.ctbbl"
        while file_name in all_ctbbl_files:
            random_no = random.randint(1, maximum)
            file_name = f"suggestions_{random_no}.ctbbl"
        # end of naming conflicts

        # we write our dictionary in json format
        with open(file_name, "w") as suggest_file:
            json.dump(dict_suggestions, suggest_file, ensure_ascii=False, indent=2)
        print(
            f"{file_name} created. You can rename this file however you want, as long as it's a .ctbbl file."
        )
        # end of json dump

    def add_new_block(block_name):
        if dict_suggestions.get(block_name):
            print(f"Block {block_name} already exists")
        else:
            dict_suggestions[block_name] = deepcopy(DEFAULT_SETTINGS)
            print(f"Block {block_name} added")

    def remove_block(block_name):
        dict_suggestions.pop(block_name)
        print(f"Block {block_name} deleted")

    def config_random(block_name, block_dict, dict_args):
        length = dict_args["<length>"]  # should it be int?
        block_dict["randomTextLength"] = length
        print(f"Block {block_name} set to be locked with {length} random characters")

    def config_range(block_name, block_dict, dict_args):
        start_time = dict_args["<start_time>"]
        end_time = dict_args["<end_time>"]

        parse_time = re.compile("(\d{1,2}):(\d{2})")

        start_time_match = parse_time.match(start_time)
        end_time_match = parse_time.match(end_time)

        sh = start_time_match.group(1)
        sm = start_time_match.group(2)

        eh = end_time_match.group(1)
        em = end_time_match.group(2)

        un = "un" if dict_args["--unlocked"] else ""

        # convert 9:00 to 9,00 somehow

        block_dict["window"] = f"{un}lock@{sh},{sm}@{eh},{em}"
        print(
            f"Block {block_name} set to {un}lock at a range from {start_time} to {end_time}"
        )

    def config_restart(block_name, block_dict, dict_args):
        no_unlock = dict_args["--no-unlock"]  # should it be bool?
        block_dict["restartUnblock"] = "true" if no_unlock else "false"
        out = "out" if no_unlock else ""
        print(
            f"Block {block_name} set to be locked until restart, with{out} auto-unlock"
        )

    def config_password(block_name, block_dict, dict_args):
        password = getpass("Password: ")
        block_dict["password"] = password
        print(f"Block {block_name} set to be locked with password")

    def set_pomodoro(block_name, block_dict, dict_args):
        block_min = dict_args["<block_minutes>"]
        break_min = dict_args["<break_minutes>"]
        block_dict["break"] = f"{block_min},{break_min}"
        print(
            f"Block {block_name} has a {block_min} min block, {break_min} break pomodoro."
        )

    def set_allowance(block_name, block_dict, dict_args):
        minutes = dict_args["<minutes>"]
        block_dict["break"] = f"{minutes}"
        print(f"Block {block_name} has an allowance of {minutes} min.")

    def set_nobreak(block_name, block_dict, dict_args):
        block_dict["break"] = "none"
        print(f"Block {block_name} has no breaks")

    def add_url(block_name, block_dict, dict_args):
        url = dict_args["<url>"]
        exception = dict_args["--except"]
        if exception:
            category = "exceptions"
        else:
            category = "web"
        block_dict[category].append(url)
        print(
            f"Added {url} {'as an exception ' if exception else ''}to block {block_name}"
        )

    def add_applications(block_name, block_dict, dict_args):
        # NOTE: This implementation is very Windows specific.
        # I do not own a Mac, so I have no idea how it might look

        path_name = dict_args["<path>"]
        for type in ["title", "win10", "folder", "file"]:
            if dict_args[type]:
                # create a path name with forward slashes
                path_name = Path(path_name).as_posix()  
                block_dict["apps"].append(f"{type}:{path_name}")
                print(f"Added {path_name} as {type} to block {block_name}")

    # print(DEFAULT_SETTINGS)

    while True:
        try:
            stdin_args = input("> suggest ")
            stdin_args = shlex.split(stdin_args)
            try:
                dict_args = docopt(__doc__, argv=stdin_args, help=True)
            except:
                # Here, I probably typed something wrong. This try
                # except block is here so that if invalid parameters,
                # it doesn't quit
                continue

            if dict_args.get("quit") or dict_args.get("q"):
                raise KeyboardInterrupt

            if dict_args["blocks"]:
                print_keys(dict_args["--verbose"])
                continue

            if dict_args["save"]:
                save_to_ctbbl()
                continue

            block_name = dict_args["<block_name>"]

            if dict_args["new"]:
                add_new_block(block_name)

            # determine if block_name exists in order to continue
            if dict_suggestions.get(block_name) == None:
                print(f"Block {block_name} doesn't exist")
                continue
            else:
                block_dict = dict_suggestions[block_name]
            # end of checking existence

            if dict_args["remove"]:
                remove_block(block_name)

            if dict_args["settings"]:
                print(json.dumps(block_dict, indent=2))

            if dict_args["unlock"]:
                block_dict["lock"] = "none"

            config_mode = dict_args["config"]
            lock_mode = dict_args["lock"] or dict_args["--lock"]

            if dict_args["random"]:
                lock_method = "randomText"
                config_method = config_random

            elif dict_args["range"]:
                lock_method = "window"
                config_method = config_range

            elif dict_args["restart"]:
                lock_method = "restart"
                config_method = config_restart

            elif dict_args["password"]:
                lock_method = "password"
                config_method = config_password

            if config_mode:
                config_method(block_name, block_dict, dict_args)

            if lock_mode:
                block_dict["lock"] = lock_method
                print(
                    f"Block {block_name} has been locked by {lock_method} on settings"
                )

            if dict_args["pomodoro"]:
                set_pomodoro(block_name, block_dict, dict_args)
            elif dict_args["allowance"]:
                set_allowance(block_name, block_dict, dict_args)

            elif dict_args["nobreak"]:
                set_nobreak(block_name, block_dict, dict_args)

            if dict_args["add"]:
                if dict_args["web"]:
                    add_url(block_name, block_dict, dict_args)
                else:
                    # NOTE: I use Windows, so I don't know how
                    # one might implement this with Mac applications
                    add_applications(block_name, block_dict, dict_args)

        except KeyboardInterrupt:
            try:
                wants_exit = False
                while True:
                    sure_exit = input(
                        "Are you sure you want to exit? Any unsaved settings will be lost. (Y/N) "
                    )

                    if sure_exit in ["Y", "y"]:
                        wants_exit = True
                        break
                    elif sure_exit in ["N", "n"]:
                        wants_exit = False
                        break
                    else:
                        continue

                if wants_exit:
                    break
                else:
                    continue

            except KeyboardInterrupt:
                break
        except EOFError:
            break


if __name__ == "__main__":
    main()
