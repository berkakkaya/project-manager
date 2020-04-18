import os
from json import load
from sys import exit
from termcolor import colored
from argparse import ArgumentParser
from src.settings_manager import SettingsManager
from src.input_controller import InputController
from src.project_manager import ProjectManager

# TODO: Add test cases

# Get Project Manager's home directory
PM_HOME = str(os.path.dirname(os.path.abspath(__file__)))

__version__ = "v0.2 Beta"

# Check if the pm-settings.json not exists in the project's home folder
if not os.path.exists(f"{PM_HOME}/pm-settings.json"):
    print(colored(f"Welcome to Project Manager {__version__}", "green"))
    print("Looks like this is first time you are running Project Manager.")
    print("Entering setup mode...")

    settings_manager = SettingsManager(PM_HOME)
    settings_manager.setup()
    exit()
else:
    try:
        with open(f"{PM_HOME}/pm-settings.json", "r") as file:
            settings = load(file)
    except:
        print(colored("""The settings cannot be read. Please check pm-settings.json file.""", "red"))
        exit(1)

parser = ArgumentParser("pm", description=f"Project Manager - Easily create, manage and categorize your projects")

options = ["open", "create", "list", "browser", "configure", "config", "reset"]
options_config = ["list", "get", "set", "open"] # Options of argument 'config'

parser.add_argument("action", help="The action you want Project Manager to make", type=str, choices=options)
parser.add_argument("-v", "--version", action="version", version=__version__)

parser.add_argument("-n", "--name", help="The project you want to specify", type=str, default=None)
parser.add_argument("-g", "--group", help="The group you want to specify", type=str, default=None)
parser.add_argument("--key", help="Key value of the setting", type=str, default=None)
parser.add_argument("--value", help="Value of the setting", type=str, default=None)
parser.add_argument("-o", "--option", help="The option that will be used in 'config' action", type=str, choices=options_config)

args = parser.parse_args()

# ANCHOR: Open project
if args.action == "open":
    if args.name is False:
        print(colored("Please specify the project you want to open. (with --name)", "yellow"))
        exit(1)
    
    project_manager = ProjectManager(PM_HOME)
    project_manager.open_project(args.name, args.group)

# ANCHOR: Create project or group
elif args.action == "create":
    input_controller = InputController() # For controlling user input
    
    if args.name: # Checks if --name is specified
        print(f"Project name: {args.name}")
        project_name = args.name
    else:
        project_name = input_controller.get_str("Project name: ")
    
    if args.group: # Checks if --group is specified
        print(f"Project group: {args.group}")
        project_group = args.group
    else:
        project_group = input_controller.get_str("Project group: ")
    
    if settings["token"] != "": # Check if token is set
        create_new_repo = input_controller.get_bool("Do you want to create a new repo at GitHub? (y/n): ")
    else:
        create_new_repo = False
        is_repo_private = False
    
    if create_new_repo:
        is_repo_private = input_controller.get_bool("Do you want to make your repo private? (y/n): ")
    else: is_repo_private = None
    
    print(f"""
    Project creation plan:

    Name: {project_name}
    Group: {project_group}
    
    {f'A new repo will be created on GitHub.' if create_new_repo else 'A new repo will not be created on Github'}
    """)
    
    is_confirmed = input_controller.get_bool("Is it OK? (y/n): ")
    if is_confirmed:
        project_manager = ProjectManager(PM_HOME)
        project_manager.create_project(project_name, project_group, create_new_repo, is_repo_private)

# ANCHOR: List all of the projects, all of the groups or all of the projects in a specified group
elif args.action == "list":
    if args.list in ["projects", "p"]:
        if len(settings["projects"]) == 0: # Check if there are any projects
            print("You don't have any projects.")
        
        elif args.group: # Check if argument "group" is specified
            if args.group not in settings["projects"]:
                print(colored(f"You don't have a group called {args.group}."))
                exit(1)
            print(f"All of the projects in group {args.group} (has {len(settings['projects'][args.group])} projects):")
            for project in settings["projects"][args.group]:
                print(project)
        
        else:
            print("All of your projects:")
            for group in settings["projects"]:
                print(f"{group} (has {len(settings['projects'][group])} project(s))")
                for project in settings["projects"][group]:
                    print(f"\t{project}")
    else:
        if len(settings["projects"]) == 0:
            print("You don't have any groups.")
        else:
            print("All of the groups:")
            for group in settings["projects"]:
                print(f"{group} (Has {len(settings['projects'][group])} project(s))")

# ANCHOR: Open the repository page in browser
elif args.action == "browser":
    if args.name == None:
        print(colored("Please specify your project with --name", "yellow"))
        exit(1)

    project_manager = ProjectManager(PM_HOME)
    project_manager.open_repo_in_browser(args.name, args.group)

# ANCHOR: Configure project settings
elif args.action == "configure":
    if args.name == None:
        print(colored("The project's name is required. Please specify it with --name", "yellow"))
        exit(1)
    
    settings_manager = SettingsManager(PM_HOME)
    settings_manager.configure_project(args.name, args.group, args.key, args.value)

# ANCHOR: Manages settings file
elif args.action == "config":
    key_list = ["projects_folder", "editor_command", "token"]

    if args.option == "set":
        if args.key == None or args.value == None:
            print(colored("Both --key and --value argument must be given.", "yellow"))
            exit(1)

        if args.key not in key_list:
            print(colored("Your specified key is not valid.", "yellow"))
            print(colored("Valid keys: projects_folder, editor_command, token"))
            exit(1)
        
        settings_manager = SettingsManager(PM_HOME)
        settings_manager.set_value(args.key, args.value)
    
    elif args.option == "get":
        if args.key not in key_list:
           print(colored("Your specified key is not valid.", "yellow"))
           print("Valid keys: ", end="")
           print(*key_list, sep=", ")
           exit(1)
        
        print(f"{args.key}: {settings[args.key] if settings[args.key] != '' else 'Not set'}")
    
    elif args.option == "list":
        print("All of your settings:")
        for key in settings:
            if key != "projects": print(f"{key}: {settings[key] if settings[key] != '' else 'Not set'}")
    
    elif args.option == "open":
        if settings["editor_command"] == "":
            print(colored("You must set your editor command in settings in order to open the settings file.", "yellow"))
            print(colored("To set: pm --config set --key editor_command --value \"your-editor-command-here\"", "yellow"))
            exit(1)
        
        print("Opening the settings file (pm-settings.json) in your editor...")
        os.chdir(PM_HOME)
        os.system(settings["editor_command"].replace(" .", " pm-settings.json"))

elif args.reset:
    print(colored("WARNING! YOU ARE GOING TO DELETE ALL OF YOUR SETTINGS!", "red", attrs=["bold"]))
    print(colored("Setup script will be executed after resetting.", "red"))
    
    input_controller = InputController()
    
    confirmation = input_controller.get_bool(colored("Are you sure about that? (y/n): ", "red"))
    if confirmation is False:
        print("Operation cancelled.")
        exit()
    
    print(colored("THIS IS THE LAST WARNING! THIS OPERATION IS NOT RECOVERABLE!", "red", attrs=["bold"]))
    confirmation = input_controller.get_bool(colored("Are you sure about that? (y/n): ", "red"))
    if confirmation is False:
        print("Operation cancelled.")
        exit()
    
    print("Deleting all of the settings...")

    try:
        os.remove(f"{PM_HOME}/pm-settings.json")
        print("Settings deleted successfully.")
    except PermissionError:
        print(colored("Access denied. Operation cannot complete.", "red"))
        exit(1)
    except OSError as e:
        print(colored(f"An I/O error occured while deleting settings.\n\n{e}", "red"))
        exit(1)

    print("Entering setup mode...")

    settings_manager = SettingsManager(PM_HOME)
    settings_manager.setup()
