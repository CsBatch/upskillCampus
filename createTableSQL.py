import mysql.connector as mysql

def connect_to_database():
    try:
        connection = mysql.connect(
            host="127.0.0.1",
            user="root",
            password="password",
            database="urlshortner"  # Assuming the database 'urlshortner' already exists
        )
        print("Connected to MySQL database successfully!")
        return connection
    except mysql.Error as err:
        print("Error connecting to database:", err)
        return None

def create_accounts_table(connection):
    
    cursor = connection.cursor()

    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS accounts(id INT AUTO_INCREMENT PRIMARY KEY, original_url VARCHAR(255) NOT NULL, short_url VARCHAR(20) UNIQUE NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        connection.commit()
        print("Accounts table created successfully (if it didn't exist).")
    except mysql.Error as err:
        print("Error creating table:", err)
        connection.rollback()  # Rollback changes if an error occurs

if __name__ == "__main__":
    connection = connect_to_database()
    if connection:
        create_accounts_table(connection)
        connection.close()
        print("Database setup completed.")
    else:
        print("Failed to establish database connection.")
