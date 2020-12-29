import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random

Builder.load_file('design.kv')      # prompts the script to use the "design.kv" file

class LoginScreen(Screen):          # third in the class hierarchy
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    
    def login(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname] ['password'] == pword:
            self.manager.current = 'login_screen_success'
        else:
            self.ids.login_wrong.text = "Wrong username or password!"

class SignUpScreen(Screen):         # third in the class hierarchy
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users=json.load(file)

        users[uname]={'username':uname,'password':pword,
            'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json", "w") as file: # overwrites the "users.json" \
            json.dump(users, file)            # with the content of the "users variable"
        self.manager.current = "sign_up_screen_success" 
        
class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right' # the page slides to the rigth \
        self.manager.current = "login_screen"      # the standard is left

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        
    def get_quote(self, feel):
        feel=feel.lower()
        available_feelings = glob.glob("quotes/*txt")
        available_feelings = [Path(filename).stem for filename in available_feelings]
       
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding="utf8") as file:   # without specifying the encoding type you get an error
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"

class ImageButton(ButtonBehavior, HoverBehavior, Image ): # ButtonBehavior must be first in line !!!
    pass

class RootWidget(ScreenManager):    # second in the class hierarchy
    pass

class MainApp(App):                 # class used for instanciating the app itself
    def build(self):                # highest in class hierarchy
        return RootWidget()

if __name__=="__main__":
    MainApp().run()