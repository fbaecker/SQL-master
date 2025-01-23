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
##################################################################################################

# --------------------Version
version = "0.1"
# ---------------------------------

ini_file = 'sql-master-password.ini'




def write_decrypted_to_ini(encrypted_text, section, kennung):
    """
    Speichert einen entschlüsselten Text in einer INI-Datei.

    Diese Methode liest eine vorhandene INI-Datei ein, fügt den entschlüsselten Text
    in die angegebene Sektion unter dem angegebenen Schlüssel (Kennung) ein
    und speichert die Änderungen zurück in die Datei. Falls die Sektion nicht existiert,
    wird sie erstellt.

    **Hinweis**:
        Der Text wird im Klartext (nach der Decodierung) in der INI-Datei gespeichert.
        Stellen Sie sicher, dass die Datei entsprechend geschützt ist, falls sensible
        Informationen wie Passwörter enthalten sind.

    Args:
        encrypted_text (bytes): Der verschlüsselte Text, der gespeichert werden soll.
                                Muss ein Byte-String sein, da er decodiert wird.
        section (str): Der Name der Sektion in der INI-Datei, in der der Text gespeichert wird.
                       Üblicherweise der Maschinenname.
        kennung (str): Der Schlüssel innerhalb der Sektion, unter dem der Text gespeichert wird.
                       Beispielsweise "User" oder "Password".
    """
    config = configparser.ConfigParser()
    config.read(ini_file)

    if section not in config:
        config[section] = {}
    config[section][kennung] = encrypted_text.decode()

    with open(ini_file, 'w') as configfile:
        config.write(configfile)


# Verschlüssele das Passwort
def encrypt_text(decrypted_text, key):
    """
    Verschlüsselt einen Klartext mit einem Verschlüsselungsschlüssel.

    Diese Funktion verwendet die Fernet-Verschlüsselung aus der
    `cryptography`-Bibliothek, um den übergebenen Klartext zu verschlüsseln.
    Der Schlüssel muss ein gültiger Fernet-Schlüssel sein, der zum Verschlüsseln
    und späteren Entschlüsseln verwendet wird.

    Args:
        decrypted_text (str): Der Klartext, der verschlüsselt werden soll.
        key (bytes): Der Verschlüsselungsschlüssel (Byte-String), der
                     für die Fernet-Verschlüsselung verwendet wird.

    Returns:
        bytes: Der verschlüsselte Text als Byte-String.


    """

    f = Fernet(key)
    encrypted_text = f.encrypt(decrypted_text.encode())
    return encrypted_text

# In dieser Funktion wird der User / eingegeben Passwort verschlüsselt und dann in die INI-Datei
# geschrieben
# Wenn User oder Passwort leer ist, wird der Key aus der INI-Datei wieder gelöscht
# Diese Funktion wird im Moment gar nicht benötigt
# def user_pwd_speichern(self):
#     if self.le_user.text() != '':
#         print('User verschlüsselt in INI-Datei speichern')
#         # User verschlüsseln und speichern
#         encrypted_user = encrypt_text(self.le_user.text(), key)
#         write_decrypted_to_ini(encrypted_user, 'ODBC-DEFAULT', 'User')
#     else:
#         delete_key_from_ini('ODBC-DEFAULT', 'User')
#
#     if self.le_password.text() != '':
#         print('Passwort verschlüsselt in INI-Datei speichern')
#         # Passwort verschlüsseln und speichern
#         encrypted_password = encrypt_text(self.le_password.text(), key)
#         write_decrypted_to_ini(encrypted_password, 'ODBC-DEFAULT', 'Password')
#     else:
#         delete_key_from_ini('ODBC-DEFAULT', 'Password')
#




# Entschlüssele das Passwort
def decrypt_text(encrypted_text, key):
    """
    Entschlüsselt einen verschlüsselten Text mithilfe eines Verschlüsselungsschlüssels.

    Diese Funktion verwendet die Fernet-Verschlüsselung aus der `cryptography`-Bibliothek,
    um den verschlüsselten Text zu entschlüsseln. Der Schlüssel muss derselbe sein,
    der zur Verschlüsselung des Textes verwendet wurde.

    Args:
        encrypted_text (bytes): Der verschlüsselte Text als Byte-String.
        key (bytes): Der Schlüssel (Byte-String), der für die Fernet-Entschlüsselung verwendet wird.

    Returns:
        str: Der entschlüsselte Text in Klartext.

    """
    f = Fernet(key)
    decrypted_text = f.decrypt(encrypted_text).decode()
    return decrypted_text




# Löschen eines Keys aus der ini-Datei
def delete_key_from_ini(section, key):
    """
    Löscht aus der INI-Datei ein Eintrag mit dem KEY aus der entsprechenden Section
    Args:
        section (string): Name der Section (Hier steht der Maschinenname)
        key (string): User oder Passwort


    """
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


def generate_key():
    """
    Erstellt ein Key-File für die Verschlüsselung, wenn das Key-File noch nicht vorhanden ist.
    Das Key-File wird parallel zu dem programm mit den Namen secret.key erzeugt.

    """
    if not os.path.exists('secret.key'):
        key = Fernet.generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)



def load_key():
    """
    Laden des Keyfiles
    Das Key-File liegt parallel zum Programm mit dem Namen secret.key

    Returns: Key für die Verschlüsselung / Entschlüsselung

    """
    return open("secret.key", "rb").read()


# Lese das verschlüsselte Passwort aus der INI-Datei
def read_decrypted_from_ini(section, key):
    """
    Lesen von verschlüsselten Texten aus einem INI-File

    Args:
        section (String): Section Name (hier der Maschinenname)
        key (String): User oder Password

    Returns (String): Text in lesbarer Form

    """
    config = configparser.ConfigParser()
    config.read(ini_file)

    # Überprüfen, ob der Abschnitt und der Schlüssel vorhanden sind
    if section in config and key in config[section]:
        encrypted_text = config[section][key]
        return encrypted_text
    else:
        print(f'Kein {key} in section {section} in der INI-Datei gefunden.')
        return ''




# Hauptlogik
if __name__ == "__main__":

    generate_key()  # Dies sollte nur einmal ausgeführt werden, um den Schlüssel zu generieren
    key = load_key()


print(f'Ich bin der Passwortmanager für den SQL-Master Version {version}')

# Test zum Löschen eines Password-Eintrags
# delete_key_from_ini('F40099DE', 'Password')
# exit()

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




