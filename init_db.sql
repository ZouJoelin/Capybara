CREATE TABLE print_order (id INTEGER NOT NULL, user_id INTEGER, 
filename TEXT NOT NULL, pages INTEGER NOT NULL, paper_type TEXT NOT NULL, color TEXT NOT NULL, side TEXT NOT NULL, copies INTEGER NOT NULL, fee REAL NOT NULL, 
out_trade_no TEXT NOT NULL PRIMARY KEY, trade_type TEXT NOT NULL, 
trade_state TEXT DEFAULT "NOTPAY", trade_time TEXT, print_state TEXT,
FOREIGN KEY(user_id) REFERENCES users(id));

CREATE UNIQUE INDEX out_trade_no ON print_order (out_trade_no);
