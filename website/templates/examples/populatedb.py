import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('../../var/users.sqlite3')

# Create a cursor object to execute SQL statements
cursor = conn.cursor()

# Define the data to be inserted
product_data = (3, 'ciao', 'Terracotta', 'cu368-marble-coaster-pompei-frescoes.jpg')

# Execute the INSERT statement
cursor.execute("INSERT INTO products (id, name, category, image_url) VALUES (?, ?, ?, ?)", product_data)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
