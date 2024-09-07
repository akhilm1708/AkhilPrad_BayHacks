import customtkinter as ctk
from tkinter import messagebox, Listbox, Frame, Label, Entry, Button, Tk
import sqlite3

# Initialize main window
root = ctk.CTk()
root.title("Party Food Planner")
root.geometry("900x500")
root.configure(bg="pale goldenrod")

# Initialize database connection
conn = sqlite3.connect("party.db")

# Configure CustomTkinter (default appearance mode)
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"

# Initialize frames
UI_Frame = Frame(root)
Display_Frame = Frame(root)

# Pack frames initially
UI_Frame.pack(pady=30)
Display_Frame.pack()

def change_theme(choice):
    ctk.set_default_color_theme(choice)
    root.update_idletasks()

def group_scroll():
    if UI_Frame.winfo_exists():
        print("Clearing UI_Frame widgets")  # Debug print
        for widget in UI_Frame.winfo_children():
            if isinstance(widget, Listbox):
                widget.destroy()

        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]

        listbox = Listbox(UI_Frame, width=40, height=10)
        for table in tables:
            listbox.insert("end", table)
        listbox.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        def on_select(event):
            selection = listbox.curselection()
            if selection:
                selected_table = listbox.get(selection[0])
                display_table_contents(selected_table)

        listbox.bind("<<ListboxSelect>>", on_select)
        view_groups_label = ctk.CTkLabel(UI_Frame, text="View Groups:", font=("Helvetica", 13, 'bold'))
        view_groups_label.grid(row=9, column=0, columnspan=2, pady=(20, 0))
    else:
        print("UI_Frame does not exist in group_scroll")  # Debug print

def display_table_contents(table_name):
    if Display_Frame.winfo_exists():
        print("Clearing Display_Frame widgets")  # Debug print
        for widget in Display_Frame.winfo_children():
            widget.destroy()

        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]

        for col_num, col_name in enumerate(columns):
            label = ctk.CTkLabel(Display_Frame, text=col_name, font=("Helvetica", 12, 'bold'))
            label.grid(row=0, column=col_num, padx=5, pady=3, sticky="w")

        cursor = conn.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        for row_num, row in enumerate(rows, start=1):
            for col_num, col_value in enumerate(row):
                label_text = f"{col_value}"
                label = ctk.CTkLabel(Display_Frame, text=label_text, font=("Helvetica", 12))
                label.grid(row=row_num, column=col_num, padx=5, pady=3, sticky="w")
    else:
        print("Display_Frame does not exist in display_table_contents")  # Debug print

def show_group_form():
    print("Entering show_group_form")  # Debug print
    if UI_Frame.winfo_exists():
        print("UI_Frame exists in show_group_form")  # Debug print
        for widget in UI_Frame.winfo_children():
            widget.destroy()

        Title = ctk.CTkLabel(UI_Frame, text="Create New Group", text_color="blue", font=("Helvetica", 15, 'bold'))
        Title.grid(row=0, column=0, columnspan=2, pady=10)

        FirstName_Label = ctk.CTkLabel(UI_Frame, text="First Name: ", font=("Helvetica", 13, 'bold'))
        FirstName_Label.grid(row=1, column=0, sticky="w", padx=10)
        FirstName_Entry = ctk.CTkEntry(UI_Frame, placeholder_text="Enter your first name")
        FirstName_Entry.grid(row=1, column=1, padx=10)

        LastName_Label = ctk.CTkLabel(UI_Frame, text="Last Name: ", font=("Helvetica", 13, 'bold'))
        LastName_Label.grid(row=2, column=0, sticky="w", padx=10)
        LastName_Entry = ctk.CTkEntry(UI_Frame, placeholder_text="Enter your last name")
        LastName_Entry.grid(row=2, column=1, padx=10)

        GroupName_Label = ctk.CTkLabel(UI_Frame, text="Group Name: ", font=("Helvetica", 13, 'bold'))
        GroupName_Label.grid(row=3, column=0, sticky="w", padx=10)
        GroupName_Entry = ctk.CTkEntry(UI_Frame, placeholder_text="Enter group name")
        GroupName_Entry.grid(row=3, column=1, padx=10)

        Favfood_Label = ctk.CTkLabel(UI_Frame, text="Favorite Food: ", font=("Helvetica", 13, 'bold'))
        Favfood_Label.grid(row=4, column=0, sticky="w", padx=10)
        Favfood_Entry = ctk.CTkEntry(UI_Frame, placeholder_text="Enter favorite food")
        Favfood_Entry.grid(row=4, column=1, padx=10)

        Allergy1_Label = ctk.CTkLabel(UI_Frame, text="Allergies: ", font=("Helvetica", 13, 'bold'))
        Allergy1_Label.grid(row=5, column=0, sticky="w", padx=10)
        Allergy1_Entry = ctk.CTkEntry(UI_Frame, placeholder_text="Enter allergies")
        Allergy1_Entry.grid(row=5, column=1, padx=10)

        Allergy2_Label = ctk.CTkLabel(UI_Frame, text="Restricted Diets: ", font=("Helvetica", 13, 'bold'))
        Allergy2_Label.grid(row=6, column=0, sticky="w", padx=10)
        Allergy2_Entry = ctk.CTkEntry(UI_Frame, placeholder_text="Enter restricted diets")
        Allergy2_Entry.grid(row=6, column=1, padx=10)

        Details_Label = ctk.CTkLabel(UI_Frame, text="Any Other Details/Info: ", font=("Helvetica", 13, 'bold'))
        Details_Label.grid(row=7, column=0, sticky="w", padx=10)
        Details_Entry = ctk.CTkEntry(UI_Frame, placeholder_text="Additional details")
        Details_Entry.grid(row=7, column=1, padx=10)

        Submit_Button = ctk.CTkButton(UI_Frame, text="Submit", font=("Helvetica", 12, 'bold'), fg_color="blue",
                                      command=lambda: submit(FirstName_Entry, LastName_Entry, GroupName_Entry, Favfood_Entry, Allergy1_Entry, Allergy2_Entry, Details_Entry))
        Submit_Button.grid(row=8, column=0, columnspan=2, pady=10, ipady=5)
    else:
        print("UI_Frame does not exist in show_group_form")  # Debug print

def submit(first_name, last_name, group_name, favfood, alg1, alg2, details):
    my_firstname = first_name.get()
    my_lastname = last_name.get()
    my_group = group_name.get()
    my_favfood = favfood.get()
    my_alg1 = alg1.get()
    my_alg2 = alg2.get()
    my_details = details.get()

    cursor = conn.execute(f"PRAGMA table_info({my_group})")
    table_exists = cursor.fetchall()

    if not table_exists:
        conn.execute(f"CREATE TABLE {my_group} (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, group_name TEXT NOT NULL, favfood TEXT, alg1 TEXT, alg2 TEXT, details TEXT)")
        conn.commit()

    insert_query = f"INSERT INTO {my_group} (first_name, last_name, group_name, favfood, alg1, alg2, details) VALUES (?, ?, ?, ?, ?, ?, ?)"
    conn.execute(insert_query, (my_firstname, my_lastname, my_group, my_favfood, my_alg1, my_alg2, my_details))
    conn.commit()

    messagebox.showinfo("Success", "Group created and data submitted successfully!")
    group_scroll()

def sign_up_func():
    def new_frame():
        Login_frame.pack_forget()  # Use pack_forget instead of destroy
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
                show_group_form()
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
            show_group_form()
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

login()
root.mainloop()
