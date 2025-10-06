from enum import Enum
from typing import Optional, Callable

def _waitcls(sleep_time, speed_mode):
    import os
    import time
    version = os.name

    clear_command = ''

    match version:
        case 'nt':
            clear_command = 'cls'
        case 'Posix':
            clear_command = 'clear'

    if speed_mode:
        time.sleep(0)
    else:
        time.sleep(sleep_time)
    os.system(clear_command)


def _simple_number_request(title, prompt_message, prompt_cursor, options, lower_limit, upper_limit, speed_mode):
    while True:
        if title:
            print(title)
        for i in range(len(options)):
            option = options[i].label
            print(str(i + 1) + '.' + ' ' + option)
        print(prompt_message)
        request = input(prompt_cursor)
        try:
            request_int = int(request)
        except ValueError:
            _waitcls(0, False)
            print('Non integer value entered!')
            _waitcls(2, speed_mode)
            continue
        if request_int < lower_limit or request_int > upper_limit:
            _waitcls(0, False)
            print('Invalid option!')
            _waitcls(2, speed_mode)
            continue
        if type(request_int) == int:
            return request_int - 1

def _simple_text_request(title, prompt_message, prompt_cursor, options, speed_mode):
    while True:
        if title:
            print(title)
        for i in range(len(options)):
            option = options[i].label
            print(" - " + option)
        print(prompt_message)
        request = input(prompt_cursor)
        for i in range(len(options)):
            option = options[i].label.lower()
            if request.lower() == option:
                return i
        #_waitcls(0, False)
        print("Invalid option. Please try again.")
        #_waitcls(2, speed_mode)


class ScreenTypes(Enum):
    MULTI_OPTIONS_NUM = "options_num"
    MULTI_OPTIONS_TEXT = "options_text"
    CONFIRMATION = "confirmation"
    CUSTOM = "custom"


class Option:
    def __init__(self, label: str, callback: Optional[Callable] = None):
        self.label: str = label
        if label is None or label.strip() == "":
            raise ValueError("Option label cannot be empty.")
        self.callback: Optional[Callable] = callback

    def execute(self):
        if self.callback:
            self.callback()


class Screen:
    def __init__(self, identifier: str, title: str = None, screen_type: ScreenTypes = ScreenTypes.MULTI_OPTIONS_NUM,
                 options: list[Option] = None, prompt: str = None, prompt_cursor: str = "> ", speed_mode: bool = False):
        import re
        pattern = re.compile(r"^[a-zA-Z0-9]+:[a-zA-Z0-9]+$")
        valid_identifier = True if pattern.match(identifier) is not None else False
        if not valid_identifier:
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
        self.speedMode = speed_mode

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

        if not self.options:
            raise ValueError("No options available for selection.")
        elif self.type == ScreenTypes.MULTI_OPTIONS_NUM:
            try:
                choice = _simple_number_request(self.title, self.prompt, self.promptCursor, self.options, 1, len(self.options),
                                                self.speedMode)
                if 0 <= choice < len(self.options):
                    option = self.options[choice]
                    option.execute()  # If using callback system
            except (IndexError, ValueError) as e:
                print(f"Invalid choice: {e}")
        elif self.type == ScreenTypes.MULTI_OPTIONS_TEXT:
            try:
                choice = _simple_text_request(self.title, self.prompt, self.promptCursor, self.options, self.speedMode)
                if 0 <= choice < len(self.options):
                    option = self.options[choice]
                    option.execute()  # If using callback system
            except (IndexError, ValueError) as e:
                print(f"Invalid choice: {e}")
        else:
            raise NotImplementedError(f"Screen type '{self.type}' is not implemented yet.")


class ScreenManager:
    def __init__(self, speed_mode: bool = False):
        self.speedMode = speed_mode
        self.screens = {}

    def add_screen(self, identifier: str) -> 'Screen':
        if identifier in self.screens:
            raise ValueError(f"Screen '{identifier}' already exists")
        self.screens[identifier] = Screen(identifier=identifier, speed_mode=self.speedMode)
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