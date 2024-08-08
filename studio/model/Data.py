from studio.Service.DBCamlive import DatabaseManager
from studio.Service.NotificationService import Connexion, NotificationService
from studio.controller.CamController import CamController
from studio.model.ThreadClass import ThreadManager
from kivymd.uix.dialog import MDDialog
import hashlib
import os
import re
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from studio.controller.ExpansionPanel import ExpansionPanelVid, FocusButton, IconButtonAction


class Data:
    index = 1
    listProces = []
    listCam = []
    connectLiveController = None
    menu_items_format = []
    menu_items_camera = []
    resource_cam_thread = None
    manager = ThreadManager()
    expansion = ExpansionPanelVid()
    expand_two = False
    expand_one = False
    app = None
    dialogConnexionBox = None
    username = None
    list_sessions = None

    def __init__(self, app) -> None:
        self.camController = CamController()
        self.app = app
        self.camController.app = app
        self.db_manager = DatabaseManager("camlive.db")
    

    def sessions(self):
        if not self.dialogConnexionBox:
            self.dialogConnexionBox = MDDialog(
                    title="[b][color=#5AA6FF]Connexion[/color][/b]",
                    type="custom",
                    content_cls=Connexion(),
                    md_bg_color="#262626",
                    buttons=[
                        MDRectangleFlatButton(
                            text="Continuer sans connexion",
                            theme_text_color="Custom",
                            text_color=self.app.theme_cls.primary_color,
                            on_release=self.continuer
                        ),
                        MDRectangleFlatButton(
                            text="Connexion",
                            theme_text_color="Custom",
                            text_color=self.app.theme_cls.primary_color,
                            on_release=self.connexion
                        ),
                        MDRectangleFlatButton(
                            text="Créer un compte",
                            theme_text_color="Custom",
                            text_color=self.app.theme_cls.primary_color,
                            on_release=self.creer_compte
                        ),
                    ],
            )
        self.dialogConnexionBox.open()

    def continuer(self, dt):
        self.app.main_view.transition.direction = "left"
        self.app.main_view.current = "screen main"
        self.dialogConnexionBox.dismiss()

    def creer_compte(self, dt):
        name = self.dialogConnexionBox.content_cls.text_username.text
        password = self.dialogConnexionBox.content_cls.text_password.text
        email = self.dialogConnexionBox.content_cls.text_email.text
        if name == "" or password == "" or self.is_valid_email(email):
            return toast("entrer invalide")
        try:
            select_user_sql = "SELECT * FROM users WHERE name = ? "
            user = self.db_manager.fetch_data(select_user_sql, (name,))
            if not user:
                password_hash = self.hash_password(password)
                insert_sql = "INSERT INTO users (name, password) VALUES (?, ?)"
                self.db_manager.insert_data(insert_sql, (name, password_hash))
                print("ok insert")
            else:
                return toast("L'utilisateur exist déjà, veiller vous connectez!")
            select_user_sql = "SELECT * FROM users WHERE name = ? AND password = ?"
            user = self.db_manager.fetch_data(select_user_sql, (name, password_hash,))
            if not user:
                return toast("Probleme de connexion, Veillez réessayer !")
            print(user)
            self.username = user[1]
            print(self.username)
            select_session_sql = "SELECT * FROM sessions WHERE user_id=?"
            self.list_sessions = self.db_manager.fetch_data(select_session_sql, (user[0],))
            print(self.list_sessions)
            self.dialogConnexionBox.dismiss()
            self.app.main_view.transition.direction = "left"
            self.app.main_view.current = "screen main"
        except Exception as e:
            print(e)
            return toast("Une erreur est survenue veillez réessayé")
    
    def connexion(self, dt):
        name = self.dialogConnexionBox.content_cls.text_username.text
        password = self.dialogConnexionBox.content_cls.text_password.text
        if name == "" or password == "":
            return toast("entrer vide")
        try:
            password_hash = self.hash_password(password)
            select_user_sql = "SELECT * FROM users WHERE name=? AND password=?"
            user = self.db_manager.fetch_data(select_user_sql, (name, password_hash))
            if not user:
                return toast("Utilisateur n'exist pas, Veillez creer un Compte")
            print(user)
            self.username = user[1]
            print(self.username)
            select_session_sql = "SELECT * FROM sessions WHERE user_id=?"
            self.list_sessions = self.db_manager.fetch_data(select_session_sql , (user[0]))
            print(self.list_sessions)
            self.dialogConnexionBox.dismiss()
            self.app.main_view.transition.direction = "left"
            self.app.main_view.current = "screen main"
        except Exception as e:
            print(e)
            return toast("Une erreur est survenue veillez réessayé")


    def hash_password(self, password):
        salt = os.urandom(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return salt + hashed

    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:16]
        stored_hash = stored_password[16:]
        hashed = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
        return hashed == stored_hash

    def is_valid_email(self, email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None



