import os
from json import dump, load
from github import Github
from termcolor import colored
from sys import exit
import webbrowser
from src.input_controller import InputController

class ProjectManager(object):
    """
    This class manages and creates projects

    Methods
    -------
    create_project(name : str, group : str, is_new_repo_requested : bool, is_new_repo_private : bool)
        Creates new project
    
    open_project(project : str)
        Open an existing project with editor
    
    open_repo_in_browser(name : str, group : str = None)
        Opens the repository page in browser
    
    find_project(self, name:str, group:str = None) -> dict
        Finds a project
    """


    def __init__(self, project_manager_home: str):
        """
        Parameters
        ----------
        project_manager_home : str
            Home folder of Project Manager
        """

        self.project_manager_home = project_manager_home

        with open(f"{project_manager_home}/pm-settings.json", "r") as file:
            self.settings = load(file)
            # TODO: Take settings directly from params
        
        if self.settings["token"] != "":
            self.is_access_token_specified = True
            try:
                self.user = Github(self.settings["token"]).get_user()
            except:
                print(colored("User cannot get. Please check your token and your internet connection."))
                exit(1)
        else:
            self.is_access_token_specified = False

    
    def create_project(self, name:str, group:str, is_new_repo_requested:bool, is_new_repo_private:bool):
        """
        Creates new project

        Parameters
        ----------
        name : str
            Name of the project
        
        group : str
            Group of the project
        
        is_new_repo_requested : bool
            A check that looks for is user want a new repo
        
        is_new_repo_private : bool
            A check that looks for is new repo private
        """

        # TODO: Make repo checks inside this function

        os.chdir(self.settings["projects_folder"])
        if not os.path.exists(group):
            print(f"Creating group directory: {group}")
            os.mkdir(group)
        os.chdir(group)

        print(f"Creating project folder: {name}")
        os.mkdir(name)
        os.chdir(name)

        print("Initializing git in the project directory")
        os.system("git init")

        if group not in self.settings["projects"]:
            print(f"Group named {group} not found in settings file. Creating...")
            self.settings["projects"][group] = dict()
        
        self.settings["projects"][group][name] = dict(dir=os.getcwd())
        
        if self.is_access_token_specified and is_new_repo_requested:
            repo_name = input(f"New repository name (if blank, {name.lower()} will be used): ")
            if repo_name == "": repo_name = name

            try:
                print(f"Creating a new repo on GitHub named {name}")
                new_repo = self.user.create_repo(repo_name, private=is_new_repo_private)
                os.system(f"git remote add origin {new_repo.clone_url}")
                self.settings["projects"][group][name]["repo_url"] = new_repo.html_url
            except:
                print(colored("WARNING: An error occured while creating a new repo on Github.", "yellow"))
                print(colored("Please check your token and your internet connection.", "yellow"))
        
        self.settings["projects"][group][name]["dir"] = os.getcwd()
        with open(f"{self.project_manager_home}/pm-settings.json", "w") as file:
            dump(self.settings, file, indent=4)
        print("Added new project to the settings file.")

        if self.settings["editor_command"] != "":
            print(f"Opening your project folder with command: {self.settings['editor_command']}")
            os.system(self.settings["editor_command"])
        
        print("Operation completed.")
    
    def open_project(self, name:str, group:str):
        """
        Open an existing project with editor

        Parameters
        ----------
        name : str
            Project name
        
        group : str
            Project group
        """

        if self.settings["editor_command"] == "":
            print(colored("You didn't specified editor_command option.", "yellow"))
            print(colored("To set: pm --config --key 'editor_command' --value 'command'", "yellow"))
            exit(1)
        
        project = self.find_project(name, group)
        os.chdir(project["dir"])
        os.system(self.settings["editor_command"])
    
    def open_repo_in_browser(self, name:str, group:str = None):
        """
        Opens the repository page in browser

        Parameters
        ----------
        name : str
            Project name
        
        group : str
            Project group
        """

        project = self.find_project(name, group)
        
        if "repo_url" not in project:
            print(colored("The project doesn't have a repository URL.", "yellow"))
            exit(1)
        
        webbrowser.open(project["repo_url"], new=2)
    
    def find_project(self, name:str, group:str = None) -> dict:
        """
        Finds a project

        Parameters
        ----------
        name : str
            Project name
        
        group : str
            Project group
        """

        found_projects = dict() # All found projects goes here with a key which is increment number
        choices = [] # In case we found many results, it will be used in input_controller.get_option
        project_key = 0 # The increment number key of projects in found_projects
        
        if group != None: # If group is given at param
            if group not in self.settings["projects"]:
                print(colored(f"Project Manager couldn't find your specified group: {group}", "yellow"))
                exit(1)
            
            if name not in self.settings["projects"][group]:
                print(colored(f"Project Manager couldn't find your specified project in group: {group}", "yellow"))
                exit(1)
            
            project = self.settings["projects"][group][name]
            project["name"] = name
            project["group"] = group
            return project
        
        # If group isn't given at param, search in projects
        for s_group in self.settings["projects"]: # s_group: selected group
            if name in self.settings["projects"][s_group]:
                project_key += 1
                found_projects[project_key] = self.settings["projects"][s_group][name]
                found_projects[project_key]["name"] = name
                found_projects[project_key]["group"] = s_group
                choices.append(project_key)
        
        if project_key == 0:
            print(colored("Project Manager couldn't find your project.", "yellow"))
            exit(1)
        elif project_key == 1:
            return found_projects[1]
        else:
            input_controller = InputController()

            print("Multiple projects found:")
            for i in found_projects:
                print(f"[{i}] {name} (in group {found_projects[i]['group']})")
            
            selected_option = input_controller.get_option("Select a project by it's number (type 'q' to quit): ", choices)

            return found_projects[selected_option]        
