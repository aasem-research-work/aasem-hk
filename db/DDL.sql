CREATE TABLE Stakeholder (
    StakeholderID    INTEGER PRIMARY KEY AUTOINCREMENT,
    StakeholderName  TEXT    NOT NULL
                             UNIQUE,
    ContactInfo      TEXT,
    IsCustomer       INTEGER DEFAULT 0,
    IsSupplier       INTEGER DEFAULT 0,
    IsEmployee       INTEGER DEFAULT 0,
    OtherRoles       TEXT,
    AmountPayable    NUMERIC DEFAULT (0),
    AmountReceivable NUMERIC DEFAULT (0),
    Notes            TEXT,
    ReminderNote     TEXT,
    ReminderDateTime TEXT,
    ReminderScript   TEXT
);


CREATE TABLE Inventory (
    ItemID            INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemName          TEXT    NOT NULL
                              UNIQUE,
    Manufacturer      TEXT,
    ItemType          TEXT    NOT NULL,
    ItemDetails       TEXT,
    StockCount        INTEGER NOT NULL,
    ReorderLevel      INTEGER,
    AssetType         TEXT,
    PricePurchaseBasic     NUMERIC DEFAULT (0),
    PricePurchaseAdd1 NUMERIC DEFAULT (0),
    PricePurchaseAdd2 NUMERIC DEFAULT (0),
    PricePurchaseAdd3 NUMERIC DEFAULT (0),
    PricePurchaseLess1 NUMERIC DEFAULT (0),
    PricePurchaseLess2 NUMERIC DEFAULT (0),
    PriceSaleBasic         NUMERIC DEFAULT (0),
    PriceSaleAdd1     NUMERIC DEFAULT (0),
    PriceSaleAdd2     NUMERIC DEFAULT (0),
    PriceSaleAdd3     NUMERIC DEFAULT (0),
    PriceSaleLess1    NUMERIC DEFAULT (0),
    PriceSaleLess2     NUMERIC DEFAULT (0)
);

CREATE TABLE Transactions (
    TransactionID       INTEGER  PRIMARY KEY AUTOINCREMENT,
    TransactionType     TEXT     NOT NULL,
    TransactionCategory TEXT,
    UserID              INTEGER,
    StakeholderID             INTEGER,
    ItemID              INTEGER,
    ItemDetails	TEXT,
    Quantity            INTEGER,
    QuantityUnit		TEXT,
    PaymentCash   NUMERIC DEFAULT (0),
	PaymentCredit   NUMERIC DEFAULT (0),
	PaymentCreditSchedule TEXT,
	PaymentCreditTerms TEXT,
    Timestamp           DATETIME DEFAULT CURRENT_TIMESTAMP,
    Notes               TEXT
);

