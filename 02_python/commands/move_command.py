from .base_command import BaseCommand
import os
import shutil
from typing import List

class MoveCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize the MoveCommand object.

        Args:
            options (List[str]): List of command options.
            args (List[str]): List of command arguments.
        """
        super().__init__(options, args)

        # Override the attributes inherited from BaseCommand
        self.description = 'Move a file or directory to another location'
        self.usage = 'Usage: mv [source] [destination]'

        # TODO 5-1: Initialize any additional attributes you may need.
        # Refer to list_command.py, grep_command.py to implement this.
        # ...
        self.name = 'mv'
        self.options = options
        if len(args) <= 1:
            raise TypeError("Error: directory or file_name is None")
        else:
            self.src = args[0]
            self.target_path = args[1]

    def execute(self) -> None:
        """
        Execute the move command.
        Supported options:
            -i: Prompt the user before overwriting an existing file.
            -v: Enable verbose mode (print detailed information)
        
        TODO 5-2: Implement the functionality to move a file or directory to another location.
        You may need to handle exceptions and print relevant error messages.
        """
        overwrite_file = '-i' in self.options
        print_moving_log = '-v' in self.options
        breakpoint()

        if (os.path.basename(self.current_path).lower() == self.target_path.lower()) or (self.target_path == './') or (self.target_path == '.'):
            if print_moving_log:
                print(f'mv: moving \'{self.src}\' to \'{os.path.basename(destination)}\'')
                if overwrite_file:
                    print(f'mv: overwrite \'{os.path.join(os.path.basename(self.current_path), self.src)}\'? (y/n)')
                else: 
                    print(f'''mv: cannot move \'{self.src}\' to \'{os.path.basename(self.current_path)}\':
                          Destination path \'{os.path.join(os.path.basename(self.current_path), self.src)}\'\n already exists''')
            if overwrite_file:
                print(f'mv: overwrite \'{os.path.join(os.path.basename(self.current_path), self.src)}\'? (y/n)')
            return None
        else:
            destination = os.path.normpath(os.path.join(self.current_path, self.target_path))

        if self.file_exists(destination, self.src):
            if not(overwrite_file or print_moving_log):
                print(f'''mv: cannot move \'{self.src}\' to \'{os.path.basename(destination)}\':
                      Destination path \'{os.path.join(os.path.basename(destination), self.src)}\'\n already exists''')
                
            elif print_moving_log:
                print(f'mv: moving \'{self.src}\' to \'{os.path.basename(destination)}\'')
                if overwrite_file:
                    print(f'mv: overwrite \'{os.path.join(os.path.basename(destination), self.src)}\'? (y/n)')
                    overwrite_choice = input("")
                    if overwrite_choice in ['y', 'Y']:
                        shutil.move(os.path.join(self.current_path, self.src), destination)

                else:
                    print(f'''mv: cannot move \'{self.src}\' to \'{os.path.basename(destination)}\':
                          Destination path \'{os.path.join(os.path.basename(destination), self.src)}\'\n already exists''')
            else:
                print(f'mv: overwrite \'{os.path.join(os.path.basename(destination), self.src)}\'? (y/n)')
                overwrite_choice = input("")
                if overwrite_choice in ['y', 'Y']:
                    shutil.move(os.path.join(self.current_path, self.src), destination)
        else:
            shutil.move(os.path.join(self.current_path, self.src), destination)
            if print_moving_log:
                print(f'mv: moving \'{self.src}\' to \'{os.path.basename(destination)}\'')
    
    def file_exists(self, directory: str, file_name: str) -> bool:
        """
        Check if a file exists in a directory.
        Feel free to use this method in your execute() method.

        Args:
            directory (str): The directory to check.
            file_name (str): The name of the file.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        file_path = os.path.join(directory, file_name)
        return os.path.exists(file_path)
