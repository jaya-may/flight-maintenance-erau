import csv
from tkinter import *
import os
import string

root = Tk()

root.title("Login Page")
root.geometry('1920x1080')

def login_page(): # Sets up GUI for login page
    username_label = Label(root, text = "Enter Username:")
    username_label.grid(column = 0, row = 0)

    username_entered = Entry(root, width=10)
    username_entered.grid(column = 1, row = 0)

    password_label = Label(root, text = "Enter Password:")
    password_label.grid(column = 0, row = 1)

    password_entered = Entry(root, width = 10, show = "*")
    password_entered.grid(column = 1, row = 1)

    login_button = Button(root, text = "Enter", fg = "red", command = lambda: button_click(username_entered.get(), password_entered.get()))
    login_button.grid(column = 2, row=0)


def button_click(username: str, password: str): # Makes action happed on button press
    if check_login(username, password):
        success_label = Label(root, text = "Username & Password Accepted", fg = "green")
        success_label.grid(column = 1, row = 3)
    else:
        failure_label = Label(root, text = "Username & Password Denied", fg = "red")
        failure_label.grid(column = 1, row = 3)


def check_login(username: str, password: str): # Checks if login info is accurate
    encrypted_login_info = load_login_info()
    decrypted_login_info = decrypt_login_info(encrypted_login_info)

    for row in decrypted_login_info:
        if username == row[0] and password == row[1]:
            return True
    
    return False


def load_login_info(): # Makes an array for all of the stored usernames and passwords
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Ensures the file is in the same directory as the script (GPT)
    os.chdir(script_dir)

    encrypted_login_info = []
    try:
        with open('login_info.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                username = row[0]
                password = row[1]
                type = row[2]
                encrypted_login_info.append([username, password, type]) # Stored as strings in a list
    except FileNotFoundError:
        print("Error: The file was not found.")
    
    return encrypted_login_info


def decrypt_login_info(encrypted_login_info: list): # Decrypts the login information from the .CSV file
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
            decrypted_username.append(character_list[position]) # Stored as a list
        for letter in encrypted_password:
            position = encryption_key.index(letter)
            decrypted_password.append(character_list[position]) # Stored as a list

        decrytped_username_string = ''.join(decrypted_username) # Turns list into string
        decrytped_password_string = ''.join(decrypted_password) # Turns list into string

        decrypted_login_info.append([decrytped_username_string, decrytped_password_string, type]) # Stores all information as a lsit
    
    return decrypted_login_info
    

def make_character_list(): # Makes a list with all characters
    all_characters = " " + string.ascii_letters + string.digits + string.punctuation
    all_characters = list(all_characters)
    return all_characters
    

def make_encryption(): # Manually set up encryption key
    encryption_key = ['&','R','~','N','e','C','B','_','Z','d',':','O','q','u','|','h','!','3','V','X','4','[','w','s','U','"','0','L','J','$','?','k','j','a','z','b','c',')','9','-','r','I','H','y','P','+','D','#','/','E','Q','A','}','o','.','W','1','(','p','5',';','^','T','\\','i',"'",'x','<','6','K','@','{',',','7',' ','F','Y','t','G','v','=','`','*','2',']','f','n','m','S','>','g','%','M','8','1']
    return encryption_key # Terribly hardcoded for now because if randomized every iteration, code wont work


login_page()
root.mainloop()
