from os.path import exists
from termcolor import colored


class InputController(object):
    """Controller class for controlling user inputs

    Methods
    -------
    get_bool(prompt : str) -> bool
        Checks if the answer is yes(y) or no(n).
    
    get_path(prompt : str) -> str
        Checks if the path that is specified in the answer is exists.
    
    get_str(prompt : str) -> str
        Checks if the answer is blank.
        Can be used if answer is required.
    
    get_option(prompt : str, choices:list) -> int
        Checks if answer is a selectable option.
    """

    def __init__(self):
        super().__init__()

    def get_path(self, prompt: str) -> str:
        """
        Checks if the path that is specified in the answer is exists.

        Parameters
        ----------
        prompt : str
            The prompt that will be asked to the user
        """

        while True:
            try: user_input = input(prompt)
            except KeyboardInterrupt:
                print(colored("Operation cancelled", "yellow"))
                exit(1)

            if not exists(user_input):
                print(colored("Your specified folder not exists. Please check your folder path and try again.", "yellow"))
            else:
                return user_input
    
    def get_bool(self, prompt: str) -> bool:
        """
        Checks if the answer is yes(y) or no(n).

        Parameters
        ----------
        prompt : str
            The prompt that will be asked to the user
        """

        acceptable_inputs = ["y", "n", "yes", "no"]

        while True:
            try: user_input = input(prompt)
            except KeyboardInterrupt:
                print(colored("Operation cancelled", "yellow"))
                exit(1)

            if user_input not in acceptable_inputs:
                print(colored("You can answer questions with yes(y) or no(n)", "yellow"))
            elif user_input in ["yes", "y"]:
                return True
            else:
                return False
    
    def get_str(self, prompt: str) -> str:
        """
        Checks if the answer is blank.
        Can be used if answer is required.

        Parameters
        ----------
        prompt : str
            The prompt that will be asked to the user
        """

        while True:
            try: user_input = input(prompt)
            except KeyboardInterrupt:
                print(colored("Operation cancelled", "yellow"))
                exit(1)
            
            if len(user_input) == 0:
                print(colored("This question cannot be left blank.", "yellow"))
            else:
                return user_input
    
    def get_option(self, prompt: str, choices: list) -> int:
        """
        Checks if answer is a selectable option.

        Parameters
        ----------
        prompt : str
            The prompt that will be asked to the user
        
        choices : list
            The choices that user must select between them
        """
        while True:
            try: user_input = input(prompt)
            except KeyboardInterrupt:
                print(colored("Operation cancelled", "yellow"))
                exit(1)
            
            if "q" in user_input:
                print("Operation cancelled.")
                exit()
            
            try: user_input = int(user_input)
            except:
                print(colored("Your answer must be an integer.", "yellow"))
                continue

            if user_input not in choices:
                print(colored("Your selection is not in options. Options are: ", "yellow"), end="")
                print(*choices, sep=", ", end=".\n")
                continue

            return user_input
