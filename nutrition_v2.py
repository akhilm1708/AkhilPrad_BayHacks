from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog  # For prompting username
import sqlite3

# Database connection
conn = sqlite3.connect("hello.db")
root = Tk()
root.title("Party Food Planner")
root.geometry("1000x600")
root.configure(bg="pale goldenrod")

# Store the user's group name
user_group = StringVar()

# Prompt user for group name on startup
def prompt_for_group():
    group_name = simpledialog.askstring("Group Login", "Enter your group name:")
    if group_name:
        user_group.set(group_name)
        group_scroll()  # After login, show only the user's group
    else:
        messagebox.showerror("Error", "Group name is required.")
        root.quit()

# Function to display only tables with the entered group name
def group_scroll():
    # Clear any existing Listbox
    for widget in UI_Frame.winfo_children():
        if isinstance(widget, Listbox):
            widget.destroy()

    # Fetch the group name entered by the user at login
    group_name = user_group.get()
    cursor = conn.execute(f"SELECT name FROM sqlite_master WHERE type='table';")
    tables = []
    
    # Iterate over all tables and check if they belong to the user's group
    for table in cursor.fetchall():
        # Check if the table has a "group_name" column
        cursor_check = conn.execute(f"PRAGMA table_info({table[0]})")
        columns = [column[1] for column in cursor_check.fetchall()]
        if "group_name" in columns:
            # Check if the table has the user's group name in it
            cursor_user_check = conn.execute(f"SELECT group_name FROM {table[0]} LIMIT 1")
            result = cursor_user_check.fetchone()
            if result and result[0] == group_name:
                tables.append(table[0])

    # Populate the listbox with filtered tables
    if tables:
        listbox = Listbox(UI_Frame, width=30, height=10, font="Helvetica 12", bg="ivory", fg="black")
        for table in tables:
            listbox.insert(END, table)
        listbox.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        # Define selection action
        def on_select(event):
            selection = listbox.curselection()
            if selection:
                selected_table = listbox.get(selection[0])
                display_table_contents(selected_table)

        listbox.bind("<<ListboxSelect>>", on_select)
    else:
        # If no tables match the user's group, display a message
        no_groups_label = Label(UI_Frame, text="No groups available for this user.", font="Helvetica 12 bold", bg="pale goldenrod")
        no_groups_label.grid(row=10, column=0, columnspan=2, pady=10)

    # Display the "View Groups" label
    view_groups_label = Label(UI_Frame, text="View Groups:", font="Helvetica 13 bold", bg="pale goldenrod")
    view_groups_label.grid(row=9, column=0, columnspan=2, pady=(20, 0))

# Function to display the contents of the selected table
def display_table_contents(table_name):
    for widget in Display_Frame.winfo_children():
        widget.destroy()

    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]

    for col_num, col_name in enumerate(columns):
        label = Label(Display_Frame, text=col_name, font="Helvetica 12 bold", bg="light yellow", anchor=W)
        label.grid(row=0, column=col_num, padx=5, pady=3)

    cursor = conn.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    for row_num, row in enumerate(rows, start=1):
        for col_num, col_value in enumerate(row):
            label_text = f"{col_value}"
            label = Label(Display_Frame, text=label_text, font="Helvetica 12", bg="white", anchor=W)
            label.grid(row=row_num, column=col_num, padx=5, pady=3)

# Submit function to add data to the selected group
def submit():
    my_firstname = FirstName_Entry.get()
    my_lastname = LastName_Entry.get()
    my_group = user_group.get()  # Use the group name provided by the user at login
    my_favfood = Favfood_Entry.get()
    my_alg1 = Allergy1_Entry.get()
    my_alg2 = Allergy2_Entry.get()
    my_details = Details_Entry.get()
    
    # Create the table if it doesn't exist for this group
    cursor = conn.execute(f"PRAGMA table_info({my_group})")
    table_exists = cursor.fetchall()

    if not table_exists:
        conn.execute(f"CREATE TABLE {my_group} (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, group_name TEXT NOT NULL, favfood TEXT, alg1 TEXT, alg2 TEXT, details TEXT)")
        conn.commit()

    insert_query = f"INSERT INTO {my_group} (first_name, last_name, group_name, favfood, alg1, alg2, details) VALUES (?, ?, ?, ?, ?, ?, ?)"
    conn.execute(insert_query, (my_firstname, my_lastname, my_group, my_favfood, my_alg1, my_alg2, my_details))
    conn.commit()

    messagebox.showinfo("Success", "Data submitted successfully!")
    group_scroll()

# UI setup
UI_Frame = Frame(root, bg="pale goldenrod")
UI_Frame.grid(row=0, column=0, padx=20, pady=10, sticky=N)

Title = Label(UI_Frame, text="Party Food Planner", fg='blue', font="Helvetica 16 bold", bg="pale goldenrod")
Title.grid(row=0, column=0, columnspan=2, pady=10)

# Labels and Entry fields for the form
fields = [("First Name: ", "FirstName_Entry"), ("Last Name: ", "LastName_Entry"),
          ("Favorite Food: ", "Favfood_Entry"), ("Allergies: ", "Allergy1_Entry"),
          ("Restricted Diets: ", "Allergy2_Entry"), ("Any Other Details/Info: ", "Details_Entry")]

for i, (label_text, var_name) in enumerate(fields, start=1):
    globals()[f"{var_name}_Label"] = Label(UI_Frame, text=label_text, font="Helvetica 13 bold", bg="pale goldenrod")
    globals()[f"{var_name}_Label"].grid(row=i, column=0, sticky=W, padx=10)
    globals()[f"{var_name}"] = Entry(UI_Frame, font="Helvetica 12", bg="ivory")
    globals()[f"{var_name}"].grid(row=i, column=1, padx=10)

# Submit button
Submit_Button = Button(UI_Frame, text="Submit", font="Helvetica 12 bold", fg='white', bg='blue', command=submit)
Submit_Button.grid(row=7, column=0, columnspan=2, pady=10, ipady=5)

# Frame to display selected table contents
Display_Frame = Frame(root, bg="light gray", relief=GROOVE, bd=2)
Display_Frame.grid(row=0, column=1, padx=20, pady=10, sticky=N+S+E+W)

# Prompt user for group on startup
root.after(100, prompt_for_group)

root.mainloop()
