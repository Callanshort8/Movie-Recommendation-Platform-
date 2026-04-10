from database import get_db_connection

def setupDatabase():    
    conn = get_db_connection()
    cursor = conn.cursor()

    commands = [
        
        """CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",

        """CREATE TABLE IF NOT EXISTS Watchlist (
        watchlist_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL, 
        canonical_id VARCHAR(36) NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uq_user_movie (user_id, canonical_id)
        )""",

        """CREATE TABLE IF NOT EXISTS Reviews (
            review_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            canonical_id VARCHAR(36) NOT NULL,
            rating INT NOT NULL,
            body TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
    ]
    
    for cmd in commands:
        try:
            cursor.execute(cmd)
        except Exception as e:
            print(f"DB setup warning {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("Database setup complete.")

