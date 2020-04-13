from json import dump, load  # For saving settings to a json file
from termcolor import colored  # For colored output
import os
from sys import exit
from src.input_controller import InputController
from src.project_manager import ProjectManager


class SettingsManager(object):
    """
    Manager class for settings file

    Attributes
    ----------
    project_manager_home : str
        The home directory of Project Manager
    input_controller : InputController
        The InputController instance for controlling inputs

    Methods
    -------
    setup()
        Runs the setup script that initializes the pm-settings.json file
    
    set_value(key : str, value : str)
        Sets given key to given value in settings
    
    configure_project(self, name : str, group : str = None, key : str = None, value : str = None)
        Configures given project by prompting the user or changing given key to given value
    """

    def __init__(self, project_manager_home: str):
        """
        Parameters
        ----------
        project_manager_home : str
            The home directory of Project Manager
        input_controller : InputController
            The InputController instance for controlling inputs
        """

        super().__init__()
        self.project_manager_home = project_manager_home

        if os.path.exists(f"{project_manager_home}/pm-settings.json"):
            with open(f"{project_manager_home}/pm-settings.json", "r") as file:
                self.settings = load(file)

    def setup(self):
        """
        Runs the setup script that initializes the pm-settings.json file
        """

        input_controller = InputController()

        print(colored(f"""
        The settings will be written to the pm-settings.json.
        You can find this file in this path: {self.project_manager_home}\n
        """, "yellow"))  # Warns the user that where user can find the settings file

        projects_folder = input_controller.get_path(
            "\nThe folder that contains all of your projects (full path): ")
        editor_command = input(
            "\nThe editor command you want to use (type . for the path parameter if required): ")
        print("\nIf you want to automatically create new repo in Github, you must set your access token.")
        print("You can generate a new token at https://github.com/settings/tokens/new with repo scope")
        token = input("\nToken: ")

        settings = dict(projects_folder=projects_folder,
                        editor_command=editor_command, token=token, projects=dict())

        print("""\nIf your directory's hierarchy is like that:
        * Group
        |-> Project
        |-> Another project
        """)
        print("Project Manager can scan your directory and index all of your projects.")
        user_wants_scan = input_controller.get_bool(
            "Do you want Project Manager to scan your directory? (y/n): ")

        print(f"\nThese settings will be written: {settings}")
        if user_wants_scan:
            print("Scan will be started after confirmation.")
        is_write_confirmed = input_controller.get_bool("\nIs it OK? (y/n): ")

        if is_write_confirmed:
            if user_wants_scan:
                print(
                    colored("Scan has been started, please wait a minute...", "yellow"))

                for directory in os.listdir(projects_folder):
                    if os.path.isfile(f"{projects_folder}/{directory}") or directory[0] == ".":
                        continue
                    settings["projects"][directory] = dict()
                    print(f"\n* {directory}")
                    for project in os.listdir(f"{projects_folder}/{directory}"):
                        if os.path.isfile(f"{projects_folder}/{directory}/{project}") or project[0] == ".":
                            continue
                        settings["projects"][directory][project] = dict(
                            dir=f"{projects_folder}/{directory}/{project}")
                        print(f"|-> {project}")

            with open(f"{self.project_manager_home}/pm-settings.json", "w") as file:
                dump(settings, file, indent=4)
            print(colored("Settings saved successfully.", "green"))

        else:
            print("Settings are not saved.")
            exit()

    def set_value(self, key: str, value: str):
        """
        Sets given key to given value in settings

        Parameters
        ----------
        key : str
            Key that it's value will be changed in project's settings (optional)
        
        value : str
            The value that will be assigned to key in settings
        """
        self.settings[key] = value
        with open(f"{self.project_manager_home}/pm-settings.json", "w") as file:
            dump(self.settings, file, indent=4)
    
    def configure_project(self, name:str, group:str = None, key:str = None, value:str = None):
        """
        Configures given project by prompting the user or changing given key to given value

        Parameters
        ----------
        name : str
            Project's name
        
        group : str
            Project's group
        
        key : str
            Key that it's value will be changed in project's settings (optional)
        
        value : str
            The value that will be assigned to key in project's settings (optional)
        """
        project_manager = ProjectManager(self.project_manager_home)
        project = project_manager.find_project(name, group)

        project_keys = ["repo_url"] # A key set that can be changed in project's settings

        if key != None: # If key and value is set
            if key not in project_keys:
                print(colored(f"Invalid key: {key}", "yellow"))
                exit(1)
            
            self.settings["projects"][project["name"]][project["group"]][key] = value
            with open(f"{self.project_manager_home}/pm-settings.json", "w") as file:
                dump(self.settings, file, indent=4)
            
            print(f"{project['name']}'s key {key} is now set to {value}")
            exit()
        
        input_controller = InputController()

        options = {
            1: "Set the project repository URL",
            2: "Change project's name",
            3: "Change project's group",
            4: "Set project's path"
        }

        print(f"""Project Manager Project Configurator
        Project name: {project["name"]}
        Group: {project["group"]}
        Project repository: {project["repo_url"] if "repo_url" in project else "Not configured"}
        Path: {project["dir"]}
        """)

        print("\nYour options:")
        for option in options:
            print(f"[{option}] {options[option]}")
        
        selected = input_controller.get_option("Please select an option, type q to quit: ", list(options.keys()))
        
        if selected == 1: # Change repostory URL
            new_url = input_controller.get_str("New repository URL: ")
            self.settings["projects"][project["group"]][project["name"]]["repo_url"] = new_url
            with open(f"{self.project_manager_home}/pm-settings.json", "w") as file:
                dump(self.settings, file, indent=4)
                print("Done!")
        
        elif selected == 2: # Change project's name
            new_name = input_controller.get_str("New name (don't use spaces): ")
            new_name = new_name.replace(" ", "")
            rename_folder = input_controller.get_bool("Do you want to rename your project folder as well? (y/n): ")

            project_group = project["group"]
            del self.settings["projects"][project["group"]][name]
            del project["name"]
            del project["group"]
            
            if rename_folder: # If user wants to rename the project folder
                os.chdir(project["dir"]) # Firstly we go into project directory
                os.chdir("..") # Then we go into parent directory for operation
                os.rename(name, new_name) # We rename our directory
                os.chdir(new_name) # We go into renamed directory for taking the new path
                project["dir"] = os.getcwd() # Lastly we asssign our dir key with the current directory's path
            
            self.settings["projects"][project_group][new_name] = project # Assign new path to old dir key

            with open(f"{self.project_manager_home}/pm-settings.json", "w") as file:
                dump(self.settings, file, indent=4)
                print("Done!")
        
        elif selected == 3: # Change project's group
            new_group = input_controller.get_str("New group (don't use spaces): ")
            new_group = new_group.replace(" ", "")

            old_group = project["group"]

            del self.settings["projects"][old_group][name]
            del project["name"]
            del project["group"]
            
            if new_group not in self.settings["projects"]:
                self.settings["projects"][new_group] = dict()
            
            self.settings["projects"][new_group][name] = project

            with open(f"{self.project_manager_home}/pm-settings.json", "w") as file:
                dump(self.settings, file, indent=4)
                print("Done!")
        
        elif selected == 4: # Set project's path
            new_path = input_controller.get_path("New path: ")
            self.settings["projects"][project["group"]][name]["dir"] = new_path

            with open(f"{self.project_manager_home}/pm-settings.json", "w") as file:
                dump(self.settings, file, indent=4)
                print("Done!")
