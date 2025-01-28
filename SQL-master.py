import configparser
from cryptography.fernet import Fernet
import sys
from typing import List

import pyodbc # ODBC
import re

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill



from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox, QTableWidget, \
    QTableWidgetItem, QPlainTextEdit, QPushButton, QApplication
from PySide6.QtCore import QTimer, QRect
from Qt.main_window import Ui_MainWindow
from decimal import Decimal

import json
import os
from datetime import datetime
from PyQt5.QtCore import Qt


#######################################################################################################################
# Releasenotes
#
# 30.06.24  0.1 Erste Version
# 15.07.24  0.2 Aufruf von mehreren Instanzen. Mit diesem Stand kann nun aufgebaut werden
# 17.11.24  0.3 Checkboxen welche HV-Version und Test und Prod in der Maske eingebaut
#               Initialwerte für die Checkboxen in der ini-Datei ablegen
# 20.11.24  0.4 Die Instanzliste mit der HV-Nummer und TST oder PROD erweitert
#               Sortfunktion für die Instanzliste eingebaut.
#               Berücksichtigung der CheckBoxen in bei der Abfrage
# 27.12.24  0.5 Das Festlegen des Table-Views erfolgt nun immer und nicht nur bei der ersten Instanz
#               Wenn die erste Instanz keine Daten hatte sind keine Werte ausgegeben worden.
#           0.6 History Funktion für die SQL-Statements
# 24.01.25  0.7 Instanzen, User und Passwort aus Dateien lesen
# 25.01.25  1.0 Alle Instanzen kommen nun aus der INI-Datei und auch die User und Passwörter
#
#
# --------------------Version
version = "1.1-Branch Excel-Ausgabe"
# ---------------------------------

# Defaultwerte aus der Ini-Datei lesen
config = configparser.ConfigParser()
config.read('SQL-master.ini', encoding='utf-8')
HV9 = config.get('Einstellungen', 'HV9')
HV8 = config.get('Einstellungen', 'HV8')
HV7 = config.get('Einstellungen', 'HV7')
Nonhv = config.get('Einstellungen', 'NONHV')
Test = config.get('Einstellungen', 'TEST')
Prod = config.get('Einstellungen', 'PROD')


#Instanzen-Datei
instanzen_datei = "instanzen.ini"
password_ini_file = "sql-master-password.ini"



# Globale Variable
sql_input = "select count(*) from pfistam where fsfirm <> '' "
history_index = 0
header_zeilen = False

HISTORY_FILE_JSON = "sql_history.json"

# Neue Excel-Arbeitsmappe erstellen
workbook = Workbook()
sheet = workbook.active
sheet.title = "SQL Ergebnisse"


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
    config.read(password_ini_file)

    # Überprüfen, ob der Abschnitt und der Schlüssel vorhanden sind
    if section in config and key in config[section]:
        encrypted_text = config[section][key]
        return encrypted_text
    else:
        print(f'Kein {key} in section {section} in der INI-Datei gefunden.')
        return ''




def save_to_json_history(sql_statement):
    """Speichert ein SQL-Statement mit Metadaten in eine JSON-Datei."""
    history = []
    if os.path.exists(HISTORY_FILE_JSON):
        with open(HISTORY_FILE_JSON, "r") as file:
            history = json.load(file)
    entry = {"timestamp": datetime.now().isoformat(), "sql": sql_statement}
    history.append(entry)
    with open(HISTORY_FILE_JSON, "w") as file:
        json.dump(history, file, indent=4)

def read_json_history():
    """Liest die JSON-History und gibt die Einträge zurück."""
    if not os.path.exists(HISTORY_FILE_JSON):
        return []
    with open(HISTORY_FILE_JSON, "r") as file:
        return json.load(file)

def aufbereiten_instanz_liste():
    """
    Liest die Instanz-Datei, und die Datei mit dem User und das Passwort
    Entschlüsselt das Passwort und User und füllt die Instanz-Liste


    RETURN: gefüllte Instanzenliste
    """
    config = configparser.ConfigParser()
    config.optionxform = str  # Behalte die Groß-/Kleinschreibung der Schlüssel bei
    config.read(instanzen_datei)


    key = load_key()
    instanzen_liste = []
    # Alle Sektionen (Abschnitte mit den Maschinen) auslesen
    for maschine in config.sections():

        # Alle Key (Key mit HV-Typ) in dieser Sektion auslesen
        for hv_typ, value in config.items(maschine):
            values = value.split(",")  # Teilt den String in eine Liste

            for instanz in values:  # Schleife über die Werte in der Liste

                user = decrypt_text(read_decrypted_from_ini(maschine, "user").encode(), key)
                password = decrypt_text(read_decrypted_from_ini(maschine, "password").encode(), key)

                # dem HV-Typ aus dem Key noch in Werte teilen
                # HV9_TST   HV9   und   TST
                hv_typ_teil =hv_typ.split("_")
                instanzen_liste.append((maschine, user, password, instanz.strip(),
                                        hv_typ_teil[0], hv_typ_teil[1]))

    # Die resultierende Liste ausgeben (zu Testzwecken)
    #for entry in instanzen_liste:
    #    print(entry)

    return instanzen_liste




class MainWindow(QMainWindow):

    global sql_input
    def __init__(self):
        super(MainWindow, self).__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        # CheckBoxen vorbelegen
        if HV9 == '1':
            self.gui.checkBox_HV9.setChecked(True)
        if HV8 == '1':
            self.gui.checkBox_HV8.setChecked(True)
        if HV7 == '1':
            self.gui.checkBox_HV7.setChecked(True)
        if Nonhv == '1':
            self.gui.checkBox_NONHV.setChecked(True)
        if Test == '1':
            self.gui.checkBox_Test.setChecked(True)
        if Prod == '1':
            self.gui.checkBox_PROD.setChecked(True)


        # Verbinde Menüpunkte mit Methoden
        self.gui.actionOpen.triggered.connect(self.open_file)
        self.gui.actionExit.triggered.connect(self.exit)
        self.gui.actionStart.triggered.connect(self.abfrage)
        self.gui.action_ber.triggered.connect(self.show_about)
        self.gui.actionSQL_Eingabe.triggered.connect(self.sql_eingabe)

        # Verbinden der Check-Boxen mit einer Änderungs-Methode
        self.gui.checkBox_HV9.stateChanged.connect(self.on_checkbox_changed)
        self.gui.checkBox_HV8.stateChanged.connect(self.on_checkbox_changed)
        self.gui.checkBox_HV7.stateChanged.connect(self.on_checkbox_changed)
        self.gui.checkBox_NONHV.stateChanged.connect(self.on_checkbox_changed)
        self.gui.checkBox_Test.stateChanged.connect(self.on_checkbox_changed)
        self.gui.checkBox_PROD.stateChanged.connect(self.on_checkbox_changed)

    def on_checkbox_changed(self):
        global HV9, HV8, HV7, Nonhv, Test, Prod

        # zuerst alle globale Variable ausmachen
        HV9 = '0'
        HV8 = '0'
        HV7 = '0'
        Nonhv = '0'
        Test = '0'
        Prod = '0'

        # Die Werte der Checkboxen in die globalen Variablen wieder an machen die an sind
        if self.gui.checkBox_HV9.isChecked():
            HV9 = '1'
        if self.gui.checkBox_HV8.isChecked():
            HV8 = '1'
        if self.gui.checkBox_HV7.isChecked():
            HV7 = '1'
        if self.gui.checkBox_NONHV.isChecked():
            Nonhv = '1'
        if self.gui.checkBox_Test.isChecked():
            Test = '1'
        if self.gui.checkBox_PROD.isChecked():
            Prod = '1'






    def open_file(self):
        print(read_json_history())
        #self.gui.plainTextEdit.setPlainText("Open File clicked")



    def show_about(self):
        QMessageBox.about(self, "About", "This is a PyQt5/PySide6 application")

    def show_help(self):
        self.gui.label.setText("Help clicked")



    def exit(self):
        exit()

    def sql_eingabe(self):
        try:
            self.table_widget.hide()
        except:
            print('hide ging schief')


        # self.gui.plainTextEdit.show()
        # text = self.gui.plainTextEdit.toPlainText()
        # print(text)

        # Erstelle und zeige ein neues Fenster mit QPlainTextEdit
        self.new_window = NewWindow(self)
        self.new_window.show()



    def abfrage(self):
        global sql_input, HV9, HV8, HV7, Nonhv, Test, Prod
        print("Taste Start gedrückt")




        # Zu beginn alle globalen Variablen für die Auswahl auf 0 setzen
        # HV9 = '0'
        # HV8 = '0'
        # HV7 = '0'
        # Nonhv = '0'
        # Test = '0'
        # Prod = '0'


        # Verhindern, dass beide Checkboxen für Test und Prod abgewählt sind
        if Test == '0'  and Prod == '0':
            # Wenn beide nicht ausgewählt sind, eine Test Checkbox wieder aktivieren
            sender = self.sender()
            self.gui.checkBox_Test.setChecked(True)
            Test = '1'
        # if not self.gui.checkBox_Test.isChecked() and not self.gui.checkBox_PROD.isChecked():
        #     # Wenn beide nicht ausgewählt sind, eine Test Checkbox wieder aktivieren
        #     sender = self.sender()
        #     if sender == self.gui.checkBox_Test:
        #         self.gui.checkBox_PROD.setChecked(True)
        #         Prod = '1'
        #     else:
        #         self.gui.checkBox_Test.setChecked(True)
        #         Test = '1'


        # Die Werte der Checkboxen in die globalen Variablen schreiben
        # if self.gui.checkBox_HV9.isChecked():
        #     HV9 = '1'
        # if self.gui.checkBox_HV8.isChecked():
        #     HV8 = '1'
        # if self.gui.checkBox_HV7.isChecked():
        #     HV7 = '1'
        # if self.gui.checkBox_NONHV.isChecked():
        #     Nonhv = '1'
        # if self.gui.checkBox_Test.isChecked():
        #     Test = '1'
        # if self.gui.checkBox_PROD.isChecked():
        #     Prod = '1'



        # Speichern des Status der CheckBoxen wenn dies angewählt ist
        ## TO DO Einstellung muss noch mal geprüft werden
        # if self.gui.checkBox_Einstellung.isChecked():
        #     config.set('Einstellungen', 'HV9', '1' if self.gui.checkBox_HV9.isChecked() else '0')
        #     config.set('Einstellungen', 'HV8', '1' if self.gui.checkBox_HV8.isChecked() else '0')
        #     config.set('Einstellungen', 'HV7', '1' if self.gui.checkBox_HV7.isChecked() else '0')
        #     config.set('Einstellungen', 'Nonhv', '1' if self.gui.checkBox_NONHV.isChecked() else '0')
        #     config.set('Einstellungen', 'Test', '1' if self.gui.checkBox_Test.isChecked() else '0')
        #     config.set('Einstellungen', 'Prod', '1' if self.gui.checkBox_PROD.isChecked() else '0')
        #
        #     # Schreiben der Änderungen zurück in die INI-Datei
        #     with open('SQL-master.ini', 'w') as configfile:
        #         config.write(configfile)


        # Haupt-Widget und Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Erstelle ein QTableWidget
        self.table_widget = QTableWidget()



        instanz_list = aufbereiten_instanz_liste()



        self.zeilen_counter = 0

        print(f' sql_input aus der Eingabe {sql_input}')

        # Sortieren nach dem letzten und dann nach dem vorletzten Eintrag
        sorted_list = sorted(instanz_list, key=lambda x: (x[-1], x[-2]))



        # SQL-Statement analysieren
        table_name = extract_table_name(sql_input)
        print(f'Table name: {table_name}')


        zeile_in_for = 0
        for i, zeile in enumerate(sorted_list):


            # wenn der Tabellen name identifiziert wurde, die Instanz und die Bibl. noch erweitern

            # # Abfrage, ob die Instanz zu der gewünschten Auswahl gehört und ob Test oder Prod
            # # gewünscht ist. Wenn nicht wird in der for-Schleife der nächste Eintrag verwendet
            # if (zeile[4] == "HV9" and HV9 == '0'):
            #     continue
            # elif (zeile[4] == "HV8" and HV8 == '0'):
            #     continue
            # elif (zeile[4] == "HV7" and HV7 == '0'):
            #     continue
            # elif (zeile[5] == "TST" and Test == '0'):
            #     continue
            # elif (zeile[5] == "PROD" and Prod == '0'):
            #     continue


            # Dies ist die elegantere Variante um die Bedingung abzufragen um
            # die Schleife zu beenden
            # Bedingungen als Dictionary definieren
            conditions = {
                "HV9": HV9,
                "HV8": HV8,
                "HV7": HV7,
                "NONHV": Nonhv,
                "TST": Test,
                "PROD": Prod
            }

            # Überprüfen, ob die Zeile zu den Bedingungen passt
            if (zeile[4] in conditions and conditions[zeile[4]] == '0') or \
                    (zeile[5] in conditions and conditions[zeile[5]] == '0'):
                continue

            if table_name:
                # Erstelle den neuen Tabellennamen mit der Instanz
                new_table_name = f"{zeile[3]}DATV7.{table_name}"
                # Ersetze den Tabellennamen im SQL-Statement
                sql_query = re.sub(rf'\b{table_name}\b', new_table_name, sql_input, flags=re.IGNORECASE)
                print(f'SQL-statement nach der Aufbereitung: {sql_query}')


            self.sql_pro_instanz(sql_query,zeile[0],zeile[1],zeile[2], zeile[3], layout, zeile_in_for, zeile[4], zeile[5])

            print(f'Ende der for schleife {i}')
            zeile_in_for += 1

        # Excel-Datei speichern
        workbook.save("sql_results.xlsx")
        print("Daten wurden in die Datei 'sql_results.xlsx' geschrieben.")






    # Methode um pro Instanz das SQL-Statement auszuführen am Bildschirm auszugeben
    def sql_pro_instanz(self, sql_statement, host, user, passwort, instanz, layout, nummer, version, art):

        global header_zeilen

        print(f'Zeilen-Zähler  {instanz}: {self.zeilen_counter}')

        # Erstelle die Verbindungszeichenfolge mit f-strings
        conn_str = (f'DRIVER={{IBM i Access ODBC Driver}};'
                    f'SYSTEM={host};'
                    f'UID={user};'
                    f'PWD={passwort}')



        # Stelle die Verbindung her
        try:
            conn = pyodbc.connect(conn_str)
        except pyodbc.Error as e:
            print(f'Fehler beim Herstellen der Verbindung: {e}')
            QMessageBox.critical(self, "Verbindungsfehler", f"Fehler beim Herstellen der Verbindung: {e}")

            return

        # Erstelle einen Cursor-Objekt
        cursor = conn.cursor()

        cursor.execute(sql_statement)

        # Hole alle Zeilen der Abfrage
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("Keine Daten gefunden")
            return


        # Ab hier werden die Daten ausgegeben

        #***************Test für EXCEL-Ausgabe**********************'

        # Überschriften nur in der ersten Zeile
        if header_zeilen == False:
            # Spaltennamen aus der Abfrage holen
            column_names = ["Version"] + ["Art"] + ["Instanz"] +[description[0] for description in cursor.description]

            # Spaltenüberschriften in die erste Zeile schreiben
            sheet.append(column_names)
            header_zeilen = True
            #Autofilter in die Überschrift mit den Feldnamen setzen
            sheet.auto_filter.ref = sheet.dimensions

            # Formatierung der Kopfzeile Schrift in Bold und Hintergrund Grau
            header_font = Font(bold=True)  # Fett
            header_fill = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")  # Grau
            for cell in sheet[1]:  # Erste Zeile (Kopfzeile)
                cell.font = header_font
                cell.fill = header_fill

        # Datenzeilen in das Excel-Blatt schreiben
        for row in rows:
            sheet.append([version]+[art]+[instanz]+list(row))  # Jede Zeile in eine Liste umwandeln

        # Spaltenbreite automatisch anpassen
        for column in sheet.columns:
            max_length = 0
            column_letter = column[0].column_letter  # Spaltenbuchstabe (z. B. "A", "B", ...)
            for cell in column:
                if cell.value:  # Falls die Zelle nicht leer ist
                    max_length = max(max_length, len(str(cell.value)))
            adjusted_width = max_length + 2  # Etwas zusätzlichen Platz hinzufügen
            sheet.column_dimensions[column_letter].width = adjusted_width


        #***********************************************************


        # Definieren der Breite und Länge der Tabelle für die Ausabe und Feldnamen setzen
        # Dies wird bei jeder Instanz gemacht, da nicht sicher ist dass bei der ersten Instanz
        # schon etwas gefunden wird.

        # Anzahl der Spalten festlegen
        #self.table_widget.setRowCount(len(rows))
        self.table_widget.setRowCount(999999)
        self.table_widget.setColumnCount(len(rows[0]) + 3)  # + 4 Felder für die Version, Art und Instanz

        layout.addWidget(self.table_widget)


        # Feldnamen aus den Metadaten der Abfrage abrufen
        column_names: list[str] = ["Version"] + ["Art"] + ["Instanz"] + [desc[0] for desc in cursor.description]  # Spalte 1,2 und ist für Version Art und Instanz
        # Feldnamen als Überschrift ausgeben
        self.table_widget.setHorizontalHeaderLabels(column_names)

        # Fülle die Tabelle mit Daten
        for row_idx, row in enumerate(rows):
            self.table_widget.setItem(row_idx+self.zeilen_counter, 0, QTableWidgetItem(version))  # Spalte 1 ist die Version)
            self.table_widget.setItem(row_idx + self.zeilen_counter, 1,QTableWidgetItem(art))  # Spalte 2 ist die Version)
            self.table_widget.setItem(row_idx+self.zeilen_counter, 2, QTableWidgetItem(instanz))  # Spalte 3 ist die Instanz
            for col_idx, item in enumerate(row, start=3):
                if isinstance(item, Decimal):
                    item = str(item)
                elif isinstance(item, int):
                    item = str(item)
                self.table_widget.setItem(row_idx+self.zeilen_counter, col_idx, QTableWidgetItem(item))

        #Zeilen-Counter auf aktuellen Wert setzen für die nächste Instanz
        self.zeilen_counter = self.zeilen_counter+row_idx+1

        conn.close()




class NewWindow(QMainWindow):

    def __init__(self, main_instance):
        # Das Eingabewindow für das SQL-Komando wurde hier von Hand erstellt nicht über
        # den QT-Designer. Dies müsste man noch mal ändern
        super().__init__()
        self.setWindowTitle("SQL-Eingabe")
        self.main_instance = main_instance  # Speichern der Instanz der anderen Klasse

        # Haupt-Widget und Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Erstelle ein QPlainTextEdit-Widget
        self.plain_text_edit = QPlainTextEdit()
        layout.addWidget(self.plain_text_edit)

        # Erstelle einen OK-Knopf
        self.ok_button = QPushButton("OK")
        layout.addWidget(self.ok_button)

        # Erstelle einen History lesen-Knopf
        self.history_button = QPushButton("History lesen")
        layout.addWidget(self.history_button)

        # Erstelle einen History schreiben-Knopf
        self.history_schreiben_button = QPushButton("History schreiben")
        layout.addWidget(self.history_schreiben_button)



        # Verbinde den OK-Knopf mit der Methode ok_button_clicked
        self.ok_button.clicked.connect(self.ok_button_clicked)

        # Verbinde den History-Knopf mit der Methode history_clicked
        self.history_button.clicked.connect(self.history_button_clicked)
        self.history_schreiben_button.clicked.connect(self.history_schreiben_button_clicked)

        # Letzte SQL Befehl vorbelegen
        self.plain_text_edit.setPlainText(sql_input)



    def ok_button_clicked(self):
        global sql_input

        sql_statement = self.plain_text_edit.toPlainText()


        sql_input = sql_statement
        print(f'OK button clicked. SQL-Statement: {sql_statement}')
        # Sie können hier weitere Aktionen hinzufügen, z.B. das Fenster schließen oder das SQL-Statement verarbeiten

        self.close()


        # Aufrufen der Methode aus der anderen Klasse
        self.main_instance.abfrage()

    def history_button_clicked(self):
        # Ein SQL-Statement aus der History holen

        global history_index

        print("History geklicked")

        print(f'Index {history_index}')
        history_json = read_json_history()

        # Neues Statement abrufen
        sql_statement = history_json[history_index]["sql"]
        print(f"Nächstes SQL-Statement: {sql_statement}")
        self.plain_text_edit.setPlainText(sql_statement)
        history_index += 1
        # Vermeiden von Indexfehlern (zirkuläre Navigation)
        if history_index >= len(history_json):
            history_index = 0  # Zurück zum Anfang

    def history_schreiben_button_clicked(self):
        # Ein SQL-Statement aus in die History schreiben

        print("History schreiben geklicked")
        # Wenn ein neues SQL-statement eingegeben wurde, dann in History ablegen.
        sql_statement = self.plain_text_edit.toPlainText()
        if sql_input != sql_statement:
           print(f'statement {sql_statement} in SQL-History ablegen')
           save_to_json_history(sql_statement)



def extract_table_name(sql_statement):
    # Suche nach dem `from`-Teil des SQL-Statements und extrahiere das Wort danach
    match = re.search(r'from\s+(\S+)', sql_statement, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle(f'SQL-Master Version {version}')
    window.show()
    sys.exit(app.exec())



