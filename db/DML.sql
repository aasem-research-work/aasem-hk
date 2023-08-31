INSERT INTO Inventory (ItemName, Manufacturer, ItemType, ItemDetails, StockCount, ReorderLevel, AssetType, PricePurchaseBasic, PricePurchaseAdd1, PricePurchaseAdd2, PricePurchaseLess1, PriceSaleBasic, PriceSaleAdd1, PriceSaleAdd2, PriceSaleLess1) VALUES ('Item1', 'BrandA', 'Electronics', 'Smartphone', 100, 10, 'Consumer Good', 100, 10, 5, 2, 120, 15, 7, 3);
INSERT INTO Inventory (ItemName, Manufacturer, ItemType, ItemDetails, StockCount, ReorderLevel, AssetType, PricePurchaseBasic, PricePurchaseAdd1, PricePurchaseAdd2, PricePurchaseLess1, PriceSaleBasic, PriceSaleAdd1, PriceSaleAdd2, PriceSaleLess1) VALUES ('Item2', 'BrandB', 'Furniture', 'Chair', 50, 5, 'Consumer Good', 40, 3, 1, 1, 45, 5, 2, 1);
INSERT INTO Inventory (ItemName, Manufacturer, ItemType, ItemDetails, StockCount, ReorderLevel, AssetType, PricePurchaseBasic, PricePurchaseAdd1, PricePurchaseAdd2, PricePurchaseLess1, PriceSaleBasic, PriceSaleAdd1, PriceSaleAdd2, PriceSaleLess1) VALUES ('Item3', 'BrandA', 'Electronics', 'Laptop', 20, 2, 'Consumer Good', 500, 30, 15, 10, 550, 40, 18, 12);
INSERT INTO Inventory (ItemName, Manufacturer, ItemType, ItemDetails, StockCount, ReorderLevel, AssetType, PricePurchaseBasic, PricePurchaseAdd1, PricePurchaseAdd2, PricePurchaseLess1, PriceSaleBasic, PriceSaleAdd1, PriceSaleAdd2, PriceSaleLess1) VALUES ('Item4', 'BrandC', 'Grocery', 'Apple', 200, 20, 'Consumer Good', 1, 0.1, 0.05, 0.02, 1.2, 0.12, 0.06, 0.02);


INSERT INTO Stakeholder (StakeholderName, ContactInfo, IsCustomer, IsSupplier, IsEmployee, OtherRoles, AmountPayable, AmountReceivable, Notes, ReminderNote, ReminderDateTime, ReminderScript) VALUES ('customer1', '123-456-7890', 1, 0, 0, '', 159.75, 782.97, 'Frequent supplier', 'Check supplies', '2023-09-10 10:00:00', 'payment_script');
INSERT INTO Stakeholder (StakeholderName, ContactInfo, IsCustomer, IsSupplier, IsEmployee, OtherRoles, AmountPayable, AmountReceivable, Notes, ReminderNote, ReminderDateTime, ReminderScript) VALUES ('customer2', '123-456-7890', 1, 0, 0, '', 630.87, 504.63, 'Full-time employee', 'Check supplies', '2023-09-10 10:00:00', 'review_script');
INSERT INTO Stakeholder (StakeholderName, ContactInfo, IsCustomer, IsSupplier, IsEmployee, OtherRoles, AmountPayable, AmountReceivable, Notes, ReminderNote, ReminderDateTime, ReminderScript) VALUES ('customer3', '123-456-7890', 1, 0, 0, '', 917.05, 903.2, 'Frequent supplier', 'Check supplies', '2023-09-10 10:00:00', 'review_script');
INSERT INTO Stakeholder (StakeholderName, ContactInfo, IsCustomer, IsSupplier, IsEmployee, OtherRoles, AmountPayable, AmountReceivable, Notes, ReminderNote, ReminderDateTime, ReminderScript) VALUES ('supplier1', '987-654-3210', 0, 1, 0, '', 482.78, 648.2, 'Frequent supplier', 'Check supplies', '2023-09-10 10:00:00', 'payment_script');
INSERT INTO Stakeholder (StakeholderName, ContactInfo, IsCustomer, IsSupplier, IsEmployee, OtherRoles, AmountPayable, AmountReceivable, Notes, ReminderNote, ReminderDateTime, ReminderScript) VALUES ('supplier2', '987-654-3210', 0, 1, 0, '', 917.13, 516.38, 'Full-time employee', 'Check supplies', '2023-09-20 09:00:00', 'supply_check_script');
INSERT INTO Stakeholder (StakeholderName, ContactInfo, IsCustomer, IsSupplier, IsEmployee, OtherRoles, AmountPayable, AmountReceivable, Notes, ReminderNote, ReminderDateTime, ReminderScript) VALUES ('supplier3', '123-456-7890', 0, 1, 0, '', 369.93, 480.86, 'Full-time employee', 'Performance review', '2023-09-15 14:00:00', 'payment_script');
INSERT INTO Stakeholder (StakeholderName, ContactInfo, IsCustomer, IsSupplier, IsEmployee, OtherRoles, AmountPayable, AmountReceivable, Notes, ReminderNote, ReminderDateTime, ReminderScript) VALUES ('employee1', '987-654-3210', 0, 0, 1, 'Manager', 983.46, 217.71, 'Full-time employee', 'Check supplies', '2023-09-20 09:00:00', 'supply_check_script');
INSERT INTO Stakeholder (StakeholderName, ContactInfo, IsCustomer, IsSupplier, IsEmployee, OtherRoles, AmountPayable, AmountReceivable, Notes, ReminderNote, ReminderDateTime, ReminderScript) VALUES ('employee2', '555-666-7777', 0, 0, 1, 'Sales', 328.2, 366.39, 'Full-time employee', 'Call for payment', '2023-09-15 14:00:00', 'review_script');
INSERT INTO Stakeholder (StakeholderName, ContactInfo, IsCustomer, IsSupplier, IsEmployee, OtherRoles, AmountPayable, AmountReceivable, Notes, ReminderNote, ReminderDateTime, ReminderScript) VALUES ('employee3', '123-456-7890', 0, 0, 1, 'Manager', 659.73, 960.3, 'Frequent supplier', 'Call for payment', '2023-09-10 10:00:00', 'payment_script');





-- Cash Sales Transactions
INSERT INTO Transactions (TransactionType, TransactionCategory, UserID, StakeholderID, ItemID, Quantity, PaymentCash, PaymentCredit, Notes) VALUES ('Sale', 'Cash', 1, 1, 1, 2, 240, 0, 'Cash Sale');
INSERT INTO Transactions (TransactionType, TransactionCategory, UserID, StakeholderID, ItemID, Quantity, PaymentCash, PaymentCredit, Notes) VALUES ('Sale', 'Cash', 1, 1, 2, 1, 45, 0, 'Cash Sale');

-- Credit Sales Transactions
INSERT INTO Transactions (TransactionType, TransactionCategory, UserID, StakeholderID, ItemID, Quantity, PaymentCash, PaymentCredit, PaymentCreditSchedule, Notes) VALUES ('Sale', 'Credit', 1, 1, 3, 1, 0, 550, '2023-10-01', 'Credit Sale');
INSERT INTO Transactions (TransactionType, TransactionCategory, UserID, StakeholderID, ItemID, Quantity, PaymentCash, PaymentCredit, PaymentCreditSchedule, Notes) VALUES ('Sale', 'Credit', 1, 1, 4, 50, 0, 60, '2023-10-05', 'Credit Sale');

-- Cash Purchase Transactions
INSERT INTO Transactions (TransactionType, TransactionCategory, UserID, StakeholderID, ItemID, Quantity, PaymentCash, PaymentCredit, Notes) VALUES ('Purchase', 'Cash', 1, 2, 1, 10, 1000, 0, 'Cash Purchase');
INSERT INTO Transactions (TransactionType, TransactionCategory, UserID, StakeholderID, ItemID, Quantity, PaymentCash, PaymentCredit, Notes) VALUES ('Purchase', 'Cash', 1, 2, 2, 5, 200, 0, 'Cash Purchase');

-- Credit Purchase Transactions
INSERT INTO Transactions (TransactionType, TransactionCategory, UserID, StakeholderID, ItemID, Quantity, PaymentCash, PaymentCredit, PaymentCreditSchedule, Notes) VALUES ('Purchase', 'Credit', 1, 2, 3, 2, 0, 1000, '2023-09-15', 'Credit Purchase');
INSERT INTO Transactions (TransactionType, TransactionCategory, UserID, StakeholderID, ItemID, Quantity, PaymentCash, PaymentCredit, PaymentCreditSchedule, Notes) VALUES ('Purchase', 'Credit', 1, 2, 4, 100, 0, 100, '2023-09-20', 'Credit Purchase');

-- Employee Salary Transaction
INSERT INTO Transactions (TransactionType, TransactionCategory, UserID, StakeholderID, PaymentCash, Notes) VALUES ('Expense', 'Salary', 1, 3, 500, 'Employee Salary');

-- Utility Bill Transaction
INSERT INTO Transactions (TransactionType, TransactionCategory, UserID, PaymentCash, Notes) VALUES ('Expense', 'Utility', 1, 100, 'Electricity Bill');
