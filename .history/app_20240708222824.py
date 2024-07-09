import tkinter as tk
from tkinter import messagebox
import psycopg2
import logging

# Setup logging
logging.basicConfig(level=logging.ERROR)

# Database connection
try:
    conn = psycopg2.connect(
    dbname="db_user",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432",
    )
    cursor = conn.cursor()
except Exception as e:
    logging.error("Error connecting to the database: %s", e)
    messagebox.showerror("Database Connection Error", str(e))
    exit()

# Functions for CRUD operations on Products
def create_product():
    try:
        name = entry_name.get()
        description = entry_description.get()
        price = entry_price.get()
        stock_quantity = entry_stock_quantity.get()
        category_id = entry_category_id.get()
        
        # Check if category_id exists in Categories table
        cursor.execute("SELECT 1 FROM Categories WHERE category_id = %s", (category_id,))
        if cursor.fetchone() is None:
            messagebox.showerror("Error", "Category ID does not exist. Please enter a valid Category ID.")
            return
        
        cursor.execute("INSERT INTO Products (name, description, price, stock_quantity, category_id) VALUES (%s, %s, %s, %s, %s)",
                       (name, description, price, stock_quantity, category_id))
        conn.commit()
        messagebox.showinfo("Success", "Product created successfully!")
    except Exception as e:
        conn.rollback()
        logging.error("Error creating product: %s", e)
        messagebox.showerror("Error", str(e))

def read_products():
    try:
        cursor.execute("SELECT * FROM Products")
        rows = cursor.fetchall()
        listbox_products.delete(0, tk.END)
        for row in rows:
            listbox_products.insert(tk.END, row)
    except Exception as e:
        logging.error("Error reading products: %s", e)
        messagebox.showerror("Error", str(e))

tk.Button(root, text="Update", command=update_product).grid(row=6, column=2)
tk.Button(root, text="Delete", command=delete_product).grid(row=6, column=3)



# Pre-defined SQL queries
def join_query():
    try:
        cursor.execute("""
        SELECT p.name, c.category_name 
        FROM Products p
        JOIN Categories c ON p.category_id = c.category_id
        """)
        rows = cursor.fetchall()
        listbox_results.delete(0, tk.END)
        for row in rows:
            listbox_results.insert(tk.END, row)
    except Exception as e:
        logging.error("Error executing join query: %s", e)
        messagebox.showerror("Error", str(e))

def subquery():
    try:
        cursor.execute("""
        SELECT * FROM Products WHERE price > (
            SELECT AVG(price) FROM Products
        )
        """)
        rows = cursor.fetchall()
        listbox_results.delete(0, tk.END)
        for row in rows:
            listbox_results.insert(tk.END, row)
    except Exception as e:
        logging.error("Error executing subquery: %s", e)
        messagebox.showerror("Error", str(e))


# GUI setup
root = tk.Tk()
root.title("Product Inventory Management")

# Labels and Entry fields
tk.Label(root, text="Product ID").grid(row=0, column=0)
tk.Label(root, text="Name").grid(row=1, column=0)
tk.Label(root, text="Description").grid(row=2, column=0)
tk.Label(root, text="Price").grid(row=3, column=0)
tk.Label(root, text="Stock Quantity").grid(row=4, column=0)
tk.Label(root, text="Category ID").grid(row=5, column=0)

entry_product_id = tk.Entry(root)
entry_name = tk.Entry(root)
entry_description = tk.Entry(root)
entry_price = tk.Entry(root)
entry_stock_quantity = tk.Entry(root)
entry_category_id = tk.Entry(root)

entry_product_id.grid(row=0, column=1)
entry_name.grid(row=1, column=1)
entry_description.grid(row=2, column=1)
entry_price.grid(row=3, column=1)
entry_stock_quantity.grid(row=4, column=1)
entry_category_id.grid(row=5, column=1)

# Buttons for CRUD operations
tk.Button(root, text="Create", command=create_product).grid(row=6, column=0)
tk.Button(root, text="Read", command=read_products).grid(row=6, column=1)

# Buttons for pre-defined SQL queries
tk.Button(root, text="Join Query", command=join_query).grid(row=8, column=0)
tk.Button(root, text="Subquery", command=subquery).grid(row=8, column=1)

# Listbox for displaying query results
listbox_results = tk.Listbox(root)
listbox_results.grid(row=9, column=0, columnspan=4)

# Run the application
root.mainloop()

# Close database connection
conn.close()
