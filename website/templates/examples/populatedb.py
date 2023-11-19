# Execute this program to update the SQLite database
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('var/users.sqlite3')

# Create a cursor object to execute SQL statements
cursor = conn.cursor()

# Define the data to be inserted/updated
product_data = (3, 'cu373', 'Terracotta', 'static\imgs\terracotta\xtcu289.jpg')
new_name = "static\imgs\marble\cu367-marble-coaster-pompei-frescoes.jpg"
product_id_to_update = 3

# Execute the INSERT statement
cursor.execute("INSERT INTO products (id, name, category, image_url) VALUES (?, ?, ?, ?)", product_data)

# Execute the UPDATE statement
#cursor.execute("UPDATE products SET image_url = ? WHERE id = ?", (new_name, product_id_to_update))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
