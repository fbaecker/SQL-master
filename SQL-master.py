import sys
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
#
#
# --------------------Version
version = "0.2"
# ---------------------------------


# Globale Variable
sql_input = ''




class MainWindow(QMainWindow):

    global sql_input
    def __init__(self):
        super(MainWindow, self).__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)



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

        # Haupt-Widget und Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Erstelle ein QTableWidget
        self.table_widget = QTableWidget()





        instanz_list =[
            ["F40099DE", "fbaecker", "hilfe33", "T49"],
            ["F40099DE", "fbaecker", "hilfe33", "E09"],
            ["F40099DE", "fbaecker", "hilfe33", "T54"],
            ["F40099DE", "fbaecker", "hilfe33", "T51"],
            #### PROD
            ["F40001DE", "fbaecker", "hilfe33", "F51"],
            ["F40001DE", "fbaecker", "hilfe33", "F56"],
            ##["F40002DE", "fbaecker", "hilfe33", "F37"],
            ["F40004DE", "fbaecker", "hilfe33", "F49"],
            ["F40005DE", "fbaecker", "hilfe33", "F64"],
            ["F40005DE", "fbaecker", "hilfe33", "F74"],
            ["F40006DE", "fbaecker", "hilfe44", "F40"],
            ["F40007DE", "fbaecker", "hilfe33", "F45"],
            ["F40007DE", "fbaecker", "hilfe33", "F54"],
            ["F40008DE", "fbaecker", "hilfe44", "F25"],
            ["F40008DE", "fbaecker", "hilfe44", "F41"],
            ["F40008DE", "fbaecker", "hilfe44", "F55"],
            ["F40009DE", "fbaecker", "hilfe44", "F24"],
            ["F40011DE", "fbaecker", "hilfe55", "F38"],
            ["F40012DE", "fbaecker", "hilfe44", "F68"],
            ["F40013DE", "fbaecker", "hilfe44", "F73"],
            ["F40003PL", "fbaecker", "hilfe33", "F69"]

        ]
        self.zeilen_counter = 0

        print(f' sql_input aus der Eingabe {sql_input}')

        # SQL-Statement analysieren
        table_name = extract_table_name(sql_input)
        print(f'Table name: {table_name}')



        for i, zeile in enumerate(instanz_list):
            # sql_query = f'''
            #                            SELECT *
            #                            from {zeile[3]}DATV7.PFISTAM
            #     '''

            # wenn der Tabellen name identifiziert wurde, die Instanz und die Bibl. noch erweitern
            if table_name:
                # Erstelle den neuen Tabellennamen mit der Instanz
                new_table_name = f"{zeile[3]}DATV7.{table_name}"
                # Ersetze den Tabellennamen im SQL-Statement
                sql_query = re.sub(rf'\b{table_name}\b', new_table_name, sql_input, flags=re.IGNORECASE)
                print(f'SQL-statement nach der Aufbereitung: {sql_query}')


            self.sql_pro_instanz(sql_query,zeile[0],zeile[1],zeile[2], zeile[3], layout, i)





    # Methode um pro Instanz das SQL-Statement auszuführen am Bildschirm auszugeben
    def sql_pro_instanz(self, sql_statement, host, user, passwort, instanz, layout, nummer):

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

        # Nur bei der ersten Abfrage
        if nummer == 0:
            # Anzahl der Spalten festlegen
            #self.table_widget.setRowCount(len(rows))
            self.table_widget.setRowCount(99999)
            self.table_widget.setColumnCount(len(rows[0]) + 1)  # + 1 Feld für die Instanz

            layout.addWidget(self.table_widget)
           

        # Feldnamen aus den Metadaten der Abfrage abrufen
        column_names = ["Instanz"] + [desc[0] for desc in cursor.description]  # Spalte 1 ist die Instanz
        # Feldnamen als Überschrift ausgeben
        self.table_widget.setHorizontalHeaderLabels(column_names)

        # Fülle die Tabelle mit Daten
        for row_idx, row in enumerate(rows):
            self.table_widget.setItem(row_idx+self.zeilen_counter, 0, QTableWidgetItem(instanz))  # Spalte 1 ist die Instanz
            for col_idx, item in enumerate(row, start=1):
                if isinstance(item, Decimal):
                    item = str(item)
                self.table_widget.setItem(row_idx+self.zeilen_counter, col_idx, QTableWidgetItem(item))

        #Zeilen-Counter auf aktuellen Wert setzen für die nächste Instanz
        self.zeilen_counter = self.zeilen_counter+row_idx

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
