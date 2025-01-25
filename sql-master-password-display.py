from cryptography.fernet import Fernet, InvalidToken
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
version = "1.0"
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
    try:
        f = Fernet(key)
        decrypted_text = f.decrypt(encrypted_text).decode()
        return decrypted_text
    except InvalidToken:
        print("Fehler: Der Schlüssel oder der verschlüsselte Text ist ungültig.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}")




def load_key():
    """
    Laden des Keyfiles
    Das Key-File liegt parallel zum Programm mit dem Namen secret.key

    Returns: Key für die Verschlüsselung / Entschlüsselung

    """
    return open("secret.key", "rb").read()


#
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


    key = load_key()


print(f'Passwort-Display für SQL-Master Version {version}')

config = configparser.ConfigParser()
config.read(ini_file)

# Erlaubte Keys
allowed_keys = {"user", "password"}


# Alle Sektionen (Abschnitte) auslesen
for section in config.sections():

    print(f'Maschine: {section}-----------')
    # Alle Optionen (Schlüssel-Wert-Paare) in dieser Sektion auslesen
    for key, value in config.items(section):
        if(key in allowed_keys):
                print(f'    {key} = {decrypt_text(value.encode(), load_key())}')
        else:
            print('Key sind nicht korrekt')


    print('---------------------------------------------')

input()
