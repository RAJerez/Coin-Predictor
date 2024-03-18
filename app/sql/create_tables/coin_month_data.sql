CREATE TABLE IF NOT EXISTS coin_month_data (
	coin VARCHAR NOT NULL, 
	year INTEGER NOT NULL, 
	month INTEGER NOT NULL, 
	min_price FLOAT, 
	max_price FLOAT, 
	PRIMARY KEY (coin, year, month)
);