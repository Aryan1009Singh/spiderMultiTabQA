import os
import sqlite3

# Define the root directory
root_dir = 'spider/database'

# Walk through the root directory
count = 0
for dirpath, dirnames, filenames in os.walk(root_dir):
    
    for filename in filenames:
        
            
        # Check if the file is a .sql file
        if filename.endswith('.sql'):
            # Create a path to the .sql file
            sql_file_path = os.path.join(dirpath, filename)
            # Create a path for the .db file
            db_file_path = os.path.join(dirpath, filename.replace('.sql', '.db'))

            # Delete the existing .db file if it exists
            if os.path.exists(db_file_path):
                continue

            # Connect to the SQLite database
            conn = sqlite3.connect(db_file_path)
            cursor = conn.cursor()

            # Execute the .sql file
            with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
                sql_script = sql_file.read()
                cursor.executescript(sql_script)

            # Commit the changes and close the connection
            conn.commit()
            conn.close()