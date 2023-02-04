import smtplib, socket
from email.message import EmailMessage
from email.utils import formataddr
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.pickers import MDDatePicker
from datetime import date

# Set multitouch simulation off
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# Set window size
Window.size = (350, 600)

# Set different screens
class SplashScreen(Screen):
    pass
class LoginScreen(Screen):
    pass
class SignupScreen(Screen):
    pass
class HomeScreen(Screen):
    pass
class HelpScreen(Screen):
    pass
class EmailScreen(Screen):
    pass
class ReportBugScreen(Screen):
    pass
class AboutScreen(Screen):
    pass
class CalendarScreen(Screen):
    pass
class WindowManager(ScreenManager):
    pass

# Define main app
class MusketeerTerminalApp(MDApp):
    logged_in = BooleanProperty(False)
    new_user = BooleanProperty(True)

    bug_sent = BooleanProperty(False)
    bug_all_filled_out = BooleanProperty(True)

    email_sent = BooleanProperty(False)
    email_all_filled_out = BooleanProperty(True)

    email = open('email.txt').read()
    password = open('password.txt').read()

    def build(self):
        self.icon = 'images/musk-term-logo.png'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.accent_palette = 'LightGreen'
        return Builder.load_file('kv/main.kv')

    def on_start(self):
        Clock.schedule_once(self.change_screen, 2.8)

    def change_screen(self, dt):
        self.root.transition = FadeTransition(duration=1)
        self.root.current = 'login'
    
    # DatePicker Click OK
    def on_save(self, instance, value, date_range):
        pass
        # app = MDApp.get_running_app()
        # cal = app.root.get_screen('calendar').ids.date_label
        # cal.text= 'You saved'

    def on_cancel(self, instance, value):
        pass

    def show_date_picker(self):
        date_dialog = MDDatePicker(mode='range')
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def login(self, email, password):
        from firebase import firebase

        firebase = firebase.FirebaseApplication('https://musketeerterminal2-default-rtdb.firebaseio.com/', None)

        data = {
            'email': email,
            'password': password
        }
        # firebase.post('https://musketeerterminal2-default-rtdb.firebaseio.com/Users', data)
        result = firebase.get('https://musketeerterminal2-default-rtdb.firebaseio.com/Users', '')

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
        
        result = firebase.get('https://musketeerterminal2-default-rtdb.firebaseio.com/Users', '')  
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

        firebase.post('https://musketeerterminal2-default-rtdb.firebaseio.com/Users', data)

    def send_bug(self, name, sender_email, message):
        msg = EmailMessage()
        msg['Subject'] = 'New Bug Report'
        msg['To'] = 'justin.triplett@stu.greenup.kyschools.us'
        msg['From'] = formataddr((name.text, sender_email.text))
        msg.set_content(
            f'''Hello. My name is {name.text}.
            
            {message.text}''')

        try:
            with smtplib.SMTP('smtp-relay.sendinblue.com', 587, timeout=8) as smtp: 
                smtp.login(self.email, self.password)
                smtp.send_message(msg)
            self.bug_sent = True
        except (TimeoutError, IndexError, smtplib.SMTPSenderRefused):
            self.bug_sent = False
        
        name.text, sender_email.text, message.text = '', '', ''

    def send_email_teacher(self, name, sender_email, reciever_email, message):
        msg = EmailMessage()
        msg['Subject'] = f'Musketeer Terminal App message from {name.text}'
        msg['To'] = str(reciever_email.text)
        msg['From'] = formataddr((name.text, sender_email.text))
        msg.set_content(
            f'''Hello. My name is {name.text}.
            
            {message.text}''')

        try:
            with smtplib.SMTP('smtp-relay.sendinblue.com', 587, timeout=8) as smtp: 
                smtp.login(self.email, self.password)
                smtp.send_message(msg)
            self.email_sent = True
        except (TimeoutError, IndexError, smtplib.SMTPSenderRefused):
            self.email_sent = False
        

        name.text, sender_email.text, reciever_email.text, message.text,   = '', '', '', ''

if __name__ == "__main__":
    MusketeerTerminalApp().run()