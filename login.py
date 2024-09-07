from tkinter import *
from tkinter import messagebox
import sqlite3

def login():
    def submit_login():
        login_username = login_username_entry.get()
        login_password = login_password_entry.get()

        # Connect to the database and check credentials
        conn = sqlite3.connect("party.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM info WHERE username = ? AND password = ?", (login_username, login_password))
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Login", "Entered successfully!")
            login_window.destroy()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    login_window = Toplevel()
    login_window.title("Login")
    login_window.geometry("300x200")
    
    # Username frame
    login_username_frame = Frame(login_window)
    login_username_frame.pack(pady=5)

    login_username_label = Label(login_username_frame, text="Username", font=("Helvetica", 12, "bold"))
    login_username_label.pack(side=LEFT, padx=5)

    login_username_entry = Entry(login_username_frame)
    login_username_entry.pack(side=LEFT)

    # Password frame
    login_password_frame = Frame(login_window)
    login_password_frame.pack(pady=10)

    login_password_label = Label(login_password_frame, text="Password", font=("Helvetica", 12, "bold"))
    login_password_label.pack(side=LEFT, padx=10)

    login_password_entry = Entry(login_password_frame, show="*")
    login_password_entry.pack(side=LEFT)

    # Submit button
    login_submit_button = Button(login_window, text="Submit", fg="black", bg="white", command=submit_login, font=("Helvetica", 12, "bold"))
    login_submit_button.pack(pady=10)

    login_window.mainloop()
