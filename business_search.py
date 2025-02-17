import tkinter as tk
from tkinter import ttk
import random
import string
from tkinter import messagebox
from datetime import datetime

class BusinessSearchTab(tk.Frame):
    def __init__(self, parent, logged_userid, conn):
        super().__init__(parent)

        self.logged_userid = logged_userid

        self.conn = conn
        self.cur = self.conn.cursor()

        self.create_widgets()

    def create_widgets(self):
        business_frame = tk.Frame(self)
        business_frame.pack(side=tk.TOP, fill=tk.X)

        self.min_stars_var = tk.StringVar()
        self.min_stars_var.set("1") 

        min_stars_label = tk.Label(business_frame, text="Minimum Stars:")
        min_stars_label.pack(side=tk.LEFT, padx=5)
        for stars in range(1, 6):
            tk.Radiobutton(business_frame, text=str(stars), variable=self.min_stars_var, value=str(stars)).pack(side=tk.LEFT)

        self.city_var = tk.StringVar()
        city_label = tk.Label(business_frame, text="City:")
        city_label.pack(side=tk.LEFT, padx=5)
        city_entry = tk.Entry(business_frame, textvariable=self.city_var)
        city_entry.pack(side=tk.LEFT, padx=5)

        self.name_var = tk.StringVar()
        name_label = tk.Label(business_frame, text="Name:")
        name_label.pack(side=tk.LEFT, padx=5)
        name_entry = tk.Entry(business_frame, textvariable=self.name_var)
        name_entry.pack(side=tk.LEFT, padx=5)

        self.order_by_var = tk.StringVar()
        self.order_by_var.set("name")

        order_by_label = tk.Label(business_frame, text="Order By:")
        order_by_label.pack(side=tk.LEFT, padx=5)
        order_by_menu = ttk.Combobox(business_frame, textvariable=self.order_by_var, values=["name", "city", "stars"])
        order_by_menu.pack(side=tk.LEFT, padx=5)
        order_by_menu.current(0)

        search_business_button = tk.Button(business_frame, text="Search Business", command=self.search_business)
        search_business_button.pack(side=tk.LEFT, padx=5)

        self.business_table = ttk.Treeview(self)
        self.business_table.pack(fill=tk.BOTH, expand=True)
        self.business_table.bind("<ButtonRelease-1>", self.review_business)

        columns = ["Business ID", "Name", "Address", "City", "Stars"]
        self.business_table["columns"] = columns
        self.business_table.heading("#0", text="Index")
        self.business_table.column("#0", width=50)
        for col in columns:
            self.business_table.heading(col, text=col)
            self.business_table.column(col, anchor=tk.CENTER, width=120)

        self.display_business_table_data()

    def review_business(self, event):
        selected_item = self.business_table.item(self.business_table.focus())
        if selected_item:
            business_id = selected_item['values'][0]

            stars = tk.IntVar()
            stars.set(1)

            def confirm_review():
                selected_stars = stars.get()
                current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                review_id = generate_unique_review_id()
                
                self.cur.execute("INSERT INTO review (review_id, user_id, business_id, stars, date) VALUES (?,?,?,?,?)",
                                (review_id, self.logged_userid, business_id, selected_stars, current_date))
                self.conn.commit()
                messagebox.showinfo("Review Added", f"Review of {selected_stars} stars added successfully.")
                                
                review_window.destroy()

            def generate_unique_review_id():
                while True:
                    review_id = ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=22))
                    
                    self.cur.execute("SELECT review_id FROM review")
                    existing_review_ids = [row[0] for row in self.cur.fetchall()]
                    
                    if review_id not in existing_review_ids:
                        return review_id      

            def cancel_review():
                nonlocal review_window 
                review_window.destroy()

            review_window = tk.Toplevel(self)
            review_window.title("Review Business")
            review_window.geometry("300x150")

            stars_frame = tk.Frame(review_window)
            stars_frame.pack(pady=10)

            stars_label = tk.Label(stars_frame, text="Stars:")
            stars_label.pack(side=tk.LEFT, padx=5)
            for rating in range(1, 6):
                tk.Radiobutton(stars_frame, text=str(rating), variable=stars, value=rating).pack(side=tk.LEFT)

            buttons_frame = tk.Frame(review_window)
            buttons_frame.pack(pady=10)

            confirm_button = tk.Button(buttons_frame, text="Confirm", command=confirm_review)
            confirm_button.pack(side=tk.LEFT, padx=5)

            cancel_button = tk.Button(buttons_frame, text="Cancel", command=cancel_review)
            cancel_button.pack(side=tk.LEFT, padx=5)

    def display_business_table_data(self):
        self.cur.execute("SELECT business_id, name, address, city, stars FROM business")
        rows = self.cur.fetchall()
        self.business_table.delete(*self.business_table.get_children())  

        for row in rows:
            formatted_row = (str(row[0]), row[1], row[2], row[3], str(row[4]))  
            self.business_table.insert("", tk.END, values=formatted_row)

    def search_business(self):
        cur = self.conn.cursor()
        min_stars = self.min_stars_var.get()
        city = self.city_var.get().strip().lower()
        name = self.name_var.get().strip().lower()
        order_by = self.order_by_var.get()

        query = f"SELECT business_id, name, address, city, stars FROM business WHERE 1=1"

        if min_stars != "":
            query += f" AND stars >= {min_stars}"
        
        elif city != "":
            query += f" AND LOWER(city) LIKE '%{city}%'"

        elif name != "":
            query += f" AND LOWER(name) LIKE '%{name}%'"
        else:
            messagebox.showwarning("Empty Field", "Please enter at least a field to search.")
            return

        query += f" ORDER BY {order_by}"
        cur.execute(query)
        rows = cur.fetchall()

        if not rows:
            messagebox.showinfo("No Results", "No businesses found based on the search criteria.")
        else:
            self.business_table.delete(*self.business_table.get_children()) 
            for row in rows:
                formatted_row = (str(row[0]), row[1], row[2], row[3], str(row[4]))
                self.business_table.insert("", tk.END, values=formatted_row)
                
