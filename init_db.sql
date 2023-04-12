CREATE TABLE print_order (id INTEGER NOT NULL, user_id INTEGER, 
filename TEXT NOT NULL, pages INTEGER NOT NULL, paper_type TEXT NOT NULL, color TEXT NOT NULL, sides TEXT NOT NULL, copies INTEGER NOT NULL, fee REAL NOT NULL, 
out_trade_no TEXT NOT NULL PRIMARY KEY, trade_type TEXT NOT NULL, 
trade_state TEXT DEFAULT "NOTPAY", trade_time TEXT, print_state TEXT,
FOREIGN KEY(user_id) REFERENCES users(id));

CREATE UNIQUE INDEX out_trade_no ON print_order (out_trade_no);

CREATE TABLE users (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password_hash TEXT NOT NULL, student_id NUMBER NOT NULL, school TEXT NOT NULL, credits INTEGER NOT NULL DEFAULT 3);

CREATE UNIQUE INDEX student_id ON users (student_id);
