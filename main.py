# Importing Kivy widgets and App class
from kivy.uix.widget import Widget as Wg
from kivy.app import App 

# Importing Kivy config and setting multitouch disabled
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# Defining the main widget
class MainWidget(Wg):
    pass

# Defining the app class
class MuskTermApp(App):
    pass

# Running the app instance
if __name__ == '__main__':
    MuskTermApp().run()