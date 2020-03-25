import os
from json import load
from sys import exit
from termcolor import colored
from argparse import ArgumentParser
from src.settings_manager import SettingsManager
from src.input_controller import InputController

# TODO: Optimize imports
# TODO: Add test cases

# Get Project Manager's home directory
PROJECT_MANAGER_HOME = str(os.path.dirname(os.path.abspath(__file__)))

__version__ = "v0.1 Beta"

parser = ArgumentParser("pm", description=f"Project Manager - Easily create, manage and categorize your projects")

exclusive_group = parser.add_mutually_exclusive_group(required=True)
exclusive_group.add_argument("-o", "--open", help="Open the specified project", action="store_true")
exclusive_group.add_argument("-c", "--create", help="Create a new project or group", action="store_true")
exclusive_group.add_argument("-l", "--list", help="List all of the groups, projects or projects in the specified group", action="store_true")
exclusive_group.add_argument("-s", "--setup", help="Run the setup for Project Manager", action="store_true")
exclusive_group.add_argument("--config", help="Configure Project Manager", choices=["list", "value", "set", "remove"])

parser.add_argument("-n", "--name", help="The project you want to specify", type=str)
parser.add_argument("-g", "--group", help="The group you want to specify", type=str)
parser.add_argument("--key", help="Key value of the setting", type=str)
parser.add_argument("--value", help="Value of the setting", type=str)
#parser.add_argument("-v", "--version", help="Shows the version number of Project Manager", version=__version__)
# FIXME: Line 30 doesn't working

args = parser.parse_args()

# Check if the pm-settings.json not exists in the project's home folder and --setup is not specified
if not os.path.exists(f"{PROJECT_MANAGER_HOME}/pm-settings.json") and not args.setup:
    print(colored("Project Manager is not configured, please run 'pm setup' before any use", "white", "on_red"))
    exit(1)
elif not args.setup:
    with open(f"{PROJECT_MANAGER_HOME}/pm-settings.json", "r") as f:
        settings = load(f)

# ANCHOR: Open project
if args.open is True:
    if args.name is None:
        print("Please specify the project you want to open. (with --file)")
        exit(1)
    
    # TODO: Complete this function
    print(colored("This function is not yet complete. Please check for an update or wait for a next release.", "white", "on_red"))
    exit(1)

# ANCHOR: Create project or group
elif args.create is True:
    # TODO: Complete this function

    print(colored("This function is not yet complete. Please check for an update or wait for a next release.", "white", "on_red"))
    exit(1)

# ANCHOR: Create project or group
elif args.list is True:
    # TODO: Complete this function

    print(colored("This function is not yet complete. Please check for an update or wait for a next release.", "white", "on_red"))
    exit(1)

# ANCHOR: Setup 
elif args.setup:
    settings_manager = SettingsManager(PROJECT_MANAGER_HOME, InputController())
    settings_manager.setup()
    exit()

# ANCHOR: Create project or group
elif args.config:
    # TODO: Complete this function

    print(colored("This function is not yet complete. Please check for an update or wait for a next release.", "white", "on_red"))
    exit(1)

# ANCHOR: Create project or group
elif args.version:
    # TODO: Complete this function

    print(colored("This function is not yet complete. Please check for an update or wait for a next release.", "white", "on_red"))
    exit(1)
