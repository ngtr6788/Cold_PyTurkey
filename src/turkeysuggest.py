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
  suggest (add | delete) <block_name> web <url> [-e]
  suggest (add | delete) <block_name> (file | folder | win10 | title) <path>
  suggest settings <block_name>
  suggest blocks [-v]
  suggest save [<file_name>]
  suggest (q | quit)
Options:
  --no-unlock     Does not automatically unlock block after a restart
  -u --unlocked   Block is unlocked between time range (default is locked)
  -l --lock       Simultaneously locks with that type and configures it
  -v --verbose    Displays all blocks as well as each block's settings
  -e --except     Adds a URL as an exception
"""

# NOTE: This can be either run as a script or imported as a module, like in how main.py is run

import re
from src.docopt import docopt
import json
from getpass import getpass
import random
from pathlib import Path
from copy import deepcopy
import shlex
from typing import Dict, List, Union

TurkeySettingsDict = Dict[str, Union[str, List[str]]]
DocoptDict = Dict[str, Union[str, bool, None]]

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

# TODO: Added more helpful comments and test this thing


def main():
    dict_suggestions: Dict[str, TurkeySettingsDict] = dict()

    def print_keys(verbose: bool):
        if verbose:
            # verbose just means that you're printing both the
            # keys AND the settings along with it
            print(json.dumps(dict_suggestions, indent=2))
        else:
            for key in dict_suggestions.keys():
                print(key)

    def create_random_filename() -> str:
        maximum = 10 ** 10
        random_no = random.randint(1, maximum)
        file_name = f"suggest_{random_no}.ctbbl"
        return file_name

    def save_to_ctbbl(dict_args: Dict[str, TurkeySettingsDict]):
        file_name = dict_args["<file_name>"]

        if file_name is None:
            # This is to avoid naming conflicts.
            all_ctbbl_files = list(Path(".").glob("**/*.ctbbl"))
            file_name = create_random_filename()
            while file_name in all_ctbbl_files:
                file_name = create_random_filename()
            # end of naming conflicts
        else:
            file_name = f"{file_name}.ctbbl"

        # we write our dictionary in json format
        with open(file_name, "w") as suggest_file:
            json.dump(dict_suggestions, suggest_file, ensure_ascii=False, indent=2)
        print(
            f"{file_name} created. You can rename this file however you want, as long as it's a .ctbbl file."
        )
        # end of json dump

    def add_new_block(block_name: str):
        if dict_suggestions.get(block_name):
            print(f"Block {block_name} already exists")
        else:
            dict_suggestions[block_name] = deepcopy(DEFAULT_SETTINGS)
            print(f"Block {block_name} added")

    def remove_block(block_name: str):
        dict_suggestions.pop(block_name)
        print(f"Block {block_name} deleted")

    def unlock_block(block_name: str, block_dict: TurkeySettingsDict):
        block_dict["lock"] = "none"
        print(f"Block {block_name} unlocked")

    def config_random(
        block_name: str, block_dict: TurkeySettingsDict, dict_args: DocoptDict
    ):
        length = dict_args["<length>"]  # should it be int?
        block_dict["randomTextLength"] = length
        print(f"Block {block_name} set to be locked with {length} random characters")

    def config_range(
        block_name: str, block_dict: TurkeySettingsDict, dict_args: DocoptDict
    ):
        start_time = dict_args["<start_time>"]
        end_time = dict_args["<end_time>"]

        parse_time = re.compile("(\d{1,2}):(\d{2})")

        start_time_match = parse_time.match(start_time)
        end_time_match = parse_time.match(end_time)

        sh = start_time_match.group(1)  # start hour
        sm = start_time_match.group(2)  # start minute

        eh = end_time_match.group(1)  # end hour
        em = end_time_match.group(2)  # end minute

        un = "un" if dict_args["--unlocked"] else ""

        # convert 9:00 to 9,00 somehow

        block_dict["window"] = f"{un}lock@{sh},{sm}@{eh},{em}"
        print(
            f"Block {block_name} set to {un}lock at a range from {start_time} to {end_time}"
        )

    def config_restart(
        block_name: str, block_dict: TurkeySettingsDict, dict_args: DocoptDict
    ):
        no_unlock = dict_args["--no-unlock"]  # should it be bool?
        block_dict["restartUnblock"] = "true" if no_unlock else "false"
        out = "out" if no_unlock else ""
        print(
            f"Block {block_name} set to be locked until restart, with{out} auto-unlock"
        )

    def config_password(
        block_name: str, block_dict: TurkeySettingsDict, dict_args: DocoptDict
    ):
        password = getpass("Password: ")
        block_dict["password"] = password
        print(f"Block {block_name} set to be locked with password")

    def set_pomodoro(
        block_name: str, block_dict: TurkeySettingsDict, dict_args: DocoptDict
    ):
        block_min = dict_args["<block_minutes>"]
        break_min = dict_args["<break_minutes>"]
        block_dict["break"] = f"{block_min},{break_min}"
        print(
            f"Block {block_name} has a {block_min} min block, {break_min} break pomodoro."
        )

    def set_allowance(
        block_name: str, block_dict: TurkeySettingsDict, dict_args: DocoptDict
    ):
        minutes = dict_args["<minutes>"]
        block_dict["break"] = f"{minutes}"
        print(f"Block {block_name} has an allowance of {minutes} min.")

    def set_nobreak(
        block_name: str, block_dict: TurkeySettingsDict, dict_args: DocoptDict
    ):
        block_dict["break"] = "none"
        print(f"Block {block_name} has no breaks")

    def manage_url(
        block_name: str,
        block_dict: TurkeySettingsDict,
        dict_args: DocoptDict,
        make_exist: bool,
    ):
        url = dict_args["<url>"]
        exception = dict_args["--except"]
        if exception:
            category = "exceptions"
        else:
            category = "web"

        if make_exist:
            # Add url
            block_dict[category].append(url)
            print(
                f"Added {url} {'as an exception ' if exception else ''}to block {block_name}"
            )
        else:
            # Remove url
            try:
                block_dict[category].remove(url)
                print(f"Removed {url} from {block_name}")
            except ValueError:
                print(f"{url} does not exit in {block_name}")

    def manage_apps(
        block_name: str,
        block_dict: TurkeySettingsDict,
        dict_args: DocoptDict,
        make_exist: bool,
    ):
        # NOTE: This implementation is very Windows specific.
        # I do not own a Mac, so I have no idea how it might look

        path_name = dict_args["<path>"]
        for type in ["title", "win10", "folder", "file"]:
            if dict_args[type]:
                # create a path name with forward slashes
                path_name = Path(path_name).as_posix()
                turkey_path = f"{type}:{path_name}"

                if make_exist:
                    # add url
                    block_dict["apps"].append(turkey_path)
                    print(f"Added {path_name} as {type} to block {block_name}")
                else:
                    # remove url
                    try:
                        block_dict["apps"].remove(turkey_path)
                        print(f"Removed {path_name} from {block_name}")
                    except:
                        print(f"{path_name} does not exit in {block_name}")

    while True:
        try:
            # Step 1: we first read input
            stdin_args = input("> suggest ")
            try:
                stdin_args = shlex.split(stdin_args)
            except ValueError as val_err:
                print(val_err)
                print("Invalid parsing of arguments")
                continue

            # Step 2: we parse the input like one would on a command line
            try:
                dict_args: DocoptDict = docopt(__doc__, argv=stdin_args, help=True)
            except SystemExit as usage_on_exit:
                print(usage_on_exit)
                # Here, I probably typed something wrong. This try
                # except block is here so that if invalid parameters,
                # it doesn't quit
                continue

            # Step 3: we do stuff based on the arguments

            # we quit
            if dict_args.get("quit") or dict_args.get("q"):
                raise KeyboardInterrupt

            # we display the block names
            if dict_args["blocks"]:
                print_keys(dict_args["--verbose"])
                continue

            # we save it into a .ctbbl file (JSON format)
            if dict_args["save"]:
                save_to_ctbbl(dict_args)
                continue

            block_name = dict_args["<block_name>"]

            # add new block name
            if dict_args["new"]:
                add_new_block(block_name)

            # determine if block_name exists in order to continue
            if dict_suggestions.get(block_name) == None:
                print(f"Block {block_name} doesn't exist")
                continue
            else:
                block_dict = dict_suggestions[block_name]
            # end of checking existence

            # remove block name
            if dict_args["remove"]:
                remove_block(block_name)

            # display a block's settings
            if dict_args["settings"]:
                print(json.dumps(block_dict, indent=2))

            # set the block name to unlock
            if dict_args["unlock"]:
                unlock_block(block_name, block_dict)

            # here, we configure and/or lock our lock
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
            # end of config/lock

            # here, we deal with breaks, like pomodoro and allowances
            if dict_args["pomodoro"]:
                set_pomodoro(block_name, block_dict, dict_args)
            elif dict_args["allowance"]:
                set_allowance(block_name, block_dict, dict_args)

            elif dict_args["nobreak"]:
                set_nobreak(block_name, block_dict, dict_args)

            # here, we deal with adding and deleting urls/paths
            create = False
            if dict_args["add"]:
                create = True
            elif dict_args["delete"]:
                create = False

            # we choose which location to add/delete
            if dict_args["web"]:
                manage_url(block_name, block_dict, dict_args, create)
            else:
                # NOTE: I use Windows, so I don't know how
                # one might implement this with Mac applications
                manage_apps(block_name, block_dict, dict_args, create)

        except KeyboardInterrupt:
            # this is when someone presses Ctrl + C (Cmd + C), you double
            # check to make sure they really want to exit suggest
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
            # if we're reading it from a text file or whatever, when
            # you finish reading, it's assumed to be the end of it
            break


if __name__ == "__main__":
    main()
