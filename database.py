import sqlite3
from datetime import datetime

DB_NAME = "education_ai.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS quiz_results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        topic TEXT,
        score INTEGER,
        total_questions INTEGER,
        attempt_date TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS learning_gaps (
        gap_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        topic TEXT,
        accuracy REAL,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_quiz_result(user_id, topic, score, total_questions):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO quiz_results (user_id, topic, score, total_questions, attempt_date)
    VALUES (?, ?, ?, ?, datetime('now'))
    """, (user_id, topic, score, total_questions))

    conn.commit()
    conn.close()
