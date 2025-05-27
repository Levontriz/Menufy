from screenManager import *

manager: ScreenManager = ScreenManager()
# Example usage of the ScreenManager and Screen classes
screen1: Screen = manager.add_screen("base:mainMenu")

screen1.set_title("Main Menu") # Set the title of the screen. This does return the screen object for chaining.
screen1.set_type(ScreenTypes.OPTIONS) # Set the type of the screen. This does return the screen object for chaining. This currently doesnt do anything, but it is here for future use.
screen1.add_option("Start Game", lambda: print("Starting game...")) # Add an option to the screen. This does return the screen object for chaining. Instead of lambda you can also use a function.
screen1.add_option("Settings", lambda: print("Opening settings...")) # Add another option to the screen.
screen1.add_option("Exit", lambda: print("Exiting...")) # Add another option to the screen.
screen1.set_prompt("Select an option: ") # Set the prompt for the screen. This does return the screen object for chaining.
screen1.set_prompt_cursor("> ") # Set the prompt cursor for the screen. This does return the screen object for chaining.
# Display the screen
screen1.display_screen()