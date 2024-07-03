import sys
import pyodbc # ODBC


from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox, QTableWidget, \
    QTableWidgetItem, QPlainTextEdit
from PySide6.QtCore import QTimer, QRect
from Qt.main_window import Ui_MainWindow
from decimal import Decimal


#######################################################################################################################
# Releasenotes
#
# 30.06.24  Erste Version

#
#
# --------------------Version
version = "0.1"
# ---------------------------------




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        # SQL Eingabe ausschalten
        #self.gui.plainTextEdit.hide()

        # Verbinde Menüpunkte mit Methoden
        self.gui.actionOpen.triggered.connect(self.open_file)
        self.gui.actionExit.triggered.connect(self.exit)
        self.gui.actionStart.triggered.connect(self.abfrage)
        self.gui.action_ber.triggered.connect(self.show_about)
        self.gui.actionSQL_Eingabe.triggered.connect(self.sql_eingabe)




    def open_file(self):
        self.gui.label.setText("Open File clicked")

    def show_about(self):
        QMessageBox.about(self, "About", "This is a PyQt5/PySide6 application")

    def show_help(self):
        self.gui.label.setText("Help clicked")



    def exit(self):
        exit()

    def sql_eingabe(self):
        #self.table_widget.hide()
        # self.gui.plainTextEdit.show()
        # text = self.gui.plainTextEdit.toPlainText()
        # print(text)

        # Erstelle und zeige ein neues Fenster mit QPlainTextEdit
        self.new_window = NewWindow()
        self.new_window.show()



    def abfrage(self):
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
            ["F40099DE", "fbaecker", "hilfe33", "T54"]

        ]
        self.zeilen_counter = 0

        for i, zeile in enumerate(instanz_list):
            sql_query = f'''
                                       SELECT *
                                       from {zeile[3]}DATV7.PFISTAM
                '''
            self.sql_pro_instanz(sql_query,zeile[0],zeile[1],zeile[2], zeile[3], layout, i)



        return

        # Erstelle die Verbindungszeichenfolge mit f-strings
        conn_str = (f'DRIVER={{IBM i Access ODBC Driver}};'
                    f'SYSTEM={host};'
                    f'UID={user};'
                    f'PWD={password}')

        # Stelle die Verbindung her
        try:
            conn = pyodbc.connect(conn_str)
        except pyodbc.Error as e:
            print(f'Fehler beim Herstellen der Verbindung: {e}')
            QMessageBox.critical(self, "Verbindungsfehler", f"Fehler beim Herstellen der Verbindung: {e}")

            return

        # Erstelle einen Cursor-Objekt
        cursor = conn.cursor()




        sql_query = f'''
                           SELECT *
                           from {instanz}DATV7.PFISTAM
                           

                       '''

        cursor.execute(sql_query)

        # Hole alle Zeilen der Abfrage
        rows = cursor.fetchall()



        # Anzahl der Spalten festlegen
        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(len(rows[0])+1) # + 1 Feld für die Instanz

        layout.addWidget(self.table_widget)




        # Feldnamen aus den Metadaten der Abfrage abrufen
        column_names = ["Instanz"]+[desc[0] for desc in cursor.description] #Spalte 1 ist die Instanz
        # Feldnamen als Überschrift ausgeben
        self.table_widget.setHorizontalHeaderLabels(column_names)





        # Fülle die Tabelle mit Daten
        for row_idx, row in enumerate(rows):
            self.table_widget.setItem(row_idx, 0,QTableWidgetItem(instanz)) # Spalte 1 ist die Instanz
            for col_idx, item in enumerate(row, start=1):
                if isinstance(item, Decimal):
                    item = str(item)
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(item))



        # 2te Abfrage
        instanz = 'T49'

        sql_query = f'''
                              SELECT *
                              from {instanz}DATV7.PFISTAM
                          '''
        cursor.execute(sql_query)

        # Hole alle Zeilen der Abfrage
        rows = cursor.fetchall()


        # Feldnamen aus den Metadaten der Abfrage abrufen
        column_names = ["Instanz"] + [desc[0] for desc in cursor.description]  # Spalte 1 ist die Instanz
        # Feldnamen als Überschrift ausgeben
        self.table_widget.setHorizontalHeaderLabels(column_names)

        # Fülle die Tabelle mit Daten
        for row_idx, row in enumerate(rows):
            self.table_widget.setItem(row_idx, 0, QTableWidgetItem(instanz))  # Spalte 1 ist die Instanz
            for col_idx, item in enumerate(row, start=1):
                if isinstance(item, Decimal):
                    item = str(item)
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(item))

        conn.close()

    # Methode um pro Instanz das SQL-Statement auszuführen am Bildschirm auszugeben
    def sql_pro_instanz(self, sql_statement, host, user, passwort, instanz, layout, nummer):

        print(f' Nummer {nummer} Instanz {instanz} host {host} user {user} passwort {passwort} sql {sql_statement}')
        print(f'Zeilen-Zähler {self.zeilen_counter}')

        # Erstelle die Verbindungszeichenfolge mit f-strings
        conn_str = (f'DRIVER={{IBM i Access ODBC Driver}};'
                    f'SYSTEM={host};'
                    f'UID={user};'
                    f'PWD={passwort}')

        print(f' conn_str={conn_str}')

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
            self.table_widget.setRowCount(100)
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


class NewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Window")

        # Haupt-Widget und Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Erstelle ein QPlainTextEdit-Widget
        plain_text_edit = QPlainTextEdit()
        layout.addWidget(plain_text_edit)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle(f'SQL-Master Version {version}')
    window.show()
    sys.exit(app.exec())
