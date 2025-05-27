from simpleNumberRequest import simpleNumberRequest
from enum import Enum
from typing import List, Optional, Callable
import os


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
        if self.title:
            print(self.title)
        
        try:
            choice = simpleNumberRequest(self.prompt, self.promptCursor, self.options, 1, len(self.options), self.speedMode)
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
        self.screens[identifier] = Screen(identifier, self.speedMode)
        return self.screens[identifier]

    def get_screen_by_identifier(self, name):
        return self.screens.get(name)

    def remove_screen(self, name):
        if name in self.screens:
            del self.screens[name]

    def clear_screens(self):
        self.screens.clear()

    def has_screen(self, name):
        return name in self.screens
    def list_screens(self):
        return list(self.screens.keys())
    
    
manager = ScreenManager()

def test1_action():
    print('Test1')

def test2_action():
    print('Test2')

def test3_action():
    print('Test3')

def create_new_screen():
    os.system('cls')
    new_screen = manager.add_screen('test:newScreen')
    new_screen.set_title('New Screen').set_type(ScreenTypes.OPTIONS)
    new_screen.add_option('Test Option', lambda: print("This is a test option"))
    new_screen.set_prompt('What do you want to do?').set_prompt_cursor('> ')
    new_screen.display_screen()

def open_screen():
    screen = manager.get_screen_by_identifier("test:newScreen")
    if screen:
        screen.display_screen()
    else:
        print("Screen not found.")

def do_nothing():
    pass

# Create and set up the main screen
screenTest: Screen = manager.add_screen("main:testScreen")

screenTest.set_title("Testing Screen 2")
screenTest.set_type(ScreenTypes.OPTIONS)

screenTest.add_option("Test1", test1_action)
screenTest.add_option("Test2", test2_action)
screenTest.add_option("Test3", test3_action)
screenTest.add_option("Create new screen", create_new_screen)
screenTest.add_option("Open test:newScreen", open_screen)
screenTest.add_option("Nothing", do_nothing)

print(screenTest.list_options())
print(screenTest.identifier)

screenTest.set_prompt("What do you want to have?")
screenTest.set_prompt_cursor("> ")

while True:
    manager.get_screen_by_identifier("main:testScreen").display_screen()