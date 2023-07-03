-- SQLite
CREATE TABLE "main_order" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "seller_wallet_address" varchar(100) NOT NULL,
    "buyer_wallet_address" varchar(100) NOT NULL,
    "order_id" varchar(100) NOT NULL NOT NULL, 
    "item_id" integer NOT NULL,  
    "price" double NOT NULL, 
    "quantity" integer NOT NULL, 
    "rewards" double,
    "state" integer NOT NULL
);
