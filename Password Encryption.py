import string
import random

def MakeCharacterList():
    All_Characters = " " + string.ascii_letters + string.digits + string.punctuation
    All_Characters = list(All_Characters)
    return All_Characters
    
def MakeEncryption(All_Characters):
    Encryption_Key = All_Characters.copy()
    random.shuffle(Encryption_Key)
    return Encryption_Key

# Encrypt Username and Password
def EncryptText(All_Characters, Encryption_Key):
    Input_Username = input("Username: ") # Still need to figure out how to integrate this into the UI, ask Wednesday
    Input_Password = input("Password: ") # Same for this

    Username_Encrypted = ""
    Password_Encrypted = ""

    for letter in Input_Username:
        Position = All_Characters.index(letter)
        Username_Encrypted = Username_Encrypted + Encryption_Key[Position]

    for letter in Input_Password:
        Position = All_Characters.index(letter)
        Password_Encrypted = Password_Encrypted + Encryption_Key[Position]

    print(f"Encrypted Username: {Username_Encrypted}")
    print(f"Encrypted Password: {Password_Encrypted}")

# Decrypt Username and Password
def DecryptText(All_Characters, Encryption_Key):
    Input_Username_Encrypted = input("Encrypted Username: ")
    Input_Password_Encrypted = input("Encrypted Password: ")

    Username_Decrypted = ""
    Password_Decrypted = ""

    for letter in Input_Username_Encrypted:
        Position = Encryption_Key.index(letter)
        Username_Decrypted = Username_Decrypted + All_Characters[Position]

    for letter in Input_Password_Encrypted:
        Position = Encryption_Key.index(letter)
        Password_Decrypted = Password_Decrypted + All_Characters[Position]

    print(f"Decrypted Username: {Username_Decrypted}")
    print(f"Decrypted Password: {Password_Decrypted}")

All_Characters = MakeCharacterList()
Encryption_Key = MakeEncryption(All_Characters)
EncryptText(All_Characters, Encryption_Key)
DecryptText(All_Characters, Encryption_Key)