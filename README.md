# Python-Screen-Manager
Manages terminal screens for easy integration into text based games such as my own PythonRPG (Unimplimented but will be added soon)
## How it works

I first created a wait function that admitedly is rarely used but is frequently used for story telling in my rpg game. The wait function takes in wait time in seconds and a bool if it should just skip over the wait entirely and only do its clear. This is used via a global variable to make testing a bit easier. 

I then created the simpleNumberRequest function, this is the basis of every screen. It takes in a message for the user after creating all the options, a cursor so that people can have a nice area to type in (my default chosen is "> "), all the options (which is a list of classes (option)), the lower limit (which its default is 1), the upper limit (which is usually the size of the array being fed in), and speedMode (which is fed into any instace of waitcls as described previously). It will print out every single option with a number next to it, if the user enters a valid number it returns which option was selected.

The final creation is the ScreenManager itself, it has many functions intended to be used to create and manage and screens along with displaying them. There are far to many functions to list here so i'll link some documentation later. For now you should be able to get a general understanding using the following example:
```

manager = ScreenManager() #Defines the screen manager

# Callback
def test1_action():
    print('Test1')

# Callback
def test2_action():
    print('Test2')

# Callback
def test3_action():
    print('Test3')

# Callback; This callback is used to show that you can create screens and show them whilst still being in a screen
def create_new_screen():
    os.system('cls')
    new_screen = manager.add_screen('test:newScreen')
    new_screen.set_title('New Screen').set_type(ScreenTypes.OPTIONS)
    new_screen.add_option('Test Option', lambda: print("This is a test option"))
    new_screen.set_prompt('What do you want to do?').set_prompt_cursor('> ')
    new_screen.display_screen()

# Callback; This callback is used to show that a created screen while inside another screen is still saved and openable
def open_screen():
    screen = manager.get_screen_by_identifier("test:newScreen")
    if screen:
        screen.display_screen()
    else:
        print("Screen not found.")

# Callback
def do_nothing():
    pass

# Create and set up the main screen

# When creating a new screen we give it an identifier structured like this "namespace:whatever"
# Although it isnt checked for when using my mod system from PythonRPG it is prefered that you use the same namespace for your own mods as it restricts overlapping screens
screenTest: Screen = manager.add_screen("main:testScreen")

# set title takes in a string that is printed just before options appear from simpleNumberRequest
screenTest.set_title("Testing Screen 2")

# Currently this does nothing and technically could be removed from the code but it will be expanded upon in later development
screenTest.set_type(ScreenTypes.OPTIONS)

# add option creates an option and takes in a string for the label and a function for callback
screenTest.add_option("Test1", test1_action)
screenTest.add_option("Test2", test2_action)
screenTest.add_option("Test3", test3_action)
screenTest.add_option("Create new screen", create_new_screen)
screenTest.add_option("Open test:newScreen", open_screen)
screenTest.add_option("Nothing", do_nothing)

# returns with every single option label in the correct order for removing
print(screenTest.list_options())

# Just grabs the identifier variable for the screen
print(screenTest.identifier)

# Sets what should be put just before the player input
screenTest.set_prompt("What do you want to have?")
# Sets what comes before the users cursor for input clarification
screenTest.set_prompt_cursor("> ")

# Loops over the main display screen so you can test everything
while True:
    manager.get_screen_by_identifier("main:testScreen").display_screen()

```
