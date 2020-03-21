import os
# TODO: OPTIMIZE IMPORTS


class InputController(object):
    def __init__(self):
        super().__init__()

        self.CONTROL_PATH = 0
        self.CONTROL_BOOL = 1
    
    def get_input(self, message, control_method):
        while True:
            if control_method == self.CONTROL_BOOL: # Bool controlling
                acceptable_inputs = ["y", "n", "yes", "no"]

                user_input = input(message).lower()
                if user_input not in acceptable_inputs:
                    print("You can answer questions with yes(y) or no(n)")
                elif user_input in ["yes", "y"]:
                    return True
                else:
                    return False
            
            elif control_method == self.CONTROL_PATH: # Path controlling
                user_input = input(message)
                if not os.path.exists(user_input):
                    print("Your specified folder not exists. Please check your folder path and try again.")
                else:
                    return user_input
