from json import dump


class SettingsManager(object):
    
    def __init__(self, project_manager_home, input_controller):
        super().__init__()
        self.project_manager_home = project_manager_home
        self.input_controller = input_controller
    
    def setup(self):
        print(f"""
        The settings will be written to the pm-settings.json.
        You can find this file in this path: {self.project_manager_home}\n
        """)

        projects_folder = self.input_controller.get_input(
            "Your projects's home folder (full path): ", self.input_controller.CONTROL_PATH)
        editor_command = input("Your editor's 'open' command (type . for the filepath): ")
        
        with open(f"{self.project_manager_home}/pm-settings.json", "w+") as f:
            settings = dict(projects_path=projects_folder, editor_command=editor_command)
            dump(settings, f, indent=4)

        print("Settings saved.")
