import getpass
from cryptography.fernet import Fernet
import configparser
import os

#######################################################################################################################
# Releasenotes
#
# 23.01.25  0.1 Erste Version
#
#
#
# --------------------Version
version = "0.1"
# ---------------------------------

ini_file = 'sql-master-password.ini'



# Schreibe das verschlüsselte Passwort in die INI-Datei
def write_decrypted_to_ini(encrypted_password, section, kennung):
    config = configparser.ConfigParser()
    config.read(ini_file)

    if section not in config:
        config[section] = {}
    config[section][kennung] = encrypted_password.decode()

    with open(ini_file, 'w') as configfile:
        config.write(configfile)


# Verschlüssele das Passwort
def encrypt_text(decrypted_text, key):
    f = Fernet(key)
    encrypted_text = f.encrypt(decrypted_text.encode())
    return encrypted_text

# In dieser Funktion wird der User / eingegeben Passwort verschlüsselt und dann in die INI-Datei
# geschrieben
# Wenn User oder Passwort leer ist, wird der Key aus der INI-Datei wieder gelöscht
def user_pwd_speichern(self):
    if self.le_user.text() != '':
        print('User verschlüsselt in INI-Datei speichern')
        # User verschlüsseln und speichern
        encrypted_user = encrypt_text(self.le_user.text(), key)
        write_decrypted_to_ini(encrypted_user, 'ODBC-DEFAULT', 'User')
    else:
        delete_key_from_ini('ODBC-DEFAULT', 'User')

    if self.le_password.text() != '':
        print('Passwort verschlüsselt in INI-Datei speichern')
        # Passwort verschlüsseln und speichern
        encrypted_password = encrypt_text(self.le_password.text(), key)
        write_decrypted_to_ini(encrypted_password, 'ODBC-DEFAULT', 'Password')
    else:
        delete_key_from_ini('ODBC-DEFAULT', 'Password')





# Entschlüssele das Passwort
def decrypt_text(encrypted_text, key):
    f = Fernet(key)
    decrypted_text = f.decrypt(encrypted_text).decode()
    return decrypted_text




# Löschen eines Keys aus der ini-Datei
def delete_key_from_ini(section, key):
    config = configparser.ConfigParser()
    config.read(ini_file)

    # Überprüfen, ob die Sektion existiert
    if section in config:
        # Überprüfen, ob der Schlüssel existiert
        if key in config[section]:
            # Entfernen des Schlüssels
            config.remove_option(section, key)
            print(f"Schlüssel '{key}' in Sektion '{section}' wurde gelöscht.")
        else:
            print(f"Schlüssel '{key}' in Sektion '{section}' nicht gefunden.")
    else:
        print(f"Sektion '{section}' nicht gefunden.")

    # Speichern der Änderungen in der INI-Datei
    with open(ini_file, 'w') as configfile:
        config.write(configfile)

# Generiere einen Schlüssel und schreibe ihn in eine Datei wenn noch nicht existiert
def generate_key():
    if not os.path.exists('secret.key'):
        key = Fernet.generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)


# Lade den Schlüssel aus der Datei
def load_key():
    return open("secret.key", "rb").read()

# Hauptlogik
if __name__ == "__main__":

    generate_key()  # Dies sollte nur einmal ausgeführt werden, um den Schlüssel zu generieren
    key = load_key()

# Lese das verschlüsselte Passwort aus der INI-Datei
def read_decrypted_from_ini(section, key):
    config = configparser.ConfigParser()
    config.read(ini_file)

    # Überprüfen, ob der Abschnitt und der Schlüssel vorhanden sind
    if section in config and key in config[section]:
        encrypted_text = config[section][key]
        return encrypted_text
    else:
        print(f'Kein {key} in section {section} in der INI-Datei gefunden.')
        return ''



print(f'Ich bin der Passwortmanager für den SQL-Master Version {version}')

# Passwort aus der INI-Datei lesen und entschlüsseln
encrypted_password_from_ini = read_decrypted_from_ini('F40099DE', 'Password')
if encrypted_password_from_ini != '':
    decrypted_password = decrypt_text(encrypted_password_from_ini.encode(), key)
    print(f" F40099DE passwort {decrypted_password}")


system = input('System: ')
user = input('User: ')
#password = getpass.getpass('Passwort: ')
password = input('Passwort: ')
print(f"System: {system}, User: {user}, Passwort {password} wurde eingegeben.")

input()

print('User verschlüsselt in INI-Datei speichern')



# User verschlüsseln und speichern
encrypted_password = encrypt_text(password, key)
encrypted_user = encrypt_text(user, key)



write_decrypted_to_ini(encrypted_user, system, 'User')
write_decrypted_to_ini(encrypted_password, system, 'Password')




