import pyodbc
import tkinter as tk
from tkinter import ttk, messagebox
from business_search import BusinessSearchTab
from user_search import UserSearchTab

def login(conn):
    root = tk.Tk()
    root.title("Yelp Database Login")
    root.state("zoomed")

    def validate_login():
        logged_userid = user_id_entry.get()

        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM dbo.user_yelp WHERE user_id = ?", (logged_userid,))
        result = cur.fetchone()[0]

        if result > 0:
            root.destroy()
            main(logged_userid)
        else:
            messagebox.showerror("Invalid User ID", "Please enter a valid User ID.")

    login_frame = tk.Frame(root)
    login_frame.pack()

    login_label = tk.Label(login_frame, text="Enter User ID:")
    login_label.pack()

    user_id_entry = tk.Entry(login_frame)
    user_id_entry.pack()

    login_button = tk.Button(login_frame, text="Login", command=validate_login)
    login_button.pack()

    root.mainloop()

def main(logged_userid):
    conn = pyodbc.connect('driver={ODBC Driver 18 for SQL Server};server=cypress.csil.sfu.ca;uid=s_jvi2;pwd=LtH4N2GqLHNbLYM2;Encrypt=yes;TrustServerCertificate=yes')
    
    root = tk.Tk()
    root.title("Yelp Database Search")
    root.state("zoomed")

    tab_control = ttk.Notebook(root)
    tab_control.pack(expand=1, fill="both")

    business_tab = BusinessSearchTab(tab_control, logged_userid, conn)
    tab_control.add(business_tab, text="Business Search")

    user_tab = UserSearchTab(tab_control, logged_userid, conn)
    tab_control.add(user_tab, text="User Search")

    root.mainloop()


if __name__ == "__main__":
    conn = pyodbc.connect('driver={ODBC Driver 18 for SQL Server};server=cypress.csil.sfu.ca;uid=s_jvi2;pwd=LtH4N2GqLHNbLYM2;Encrypt=yes;TrustServerCertificate=yes')
    login(conn)
