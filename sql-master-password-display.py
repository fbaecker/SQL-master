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

    #generate_key()  # Dies sollte nur einmal ausgeführt werden, um den Schlüssel zu generieren
    key = load_key()


print(f'Ich bin der Passwort-Anzeiger für den SQL-Master Version {version}')

config = configparser.ConfigParser()
config.read(ini_file)

# Alle Sektionen (Abschnitte) auslesen
for section in config.sections():
    print(f'Sektion: {section}')

    # Alle Optionen (Schlüssel-Wert-Paare) in dieser Sektion auslesen
    for key1, value in config.items(section):
        print(f'{key1} = {decrypt_text(value.encode(), load_key())}')

exit()
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




