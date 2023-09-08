from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem,QLineEdit, QCheckBox, QComboBox, QTreeWidgetItem
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListView, QCompleter
from PyQt5.QtCore import QStringListModel

from ui_main import Ui_MainWindow
import sqlite3
import re

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.database="db/sample_computer.db"
        self.global_dictionary={"currentTab":3,
                                "tab":
                                [{"tabname":"Deshboard"},
                                 {"tabname":"Stakeholder","query":"SELECT * FROM Stakeholder_View_Summary","tableWidget":self.tableWidget_stk},
                                {"tabname":"Inventory","query":"SELECT * FROM Inventory_View_Summary","tableWidget":self.tableWidget_inv},
                                {"tabname":"Transaction","query":"select * from Transactions_View_Summary","tableWidget":self.tableWidget_transaction},
                                {"tabname":"Admin"}]
                                }
        self.query_insert = '''
            INSERT INTO Inventory (
                ItemID, ItemName, Manufacturer, ItemType, ItemDetails,
                StockCount, ReorderLevel, AssetType, PricePurchaseBasic,
                PricePurchaseAdd1, PricePurchaseAdd2, PricePurchaseAdd3,
                PricePurchaseLess1, PricePurchaseLess2, PriceSaleBasic,
                PriceSaleAdd1, PriceSaleAdd2, PriceSaleAdd3, PriceSaleLess1,
                PriceSaleLess2
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);

                '''
        
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
            self.lineEdit_inv_PriceSaleAdd3:17,
            self.lineEdit_inv_PriceSaleLess1:18,
            self.lineEdit_inv_PriceSaleLess2:19
        }
        
        self.dictionary_trans_enrich_form_via_treeWidget={
            self.lineEdit_trans_sale_timestamp:"Timestamp",
            self.lineEdit_trans_sale_InvoiceNumber:"InvoiceNumber",
            self.lineEdit_trans_sale_StakeholderID:"StakeholderID",
            self.lineEdit_trans_sale_StakeholderName:"StakeholderName",
            self.lineEdit_trans_sale_ItemID:"ItemID",

            self.lineEdit_trans_sale_TransactionType:"TransactionType",
            self.lineEdit_trans_sale_trans_id:"TransactionID",
            self.lineEdit_trans_sale_ItemName:"ItemName",
            
            self.lineEdit_trans_sale_Item_details:"ItemDetails",
            self.lineEdit_trans_sale_quantity:"Quantity",
            self.lineEdit_trans_sale_unit:"QuantityUnit",
            self.lineEdit_trans_sale_rate:"SaleRateNet",
            self.lineEdit_trans_sale_cash:"PaymentCash",
            self.lineEdit_trans_sale_credit:"PaymentCredit"
            #self.lineEdit_trans_sale_schedule,
            #self.lineEdit_trans_sale_terms,
            #self.lineEdit_trans_sale_note
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


        # Evnets to be triggered
        self.lineEdit_search_tableWidget_stk.textChanged.connect(lambda: self.search_and_navigate(self.tableWidget_stk, 
                                                                                                  self.lineEdit_search_tableWidget_stk.text()))
        self.pushButton_search_prev_tableWidget_stk.clicked.connect(lambda: self.search_and_navigate(self.tableWidget_stk, direction='prev'))
        self.pushButton_search_next_tableWidget_stk.clicked.connect(lambda: self.search_and_navigate(self.tableWidget_stk, direction='next'))

        self.lineEdit_search_tableWidget_inv.textChanged.connect(lambda: self.search_and_navigate(self.tableWidget_inv, 
                                                                                                  self.lineEdit_search_tableWidget_inv.text()))
        self.pushButton_search_prev_tableWidget_inv.clicked.connect(lambda: self.search_and_navigate(self.tableWidget_inv, direction='prev'))
        self.pushButton_search_next_tableWidget_inv.clicked.connect(lambda: self.search_and_navigate(self.tableWidget_inv, direction='next'))

        self.pushButton_inv_new.clicked.connect(lambda: self.clearForm(self.dictionary_inventory_enrich_form_via_tableWidget, self.tableWidget_inv))
        self.pushButton_inv_save.clicked.connect(lambda: self.saveForm(self.query_insert, self.dictionary_inventory_enrich_form_via_tableWidget))
        self.pushButton_inv_duplicate.clicked.connect(lambda: self.duplicateForm(self.dictionary_inventory_enrich_form_via_tableWidget, self.tableWidget_inv))
        self.pushButton_inv_delete.clicked.connect(lambda: self.delete_record(self.dictionary_inventory_enrich_form_via_tableWidget, self.tableWidget_inv))

        self.toolBox_trans_SalePurchase.currentChanged.connect(self.page_changed)
        self.treeWidget_trans.currentItemChanged.connect(self.handle_tree_item_click)

        # Initialize the database connection and move to a Tab
        self.conn = sqlite3.connect(self.database)
        self.tabWidget.setCurrentIndex(0)
        self.page_changed(1)
   

    def page_changed(self, index):
        current_widget = self.toolBox_trans_SalePurchase.widget(index)
        if current_widget == self.page_History:
            query = '''
            SELECT
                strftime('%Y-%m-%d', T.Timestamp) AS Timestamp,
                T.InvoiceNumber,
                T.TransactionID,
                T.ItemID,
                T.TransactionType,
                T.StakeholderID,
                S.StakeholderName, 
                I.ItemName,
                T.Quantity, 
                I.PriceSaleBasic+I.PriceSaleAdd1+I.PriceSaleAdd2+I.PriceSaleAdd1-I.PriceSaleLess1-I.PriceSaleLess2 SaleRateNet,
                T.PaymentCash, 
                T.PaymentCredit   
            FROM 
                Transactions T
                LEFT JOIN Stakeholder S ON T.StakeholderID = S.StakeholderID
                LEFT JOIN Inventory I ON T.ItemID = I.ItemID
            ORDER BY Timestamp desc
            '''
            self.make_tree(self.treeWidget_trans, query, self.conn)

    def make_tree(self, p_treeWidget_trans, p_query, p_conn):
        try:
            cursor = p_conn.cursor()
            cursor.execute(p_query)
            results = cursor.fetchall()

            # Clear existing items from the tree widget
            p_treeWidget_trans.clear()

            # Set the column headers
            p_treeWidget_trans.setHeaderLabels([
                "Timestamp/Invoice/TransID", "Transaction Type", "Item ID", "Stk ID", "Stk Name", 
                "Item", "Quantity","Sale Rate Net", "Payment Cash", "Payment Credit"
            ])

            current_timestamp = None
            current_invoice = None
            timestamp_item = None
            invoice_item = None

            for row in results:
                timestamp, invoice_number,transaction_id,item_id, transaction_type, stakeholder_id,stakeholder_name, item_name, quantity, sale_rate_net,payment_cash, payment_credit = row  # Include TransactionID

                if timestamp != current_timestamp:
                    current_timestamp = timestamp
                    timestamp_item = QTreeWidgetItem(p_treeWidget_trans)
                    timestamp_item.setText(0, str(timestamp))

                if invoice_number != current_invoice:
                    current_invoice = invoice_number
                    invoice_item = QTreeWidgetItem(timestamp_item)
                    invoice_item.setText(0, str(invoice_number))

                # Create a child_item for the transaction details
                child_item = QTreeWidgetItem(invoice_item)
                child_item.setText(0, str(transaction_id))  # Use TransactionID here
                child_item.setText(1, transaction_type)
                child_item.setText(2, str(stakeholder_id))
                child_item.setText(3, str(item_id))

                child_item.setText(4, stakeholder_name)
                child_item.setText(5, item_name)
                child_item.setText(6, str(quantity))
                child_item.setText(7,str(sale_rate_net))
                child_item.setText(7, str(payment_cash))
                child_item.setText(8, str(payment_credit))

        except Exception as e:
            print(f"An error occurred: {e}")

    def handle_tree_item_click(self, current_item, previous_item):
        # Initialize an empty list to hold the details
        clicked_details = []
        
        # Traverse up the tree from the clicked item to collect details
        item = current_item
        while item:
            clicked_details.insert(0, item.text(0))
            item = item.parent()

        p_query = f'''
            SELECT
                T.Timestamp,
                T.InvoiceNumber,
                T.TransactionID,
                T.ItemID,
                T.TransactionType,
                T.StakeholderID,
                S.StakeholderName, 
                I.ItemName,
                T.Quantity, 
                T.QuantityUnit,
                I.PriceSaleBasic+I.PriceSaleAdd1+I.PriceSaleAdd2+I.PriceSaleAdd1-I.PriceSaleLess1-I.PriceSaleLess2 SaleRateNet,
                T.PaymentCash, 
                T.PaymentCredit
            FROM 
                Transactions T
                LEFT JOIN Stakeholder S ON T.StakeholderID = S.StakeholderID
                LEFT JOIN Inventory I ON T.ItemID = I.ItemID      
            '''
        # Prepare the query based on the level clicked
        if len(clicked_details) == 2:  # Level 2 (Invoice)
            invoice_number = clicked_details[1]
            p_query = f'''{p_query} 
                WHERE T.InvoiceNumber = '{invoice_number}'       
                '''
            
        elif len(clicked_details) == 3:  # Level 3 (Transaction)
            transaction_id = clicked_details[2]
            p_query = f'''{p_query} 
                WHERE TransactionID = '{transaction_id}'
                '''
        
        else:
            return  # Do nothing for other levels
        
        # Call enrich_form_via_treeWidget to populate the form
        self.enrich_form_via_treeWidget(self.dictionary_trans_enrich_form_via_treeWidget, p_query)

    def enrich_form_via_treeWidget(self, dictionary_trans_enrich_form_via_treeWidget, p_query):
        # Initialize an empty dictionary to hold the data
        data_dict = {}
        
        try:
            # Execute the SQL query
            cursor = self.conn.cursor()
            cursor.execute(p_query)
            result = cursor.fetchall()

            # If no data is returned, return early
            if not result:
                return

            # Get the column names from the cursor description
            column_names = [desc[0] for desc in cursor.description]
            

            # Populate the data dictionary
            for col_name in column_names:
                data_dict[col_name] = []

            for row in result:
                for i, value in enumerate(row):
                    data_dict[column_names[i]].append(value)

            # Populate the QLineEdit fields
            for line_edit, column_name in dictionary_trans_enrich_form_via_treeWidget.items():
                if column_name in data_dict:
                    # Assume the first row of data should be used to populate the form
                    value = data_dict[column_name][0]
                    line_edit.setText(str(value))
                 
                    
                    # self.lineEdit_trans_sale_StakeholderName:"StakeholderName",

        except Exception as e:
            print(f"An error occurred while enriching the form: {e}")

    def delete_record(self, p_dictionary_items, p_tableWidget):
        # Get list of selected items
        selected_items = p_tableWidget.selectedItems()
        
        # Identify unique rows that are selected
        selected_rows = set()
        for item in selected_items:
            selected_rows.add(item.row())
        
        # Sort the row numbers to find the predecessor
        selected_rows = sorted(list(selected_rows))

        # Store the row number of the first selected row's predecessor
        predecessor_row = selected_rows[0] - 1 if selected_rows else -1
        
        # Sort the row numbers in descending order to avoid shifting issues while deleting
        selected_rows = sorted(selected_rows, reverse=True)
        
        # Delete selected rows from the table widget
        for row in selected_rows:
            p_tableWidget.removeRow(row)
            
        # Clear the dictionary items
        for widget in p_dictionary_items.keys():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
                
        # Select the predecessor row in the table widget
        if predecessor_row >= 0:
            p_tableWidget.selectRow(predecessor_row)

    def clearForm(self, p_dictionary_items, p_calcID_from_tableWidget):
        # Find the maximum number of rows in the table widget
        max_rows = p_calcID_from_tableWidget.rowCount()
        
        # Assign this value to the first item in the dictionary
        first_item_key = list(p_dictionary_items.keys())[0]
        first_item_key.setText(str(max_rows + 1))

        # Clear the rest of the items
        for widget in list(p_dictionary_items.keys())[1:]:
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
        #self.enrich_tableWidget_via_form(self.tableWidget_inv, self.dictionary_inventory_enrich_form_via_tableWidget)

    def duplicateForm(self, p_dictionary_items, p_calcID_from_tableWidget):
        # Find the maximum number of rows in the table widget
        max_rows = p_calcID_from_tableWidget.rowCount()
        
        # Assign this value to the first item in the dictionary
        first_item_key = list(p_dictionary_items.keys())[0]
        first_item_key.setText(str(max_rows + 1))
        
        #self.enrich_tableWidget_via_form(self.tableWidget_inv, self.dictionary_inventory_enrich_form_via_tableWidget)

    def saveForm(self, p_query, p_dictionary_items):
        # Fetch the actual values from the widgets
        actual_values = []
        for widget in p_dictionary_items.keys():
            if isinstance(widget, QLineEdit):
                value = f"'{widget.text()}'"
            elif isinstance(widget, QCheckBox):
                value = '1' if widget.isChecked() else '0'
            elif isinstance(widget, QComboBox):
                value = f"'{widget.currentText()}'"
            else:
                value = "Unknown Type"
            actual_values.append(value)
            
        # Debugging lines to check lengths
        placeholders = p_query.split('?')

        if len(placeholders) - 1 != len(actual_values):
            print("Mismatch in the number of placeholders and actual values.")
            print("Number of placeholders:", len(placeholders) - 1)
            print("Number of actual values:", len(actual_values))
            return

        # Replace '?' placeholders with the actual widget values
        updated_query = ''
        for i in range(len(placeholders) - 1):
            updated_query += placeholders[i] + actual_values[i]
        updated_query += placeholders[-1]




    def search_and_navigate(self, tableWidget, query=None, direction=None, Filter=True):
        current_search_index = -1

        if query is not None:  # New search query entered
            search_results = []
            for i in range(tableWidget.rowCount()):
                match_found = False
                for j in range(tableWidget.columnCount()):
                    item = tableWidget.item(i, j)
                    if item and query.lower() in item.text().lower():
                        search_results.append(i)
                        match_found = True
                        break  # Exit inner loop as we found a match in this row
                if Filter:
                    tableWidget.setRowHidden(i, not match_found)
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
            if Filter:
                for i in range(tableWidget.rowCount()):
                    tableWidget.setRowHidden(i, False)
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

    def enrich_tableWidget_via_form(self, p_tableWidget, p_dictionary_items):
        # Initialize a list to hold the new row items
        new_row = []
        
        # Loop through the dictionary to get values from the widgets
        for widget, column_index in p_dictionary_items.items():
            value = ""
            if isinstance(widget, QLineEdit):
                value = widget.text()
            elif isinstance(widget, QCheckBox):
                value = 'Yes' if widget.isChecked() else 'No'
            elif isinstance(widget, QComboBox):
                value = widget.currentText()
            
            new_row.append(QTableWidgetItem(str(value)))
            
        # Insert a new row at the end of the table
        row_position = p_tableWidget.rowCount()
        p_tableWidget.insertRow(row_position)
        
        # Populate the new row with the collected items
        for i, item in enumerate(new_row):
            p_tableWidget.setItem(row_position, i, item)

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