import customtkinter as ctk
from tkinter import Menu, messagebox
import sqlite3
import uuid
import pyperclip  # Make sure to install this library using `pip install pyperclip`

class PartyFoodPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Party Food Planner")
        self.root.geometry("900x500")
        self.root.configure(bg="pale goldenrod")

        # Initialize database connection
        self.conn = sqlite3.connect("hello.db")

        # Configure CustomTkinter (default appearance mode)
        ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"

        # Create menu bar
        self.create_menu()

        # UI setup
        self.UI_Frame = ctk.CTkFrame(root, width=400, height=500)
        self.UI_Frame.grid(row=1, column=0, padx=10, pady=10)

        self.Display_Frame = ctk.CTkFrame(root, bg_color="white", width=500, height=500)
        self.Display_Frame.grid(row=1, column=1, rowspan=10, padx=20, pady=10, sticky="nsew")

        # Display "Find or Create" on screen
        self.display_find_create_options()

    def create_menu(self):
        menubar = Menu(self.root)

        settings_menu = Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Change Theme", command=self.open_theme_selection)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        home_menu = Menu(menubar, tearoff=0)
        home_menu.add_command(label="Home", command=self.show_home_page)
        menubar.add_cascade(label="Home", menu=home_menu)

        self.root.config(menu=menubar)

    def open_theme_selection(self):
        theme_window = ctk.CTkToplevel(self.root)
        theme_window.title("Select Theme")
        theme_window.geometry("450x450")

        theme_label = ctk.CTkLabel(theme_window, text="Select Theme:", font=("Helvetica", 12, 'bold'))
        theme_label.pack(pady=10)

        theme_options = ["Light", "Dark", "System"]
        theme_dropdown = ctk.CTkOptionMenu(theme_window, values=theme_options, command=self.change_theme)
        theme_dropdown.pack(pady=10)

    def change_theme(self, choice):
        ctk.set_appearance_mode(choice)
        self.root.update_idletasks()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def group_scroll(self):
        self.clear_frame(self.UI_Frame)
        self.clear_frame(self.Display_Frame)

        back_button = ctk.CTkButton(self.UI_Frame, text="Back to Home", command=self.show_home_page)
        back_button.grid(row=0, column=0, padx=10, pady=10)

        search_label = ctk.CTkLabel(self.UI_Frame, text="Search Group Name:", font=("Helvetica", 12, 'bold'))
        search_label.grid(row=1, column=0, padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(self.UI_Frame, placeholder_text="Enter group name")
        self.search_entry.grid(row=1, column=1, padx=10, pady=5)

        search_button = ctk.CTkButton(self.UI_Frame, text="Find Group", command=self.find_group)
        search_button.grid(row=1, column=2, padx=10, pady=5)

        self.details_label = ctk.CTkLabel(self.UI_Frame, text="", font=("Helvetica", 12))
        self.details_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def find_group(self):
        group_name = self.search_entry.get()
        cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]

        if group_name in tables:
            self.selected_group = group_name
            self.check_user_allergies(group_name)
        else:
            messagebox.showwarning("Not Found", f"Group '{group_name}' does not exist.")
            self.details_label.configure(text="")

    def check_user_allergies(self, group_name):
        cursor = self.conn.execute(f"SELECT * FROM {group_name}")
        rows = cursor.fetchall()

        if not rows:
            messagebox.showwarning("No Data", f"No data found for group '{group_name}'.")
            return

        first_user = rows[0]
        user_id, first_name, last_name, group_name, favfood, alg1, alg2, details = first_user

        if not alg1 or not alg2:
            self.prompt_allergy_update(group_name, user_id, alg1, alg2)
        else:
            self.display_table_contents(group_name)
            self.details_label.configure(text=f"Group '{group_name}' found. You have access to the party.")
            add_entry_button = ctk.CTkButton(self.UI_Frame, text="Add Entry", font=("Helvetica", 12), command=self.show_add_entry_form)
            add_entry_button.grid(row=3, column=0, columnspan=3, pady=10)

    def prompt_allergy_update(self, group_name, user_id, alg1, alg2):
        def update_allergies():
            new_alg1 = alg1_entry.get()
            new_alg2 = alg2_entry.get()

            self.conn.execute(f"UPDATE {group_name} SET alg1 = ?, alg2 = ? WHERE id = ?", (new_alg1, new_alg2, user_id))
            self.conn.commit()

            messagebox.showinfo("Updated", "Allergy information updated successfully!")
            self.display_table_contents(group_name)

        update_window = ctk.CTkToplevel(self.root)
        update_window.title("Update Allergy Information")
        update_window.geometry("300x200")

        alg1_label = ctk.CTkLabel(update_window, text="Allergy 1:", font=("Helvetica", 12))
        alg1_label.pack(pady=5)
        alg1_entry = ctk.CTkEntry(update_window, placeholder_text="Enter Allergy 1")
        alg1_entry.pack(pady=5)

        alg2_label = ctk.CTkLabel(update_window, text="Allergy 2:", font=("Helvetica", 12))
        alg2_label.pack(pady=5)
        alg2_entry = ctk.CTkEntry(update_window, placeholder_text="Enter Allergy 2")
        alg2_entry.pack(pady=5)

        submit_button = ctk.CTkButton(update_window, text="Submit", command=update_allergies)
        submit_button.pack(pady=10)

    def display_table_contents(self, table_name):
        self.clear_frame(self.Display_Frame)

        cursor = self.conn.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]

        for col_num, col_name in enumerate(columns):
            label = ctk.CTkLabel(self.Display_Frame, text=col_name, font=("Helvetica", 12, 'bold'))
            label.grid(row=0, column=col_num, padx=5, pady=3, sticky="w")

        cursor = self.conn.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        for row_num, row in enumerate(rows, start=1):
            for col_num, col_value in enumerate(row):
                label = ctk.CTkLabel(self.Display_Frame, text=f"{col_value}", font=("Helvetica", 12))
                label.grid(row=row_num, column=col_num, padx=5, pady=3, sticky="w")

    def show_add_entry_form(self):
        self.clear_frame(self.UI_Frame)
        self.clear_frame(self.Display_Frame)

        back_button = ctk.CTkButton(self.UI_Frame, text="Back to Home", command=self.show_home_page)
        back_button.grid(row=0, column=0, padx=10, pady=10)

        Title = ctk.CTkLabel(self.UI_Frame, text="Add New Entry", text_color="blue", font=("Helvetica", 15, 'bold'))
        Title.grid(row=1, column=0, columnspan=2, pady=10)

        self.create_add_entry_fields()

        Confirm_Button = ctk.CTkButton(self.UI_Frame, text="Confirm", font=("Helvetica", 12, 'bold'), fg_color="blue", command=self.add_entry)
        Confirm_Button.grid(row=9, column=0, columnspan=2, pady=10, ipady=5)

    def create_add_entry_fields(self):
        self.FirstName_Entry = self.create_entry("First Name: ", 2)
        self.LastName_Entry = self.create_entry("Last Name: ", 3)
        self.Favfood_Entry = self.create_entry("Favorite Food: ", 4)
        self.Allergy1_Entry = self.create_entry("Allergies: ", 5)
        self.Allergy2_Entry = self.create_entry("Restricted Diets: ", 6)
        self.Details_Entry = self.create_entry("Any Other Details/Info: ", 7)

    def add_entry(self):
        my_firstname = self.FirstName_Entry.get()
        my_lastname = self.LastName_Entry.get()
        my_groupname = self.selected_group
        my_favfood = self.Favfood_Entry.get()
        my_allergy1 = self.Allergy1_Entry.get()
        my_allergy2 = self.Allergy2_Entry.get()
        my_details = self.Details_Entry.get()

        if not my_firstname or not my_lastname or not my_groupname or not my_favfood:
            messagebox.showwarning("Missing Information", "Please fill out all required fields.")
            return

        self.conn.execute(f"""
            INSERT INTO {my_groupname} (firstname, lastname, groupname, favfood, alg1, alg2, details)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (my_firstname, my_lastname, my_groupname, my_favfood, my_allergy1, my_allergy2, my_details))
        self.conn.commit()

        messagebox.showinfo("Entry Added", "New entry added successfully!")

    def show_copy_group_name_dialog(self, group_name):
        copy_dialog = ctk.CTkToplevel(self.root)
        copy_dialog.title("Group Created")
        copy_dialog.geometry("300x150")

        label = ctk.CTkLabel(copy_dialog, text=f"Group '{group_name}' created successfully!", font=("Helvetica", 12))
        label.pack(pady=10)

        def copy_to_clipboard():
            pyperclip.copy(group_name)
            messagebox.showinfo("Copied", "Group name copied to clipboard!")

        copy_button = ctk.CTkButton(copy_dialog, text="Copy to Clipboard", command=copy_to_clipboard)
        copy_button.pack(pady=10)

    def create_group_table(self):
        generated_group_name = f"party_{str(uuid.uuid4())[:8]}"  # Generate unique group name
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {generated_group_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                groupname TEXT NOT NULL,
                favfood TEXT NOT NULL,
                alg1 TEXT,
                alg2 TEXT,
                details TEXT
            )""")
        self.conn.commit()

        self.show_copy_group_name_dialog(generated_group_name)
        self.selected_group = generated_group_name
        self.show_add_entry_form()

    def show_home_page(self):
        self.clear_frame(self.UI_Frame)
        self.clear_frame(self.Display_Frame)

        find_group_button = ctk.CTkButton(self.UI_Frame, text="Find Group", command=self.group_scroll)
        find_group_button.grid(row=1, column=0, padx=10, pady=10)

        create_group_button = ctk.CTkButton(self.UI_Frame, text="Create Group", command=self.create_group_table)
        create_group_button.grid(row=2, column=0, padx=10, pady=10)

        self.details_label = ctk.CTkLabel(self.UI_Frame, text="", font=("Helvetica", 12))
        self.details_label.grid(row=3, column=0, padx=10, pady=10)

    def create_entry(self, label_text, row):
        label = ctk.CTkLabel(self.UI_Frame, text=label_text, font=("Helvetica", 12))
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = ctk.CTkEntry(self.UI_Frame)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        return entry

    def display_find_create_options(self):
        # This method sets up the initial UI for finding or creating a group
        self.clear_frame(self.UI_Frame)
        self.clear_frame(self.Display_Frame)

        find_group_button = ctk.CTkButton(self.UI_Frame, text="Find Group", command=self.group_scroll)
        find_group_button.grid(row=1, column=0, padx=10, pady=10)

        create_group_button = ctk.CTkButton(self.UI_Frame, text="Create Group", command=self.create_group_table)
        create_group_button.grid(row=2, column=0, padx=10, pady=10)

        self.details_label = ctk.CTkLabel(self.UI_Frame, text="", font=("Helvetica", 12))
        self.details_label.grid(row=3, column=0, padx=10, pady=10)

if __name__ == "__main__":
    root = ctk.CTk()  # Make sure to initialize CTk root here
    app = PartyFoodPlanner(root)
    root.mainloop()
