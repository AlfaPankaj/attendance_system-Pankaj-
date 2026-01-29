import sqlite3
from datetime import datetime
from typing import Optional, Tuple
import os


DB_NAME = os.path.join("data", "attendance_v.db")

def init_db():
    """Initializes the database with Users and Logs tables."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT CHECK(action IN ('PUNCH_IN', 'PUNCH_OUT')),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )''')
    
    conn.commit()
    conn.close()

def add_user(name: str) -> int:
    """Adds a new user and returns their User ID."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO users (name) VALUES (?)", (name,))
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    return user_id

def get_user_name(user_id: int) -> Optional[str]:
    """Fetches user name by ID."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name FROM users WHERE id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def log_attendance(user_id, name, action):
    """Logs a punch-in or punch-out event."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    now = datetime.now()
    
    c.execute('''SELECT action, timestamp FROM logs 
                 WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1''', (user_id,))
    last_entry = c.fetchone()
    
    if last_entry:
        last_action, last_time_str = last_entry
        last_time = datetime.strptime(str(last_time_str), "%Y-%m-%d %H:%M:%S.%f")
        seconds_diff = (now - last_time).total_seconds()
        
        if last_action == action and seconds_diff < 60:
            conn.close()
            return False, "Cooldown active. Please wait 1 minute."

    c.execute("INSERT INTO logs (user_id, action, timestamp) VALUES (?, ?, ?)",
              (user_id, action, now))
    
    conn.commit()
    conn.close()
    return True, f"Successfully marked {action} at {now.strftime('%H:%M:%S')}"

def get_logs():
    """Fetches all logs for the Admin Dashboard."""
    conn = sqlite3.connect(DB_NAME)
    import pandas as pd
    df = pd.read_sql_query("""
        SELECT users.name, logs.action, logs.timestamp 
        FROM logs 
        JOIN users ON logs.user_id = users.id 
        ORDER BY logs.timestamp DESC
    """, conn)
    conn.close()
    return df
