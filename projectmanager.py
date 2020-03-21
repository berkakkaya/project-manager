import os
from sys import exit
from argparse import ArgumentParser
from src.settings_manager import SettingsManager
from src.input_controller import InputController

# TODO: Optimize imports
# TODO: Add test cases

# Get Project Manager's home directory
PROJECT_MANAGER_HOME = str(os.path.dirname(os.path.abspath(__file__)))

VER = "v0.1 Beta"

parser = ArgumentParser("pm", description=f"Project Manager\nEasily create, manage and categorize your projects")

exclusive_group = parser.add_mutually_exclusive_group(required=True)
exclusive_group.add_argument("-o", "--open", help="Open the specified project", action="store_true")
exclusive_group.add_argument("-c", "--create", help="Create a new project or group", action="store_true")
exclusive_group.add_argument("-l", "--listgroups", help="List all of the groups, projects or projects in the specified group", action="store_true")
exclusive_group.add_argument("-s", "--setup", help="Run the setup for Project Manager", action="store_true")
exclusive_group.add_argument("--config", help="Configure Project Manager", choices=["list", "value", "set", "remove"])
exclusive_group.add_argument("-v", "--version", help="Shows the version number of Project Manager", version=f"Project Manager {VER}")

parser.add_argument("-n", "--name", help="The project you want to specify", type=str)
parser.add_argument("-g", "--group", help="The group you want to specify", type=str)
parser.add_argument("--key", help="Key value of the setting", type=str)
parser.add_argument("--value", help="Value of the setting", type=str)

args = parser.parse_args()

# Check if the pm-settings.json not exists in the project's home folder and --setup is not specified
if not os.path.exists(f"{PROJECT_MANAGER_HOME}/pm-settings.json") and not args.setup:
    print("Project Manager is not configured, please run 'pm setup' before any use")
    exit(1)

# SECTION: Open project
if args.open:
    # TODO: Complete this function

    print("This function is not yet complete. Please check for an update or wait for a next release.")
    exit(1)

# SECTION: Create project or group
elif args.create:
    # TODO: Complete this function

    print("This function is not yet complete. Please check for an update or wait for a next release.")
    exit(1)

# SECTION: Create project or group
elif args.listgroups:
    # TODO: Complete this function

    print("This function is not yet complete. Please check for an update or wait for a next release.")
    exit(1)

# SECTION: Setup 
elif args.setup:
    settings_manager = SettingsManager(PROJECT_MANAGER_HOME, InputController())
    settings_manager.setup()
    exit()

# SECTION: Create project or group
elif args.config:
    # TODO: Complete this function

    print("This function is not yet complete. Please check for an update or wait for a next release.")
    exit(1)

# SECTION: Create project or group
elif args.version:
    # TODO: Complete this function

    print("This function is not yet complete. Please check for an update or wait for a next release.")
    exit(1)