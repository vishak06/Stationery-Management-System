import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as sql
import datetime

# Global lists to store purchased items and their amounts
item_counts = []
item_amounts = []

# Database connection
conn = sql.connect(host='localhost', user='root', password='vishak06', database='sales')
c1 = conn.cursor()

# Initialize tkinter
root = tk.Tk()
root.title("Stationery Management")
root.geometry("800x600")  # Set the window size

# Create a style to set the font
style = ttk.Style()
style.configure("Bold.TButton", font=("Helvetica", 16, "bold"))

# Utility functions
def get_current_datetime():
    current_time = datetime.datetime.now()
    return current_time.strftime("%d/%m/%Y %H:%M")

def display_bill():
    total_items = sum(item_counts)
    total_amount = sum(item_amounts)
    bill_text = f"Number of items purchased: {total_items}\nTotal Amount: {total_amount}"
    bill_label.config(text=bill_text)

def set_large_bold_font(widget):
    widget.config(font=("Helvetica", 16, "bold"))

def customer_interaction():
    customer_window = tk.Toplevel(root)
    customer_window.title("Customer Interface")
    current_datetime = get_current_datetime()
    current_datetime_label = ttk.Label(customer_window, text=current_datetime, font=("Helvetica", 16))
    current_datetime_label.pack()

    product_list_label = ttk.Label(customer_window, text="PRODUCT PRODUCT NAME", font=("Helvetica", 16, "bold"))
    product_list_label.pack()

    c1.execute('select product_no, product_name from stock;')
    peee = c1.fetchall()

    for product_no, product_name in peee:
        product_label = ttk.Label(customer_window, text=f"{product_no} {product_name}", font=("Helvetica", 14))
        product_label.pack()

    def buy_product():
        product_number = product_number_entry.get()
        if product_number.isdigit() and 1 <= int(product_number) <= len(peee):
            product_number = int(product_number) - 1  # Adjust for 0-based index
            product_name, cost_per_product = peee[product_number]
            confirmation = messagebox.askyesno("Confirmation", f"Do you want to buy {product_name} for ${cost_per_product}?")
            if confirmation:
                c1.execute(f"update stock set stock = stock - 1, purchased = purchased + 1 where product_no = {product_number + 1}")
                conn.commit()
                item_counts.append(1)
                item_amounts.append(cost_per_product)
                display_bill()
            else:
                messagebox.showerror("Error", "Invalid product number")

    item_counts = []
    item_amounts = []

    product_number_label = ttk.Label(customer_window, text="Enter product number:", font=("Helvetica", 16))
    product_number_label.pack()
    product_number_entry = ttk.Entry(customer_window, font=("Helvetica", 14))
    product_number_entry.pack()

    buy_button = ttk.Button(customer_window, text="Buy", command=buy_product, style="Bold.TButton")
    buy_button.pack()

    bill_label = ttk.Label(customer_window, text="", font=("Helvetica", 16))
    bill_label.pack()

def admin_interaction():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Interface")

    def login():
        username = username_entry.get()
        password = password_entry.get()
        c1.execute("select * from user where username = %s and passwd = %s", (username, password))
        data = c1.fetchall()
        if data:
            show_admin_operations()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def show_admin_operations():
        login_frame.pack_forget()
        admin_operations_frame = ttk.Frame(admin_window)
        admin_operations_frame.pack()

        stock_button = ttk.Button(admin_operations_frame, text="View Stock", command=view_stock, style="Bold.TButton")
        stock_button.grid(row=0, column=0, padx=10, pady=10)

        add_stock_button = ttk.Button(admin_operations_frame, text="Add Stock", command=add_stock, style="Bold.TButton")
        add_stock_button.grid(row=1, column=0, padx=10, pady=10)

        add_product_button = ttk.Button(admin_operations_frame, text="Add Product", command=add_product, style="Bold.TButton")
        add_product_button.grid(row=2, column=0, padx=10, pady=10)

    def view_stock():
        stock_window = tk.Toplevel(admin_window)
        stock_window.title("Stock Information")

        c1.execute("select * from stock")
        stock_data = c1.fetchall()

        stock_list_label = ttk.Label(stock_window, text="Product Name\tCost per Product\tStock\tPurchased", font=("Helvetica", 16, "bold"))
        stock_list_label.pack()

        for row in stock_data:
            product_name, cost_per_product, stock, purchased = row[1], row[2], row[3], row[4]
            stock_info_label = ttk.Label(stock_window, text=f"{product_name}\t${cost_per_product}\t{stock}\t{purchased}", font=("Helvetica", 14))
            stock_info_label.pack()

    def add_stock():
        add_stock_window = tk.Toplevel(admin_window)
        add_stock_window.title("Add Stock")

        product_number_label = ttk.Label(add_stock_window, text="Product Number:", font=("Helvetica", 16))
        product_number_label.pack()
        product_number_entry = ttk.Entry(add_stock_window, font=("Helvetica", 14))
        product_number_entry.pack()

        stock_amount_label = ttk.Label(add_stock_window, text="Stock Amount:", font=("Helvetica", 16))
        stock_amount_label.pack()
        stock_amount_entry = ttk.Entry(add_stock_window, font=("Helvetica", 14))
        stock_amount_entry.pack()

        def update_stock():
            product_number = product_number_entry.get()
            stock_amount = stock_amount_entry.get()
            if product_number.isdigit() and stock_amount.isdigit():
                product_number = int(product_number)
                stock_amount = int(stock_amount)
                c1.execute(f"update stock set stock = stock + {stock_amount} where product_no = {product_number}")
                conn.commit()
                messagebox.showinfo("Success", f"Stock for product {product_number} updated by {stock_amount}")
            else:
                messagebox.showerror("Error", "Invalid input")

        update_button = ttk.Button(add_stock_window, text="Update Stock", command=update_stock, style="Bold.TButton")
        update_button.pack()

    def add_product():
        add_product_window = tk.Toplevel(admin_window)
        add_product_window.title("Add Product")

        product_number_label = ttk.Label(add_product_window, text="Product Number:", font=("Helvetica", 16))
        product_number_label.pack()
        product_number_entry = ttk.Entry(add_product_window, font=("Helvetica", 14))
        product_number_entry.pack()

        product_name_label = ttk.Label(add_product_window, text="Product Name:", font=("Helvetica", 16))
        product_name_label.pack()
        product_name_entry = ttk.Entry(add_product_window, font=("Helvetica", 14))
        product_name_entry.pack()

        cost_label = ttk.Label(add_product_window, text="Cost per Product:", font=("Helvetica", 16))
        cost_label.pack()
        cost_entry = ttk.Entry(add_product_window, font=("Helvetica", 14))
        cost_entry.pack()

        stock_label = ttk.Label(add_product_window, text="Initial Stock:", font=("Helvetica", 16))
        stock_label.pack()
        stock_entry = ttk.Entry(add_product_window, font=("Helvetica", 14))
        stock_entry.pack()

        def add_new_product():
            product_number = product_number_entry.get()
            product_name = product_name_entry.get()
            cost = cost_entry.get()
            stock = stock_entry.get()

            if product_number.isdigit() and cost.replace('.', '', 1).isdigit() and stock.isdigit():
                c1.execute("insert into stock (product_no, product_name, cost_per_product, stock, purchased) values (%s, %s, %s, %s, 0)",
                           (product_number, product_name, cost, stock))
                conn.commit()
                messagebox.showinfo("Success", "Product added successfully!")
            else:
                messagebox.showerror("Error", "Invalid input")

        add_button = ttk.Button(add_product_window, text="Add Product", command=add_new_product, style="Bold.TButton")
        add_button.pack()

    login_frame = ttk.Frame(admin_window)
    login_frame.pack()

    username_label = ttk.Label(login_frame, text="Username:", font=("Helvetica", 16))
    username_label.grid(row=0, column=0, padx=10, pady=10)
    username_entry = ttk.Entry(login_frame, font=("Helvetica", 14))
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    password_label = ttk.Label(login_frame, text="Password:", font=("Helvetica", 16))
    password_label.grid(row=1, column=0, padx=10, pady=10)
    password_entry = ttk.Entry(login_frame, show="*", font=("Helvetica", 14))
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    login_button = ttk.Button(login_frame, text="Login", command=login, style="Bold.TButton")
    login_button.grid(row=2, columnspan=2, padx=10, pady=10)

# Main interface
customer_button = ttk.Button(root, text="Customer", command=customer_interaction, style="Bold.TButton")
customer_button.pack(pady=10)

admin_button = ttk.Button(root, text="Admin", command=admin_interaction, style="Bold.TButton")
admin_button.pack(pady=10)

exit_button = ttk.Button(root, text="Exit", command=root.destroy, style="Bold.TButton")
exit_button.pack(pady=10)

root.mainloop()
