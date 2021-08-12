import sqlite3
from typing import Optional
import sys, getopt, os


class DatabaseHandler:

    def __init__(self, abs_path: str):
        """ Creates or uses existing database located in {abs_path} and stores its connection """
        try:
            self.conn = sqlite3.connect(str(abs_path))
            assert self.conn is not None
        except sqlite3.Error as e:
            # database could not be created (or opened) -> abort
            print(e)
            sys.exit(1)

    def create_table_trades(self) -> None:
        try:
            sql = 'CREATE TABLE trades(event_type TEXT, ' \
                  'event_time INT, ' \
                  'symbol TEXT, ' \
                  'trade_id INT NOT NULL PRIMARY KEY,' \
                  'price REAL,' \
                  'quantity REAL,' \
                  'buyer_order_id INT,' \
                  'seller_order_id INT,' \
                  'is_market_maker BOOLEAN CHECK (is_market_maker IN (0, 1)),' \
                  'ignore BOOLEAN CHECK (ignore IN (0, 1)))'
            self.conn.cursor().execute(sql)
            # conn.commit()
        except sqlite3.Error as e:
            print('creation failed:')
            print(e)

    def remove_table(self, tablename: str) -> None:
        sql = "DROP TABLE {}".format(tablename)
        try:
            self.conn.cursor().executescript(sql)
            self.conn.commit()
        except sqlite3.Error as e:
            print('removing failed:')
            print(e)

    def insert_many(self, tablename, data, mode='replace') -> bool:

        assert mode in ['ignore', 'replace']
        try:
            if mode == "ignore":
                self.conn.cursor().executemany(
                    "INSERT OR IGNORE INTO {} VALUES (?,?,?,?,?,?,?,?,?,?)".format(tablename), data)
            elif mode == "replace":
                self.conn.cursor().executemany(
                    "INSERT OR REPLACE INTO {} VALUES (?,?,?,?,?,?,?,?,?,?)".format(tablename), data)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print('insertion failed:')
            print(e)
        return False