import PyQt5 
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem,QLineEdit, QCheckBox, QComboBox, QTreeWidgetItem
from PyQt5.QtWidgets import QStatusBar,QMessageBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListView, QCompleter
from PyQt5.QtCore import QStringListModel
import json

from ui_main import Ui_MainWindow
import sqlite3
import re, os

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.current_screen="None"
        self.actionName="None"
        self.database="db/sample_computer.db"
        self.manubar_actions("actionCancel")
        self.global_dictionary={"currentTab":3,
                                "tab":
                                [{"tabname":"Deshboard"},
                                 {"tabname":"Stakeholder","query":"SELECT * FROM Stakeholder_View_Summary","tableWidget":self.tableWidget_stk},
                                {"tabname":"Inventory","query":"SELECT * FROM Inventory_View_Summary","tableWidget":self.tableWidget_inv},
                                {"tabname":"Transaction","query":"select * from Transactions_View_Summary","tableWidget":self.tableWidget_transaction},
                                {"tabname":"Admin"}]
                                }
        self.query_insert_inv = '''
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
        self.query_insert_stk = '''
            INSERT INTO Stakeholder (
                            StakeholderID, StakeholderName,ContactInfo,
                            IsCustomer,IsSupplier,IsEmployee,
                            AmountPayable,AmountReceivable,Notes,
                            ReminderNote, ReminderDateTime
                        )
                        VALUES (?,?,?,?,?,?, ?,?,?,?,? );


                '''
                
        # Model for Stakeholder
        self.model_stakeholder = {
            'table': 'stakeholder',
            'screen': 'stakeholder',
            'data': [
                {
                    'StakeholderID': self.lineEdit_Stk_StakeholderID,
                    'StakeholderName': self.lineEdit_Stk_StakeholderName,
                    'ContactInfo': self.lineEdit_Stk_ContactInfo,
                    'IsCustomer': self.checkBox_IsCustomer,
                    'IsSupplier': self.checkBox_IsSupplier,
                    'IsEmployee': self.checkBox_IsEmployee,
                    'OtherRoles': "None",
                    'AmountPayable': self.lineEdit_Stk_AmountPayable,
                    'AmountReceivable': self.lineEdit_Stk_AmountReceivable,
                    'Notes': self.lineEdit_Stk_Notes,
                    'ReminderNote': self.lineEdit_Stk_ReminderNote,
                    'ReminderDateTime': self.lineEdit_Stk_ID_ReminderDateTime,
                    'ReminderScript': "None"
                }
                # Add more instances as needed
            ]
        }
        self.lock_for_edit(self.model_stakeholder, True)
        # Model for Inventory
        self.model_inventory = {
            'table': 'inventory',
            'screen': 'inventory',
            'data': [
                {
                    'ItemID': self.lineEdit_inv_ItemID,
                    'ItemName': self.lineEdit_inv_ItemName,
                    'Manufacturer': self.lineEdit_inv_Manufacturer,
                    'ItemType': self.lineEdit_inv_ItemType,
                    'ItemDetails': self.lineEdit_inv_ItemDetails,
                    'StockCount': self.lineEdit_inv_StockCount,
                    'ReorderLevel': self.lineEdit_inv_ReorderLevel,
                    'AssetType': self.lineEdit_inv_AssetType,
                    'PricePurchaseBasic': self.lineEdit_inv_PricePurchaseBasic,
                    'PricePurchaseAdd1': self.lineEdit_inv_PricePurchaseAdd1,
                    'PricePurchaseAdd2': self.lineEdit_inv_PricePurchaseAdd2,
                    'PricePurchaseAdd3': self.lineEdit_inv_PricePurchaseAdd3,
                    'PricePurchaseLess1': self.lineEdit_inv_PricePurchaseLess1,
                    'PricePurchaseLess2': self.lineEdit_inv_PricePurchaseLess1,
                    'PriceSaleBasic': self.lineEdit_inv_PriceSaleBasic,
                    'PriceSaleAdd1': self.lineEdit_inv_PriceSaleAdd1,
                    'PriceSaleAdd2': self.lineEdit_inv_PriceSaleAdd2,
                    'PriceSaleAdd3': self.lineEdit_inv_PriceSaleAdd3,
                    'PriceSaleLess1': self.lineEdit_inv_PriceSaleLess1,
                    'PriceSaleLess2': self.lineEdit_inv_PriceSaleLess2
                }
                # Add more instances as needed
            ]
        }  
        self.lock_for_edit(self.model_inventory, True)

        # Model for Transaction
        self.model_transaction = {
            'table': 'transaction',
            'screen': 'transaction',
            'data': [
                {
                    'InvoiceNumber': self.lineEdit_trans_sale_InvoiceNumber,
                    'Timestamp': self.lineEdit_trans_sale_timestamp,
                    'TransactionID': self.lineEdit_trans_sale_trans_id,
                    'TransactionType': self.lineEdit_trans_sale_TransactionType,
                    'TransactionCategory': "Retail",
                    'UserID': "Admin",
                    'StakeholderID': self.lineEdit_trans_sale_StakeholderID,
                    'ItemID': self.lineEdit_trans_sale_ItemID,
                    'ItemDetails': self.lineEdit_trans_sale_Item_details,
                    'Quantity': self.lineEdit_trans_sale_quantity,
                    'QuantityUnit': self.lineEdit_trans_sale_unit,
                    'PaymentCash': self.lineEdit_trans_sale_cash,
                    'PaymentCredit': self.lineEdit_trans_sale_credit,
                    'PaymentCreditSchedule': self.lineEdit_trans_sale_schedule,
                    'PaymentCreditTerms': self.lineEdit_trans_sale_terms,
                    'Notes': self.lineEdit_trans_sale_notes
                }
                # Add more instances as needed
            ]
        }
        #self.lock_for_edit(self.model_transaction, True)
       
       
        # Create a dictionary mapping the widgets to their respective column indices

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

        self.dictionary_stakeholder_enrich_form_via_tableWidget = {
            
            self.lineEdit_Stk_StakeholderID:0,
            self.lineEdit_Stk_StakeholderName: 1,
            self.lineEdit_Stk_ContactInfo: 2,
            self.checkBox_IsCustomer: 3,
            self.checkBox_IsSupplier: 4,
            self.checkBox_IsEmployee: 5,
            
            self.lineEdit_Stk_AmountPayable:6,
            self.lineEdit_Stk_AmountReceivable:7,
            self.lineEdit_Stk_Notes:8,
            self.lineEdit_Stk_ReminderNote:9,
            self.lineEdit_Stk_ID_ReminderDateTime:10
         
        }


        self.dictionary_invoice_live={
            "key_timestamp":"Timestamp",
            "key_InvoiceNumber":"InvoiceNumber",
            "key_StakeholderID":"StakeholderID",
            "key_StakeholderName":"StakeholderName",
            "transactions":[{
            "key_ItemID":"ItemID",

            "key_TransactionType":"TransactionType",
            "key_trans_id":"TransactionID",
            "key_ItemName":"ItemName",
            
            "key_Item_details":"ItemDetails",
            "key_quantity":"Quantity",
            "key_unit":"QuantityUnit",
            "key_rate":"SaleRateNet",
            "key_cash":"PaymentCash",
            "key_credit":"PaymentCredit"
            #key_schedule,
            #key_terms,
            #key_note
           }]
        }
        # Manu-bar
        self.actionNewRecord.triggered.connect(lambda: self.manubar_actions("actionNewRecord"))
        self.actionDuplicateRecord.triggered.connect(lambda: self.manubar_actions("actionDuplicateRecord"))

        self.actionEdit.triggered.connect(lambda: self.manubar_actions("actionEdit"))
        self.actionSave.triggered.connect(lambda: self.manubar_actions("actionSave"))
        self.actionCancel.triggered.connect(lambda: self.manubar_actions("actionCancel"))
        self.actionLoadDraft.triggered.connect(lambda: self.manubar_actions("actionLoadDraft"))

        self.actionFilterRecord.triggered.connect(lambda: self.manubar_actions("actionFilterRecord"))

        self.actionDeleteRecord.triggered.connect(lambda: self.manubar_actions("actionDeleteRecord"))
        self.actionRollback.triggered.connect(lambda: self.manubar_actions("actionRollback"))
        self.actionCommit.triggered.connect(lambda: self.manubar_actions("actionCommit"))
      

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

        self.lineEdit_trans_sale_StakeholderID.textChanged.connect(lambda: self.copy_value(self.lineEdit_trans_sale_StakeholderName, self.lineEdit_filter_trans))

        self.tableWidget_trans_list.selectionModel().currentRowChanged.connect(lambda: self.helloworld(self.tableWidget_trans_list))
        #self.tableWidget_invoice.selectionModel().currentRowChanged.connect(lambda: self.helloworld(self.tableWidget_invoice))


        #self.toolBox_trans_SalePurchase.currentChanged.connect(self.page_changed)
        self.treeWidget_trans.currentItemChanged.connect(self.handle_tree_item_click)

        self.lineEdit_trans_sale_InvoiceNumber.textChanged.connect(self.on_Invoice_Value_Change)


        # Initialize the database connection and move to a Tab
        self.conn = sqlite3.connect(self.database)
        self.tabWidget.setCurrentIndex(0)
        self.current_screen=self.tabWidget.tabText(0)
        self.page_changed(1)
   
    def on_Invoice_Value_Change(self):
        # Get the value from lineEdit_trans_sale_InvoiceNumber, trim and convert to uppercase
        currentInvoiceNumber = self.lineEdit_trans_sale_InvoiceNumber.text().strip().upper()
        
        # SQL query to fetch records based on currentInvoiceNumber
        p_query = '''
            SELECT
                T.ItemID,
                I.ItemName,
                T.Quantity, 
                I.PriceSaleBasic+I.PriceSaleAdd1+I.PriceSaleAdd2+I.PriceSaleAdd1-I.PriceSaleLess1-I.PriceSaleLess2 SaleRateNet,
                T.PaymentCash, 
                T.PaymentCredit,
                T.TransactionType Account,
                T.TransactionID TID   
            FROM 
                Transactions T
                LEFT JOIN Inventory I ON T.ItemID = I.ItemID
            WHERE T.InvoiceNumber=?
            ORDER BY Timestamp desc
        '''
        p_param = (currentInvoiceNumber, )  # Query parameters
        
        # Execute the query and fetch results
        cursor = self.conn.cursor()
        cursor.execute(p_query, p_param)
        results = cursor.fetchall()
        
        # Update the status bar and tableWidget based on fetched records
        if not results:
            self.statusBar().showMessage(f"No records found for Invoice {currentInvoiceNumber}")
        else:
            self.statusBar().showMessage(f"{len(results)} records found for the invoice {currentInvoiceNumber}")
            self.load_data_to_tableWidget(p_query, self.tableWidget_trans_list, p_param)

            invNumber=currentInvoiceNumber #self.lineEdit_trans_sale_InvoiceNumber.text()
            self.preview_Invoice_create( invNumber, 'tmp_trans.htm')
            self.preview_Invoice_live(self.textBrowser_InvoicePreview, 'tmp_trans.htm')
                
    def helloworld(self, p_tableWidget):
        # Initialize an empty dictionary to hold the data
        data_dict = {}

        # Get the current row and fetch the TransactionID from the column named "TID"
        current_row = p_tableWidget.currentRow()
        transaction_id_item = p_tableWidget.item(current_row, p_tableWidget.columnCount() - 1)  # Assuming TID is in the last column
        if transaction_id_item is not None:
            transaction_id = transaction_id_item.text()
        else:
            print("No row selected.")
            return

        # Define the query using the fetched TransactionID
        p_query = '''
        SELECT
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
        WHERE T.TransactionID = ?
        ORDER BY Timestamp desc
        '''

        # Dictionary for QLineEdit fields
        dictionary_trans_enrich_form = {
            self.lineEdit_trans_sale_timestamp: "Timestamp",
            self.lineEdit_trans_sale_InvoiceNumber: "InvoiceNumber",
            self.lineEdit_trans_sale_StakeholderID: "StakeholderID",
            self.lineEdit_trans_sale_StakeholderName: "StakeholderName",
            self.lineEdit_trans_sale_ItemID: "ItemID",
            self.lineEdit_trans_sale_TransactionType: "TransactionType",
            self.lineEdit_trans_sale_trans_id: "TransactionID",
            self.lineEdit_trans_sale_ItemName: "ItemName",
            self.lineEdit_trans_sale_Item_details: "ItemDetails",
            self.lineEdit_trans_sale_quantity: "Quantity",
            self.lineEdit_trans_sale_unit: "QuantityUnit",
            self.lineEdit_trans_sale_rate: "SaleRateNet",
            self.lineEdit_trans_sale_cash: "PaymentCash",
            self.lineEdit_trans_sale_credit: "PaymentCredit"
        }

        try:
            # Execute the SQL query
            cursor = self.conn.cursor()
            cursor.execute(p_query, (transaction_id,))
            result = cursor.fetchall()

            # If no data is returned, return early
            if not result:
                print("No records found.")
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
            for line_edit, column_name in dictionary_trans_enrich_form.items():
                if column_name in data_dict:
                    # Assume the first row of data should be used to populate the form
                    value = data_dict[column_name][0]
                    line_edit.setText(str(value))

        except Exception as e:
            print(f"An error occurred while enriching the form: {e}")



    def copy_value(self, source_Widget, target_Widget):
        # Initialize variable to hold the source value
        source_value = None

        # Check the type of source_Widget and retrieve its value accordingly
        if isinstance(source_Widget, QLineEdit):
            source_value = source_Widget.text()
        elif isinstance(source_Widget, QLabel):
            source_value = source_Widget.text()
        # Add more widget types here if needed

        # If source_value is None, it means the widget type is not supported
        if source_value is None:
            print("Unsupported source widget type.")
            return

        # Check the type of target_Widget and set its value accordingly
        if isinstance(target_Widget, QLineEdit):
            target_Widget.setText(source_value)
        elif isinstance(target_Widget, QLabel):
            target_Widget.setText(source_value)
        # Add more widget types here if needed
        else:
            print("Unsupported target widget type.")


    def page_changed(self, index):
        #current_widget = self.toolBox_trans_SalePurchase.widget(index)
        if True: # current_widget == self.page_History:
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
        print (updated_query)


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
        self.current_screen=self.tabWidget.tabText(index)
        self.label_Tab_Title.setText(current_tab_title)
        self.global_dictionary["currentTab"] = index

        tabIndex=self.global_dictionary["currentTab"]

        if "query" in self.global_dictionary["tab"][tabIndex]:
            query=self.global_dictionary["tab"][tabIndex]["query"]
            tableWidget=self.global_dictionary["tab"][tabIndex]["tableWidget"]
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


    def create_invoice_live(self, p_dictionary_items_source, p_dictionary_items_target):
        # Assuming p_dictionary_items_target has a 'transactions' key that contains a list
        if 'transactions' not in p_dictionary_items_target:
            p_dictionary_items_target['transactions'] = []
        
        # Extract parent keys
        parent_keys = ['Timestamp', 'InvoiceNumber', 'StakeholderID', 'StakeholderName']
        
        # Check if parent keys are different
        parent_keys_different = False
        for key, value in p_dictionary_items_source.items():
            if value in parent_keys:
                target_key = f"key_{value}"
                if target_key in p_dictionary_items_target and p_dictionary_items_target[target_key] != key.text():
                    parent_keys_different = True
                    break
                    
        # If parent keys are different, reset the transactions list
        if parent_keys_different:
            p_dictionary_items_target['transactions'] = []
        
        # Update the parent keys
        for key, value in p_dictionary_items_source.items():
            if value in parent_keys:
                p_dictionary_items_target[f"key_{value}"] = key.text()
        
        # Prepare a transaction dictionary
        transaction = {}
        for key, value in p_dictionary_items_source.items():
            if value not in parent_keys:
                transaction[f"key_{value}"] = key.text()
        
        # Append the transaction to the 'transactions' list
        p_dictionary_items_target['transactions'].append(transaction)

    def update_live_invoice(self, p_invoice_data, p_dictionary_common_items, p_table):
        # Update common items
        for label_widget, key in p_dictionary_common_items.items():
            if key in p_invoice_data:
                label_widget.setText(str(p_invoice_data[key]))
        
        # Assuming p_table is a QTableWidget, clear it for new data
        p_table.setRowCount(0)


    # The lock_for_edit function
    def lock_for_edit(self, p_dictionary, p_mode=True):
        try:
            # Access the data key in the dictionary which holds another dictionary of widget names and their instances
            data_list = p_dictionary.get('data', [])
            
            if not data_list:
                print("No data found in the provided dictionary.")
                return
            
            # Loop through the data dictionary to get the widget instances
            for data_dict in data_list:
                for key, widget in data_dict.items():
                    #print(f"Debug: Processing key {key}, widget {widget}")
                    
                    # Check if the widget has a setReadOnly method (i.e., it's an input widget like QLineEdit)
                    if hasattr(widget, 'setReadOnly'):
                        widget.setReadOnly(p_mode)
                    elif isinstance(widget, PyQt5.QtWidgets.QCheckBox):
                        widget.setEnabled(not p_mode)
                    else:
                        print(f"Warning: The widget for key {key} doesn't support locking for edit.")
        
        except Exception as e:
            print(f"An error occurred: {e}")






    def dbAction_execute(self, p_file, p_conn):
        try:
            # Read the SQL file to get the SQL query
            with open(p_file, 'r') as file:
                sql_query = file.read().strip()  # Remove leading/trailing whitespace

            if not sql_query:
                return -1, "No command found to execute."

            # Execute the SQL query
            cursor = p_conn.cursor()
            cursor.execute(sql_query)
            
            return 1, "SQL query executed successfully."
            
        except FileNotFoundError:
            return -1, "SQL file not found."
        except sqlite3.IntegrityError as e:
            return -1, f"Integrity Error: {e}"
        except Exception as e:
            return -1, f"An error occurred while executing SQL: {e}"


    def dbAction_commit(self, p_conn=None):
        try:
            # Commit all the changes made so far
            p_conn.commit()
            print("All changes committed successfully.")
            return "Commit successful."
            
        except Exception as e:
            print(f"An error occurred while committing: {e}")
            return f"Commit failed: {e}"

    def dbAction_rollback(self, p_conn=None):
        try:
            # Roll back all the changes made so far
            p_conn.rollback()
            print("All changes rolled back successfully.")
            return "Rollback successful."
            
        except Exception as e:
            print(f"An error occurred while rolling back: {e}")
            return f"Rollback failed: {e}"

    def show_message(self, p_title, p_message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(p_title)
        msg.setText(p_message)
        msg.exec_()

    def menuController(self, p_action):
        # Create a dictionary mapping actions to the menu items they should enable or disable
        menuDict = {
            "actionNewRecord": {
                "enable": ["actionLoadDraft", "actionSave", "actionCancel", "actionRollback", "actionCommit"],
                "disable": ["actionNewRecord", "actionDuplicateRecord", "actionFilterRecord", "actionDeleteRecord", "actionEdit"]
            },
            "actionDuplicateRecord": {
                "enable": ["actionLoadDraft", "actionSave", "actionCancel", "actionRollback", "actionCommit"],
                "disable": ["actionNewRecord", "actionDuplicateRecord", "actionFilterRecord", "actionDeleteRecord", "actionEdit"]
            },
            "actionEdit": {
                "enable": ["actionLoadDraft", "actionSave", "actionCancel", "actionRollback", "actionCommit"],
                "disable": ["actionNewRecord", "actionDuplicateRecord", "actionFilterRecord", "actionDeleteRecord", "actionEdit"]
            },
            "actionLoadDraft": {
                "enable": ["actionLoadDraft", "actionSave", "actionCancel", "actionRollback", "actionCommit"],
                "disable": ["actionNewRecord", "actionDuplicateRecord", "actionFilterRecord", "actionDeleteRecord", "actionEdit"]
            },
            "actionSave": {
                "enable": ["actionNewRecord", "actionDuplicateRecord", "actionFilterRecord", "actionDeleteRecord", "actionLoadDraft", "actionEdit", "actionRollback", "actionCommit"],
                "disable": ["actionSave", "actionCancel"]
            },
            "actionCancel": {
                "enable": ["actionNewRecord", "actionDuplicateRecord", "actionFilterRecord", "actionDeleteRecord", "actionLoadDraft", "actionEdit", "actionRollback", "actionCommit"],
                "disable": ["actionSave", "actionCancel"]
            },
            "actionCommit": {
                "enable": ["actionNewRecord", "actionDuplicateRecord", "actionFilterRecord", "actionDeleteRecord", "actionLoadDraft", "actionEdit", "actionRollback", "actionCommit"],
                "disable": ["actionSave", "actionCancel"]
            },
            "actionRollback": {
                "enable": ["actionNewRecord", "actionDuplicateRecord", "actionFilterRecord", "actionDeleteRecord", "actionLoadDraft", "actionEdit", "actionRollback", "actionCommit"],
                "disable": ["actionSave", "actionCancel"]
            },
            "actionDeleteRecord": {
                "enable": ["actionLoadDraft", "actionSave", "actionCancel", "actionRollback", "actionCommit", "actionNewRecord", "actionDuplicateRecord", "actionFilterRecord", "actionDeleteRecord", "actionEdit"],
                "disable": []
            }
        }

        # Check if the provided p_action exists in menuDict
        if p_action in menuDict:
            # Enable the necessary actions
            for action in menuDict[p_action]["enable"]:
                getattr(self, action).setEnabled(True)
            # Disable the necessary actions
            for action in menuDict[p_action]["disable"]:
                getattr(self, action).setEnabled(False)
        else:
            print(f"Action {p_action} not found in menuDict.")

    def manubar_actions(self, p_actionName):

        print (self.current_screen,"->",p_actionName)
        self.menuController(p_actionName)

        if p_actionName=="actionCommit":
            self.dbAction_commit(self.conn)
            self.lockEdit(self.dictionary_inventory_enrich_form_via_tableWidget, self.tableWidget_inv)

            

        elif p_actionName=="actionRollback":
            self.actionName=p_actionName
            self.dbAction_rollback(self.conn)
            

        if self.current_screen=="Inventory":
            self.model_inventory = {
                'table': 'inventory',
                'screen': 'inventory',
                'data': [
                    {
                        'ItemID': self.lineEdit_inv_ItemID,
                        'ItemName': self.lineEdit_inv_ItemName,
                        'Manufacturer': self.lineEdit_inv_Manufacturer,
                        'ItemType': self.lineEdit_inv_ItemType,
                        'ItemDetails': self.lineEdit_inv_ItemDetails,
                        'StockCount': self.lineEdit_inv_StockCount,
                        'ReorderLevel': self.lineEdit_inv_ReorderLevel,
                        'AssetType': self.lineEdit_inv_AssetType,
                        'PricePurchaseBasic': self.lineEdit_inv_PricePurchaseBasic,
                        'PricePurchaseAdd1': self.lineEdit_inv_PricePurchaseAdd1,
                        'PricePurchaseAdd2': self.lineEdit_inv_PricePurchaseAdd2,
                        'PricePurchaseAdd3': self.lineEdit_inv_PricePurchaseAdd3,
                        'PricePurchaseLess1': self.lineEdit_inv_PricePurchaseLess1,
                        'PricePurchaseLess2': self.lineEdit_inv_PricePurchaseLess1,
                        'PriceSaleBasic': self.lineEdit_inv_PriceSaleBasic,
                        'PriceSaleAdd1': self.lineEdit_inv_PriceSaleAdd1,
                        'PriceSaleAdd2': self.lineEdit_inv_PriceSaleAdd2,
                        'PriceSaleAdd3': self.lineEdit_inv_PriceSaleAdd3,
                        'PriceSaleLess1': self.lineEdit_inv_PriceSaleLess1,
                        'PriceSaleLess2': self.lineEdit_inv_PriceSaleLess2
                    }
                    # Add more instances as needed
                ]
            }
            if p_actionName=="actionNewRecord":
                self.actionName=p_actionName
                self.clearForm(self.dictionary_inventory_enrich_form_via_tableWidget, self.tableWidget_inv)
                self.lock_for_edit(self.model_inventory, p_mode=False)
            if p_actionName=="actionDuplicateRecord":
                self.actionName=p_actionName
                self.duplicateForm(self.dictionary_inventory_enrich_form_via_tableWidget, self.tableWidget_inv)
                self.lock_for_edit(self.model_inventory, p_mode=False)
            if p_actionName=="actionEdit":
                self.actionName=p_actionName
                self.lock_for_edit(self.model_inventory, p_mode=False)
            if p_actionName=="actionDeleteRecord":
                self.actionName=p_actionName
                self.delete_record(self.dictionary_inventory_enrich_form_via_tableWidget, self.tableWidget_inv)
            if p_actionName=="actionLoadDraft":
                self.actionName=p_actionName
                self.lock_for_edit(self.model_inventory, p_mode=False)
                self.dbAction_load_from_json(self.model_inventory, "tmp_model_inventory.json")
            if p_actionName=="actionCancel":
                self.actionName=p_actionName
                self.lock_for_edit(self.model_inventory, p_mode=True)

            if p_actionName=="actionSave":
                self.actionName=p_actionName
                #self.saveForm(self.query_insert_inv, self.dictionary_inventory_enrich_form_via_tableWidget)
                self.dbAction_dump_in_json(self.model_inventory , "tmp_model_inventory.json")
                self.dbAction_json_to_sql('tmp_model_inventory.json', p_dml="insert")
                status, message = self.dbAction_execute('tmp_to_execute.sql', self.conn)
                if status < 0:
                    self.show_message("Not Saved", message)
                    self.lock_for_edit(self.model_inventory, p_mode=False)
                else:
                    self.statusBar().showMessage(message)
                    #self.lock_for_edit(self.model_stakeholder, p_mode=True)
                    self.lock_for_edit(self.model_inventory, p_mode=True)

            if p_actionName=="actionFilterRecord":
                self.actionName=p_actionName
                self.lock_for_edit(self.model_inventory, p_mode=True)

        elif self.current_screen=="Stakeholder":
            self.model_stakeholder = {
                'table': 'stakeholder',
                'screen': 'stakeholder',
                'data': [
                    {
                        'StakeholderID': self.lineEdit_Stk_StakeholderID,
                        'StakeholderName': self.lineEdit_Stk_StakeholderName,
                        'ContactInfo': self.lineEdit_Stk_ContactInfo,
                        'IsCustomer': self.checkBox_IsCustomer,
                        'IsSupplier': self.checkBox_IsSupplier,
                        'IsEmployee': self.checkBox_IsEmployee,
                        'OtherRoles': "None",
                        'AmountPayable': self.lineEdit_Stk_AmountPayable,
                        'AmountReceivable': self.lineEdit_Stk_AmountReceivable,
                        'Notes': self.lineEdit_Stk_Notes,
                        'ReminderNote': self.lineEdit_Stk_ReminderNote,
                        'ReminderDateTime': self.lineEdit_Stk_ID_ReminderDateTime,
                        'ReminderScript': "None"
                    }
                    # Add more instances as needed
                ]
            }            
            if p_actionName=="actionNewRecord":
                self.actionName=p_actionName
                self.clearForm(self.dictionary_stakeholder_enrich_form_via_tableWidget, self.tableWidget_stk)
                self.lock_for_edit(self.model_stakeholder, p_mode=False)
            if p_actionName=="actionDuplicateRecord":
                self.actionName=p_actionName
                self.duplicateForm(self.dictionary_stakeholder_enrich_form_via_tableWidget, self.tableWidget_stk)
                self.lock_for_edit(self.model_stakeholder, p_mode=False)
            if p_actionName=="actionEdit":
                self.actionName=p_actionName
                self.lock_for_edit(self.model_stakeholder, p_mode=False)
            if p_actionName=="actionDeleteRecord":
                self.actionName=p_actionName
                self.delete_record(self.dictionary_stakeholder_enrich_form_via_tableWidget, self.tableWidget_stk)
                self.lock_for_edit(self.model_stakeholder, p_mode=True)
            if p_actionName=="actionLoadDraft":
                self.actionName=p_actionName
                print ("loading draft-Stakeholder")
                self.dbAction_load_from_json(self.model_stakeholder, "tmp_model_stakeholder.json")
                self.lock_for_edit(self.model_stakeholder, p_mode=False)
            if p_actionName=="actionCancel":
                self.actionName=p_actionName
                self.lock_for_edit(self.model_stakeholder, p_mode=True)
            if p_actionName=="actionSave":
                self.actionName=p_actionName
                #self.saveForm(self.query_insert_stk, self.dictionary_stakeholder_enrich_form_via_tableWidget)      
                self.dbAction_dump_in_json(self.model_stakeholder , "tmp_model_stakeholder.json")
                self.dbAction_json_to_sql('tmp_model_stakeholder.json', p_dml="insert")
       
                status, message = self.dbAction_execute('tmp_to_execute.sql', self.conn)
                if status < 0:
                    self.show_message("Not Saved", message)
                    self.lock_for_edit(self.model_stakeholder, p_mode=False)
                else:
                    self.statusBar().showMessage(message)  
                    self.lock_for_edit(self.model_stakeholder, p_mode=True)              
                
            if p_actionName=="actionFilterRecord":
                self.actionName=p_actionName
                self.lock_for_edit(self.model_stakeholder, p_mode=True)

        elif self.current_screen=="Transaction":
            self.actionName=p_actionName
            if p_actionName=="actionLoadDraft":
                print ("loading draft-transactoin")
            if p_actionName=="actionSave":
                invNumber=self.lineEdit_trans_sale_InvoiceNumber.text()
                self.preview_Invoice_create( invNumber, 'tmp_trans.htm')
                self.preview_Invoice_live(self.textBrowser_InvoicePreview, 'tmp_trans.htm')
        self.statusBar().showMessage(f"Action called: {self.actionName}")


    def dbAction_json_to_sql(self, p_file, p_dml="insert", p_param={}, p_sql_file='tmp_to_execute.sql'):
        try:
            # Read the JSON file
            with open(p_file, 'r') as file:
                json_data = json.load(file)
            
            table = json_data.get('table')
            data = json_data.get('data')[0]  # assuming one record for simplicity

            # Generate SQL query based on the DML type
            if p_dml == "insert":
                columns = ", ".join(data.keys())
                values = ", ".join([f"'{val}'" for val in data.values()])
                sql_query = f"INSERT INTO {table} ({columns}) VALUES ({values});"

            elif p_dml == "delete":
                where_clause = " AND ".join([f"{key} = '{value}'" for key, value in p_param.items()])
                sql_query = f"DELETE FROM {table} WHERE {where_clause};"

            elif p_dml == "update":
                set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
                where_clause = " AND ".join([f"{key} = '{value}'" for key, value in p_param.items()])
                sql_query = f"UPDATE {table} SET {set_clause} WHERE {where_clause};"

            else:
                return "Unsupported DML operation."

            # Save the SQL query to a SQL file
            with open(p_sql_file, 'w') as sql_file:
                sql_file.write(sql_query)

            print(sql_query)
            return sql_query

        except Exception as e:
            return f"An error occurred: {e}"


    def preview_Invoice_live(self, p_textBrowser, p_file):
        try:
            with open(p_file, 'r', encoding='utf-8') as f:
                content = f.read()
            #p_textBrowser.setPlainText(content)  # For plain text
            p_textBrowser.setHtml(content)  # For HTML content
        except FileNotFoundError:
            print(f"File {p_file} not found.")
        except Exception as e:
            print(f"An error occurred while previewing the invoice: {e}")


    def preview_Invoice_create(self, p_invoicenumber, p_file):
        try:
            # Connect to the database
            cursor = self.conn.cursor()

            # Execute the query
            cursor.execute("""
                SELECT
                    T.InvoiceNumber, 
                    T.TransactionID, 
                    T.TransactionType, 
                    T.TransactionCategory, 
                    T.UserID,
                    T.StakeholderID, S.StakeholderName, S.ContactInfo, 
                    T.ItemID, I.ItemName, I.ItemType, 
                    T.Quantity, 
                    T.PaymentCash, 
                    T.PaymentCredit, 
                    T.PaymentCreditSchedule,
                    T.PaymentCreditTerms,
                    T.Timestamp,
                    T.Notes
                FROM 
                    Transactions T
                    LEFT JOIN Stakeholder S ON T.StakeholderID = S.StakeholderID
                    LEFT JOIN Inventory I ON T.ItemID = I.ItemID
                WHERE T.InvoiceNumber=?
            """, (p_invoicenumber,))

            results = cursor.fetchall()

            if results:
                # Create the HTML content
                header_content = f"""
                    <p> <b>Invoice:</b><u> {results[0][0]}</u></p>
                    <p> <b> Date: </b><u> {results[0][16]}</u></p>
                    <p> <b> Customer:</b><u> {results[0][6]}</u></p>
                    <p>Contact: <u>{results[0][7]}</u></p>
                """

                table_content = "<table border='1'>"
                table_content += "<tr><th>ID</th><th>Item Name</th><th>Type</th><th>Quantity</th><th>Cash</th><th>Credit</th></tr>"

                for row in results:
                    table_content += f"<tr><td>{row[8]}</td><td>{row[9]}</td><td>{row[10]}</td><td>{row[11]}</td><td>{row[12]}</td><td>{row[13]}</td></tr>"

                table_content += "</table>"

                full_content = header_content + table_content

                # Write the HTML content to the file
                with open(p_file, 'w', encoding='utf-8') as f:
                    f.write(full_content)

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def dbAction_dump_in_json(self, p_dictionary, p_file):
        try:
            # Serialize the widgets to simple Python types
            serialized_data = []
            for instance in p_dictionary['data']:
                serialized_instance = {}
                for key, widget in instance.items():
                    if isinstance(widget, QLineEdit):
                        serialized_instance[key] = widget.text()
                    elif isinstance(widget, QCheckBox):
                        serialized_instance[key] = widget.isChecked()
                    # Handle other widget types here
                serialized_data.append(serialized_instance)

            # Update the dictionary
            p_dictionary['data'] = serialized_data

            # Write to the file
            with open(p_file, 'w') as f:
                json.dump(p_dictionary, f)

            print("Data dumped successfully in JSON.")

        except Exception as e:
            print(f"An error occurred while dumping data to JSON: {e}")


    def dbAction_load_from_json(self, p_model, p_file):
        try:
            # Read the JSON file
            with open(p_file, 'r') as f:
                json_data = json.load(f)

            # Validate that the JSON data is a dictionary
            if not isinstance(json_data, dict):
                print("JSON data is not a dictionary.")
                return

            # Create a mapping from JSON field names to widgets
            widget_dict = {k: v for k, v in p_model['data'][0].items()}

            # Validate that the 'data' in JSON is a list
            if not isinstance(json_data.get('data', []), list):
                print("JSON data field is not a list.")
                return

            # Loop through each instance (in case of multiple instances)
            for instance_data in json_data['data']:
                if not isinstance(instance_data, dict):
                    print("Instance data is not a dictionary.")
                    continue

                for key, value in instance_data.items():
                    widget = widget_dict.get(key, None)
                    if widget is None:
                        print(f"Key {key} not found in widget dictionary.")
                        continue

                    if isinstance(widget, QLineEdit):
                        widget.setText(str(value))
                    elif isinstance(widget, QCheckBox):
                        widget.setChecked(bool(value))
                    elif isinstance(widget, QComboBox):
                        index = widget.findText(str(value))
                        if index >= 0:
                            widget.setCurrentIndex(index)

            print("Data loaded successfully from JSON.")

        except Exception as e:
            print(f"An error occurred while loading data from JSON: {e}")



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()