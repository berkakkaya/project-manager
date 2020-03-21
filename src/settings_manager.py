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

        user_folder_path = self.input_controller.get_input(
            "Your projects's home folder (full path): ", self.input_controller.CONTROL_PATH)
        user_allowed_categorization = self.input_controller.get_input(
            "Do you want to enable categorization [yes(y) / no(n)]: ", self.input_controller.CONTROL_BOOL)
        
        with open(f"{self.project_manager_home}/pm-settings.json", "w+") as f:
            settings = dict(folder_path=user_folder_path, categorization_enabled=user_allowed_categorization)
            dump(settings, f, indent=4)

        print("Settings saved.")
