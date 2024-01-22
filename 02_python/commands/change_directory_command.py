from .base_command import BaseCommand
import os
import shutil
from typing import List

class ChangeDirectoryCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize the ChangeDirectoryCommand object.

        Args:
            options (List[str]): List of command options.
            args (List[str]): List of command arguments.
        """
        super().__init__(options, args)

        # Override the attributes inherited from BaseCommand
        self.description = 'Change the current working directory'
        self.usage = 'Usage: cd [options] [directory]'

        # TODO 7-1: Initialize any additional attributes you may need.
        # Refer to list_command.py, grep_command.py to implement this.
        # ...
        self.name = 'cd'
        self.options = options
        self.target_path = args[0] if args else self.current_path

    def execute(self) -> None:
        """
        Execute the cd command.
        Supported options:
            -v: Enable verbose mode (print detailed information)
        
        TODO 7-2: Implement the functionality to change the current working directory.
        You may need to handle exceptions and print relevant error messages.
        """
        if self.target_path == os.path.basename(self.current_path): # When cd arg is same dir "name"
            destination = self.current_path
        else:
            destination = os.path.normpath(os.path.join(self.current_path, self.target_path))

        print_moving_log = '-v' in self.options
        if print_moving_log:
            print(f'cd: changing directory to \'{os.path.basename(destination)}\'')

        # Operate cd
        if os.path.exists(destination) and not(destination == self.current_path):
            BaseCommand.update_current_path(self.target_path)
            os.chdir(self.current_path)
        elif (destination == self.current_path):
            pass
        else:
            print(f'''cd: cannot change directory to \'{os.path.basename(destination)}\': [Errno 2] No such\n
                  file or directory: \'{os.path.basename(destination)}\'''')

