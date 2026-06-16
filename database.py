import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                game_id TEXT,
                amount REAL,
                receipt_file_id TEXT,
                status TEXT DEFAULT 'pending',
                rejection_reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_order(self, user_id, username, game_id, amount, receipt_file_id):
        self.cursor.execute('''
            INSERT INTO orders (user_id, username, game_id, amount, receipt_file_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, game_id, amount, receipt_file_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_order_status(self, order_id, status, reason=None):
        self.cursor.execute('''
            UPDATE orders SET status = ?, rejection_reason = ? WHERE id = ?
        ''', (status, reason, order_id))
        self.conn.commit()

    def get_order(self, order_id):
        self.cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        return self.cursor.fetchone()
