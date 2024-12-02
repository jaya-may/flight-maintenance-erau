import csv
from tkinter import *
import os
import string

def login_page(root):
    # Variable to track login success
    login_success = [False]

    def button_click(username: str, password: str):
        if check_login(username, password):
            success_label = Label(login_frame, text="Username & Password Accepted", fg="green")
            success_label.grid(column=1, row=3)
            login_success[0] = True
            # Destroy login_frame after successful login
            login_frame.after(1000, login_frame.destroy)
        else:
            failure_label = Label(login_frame, text="Username & Password Denied", fg="red")
            failure_label.grid(column=1, row=3)

    def check_login(username: str, password: str):
        encrypted_login_info = load_login_info()
        decrypted_login_info = decrypt_login_info(encrypted_login_info)

        for row in decrypted_login_info:
            if username == row[0] and password == row[1]:
                return True

        return False

    def load_login_info():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

        encrypted_login_info = []
        try:
            with open('login_info.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    username = row[0]
                    password = row[1]
                    type = row[2]
                    encrypted_login_info.append([username, password, type])
        except FileNotFoundError:
            print("Error: The file was not found.")

        return encrypted_login_info

    def decrypt_login_info(encrypted_login_info: list):
        character_list = make_character_list()
        encryption_key = make_encryption()

        decrypted_login_info = []

        for row in encrypted_login_info:
            encrypted_username = row[0]
            encrypted_password = row[1]
            type = row[2]

            decrypted_username = []
            decrypted_password = []

            for letter in encrypted_username:
                position = encryption_key.index(letter)
                decrypted_username.append(character_list[position])
            for letter in encrypted_password:
                position = encryption_key.index(letter)
                decrypted_password.append(character_list[position])

            decrypted_username_string = ''.join(decrypted_username)
            decrypted_password_string = ''.join(decrypted_password)

            decrypted_login_info.append([decrypted_username_string, decrypted_password_string, type])

        return decrypted_login_info

    def make_character_list():
        all_characters = " " + string.ascii_letters + string.digits + string.punctuation
        all_characters = list(all_characters)
        return all_characters

    def make_encryption():
        encryption_key = ['&','R','~','N','e','C','B','_','Z','d',':','O','q','u','|','h','!','3','V','X','4','[','w','s','U','"','0','L','J','$','?','k','j','a','z','b','c',')','9','-','r','I','H','y','P','+','D','#','/','E','Q','A','}','o','.','W','1','(','p','5',';','^','T','\\','i',"'",'x','<','6','K','@','{',',','7',' ','F','Y','t','G','v','=','`','*','2',']','f','n','m','S','>','g','%','M','8','1']
        return encryption_key

    # Create a frame for the login widgets
    login_frame = Frame(root)
    login_frame.pack(pady=100)

    username_label = Label(login_frame, text="Enter Username:", font=("Arial", 16))
    username_label.grid(column=0, row=0, padx=5, pady=5, sticky='e')

    username_entered = Entry(login_frame, width=20, font=("Arial", 16))
    username_entered.grid(column=1, row=0, padx=5, pady=5)

    password_label = Label(login_frame, text="Enter Password:", font=("Arial", 16))
    password_label.grid(column=0, row=1, padx=5, pady=5, sticky='e')

    password_entered = Entry(login_frame, width=20, show="*", font=("Arial", 16))
    password_entered.grid(column=1, row=1, padx=5, pady=5)

    login_button = Button(login_frame, text="Enter", fg="red", font=("Arial", 16),
                          command=lambda: button_click(username_entered.get(), password_entered.get()))
    login_button.grid(column=1, row=2, padx=5, pady=20)

    # Wait for the login process to complete
    root.wait_window(login_frame)

    return login_success[0]
