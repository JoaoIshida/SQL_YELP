import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class UserSearchTab(tk.Frame):
    def __init__(self, parent, logged_userid, conn):
        super().__init__(parent)

        self.logged_userid = logged_userid

        self.conn = conn
        self.cur = self.conn.cursor()

        self.create_widgets()

    def create_widgets(self):
        user_frame = tk.Frame(self)
        user_frame.pack(side=tk.TOP, fill=tk.X)

        self.min_review_count_var = tk.StringVar()
        self.min_review_count_var.set("")

        self.min_avg_stars_var = tk.StringVar()
        self.min_avg_stars_var.set("1") 

        min_avg_stars_label = tk.Label(user_frame, text="Minimum Average Stars:")
        min_avg_stars_label = tk.Label(user_frame, text="Minimum Average Stars:")
        min_avg_stars_label.pack(side=tk.LEFT, padx=5)
        for stars in range(1, 6):
            tk.Radiobutton(user_frame, text=str(stars), variable=self.min_avg_stars_var, value=str(stars)).pack(side=tk.LEFT)

        min_review_count_label = tk.Label(user_frame, text="Minimum Review Count:")
        min_review_count_label.pack(side=tk.LEFT, padx=5)
        min_review_count_entry = tk.Entry(user_frame, textvariable=self.min_review_count_var)
        min_review_count_entry.pack(side=tk.LEFT, padx=5)

        self.user_name_var = tk.StringVar()
        user_name_label = tk.Label(user_frame, text="User Name:")
        user_name_label.pack(side=tk.LEFT, padx=5)
        user_name_entry = tk.Entry(user_frame, textvariable=self.user_name_var)
        user_name_entry.pack(side=tk.LEFT, padx=5)

        search_users_button = tk.Button(user_frame, text="Search Users", command=self.search_users)
        search_users_button.pack(side=tk.LEFT, padx=5)

        self.user_table = ttk.Treeview(self)
        self.user_table.pack(fill=tk.BOTH, expand=True)
        self.user_table.bind("<ButtonRelease-1>", self.make_friendship)

        user_columns = ["User ID", "Name", "Review Count", "Useful", "Funny", "Cool", "Average Stars", "Yelping Since"]
        self.user_table["columns"] = user_columns
        self.user_table.heading("#0", text="Index")
        self.user_table.column("#0", width=50)
        for col in user_columns:
            self.user_table.heading(col, text=col)
            self.user_table.column(col, anchor=tk.CENTER, width=120)

        self.display_users_table_data()
    
    def make_friendship(self, event):
        selected_item = self.user_table.item(self.user_table.focus())
        if selected_item:
            user_id = selected_item['values'][0]
            name = selected_item['values'][1]
            if user_id == self.logged_userid:
                messagebox.showwarning("Invalid Operation", "You cannot add yourself as a friend.")
                return

            self.cur.execute("SELECT * FROM dbo.friendship WHERE (user_id=? AND friend=?) OR (user_id=? AND friend=?)",
                             (self.logged_userid, user_id, user_id, self.logged_userid))
            existing_friendship = self.cur.fetchone()

            if existing_friendship:
                messagebox.showinfo("Friendship Exists", f"You are already friends with {name}:{user_id}.")
            else:
                confirm = messagebox.askyesno("Confirm Friendship", f"Do you want to add {name}:{user_id} as a friend?")
                if confirm:
                    self.cur.execute("INSERT INTO dbo.friendship VALUES (?, ?)", (self.logged_userid, user_id))
                    self.conn.commit()
                    messagebox.showinfo("Friendship Created", f"You are now friends with {name}:{user_id}.")

    def display_users_table_data(self):
        self.cur.execute("SELECT user_id, name, review_count, useful, funny, cool, average_stars, yelping_since FROM dbo.user_yelp")
        rows = self.cur.fetchall()
        self.user_table.delete(*self.user_table.get_children()) 

        for row in rows:
            formatted_row = (str(row[0]), row[1], row[2], row[3], row[4], row[5], str(row[6]), str(row[7]))

            self.user_table.insert("", "end", values=formatted_row)

    def search_users(self):
        min_review_count = self.min_review_count_var.get()
        min_avg_stars = self.min_avg_stars_var.get()
        name = self.user_name_var.get().strip().lower()

        query = f"SELECT user_id, name, review_count, useful, funny, cool, average_stars, yelping_since FROM dbo.user_yelp WHERE 1=1"

        if min_review_count != "":
            query += f" AND review_count >= {min_review_count}"

        if min_avg_stars != "":
            query += f" AND average_stars >= {min_avg_stars}"

        if name != "":
            query += f" AND LOWER(name) LIKE '%{name}%'"
        else:
            messagebox.showwarning("Empty Name Field", "Please enter a name to search.")
            return

        query += " ORDER BY name"
        self.cur.execute(query)
        rows = self.cur.fetchall()

        if not rows:
            messagebox.showinfo("No Results", "No users found based on the search criteria.")
        else:
            self.user_table.delete(*self.user_table.get_children())
            for row in rows:
                formatted_row = (str(row[0]), row[1], row[2], row[3], row[4], row[5], str(row[6]), str(row[7]))              
                self.user_table.insert("", "end", values=formatted_row)