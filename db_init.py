# db_init.py
import sqlite3

def create_database():
    conn = sqlite3.connect('golf_picks.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
             email TEXT
        )
    ''')
    # Add email column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
         pass

    # Create tournaments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tournaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            picks_allowed INTEGER NOT NULL,
            date TEXT
        )
    ''')

    # Create golfers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS golfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    # Create picks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS picks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tournament_id INTEGER NOT NULL,
            golfer_id INTEGER NOT NULL,
            is_additional_pick BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (tournament_id) REFERENCES tournaments(id),
            FOREIGN KEY (golfer_id) REFERENCES golfers(id)
        )
    ''')
    # Drop Results Table
    cursor.execute("DROP TABLE IF EXISTS results")

    # Create results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER NOT NULL,
            golfer_id INTEGER NOT NULL,
            purse_money REAL NOT NULL,
             FOREIGN KEY (tournament_id) REFERENCES tournaments(id),
            FOREIGN KEY (golfer_id) REFERENCES golfers(id)
        )
    ''')

    # Create winnings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS winnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tournament_id INTEGER NOT NULL,
            weekly_winnings REAL DEFAULT 0,
            cumulative_winnings REAL DEFAULT 0,
             additional_pick_fee REAL DEFAULT 0,
              FOREIGN KEY (user_id) REFERENCES users(id),
             FOREIGN KEY (tournament_id) REFERENCES tournaments(id)
        )
    ''')

    conn.commit()
    conn.close()
if __name__ == "__main__":
    create_database()
    print("Database 'golf_picks.db' and tables created successfully.")