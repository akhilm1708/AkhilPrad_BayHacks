import customtkinter as ctk
from tkinter import messagebox, Entry, Button, Label, Frame
import sqlite3

# Initialize main window
root = ctk.CTk()
root.title("Party Food Planner")
root.geometry("900x500")
root.configure(bg="pale goldenrod")

# Initialize database connection
conn = sqlite3.connect("party.db")

# Configure CustomTkinter
ctk.set_appearance_mode("System")

def sign_up_func():
    def new_frame():
        Signup_frame.pack_forget()  # Use pack_forget instead of destroy
        Success_Label = Label(root, text="Welcome", font=("Helvetica", 16, "bold"))
        Success_Label.pack(expand=True)

    def submit():
        my_username = Username_Entry.get()
        my_password = Password_Entry.get()
        confirm_password = Confirm_Password_Entry.get()

        if my_password == confirm_password:
            cursor = conn.execute("SELECT * FROM info WHERE username = ?", (my_username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
            else:
                conn.execute("INSERT INTO info (username, password) VALUES (?, ?)", (my_username, my_password))
                conn.commit()
                new_frame()
       
        else:
            messagebox.showerror("Error", "Passwords do not match")

    for widget in root.winfo_children():
        widget.destroy()

    Signup_frame = Frame(root, bg="light blue")
    Signup_frame.pack(pady=30)

    Label(root, text="SIGN UP", font=("Helvetica", 16, 'bold')).pack()

    Username_Label = Label(Signup_frame, text="Create Username: ", font=("Helvetica", 12, 'bold'))
    Username_Label.grid(row=1, column=0)
    Username_Entry = Entry(Signup_frame)
    Username_Entry.grid(row=1, column=1)

    Password_Label = Label(Signup_frame, text="Create Password: ", font=("Helvetica", 12, 'bold'))
    Password_Label.grid(row=2, column=0)
    Password_Entry = Entry(Signup_frame, show="*")
    Password_Entry.grid(row=2, column=1)

    Confirm_Password_Label = Label(Signup_frame, text="Confirm Password: ", font=("Helvetica", 12, 'bold'))
    Confirm_Password_Label.grid(row=3, column=0)
    Confirm_Password_Entry = Entry(Signup_frame, show="*")
    Confirm_Password_Entry.grid(row=3, column=1)

    Submit_Button = Button(Signup_frame, text="Sign Up", font=("Helvetica", 12, 'bold'), bg="blue", fg="white",
                           command=submit)
    Submit_Button.grid(row=4, column=0, columnspan=2, pady=10)

    Login_link = Label(Signup_frame, text="Already have an account? Login here", font=("Helvetica", 10), fg="blue")
    Login_link.grid(row=5, column=0, columnspan=2)
    Login_link.bind("<Button-1>", lambda event: login())

def login():
    def new_frame():
        Login_frame.pack_forget()  # Use pack_forget instead of destroy
        Success_Label = Label(root, text="Login Successful", font=("Helvetica", 16, "bold"))
        Success_Label.pack(expand=True)

    def submit():
        my_username = Username_Entry.get()
        my_password = Password_Entry.get()

        cursor = conn.execute("SELECT * FROM info WHERE username = ? AND password = ?", (my_username, my_password))
        result = cursor.fetchone()

        if result:
            new_frame()
        else:
            messagebox.showerror("Error", "Invalid login credentials")

    for widget in root.winfo_children():
        widget.destroy()

    Login_frame = Frame(root, bg="light blue")
    Login_frame.pack(pady=30)

    Label(root, text="LOGIN", font=("Helvetica", 16, 'bold')).pack()

    Username_Label = Label(Login_frame, text="Username: ", font=("Helvetica", 12, 'bold'))
    Username_Label.grid(row=1, column=0)
    Username_Entry = Entry(Login_frame)
    Username_Entry.grid(row=1, column=1)

    Password_Label = Label(Login_frame, text="Password: ", font=("Helvetica", 12, 'bold'))
    Password_Label.grid(row=2, column=0)
    Password_Entry = Entry(Login_frame, show="*")
    Password_Entry.grid(row=2, column=1)

    Submit_Button = Button(Login_frame, text="Login", font=("Helvetica", 12, 'bold'), bg="blue", fg="white",
                           command=submit)
    Submit_Button.grid(row=3, column=0, columnspan=2, pady=10)

    Signup_link = Label(Login_frame, text="Don't have an account? Sign up here", font=("Helvetica", 10), fg="blue")
    Signup_link.grid(row=4, column=0, columnspan=2)
    Signup_link.bind("<Button-1>", lambda event: sign_up_func())

# Start with login
login()

# Run the application
root.mainloop()

# Close the database connection
conn.close()
