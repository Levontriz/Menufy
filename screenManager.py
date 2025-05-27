from enum import Enum
from typing import List, Optional, Callable
import time
import os

def waitcls(sleepTime, speedMode):
    version = os.name

    clearCommand = ''

    match version:
        case 'nt':
            clearCommand = 'cls'
        case 'Posix':
            clearCommand = 'clear'


    if speedMode:
        time.sleep(0)
    else:
        time.sleep(sleepTime)
    os.system(clearCommand)

def simpleNumberRequest(title, promptMessage, promptCursor, options, lowerLimit, upperLimit, speedMode):
    while True:
        if title:
            print(title)
        for i in range(len(options)):
            option = options[i].label
            print(i+1, '.', ' ', option, sep='')
        print(promptMessage)
        request = input(promptCursor)
        try:
            requestInt = int(request)
        except ValueError:
            waitcls(0, False)
            print('Non integer value entered!')
            waitcls(2, speedMode)
            continue
        if requestInt < lowerLimit or requestInt > upperLimit:
            waitcls(0, False)
            print('Invalid option!')
            waitcls(2, speedMode)
            continue
        if type(requestInt) == int:
            return requestInt-1

class ScreenTypes(Enum):
        OPTIONS = "options"
        INPUT = "input"
        CONFIRMATION = "confirmation"
        CUSTOM = "custom"

class Option:
    def __init__(self, label: str = "Fill the label boyo", callback: Optional[Callable] = None):
        self.label: str = label
        self.callback: Optional[Callable] = callback
    
    def execute(self):
        if self.callback:
            self.callback()

class Screen:
    def __init__(self, identifier: str, title: str=None, screen_type: ScreenTypes=ScreenTypes.OPTIONS, options: list[Option]=None, prompt: str=None, prompt_cursor: str="> ", speedMode: bool = False):
        if ":" not in identifier:
            raise ValueError("Identifier must be in the format 'namespace:identifier'.")
        namespace, identifier = identifier.split(":", 1)
        if not namespace or not identifier:
            raise ValueError("Both namespace and identifier must be non-empty.")
        self._identifier = identifier
        self.title = title
        self.type = screen_type
        self.options = options if options is not None else []  # Create new list for each instance
        self.prompt = prompt
        self.promptCursor = prompt_cursor
        self.speedMode = speedMode

    @property
    def identifier(self):
        return self._identifier
    
    def __repr__(self):
        return f"Screen(identifier='{self.identifier}', title='{self.title}')"
    
    def __str__(self):
        return f"Screen: {self.title or self.identifier}"
    
    def set_title(self, title) -> 'Screen':
        self.title = title
        return self
    def set_type(self, screen_type) -> 'Screen':
        self.type = screen_type
        return self
    def add_option(self, label: str, callback) -> 'Screen':
        self.options.append(Option(label, callback))
        return self
    def list_options(self):
        return [option.label for option in self.options]
    def get_option(self, index: int) -> Option:
        if 0 <= index < len(self.options):
            return self.options[index]
        else:
            raise IndexError("Option index out of range.")
    def delete_option(self, index: int) -> 'Screen':
        if 0 <= index < len(self.options):
            del self.options[index]
            return self
        else:
            raise IndexError("Option index out of range.")
    def set_prompt(self, prompt) -> 'Screen':
        self.prompt = prompt
        return self
    def set_prompt_cursor(self, prompt_cursor) -> 'Screen':
        self.promptCursor = prompt_cursor
        return self

    def display_screen(self):
        try:
            choice = simpleNumberRequest(self.title, self.prompt, self.promptCursor, self.options, 1, len(self.options), self.speedMode)
            if 0 <= choice < len(self.options):
                option = self.options[choice]
                option.execute()  # If using callback system
        except (IndexError, ValueError) as e:
            print(f"Invalid choice: {e}")
    

class ScreenManager:
    def __init__(self, speedMode: bool = False):
        self.speedMode = speedMode
        self.screens = {}

    def add_screen(self, identifier: str) -> 'Screen':
        if identifier in self.screens:
            raise ValueError(f"Screen '{identifier}' already exists")
        self.screens[identifier] = Screen(identifier=identifier, speedMode=self.speedMode)
        return self.screens[identifier]

    def get_screen_by_identifier(self, identifier):
        return self.screens.get(identifier)

    def remove_screen(self, identifier):
        if identifier in self.screens:
            del self.screens[identifier]

    def clear_screens(self):
        self.screens.clear()

    def has_screen(self, identifier):
        return identifier in self.screens
    def list_screens(self):
        return list(self.screens.keys())

__all__ = ['ScreenManager', 'Screen', 'Option', 'ScreenTypes']