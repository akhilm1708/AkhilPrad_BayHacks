from tkinter import *
from tkinter import messagebox
import sqlite3

def sign_up_func():
    def new_frame():
        Login_frame.pack_forget()  # Use pack_forget instead of destroy
        Success_Label = Label(root, text="Welcome", font=("Helvetica", 16, "bold"))
        Success_Label.pack(expand=True)

    def submit():
        my_username = Username_Entry.get()
        my_password = Password_Entry.get()
        confirm_password = Confirm_Password_Entry.get()

        if len(my_username) >= 4 and len(my_password) >= 4:
            if my_password == confirm_password:
                conn.execute("INSERT INTO info (username, password) VALUES(?, ?)", (my_username, my_password))
                conn.commit()  # Ensure changes are saved to the database
                messagebox.showinfo(title="Success", message="Details saved!")
                new_frame()

                # Import and call the login function from the login module
                import login  # Ensure that login module is in the same directory
                login.login()  # Call the login function from the login module
            else:
                messagebox.showerror("Password Error", "Passwords do not match")
        else:
            messagebox.showerror("Input Error", "The username and password must be at least 4 characters long")

    root = Tk()
    conn = sqlite3.connect("party.db")

    # Drop the table if it already exists (for testing purposes)
    conn.execute("DROP TABLE IF EXISTS info")

    # Create the table with the correct column names
    conn.execute("CREATE TABLE IF NOT EXISTS info (username TEXT, password TEXT)")
    root.geometry("500x500")

    global Username_Entry, Password_Entry, Confirm_Password_Entry, Login_frame
    Login_frame = Frame(root)
    Login_frame.pack(expand=True)

    # Title
    Title_Label = Label(Login_frame, text="NutriFest", font=("Helvetica", 30, "bold"))
    Title_Label.pack()

    # Username frame
    username_frame = Frame(Login_frame)
    username_frame.pack(pady=5)

    Username_Label = Label(username_frame, text="Username", font=("Helvetica", 14, "bold"))
    Username_Label.pack(side=LEFT, padx=5)

    Username_Entry = Entry(username_frame)
    Username_Entry.pack(side=LEFT)

    # Password frame
    password_frame = Frame(Login_frame)
    password_frame.pack(pady=10)

    Password_Label = Label(password_frame, text="Password", font=("Helvetica", 14, "bold"))
    Password_Label.pack(side=LEFT, padx=10)

    Password_Entry = Entry(password_frame, show="*")
    Password_Entry.pack(side=LEFT)

    # Confirm Password frame
    confirm_password_frame = Frame(Login_frame)
    confirm_password_frame.pack(pady=10)

    Confirm_Password_Label = Label(confirm_password_frame, text="Confirm Password", font=("Helvetica", 14, "bold"))
    Confirm_Password_Label.pack(side=LEFT, padx=10)

    Confirm_Password_Entry = Entry(confirm_password_frame, show="*")
    Confirm_Password_Entry.pack(side=LEFT)

    Submit_button = Button(Login_frame, text="Next", fg="black", bg="white", command=submit, font=("Helvetica", 16, "bold"))
    Submit_button.pack(pady=10)

    root.mainloop()
