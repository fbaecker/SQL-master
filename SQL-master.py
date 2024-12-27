import configparser
import sys
from typing import List

import pyodbc # ODBC
import re



from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox, QTableWidget, \
    QTableWidgetItem, QPlainTextEdit, QPushButton, QApplication
from PySide6.QtCore import QTimer, QRect
from Qt.main_window import Ui_MainWindow
from decimal import Decimal


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
#
#
# --------------------Version
version = "0.5"
# ---------------------------------

# Defaultwerte aus der Ini-Datei lesen
config = configparser.ConfigParser()
config.read('SQL-master.ini', encoding='utf-8')
HV9 = config.get('Einstellungen', 'HV9')
HV8 = config.get('Einstellungen', 'HV8')
HV7 = config.get('Einstellungen', 'HV7')
Nonhv = config.get('Einstellungen', 'NON-HV')
Test = config.get('Einstellungen', 'TEST')
Prod = config.get('Einstellungen', 'PROD')



# Globale Variable
sql_input = "select count(*) from pfistam where fsfirm <> '' "




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






    def open_file(self):
        self.gui.plainTextEdit.setPlainText("Open File clicked")

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
        global sql_input
        print("Taste Start gedrückt")




        # Zu beginn alle globalen Variablen für die Auswahl auf 0 setzen
        HV9 = '0'
        HV8 = '0'
        HV7 = '0'
        Nonhv = '0'
        Test = '0'
        Prod = '0'


        # Verhindern, dass beide Checkboxen für Test und Prod abgewählt sind
        if not self.gui.checkBox_Test.isChecked() and not self.gui.checkBox_PROD.isChecked():
            # Wenn beide nicht ausgewählt sind, eine Test Checkbox wieder aktivieren
            sender = self.sender()
            if sender == self.gui.checkBox_Test:
                self.gui.checkBox_PROD.setChecked(True)
                Prod = '1'
            else:
                self.gui.checkBox_Test.setChecked(True)
                Test = '1'


        # Die Werte der Checkboxen in die globalen Variablen schreiben
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



        # Speichern des Status der CheckBoxen wenn dies angewählt ist
        if self.gui.checkBox_Einstellung.isChecked():
            config.set('Einstellungen', 'HV9', '1' if self.gui.checkBox_HV9.isChecked() else '0')
            config.set('Einstellungen', 'HV8', '1' if self.gui.checkBox_HV8.isChecked() else '0')
            config.set('Einstellungen', 'HV7', '1' if self.gui.checkBox_HV7.isChecked() else '0')
            config.set('Einstellungen', 'Nonhv', '1' if self.gui.checkBox_NONHV.isChecked() else '0')
            config.set('Einstellungen', 'Test', '1' if self.gui.checkBox_Test.isChecked() else '0')
            config.set('Einstellungen', 'Prod', '1' if self.gui.checkBox_PROD.isChecked() else '0')

            # Schreiben der Änderungen zurück in die INI-Datei
            with open('SQL-master.ini', 'w') as configfile:
                config.write(configfile)


        # Haupt-Widget und Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Erstelle ein QTableWidget
        self.table_widget = QTableWidget()





        instanz_list =[
            ##HV9 TST
            ["F40099DE", "fbaecker", "hilfe44", "E09", "HV9", "TST"],
            ["F40099DE", "fbaecker", "hilfe44", "T43", "HV9", "TST"],
            ["F40099DE", "fbaecker", "hilfe44", "T49", "HV9", "TST"],
            ["F40099DE", "fbaecker", "hilfe44", "T54", "HV9", "TST"],
            ["F40099DE", "fbaecker", "hilfe44", "T51", "HV9", "TST"],
            ["F40099DE", "fbaecker", "hilfe44", "T72", "HV9", "TST"],
            ["F40099DE", "fbaecker", "hilfe44", "T76", "HV9", "TST"],
            ["F40099DE", "fbaecker", "hilfe44", "T78", "HV9", "TST"],

            ##HV7 TEST
            ["F40099DE", "fbaecker", "hilfe44", "T20", "HV7", "TST"],
            ["F40099DE", "fbaecker", "hilfe44", "T22", "HV7", "TST"],
            ["F40099DE", "fbaecker", "hilfe44", "T24", "HV7", "TST"],
            ["F40099DE", "fbaecker", "hilfe44", "T45", "HV7", "TST"],
            ##HV7 PROD
            ["F40001DE", "fbaecker", "hilfe33", "F20", "HV7", "PROD"],
            ["F40001DE", "fbaecker", "hilfe33", "F22", "HV7", "PROD"],
            ["F40009DE", "fbaecker", "hilfe44", "F24", "HV7", "PROD"],
            ["F40007DE", "fbaecker", "hilfe33", "F45", "HV7", "PROD"],
            ##["F40002DE", "fbaecker", "hilfe33", "F37"],
            ##HV8 PROD
            ["F40006DE", "fbaecker", "hilfe44", "F40", "HV8", "PROD"],
            ["F40008DE", "fbaecker", "hilfe44", "F41", "HV8", "PROD"],
            ["F40011DE", "fbaecker", "hilfe55", "F38", "HV8", "PROD"],
            ["F40004DE", "fbaecker", "hilfe33", "F42", "HV8", "PROD"],
            ["F40013DE", "fbaecker", "hilfe44", "F73", "HV8", "PROD"],
            ##HV9 PROD
            ##["FG400FE", "fbaecker", "hilfe33", "F43"],
            ["F40004DE", "fbaecker", "hilfe33", "F49", "HV9", "PROD"],
            ["F40005DE", "fbaecker", "hilfe33", "F64", "HV9", "PROD"],
            ["F40001DE", "fbaecker", "hilfe33", "F51", "HV9", "PROD"],
            ["F40007DE", "fbaecker", "hilfe33", "F54", "HV9", "PROD"],
            ["F40008DE", "fbaecker", "hilfe44", "F55", "HV9", "PROD"],
            ["F40001DE", "fbaecker", "hilfe33", "F56", "HV9", "PROD"],
            ["F40012DE", "fbaecker", "hilfe44", "F68", "HV9", "PROD"],
            ["F40003PL", "fbaecker", "hilfe33", "F69", "HV9", "PROD"],
            ["F40008DE", "fbaecker", "hilfe44", "F72", "HV9", "PROD"],
            ["F40005DE", "fbaecker", "hilfe33", "F74", "HV9", "PROD"],
            ["F40007DE", "fbaecker", "hilfe33", "F76", "HV9", "PROD"]


        ]
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






    # Methode um pro Instanz das SQL-Statement auszuführen am Bildschirm auszugeben
    def sql_pro_instanz(self, sql_statement, host, user, passwort, instanz, layout, nummer, version, art):

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


        # Ab hier werden die die Daten ausgegeben



        # Definieren der Breite und Länge der Tabelle für die Ausabe und Feldnamen setzen
        # Dies wird bei jeder Instanz gemacht, da nicht sicher ist dass bei der ersten Instanz
        # schon etwas gefunden wirdn.

        # Anzahl der Spalten festlegen
        #self.table_widget.setRowCount(len(rows))
        self.table_widget.setRowCount(99999)
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



        # Verbinde den OK-Knopf mit der Methode ok_button_clicked
        self.ok_button.clicked.connect(self.ok_button_clicked)

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



