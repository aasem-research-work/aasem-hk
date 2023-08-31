from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from ui_main import Ui_MainWindow
import sqlite3


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.global_dictionary={"currentTab":3,
                                "tab":
                                [{"tabname":"Deshboard"},
                                 {"tabname":"Stakeholder","query":"SELECT * FROM Stakeholder_View_Summary","tableWidget":self.tableWidget_party},
                                {"tabname":"Inventory","query":"SELECT * FROM Inventory_View_Summary","tableWidget":self.tableWidget_inventory},
                                {"tabname":"Transaction","query":"select * from Transactions_View_Summary","tableWidget":self.tableWidget_transaction},
                                {"tabname":"Admin"}]
                                }

        self.tabWidget.currentChanged.connect(self.event_tab_change)


        # Initialize the database connection and move to a Tab
        self.conn = sqlite3.connect("db/sampledb.db")
        self.tabWidget.setCurrentIndex(0)
        
    def event_tab_change(self, index):
        current_tab_title = self.tabWidget.tabText(index)
        self.label_Tab_Title.setText(current_tab_title)
        self.global_dictionary["currentTab"] = index

        tabIndex=self.global_dictionary["currentTab"]

        if "query" in self.global_dictionary["tab"][tabIndex]:
            query=self.global_dictionary["tab"][tabIndex]["query"]
            tableWidget=self.global_dictionary["tab"][tabIndex]["tableWidget"]

            self.actionNewRecord.triggered.connect(lambda: self.insert_row_into_table(tableWidget))
            self.actionDeleteRecord.triggered.connect(lambda: self.delete_row_from_table(tableWidget))

            self.load_data_to_tableWidget(query, tableWidget)

    def load_data_to_tableWidget(self, p_query, p_tableWidget, p_param={}):
        try:
            cursor = self.conn.cursor()

            # Execute the query with parameters if provided
            if p_param:
                cursor.execute(p_query, p_param)
            else:
                cursor.execute(p_query)

            result = cursor.fetchall()

            # Fetch column names
            column_names = [description[0] for description in cursor.description]

            # Set the row count based on the number of rows in the result
            p_tableWidget.setRowCount(len(result))

            # Set the column count and headers based on the number of columns in the result
            if result:
                p_tableWidget.setColumnCount(len(result[0]))
                p_tableWidget.setHorizontalHeaderLabels(column_names)

            for row_number, row_data in enumerate(result):
                for column_number, data in enumerate(row_data):
                    p_tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            p_tableWidget.resizeColumnsToContents()


        except Exception as e:
            # Debugging: Print exception
            print("Exception:", e)
  
    def delete_row_from_table(self, p_tableWidget):
        try:
            # Get list of selected items
            selected_items = p_tableWidget.selectedItems()
            
            # Identify unique rows that are selected
            selected_rows = set()
            for item in selected_items:
                selected_rows.add(item.row())
            
            # Sort the row numbers in descending order to avoid shifting issues while deleting
            selected_rows = sorted(list(selected_rows), reverse=True)
            
            # Delete selected rows from the table widget
            for row in selected_rows:
                p_tableWidget.removeRow(row)
                
        except Exception as e:
            # Debugging: Print exception
            print("Exception:", e)

    def insert_row_into_table(self, p_tableWidget):
        try:
            # Get the current number of rows
            current_row_count = p_tableWidget.rowCount()
            
            # Insert a new row at the end
            p_tableWidget.insertRow(current_row_count)

        except Exception as e:
            # Debugging: Print exception
            print("Exception:", e)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
