import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import customedProject  # Assuming this is a separate module you're working with

# Initialize main window
root = ctk.CTk()
root.title("Party Food Planner")
root.geometry("900x500")

# Initialize database connection
conn = sqlite3.connect("party.db")

# Create table if not exists
conn.execute('''CREATE TABLE IF NOT EXISTS info 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT NOT NULL, 
                 password TEXT NOT NULL)''')

# Configure CustomTkinter theme
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Default theme colors

def sign_up_func():
    def new_frame():
        Signup_frame.pack_forget()
        messagebox.showinfo("Success", "Sign up successful! You can now log in.")
        login()  # Redirect to login screen after successful sign-up

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
                new_frame()  # Show success message and move to login
        else:
            messagebox.showerror("Error", "Passwords do not match")

    # Clear the window for new content
    for widget in root.winfo_children():
        widget.destroy()

    Signup_frame = ctk.CTkFrame(root, corner_radius=15, width=400, height=300)
    Signup_frame.pack(pady=30)

    title_label = ctk.CTkLabel(Signup_frame, text="SIGN UP", font=ctk.CTkFont(size=20, weight="bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    Username_Label = ctk.CTkLabel(Signup_frame, text="Create Username:", font=ctk.CTkFont(size=14))
    Username_Label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    Username_Entry = ctk.CTkEntry(Signup_frame, width=200)
    Username_Entry.grid(row=1, column=1, padx=10, pady=5)

    Password_Label = ctk.CTkLabel(Signup_frame, text="Create Password:", font=ctk.CTkFont(size=14))
    Password_Label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    Password_Entry = ctk.CTkEntry(Signup_frame, show="*", width=200)
    Password_Entry.grid(row=2, column=1, padx=10, pady=5)

    Confirm_Password_Label = ctk.CTkLabel(Signup_frame, text="Confirm Password:", font=ctk.CTkFont(size=14))
    Confirm_Password_Label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    Confirm_Password_Entry = ctk.CTkEntry(Signup_frame, show="*", width=200)
    Confirm_Password_Entry.grid(row=3, column=1, padx=10, pady=5)

    Submit_Button = ctk.CTkButton(Signup_frame, text="Sign Up", font=ctk.CTkFont(size=14), command=submit)
    Submit_Button.grid(row=4, column=0, columnspan=2, pady=20)

    Login_link = ctk.CTkLabel(Signup_frame, text="Already have an account? Login here", font=ctk.CTkFont(size=12),
                              fg_color="transparent", text_color="blue", cursor="hand2")
    Login_link.grid(row=5, column=0, columnspan=2)
    Login_link.bind("<Button-1>", lambda event: login())

def login():
    def new_frame():
        Login_frame.pack_forget()
        Success_Label = ctk.CTkLabel(root, text="Login Successful!", font=ctk.CTkFont(size=20, weight="bold"))
        Success_Label.pack(expand=True)
        root.after(1000, root.destroy)  # Close the window after 1 second
        customedProject.main()  # Call to the external project function if login succeeds

    def submit():
        my_username = Username_Entry.get()
        my_password = Password_Entry.get()

        cursor = conn.execute("SELECT * FROM info WHERE username = ? AND password = ?", (my_username, my_password))
        result = cursor.fetchone()

        if result:
            new_frame()  # Successful login
        else:
            messagebox.showerror("Error", "Invalid login credentials")

    # Clear the window for new content
    for widget in root.winfo_children():
        widget.destroy()

    Login_frame = ctk.CTkFrame(root, corner_radius=15, width=400, height=300)
    Login_frame.pack(pady=30)

    title_label = ctk.CTkLabel(Login_frame, text="LOGIN", font=ctk.CTkFont(size=20, weight="bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    Username_Label = ctk.CTkLabel(Login_frame, text="Username:", font=ctk.CTkFont(size=14))
    Username_Label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    Username_Entry = ctk.CTkEntry(Login_frame, width=200)
    Username_Entry.grid(row=1, column=1, padx=10, pady=5)

    Password_Label = ctk.CTkLabel(Login_frame, text="Password:", font=ctk.CTkFont(size=14))
    Password_Label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    Password_Entry = ctk.CTkEntry(Login_frame, show="*", width=200)
    Password_Entry.grid(row=2, column=1, padx=10, pady=5)

    Submit_Button = ctk.CTkButton(Login_frame, text="Login", font=ctk.CTkFont(size=14), command=submit)
    Submit_Button.grid(row=3, column=0, columnspan=2, pady=20)

    Signup_link = ctk.CTkLabel(Login_frame, text="Don't have an account? Sign up here", font=ctk.CTkFont(size=12),
                               fg_color="transparent", text_color="blue", cursor="hand2")
    Signup_link.grid(row=4, column=0, columnspan=2)
    Signup_link.bind("<Button-1>", lambda event: sign_up_func())

# Start with login
login()

# Run the application
root.mainloop()

# Close the database connection when the app is closed
conn.close()
