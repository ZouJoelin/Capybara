
-- ALTER TABLE print_order ADD COLUMN device TEXT NOT NULL DEFAULT "unknown";
-- ALTER TABLE print_order rename to print_order_bkp;


CREATE TABLE print_order (user_open_id TEXT, 
filename TEXT NOT NULL, pages INTEGER NOT NULL, paper_type TEXT NOT NULL, color TEXT NOT NULL, sides TEXT NOT NULL, copies INTEGER NOT NULL, spend_coins INTEGER NOT NULL DEFAULT 0, fee REAL NOT NULL,
out_trade_no TEXT NOT NULL PRIMARY KEY, device TEXT NOT NULL, trade_type TEXT NOT NULL, trade_state TEXT NOT NULL DEFAULT "NOTPAY", trade_time TEXT, print_state TEXT);
-- FOREIGN KEY(user_open_id) REFERENCES users(open_id)

CREATE UNIQUE INDEX print_order_index ON print_order (out_trade_no);
CREATE INDEX print_user_index ON print_order (user_open_id);


-- INSERT INTO print_order SELECT id, user_id, filename, pages, paper_type, color, sides, copies, fee, out_trade_no, device, trade_type, trade_state, trade_time, print_state FROM print_order_bkp;
-- DROP TABLE print_order_bkp;
-- DROP TABLE users;


CREATE TABLE users (open_id TEXT NOT NULL PRIMARY KEY, nickname TEXT NOT NULL, student_name TEXT NOT NULL, student_id TEXT NOT NULL, university TEXT NOT NULL, region TEXT NOT NULL, school TEXT NOT NULL, dormitory TEXT NOT NULL, coins INTEGER NOT NULL DEFAULT 3);
CREATE UNIQUE INDEX user_index ON users (open_id);



-- initialize TABLE print_order...
-- INSERT INTO print_order (id, filename, pages, paper_type, color, sides, copies, fee, out_trade_no, trade_type, device) VALUES(0, 'test.pdf', 2, 'A4', '黑白', 'two-sided-long-edge', 1, 0.02, '20230420T0043KLP', 'NATIVE', 'PC');
-- INSERT INTO users (open_id, nickname, student_name, student_id, university, region, school, dormitory, coins) VALUES('h9adb30cjwq', '黄毛鸭头', '邹家林', '19333091', '中山大学', '东校区', '生命科学学院', '慎思园6号', 3);