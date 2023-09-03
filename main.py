from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem,QLineEdit, QCheckBox, QComboBox
from PyQt5.QtCore import Qt
from ui_main import Ui_MainWindow
import sqlite3
import re

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.global_dictionary={"currentTab":3,
                                "tab":
                                [{"tabname":"Deshboard"},
                                 {"tabname":"Stakeholder","query":"SELECT * FROM Stakeholder_View_Summary","tableWidget":self.tableWidget_stk},
                                {"tabname":"Inventory","query":"SELECT * FROM Inventory_View_Summary","tableWidget":self.tableWidget_inv},
                                {"tabname":"Transaction","query":"select * from Transactions_View_Summary","tableWidget":self.tableWidget_transaction},
                                {"tabname":"Admin"}]
                                }
        # Create a dictionary mapping the widgets to their respective column indices
        self.dictionary_stakeholder_enrich_form_via_tableWidget = {
            self.lineEdit_Stk_StakeholderID:0,
            self.lineEdit_Stk_StakeholderName: 1,
            self.lineEdit_Stk_ContactInfo: 2,
            self.checkBox_IsCustomer: 3,
            self.checkBox_IsSupplier: 4,
            self.checkBox_IsEmployee: 5,
            #self.lineEdit_OtherRoles:6,
            self.lineEdit_Stk_AmountPayable:7,
            self.lineEdit_Stk_AmountReceivable:8,
            self.lineEdit_Stk_Notes:9,
            self.lineEdit_Stk_ReminderNote:10,
            self.lineEdit_Stk_ID_ReminderDateTime:11
        }

        self.dictionary_inventory_enrich_form_via_tableWidget={
            self.lineEdit_inv_ItemID:0,
            self.lineEdit_inv_ItemName:1,
            self.lineEdit_inv_Manufacturer:2,
            self.lineEdit_inv_ItemType:3,
            self.lineEdit_inv_ItemDetails:4,
            self.lineEdit_inv_StockCount:5,
            self.lineEdit_inv_ReorderLevel:6,
            self.lineEdit_inv_AssetType:7,
            self.lineEdit_inv_PricePurchaseBasic:8,
            self.lineEdit_inv_PricePurchaseAdd1:9,
            self.lineEdit_inv_PricePurchaseAdd2:10,
            self.lineEdit_inv_PricePurchaseAdd3:11,
            self.lineEdit_inv_PricePurchaseLess1:12,
            self.lineEdit_inv_PricePurchaseLess2:13,
            self.lineEdit_inv_PriceSaleBasic:14,
            self.lineEdit_inv_PriceSaleAdd1:15,
            self.lineEdit_inv_PriceSaleAdd2:16,
            self.lineEdit_inv_PriceSaleLess1:17,
            self.lineEdit_inv_PriceSaleLess2:18
        }

        # Connect the function to the cell click signal
        self.tableWidget_stk.currentCellChanged.connect(lambda: self.enrich_form_via_tableWidget(self.tableWidget_stk, self.dictionary_stakeholder_enrich_form_via_tableWidget))
        self.tableWidget_stk.cellClicked.connect(lambda: self.enrich_form_via_tableWidget(self.tableWidget_stk, self.dictionary_stakeholder_enrich_form_via_tableWidget))
        self.tableWidget_inv.currentCellChanged.connect(lambda: self.enrich_form_via_tableWidget(self.tableWidget_inv, self.dictionary_inventory_enrich_form_via_tableWidget))
        self.tableWidget_inv.cellClicked.connect(lambda: self.enrich_form_via_tableWidget(self.tableWidget_inv, self.dictionary_inventory_enrich_form_via_tableWidget))

        self.tabWidget.currentChanged.connect(self.event_tab_change)

        # For Calculating Net Value
        self.lineEdit_inv_PriceSaleBasic.textChanged.connect(self.update_net_sale_price)
        self.lineEdit_inv_PriceSaleAdd1.textChanged.connect(self.update_net_sale_price)
        self.lineEdit_inv_PriceSaleAdd2.textChanged.connect(self.update_net_sale_price)
        self.lineEdit_inv_PriceSaleAdd3.textChanged.connect(self.update_net_sale_price)
        self.lineEdit_inv_PriceSaleLess1.textChanged.connect(self.update_net_sale_price)
        self.lineEdit_inv_PriceSaleLess2.textChanged.connect(self.update_net_sale_price)

        self.lineEdit_inv_PricePurchaseBasic.textChanged.connect(self.update_net_purchase_price)
        self.lineEdit_inv_PricePurchaseAdd1.textChanged.connect(self.update_net_purchase_price)
        self.lineEdit_inv_PricePurchaseAdd2.textChanged.connect(self.update_net_purchase_price)
        self.lineEdit_inv_PricePurchaseAdd3.textChanged.connect(self.update_net_purchase_price)
        self.lineEdit_inv_PricePurchaseLess1.textChanged.connect(self.update_net_purchase_price)
        self.lineEdit_inv_PricePurchaseLess2.textChanged.connect(self.update_net_purchase_price)

        # search in stakeholder
        self.lineEdit_search_tableWidget_stk.textChanged.connect(lambda: self.search_and_navigate(self.tableWidget_stk, 
                                                                                                  self.lineEdit_search_tableWidget_stk.text()))
        self.pushButton_search_prev_tableWidget_stk.clicked.connect(lambda: self.search_and_navigate(self.tableWidget_stk, direction='prev'))
        self.pushButton_search_next_tableWidget_stk.clicked.connect(lambda: self.search_and_navigate(self.tableWidget_stk, direction='next'))

        # search in inventory
        self.lineEdit_search_tableWidget_inv.textChanged.connect(lambda: self.search_and_navigate(self.tableWidget_inv, 
                                                                                                  self.lineEdit_search_tableWidget_inv.text()))
        self.pushButton_search_prev_tableWidget_inv.clicked.connect(lambda: self.search_and_navigate(self.tableWidget_inv, direction='prev'))
        self.pushButton_search_next_tableWidget_inv.clicked.connect(lambda: self.search_and_navigate(self.tableWidget_inv, direction='next'))


        # Initialize the database connection and move to a Tab
        self.conn = sqlite3.connect("db/sampledb.db")
        self.tabWidget.setCurrentIndex(0)

    def search_and_navigate(self, tableWidget, query=None, direction=None):
        current_search_index = -1

        if query is not None:  # New search query entered
            search_results = []
            for i in range(tableWidget.rowCount()):
                for j in range(tableWidget.columnCount()):
                    item = tableWidget.item(i, j)
                    if item and query.lower() in item.text().lower():
                        search_results.append(i)
                        break  # Exit inner loop as we found a match in this row

            # Store the search_results and current_search_index in the tableWidget object
            tableWidget.search_results = search_results
            tableWidget.current_search_index = current_search_index

        else:  # Retrieve existing search state from tableWidget's attributes
            search_results = getattr(tableWidget, 'search_results', [])
            current_search_index = getattr(tableWidget, 'current_search_index', current_search_index)

        # If there are no search results, update the label and return
        if not search_results:
            self.label_search_status_tableWidget_stk.setText("0/0")
            tableWidget.clearSelection()  # Clear any previous selection
            return

        if direction == 'next':
            current_search_index = (current_search_index + 1) % len(search_results)
        elif direction == 'prev':
            current_search_index = (current_search_index - 1) % len(search_results)

        # Select the row in the tableWidget
        tableWidget.selectRow(search_results[current_search_index])

        # Update the label to show the current search status
        self.label_search_status_tableWidget_stk.setText(f"{current_search_index + 1}/{len(search_results)}")

        # Save the current search state back to the tableWidget's attributes
        tableWidget.current_search_index = current_search_index

    def calc_net_value(self, add_widgets, sub_widgets, net_widget):
        try:
            net_value = 0.0
            for widget in add_widgets:
                net_value += float(widget.text())
            for widget in sub_widgets:
                net_value -= float(widget.text())
            net_widget.setText(str(net_value))
        except ValueError:  # If conversion to float fails
            net_widget.setText("- - -")

    def update_net_sale_price(self):
        add_widgets = [
            self.lineEdit_inv_PriceSaleBasic, 
            self.lineEdit_inv_PriceSaleAdd1, 
            self.lineEdit_inv_PriceSaleAdd2, 
            self.lineEdit_inv_PriceSaleAdd3
        ]
        sub_widgets = [
            self.lineEdit_inv_PriceSaleLess1,
            self.lineEdit_inv_PriceSaleLess2
        ]
        self.calc_net_value(add_widgets, sub_widgets, self.lineEdit_inv__PriceNetSale)

    def update_net_purchase_price(self):
        add_widgets = [
            self.lineEdit_inv_PricePurchaseBasic, 
            self.lineEdit_inv_PricePurchaseAdd1, 
            self.lineEdit_inv_PricePurchaseAdd2, 
            self.lineEdit_inv_PricePurchaseAdd3
        ]
        sub_widgets = [
            self.lineEdit_inv_PricePurchaseLess1,
            self.lineEdit_inv_PricePurchaseLess2
        ]
        self.calc_net_value(add_widgets, sub_widgets, self.lineEdit_inv__PriceNetPurchase)

    def enrich_form_via_tableWidget(self,p_tableWidget, p_dictionary_items):
        selected_items = p_tableWidget.selectedItems()
        if not selected_items:
            return

        selected_row = selected_items[0].row()

        for widget, column_index in p_dictionary_items.items():
            cell_item = p_tableWidget.item(selected_row, column_index)
            if cell_item:
                value = cell_item.text()

                if isinstance(widget, QLineEdit):
                    widget.setText(value)
                elif isinstance(widget, QCheckBox):
                    true_values = ["yes", "1", "ok", "enabled"]
                    widget.setChecked(value.lower() in true_values)
                elif isinstance(widget, QComboBox):
                    index = widget.findText(value)
                    if index != -1:
                        widget.setCurrentIndex(index)

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
