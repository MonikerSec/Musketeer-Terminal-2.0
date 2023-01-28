from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import BooleanProperty

# Importing Firebase (Database)
from firebase import firebase

# Set multitouch simulation off
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# Set window size
Window.size = (550, 675)

# Set different screens
class LoginScreen(Screen):
    pass

class SigninScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class HelpScreen(Screen):
    pass

class EmailScreen(Screen):
    pass

class ReportBugScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

# Define main app
class MusketeerTerminalApp(MDApp):
    logged_in = BooleanProperty(False)
    new_user = BooleanProperty(True)

    def build(self):
        self.icon = 'Musketeer_Terminal_Logo.png'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.accent_palette = 'LightGreen'
        return Builder.load_file('main.kv')


    def login(self, email, password):
        from firebase import firebase

        firebase = firebase.FirebaseApplication('https://musketeerterminal2-default-rtdb.firebaseio.com/', None)

        data = {
            'email': email,
            'password': password
        }
        # firebase.post('https://musketeerterminal2-default-rtdb.firebaseio.com/Users', data)
        result = firebase.get('https://musketeerterminal2-default-rtdb.firebaseio.com/Users', '')  # type: ignore

        for i in result.keys():
            if result[i]['email'] == email:
                if result[i]['password'] == password:
                    self.logged_in = True
                else:
                    self.logged_in = False
    

    def CheckForExistingUser(self, email, password):
        from firebase import firebase

        firebase = firebase.FirebaseApplication('https://musketeerterminal2-default-rtdb.firebaseio.com/', None)

        data = {
            'email': email,
            'password': password
        }
        
        result = firebase.get('https://musketeerterminal2-default-rtdb.firebaseio.com/Users', '')  # type: ignore
        for i in result.keys():
            if result[i]['email'] == email:
                if result[i]['password'] == password:
                    self.new_user = False

    def signup(self, email, password):
        from firebase import firebase

        firebase = firebase.FirebaseApplication('https://musketeerterminal2-default-rtdb.firebaseio.com/', None)

        data = {
            'email': email,
            'password': password
            }
        
        firebase.post('https://musketeerterminal2-default-rtdb.firebaseio.com/Users', data) # type: ignore

if __name__ == "__main__":
    MusketeerTerminalApp().run()