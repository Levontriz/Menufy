from screenManager import *

manager: ScreenManager = ScreenManager()
# Example usage of the ScreenManager and Screen classes
screen1: Screen = manager.add_screen("base:mainMenu", ScreenTypes.MULTI_OPTIONS_NUM) # Create a new screen with identifier and type

screen1.set_title("Main Menu") # Set the title of the screen. This does return the screen object for chaining.
# screen1.set_type(ScreenTypes.MULTI_OPTIONS_NUM) # Set the type of the screen. This does return the screen object for chaining. This currently doesn't do anything, but it is here for future use.
screen1.add_option("Start Game", lambda: print("Starting game...")) # Add an option to the screen. This does return the screen object for chaining. Instead of lambda you can also use a function.
screen1.add_option("Settings", lambda: print("Opening settings...")) # Add another option to the screen.
screen1.add_option("Exit", lambda: print("Exiting...")) # Add another option to the screen.
screen1.set_prompt("Select an option: ") # Set the prompt for the screen. This does return the screen object for chaining.
screen1.set_prompt_cursor("> ") # Set the prompt cursor for the screen. This does return the screen object for chaining.
# Display the screen
screen1.display_screen()

# Note: If you have the entire definition of the screen from display screen all the way to manager.add_screen inside a while loop it will inexplicably exit the loop after just one input.
# To fix this you can define the screen outside the while loop and run screen.display_screen inside the loop
# I still have no idea why it does this but it has an easy fix that I believe won't cause problems in any use case, if it is a problem contact me
# Might have something to do with garbage collection but I am not sure