import customtkinter as ctk
from tkinter import messagebox, Listbox
import sqlite3

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

        # UI setup
        self.UI_Frame = ctk.CTkFrame(root, width=400, height=500)
        self.UI_Frame.grid(row=1, column=0, padx=10, pady=10)

        self.Display_Frame = ctk.CTkFrame(root, bg_color="white", width=500, height=500)
        self.Display_Frame.grid(row=1, column=1, rowspan=10, padx=20, pady=10, sticky="nsew")

        # Add theme selection dropdown
        self.create_theme_dropdown()

        # Display "Find or Create" on screen
        self.display_find_create_options()

    def create_theme_dropdown(self):
        theme_label = ctk.CTkLabel(self.root, text="Select Theme:", font=("Helvetica", 12, 'bold'))
        theme_label.grid(row=0, column=0, padx=10, pady=10)

        theme_options = ["blue", "dark-blue", "green"]
        theme_dropdown = ctk.CTkOptionMenu(self.root, values=theme_options, command=self.change_theme)
        theme_dropdown.grid(row=0, column=1, padx=10, pady=10)

    def change_theme(self, choice):
        ctk.set_default_color_theme(choice)
        self.root.update_idletasks()

    def group_scroll(self):
        for widget in self.UI_Frame.winfo_children():
            if isinstance(widget, Listbox):
                widget.destroy()

        cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]

        listbox = Listbox(self.UI_Frame, width=40, height=10)
        for table in tables:
            listbox.insert("end", table)
        listbox.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        listbox.bind("<<ListboxSelect>>", self.on_select)
        view_groups_label = ctk.CTkLabel(self.UI_Frame, text="View Groups:", font=("Helvetica", 13, 'bold'))
        view_groups_label.grid(row=9, column=0, columnspan=2, pady=(20, 0))

    def on_select(self, event):
        selection = event.widget.curselection()
        if selection:
            selected_table = event.widget.get(selection[0])
            self.display_table_contents(selected_table)

    def display_table_contents(self, table_name):
        for widget in self.Display_Frame.winfo_children():
            widget.destroy()

        cursor = self.conn.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]

        for col_num, col_name in enumerate(columns):
            label = ctk.CTkLabel(self.Display_Frame, text=col_name, font=("Helvetica", 12, 'bold'))
            label.grid(row=0, column=col_num, padx=5, pady=3, sticky="w")

        cursor = self.conn.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        for row_num, row in enumerate(rows, start=1):
            for col_num, col_value in enumerate(row):
                label_text = f"{col_value}"
                label = ctk.CTkLabel(self.Display_Frame, text=label_text, font=("Helvetica", 12))
                label.grid(row=row_num, column=col_num, padx=5, pady=3, sticky="w")

    def show_group_form(self):
        for widget in self.UI_Frame.winfo_children():
            if isinstance(widget, Listbox):
                widget.destroy()

        Title = ctk.CTkLabel(self.UI_Frame, text="Create New Group", text_color="blue", font=("Helvetica", 15, 'bold'))
        Title.grid(row=0, column=0, columnspan=2, pady=10)

        # Form fields for creating a group
        self.create_form_fields()

        Submit_Button = ctk.CTkButton(self.UI_Frame, text="Submit", font=("Helvetica", 12, 'bold'), fg_color="blue",
                                      command=self.submit)
        Submit_Button.grid(row=8, column=0, columnspan=2, pady=10, ipady=5)

    def create_form_fields(self):
        self.FirstName_Entry = self.create_entry("First Name: ", 1)
        self.LastName_Entry = self.create_entry("Last Name: ", 2)
        self.GroupName_Entry = self.create_entry("Group Name: ", 3)
        self.Favfood_Entry = self.create_entry("Favorite Food: ", 4)
        self.Allergy1_Entry = self.create_entry("Allergies: ", 5)
        self.Allergy2_Entry = self.create_entry("Restricted Diets: ", 6)
        self.Details_Entry = self.create_entry("Any Other Details/Info: ", 7)

    def create_entry(self, label_text, row):
        label = ctk.CTkLabel(self.UI_Frame, text=label_text, font=("Helvetica", 13, 'bold'))
        label.grid(row=row, column=0, sticky="w", padx=10)
        entry = ctk.CTkEntry(self.UI_Frame, placeholder_text=f"Enter {label_text.lower()}")
        entry.grid(row=row, column=1, padx=10)
        return entry

    def submit(self):
        my_firstname = self.FirstName_Entry.get()
        my_lastname = self.LastName_Entry.get()
        my_group = self.GroupName_Entry.get()
        my_favfood = self.Favfood_Entry.get()
        my_alg1 = self.Allergy1_Entry.get()
        my_alg2 = self.Allergy2_Entry.get()
        my_details = self.Details_Entry.get()

        cursor = self.conn.execute(f"PRAGMA table_info({my_group})")
        table_exists = cursor.fetchall()

        if not table_exists:
            self.conn.execute(f"CREATE TABLE {my_group} (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, group_name TEXT NOT NULL, favfood TEXT, alg1 TEXT, alg2 TEXT, details TEXT)")
            self.conn.commit()

        insert_query = f"INSERT INTO {my_group} (first_name, last_name, group_name, favfood, alg1, alg2, details) VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.conn.execute(insert_query, (my_firstname, my_lastname, my_group, my_favfood, my_alg1, my_alg2, my_details))
        self.conn.commit()

        messagebox.showinfo("Success", "Group created and data submitted successfully!")
        self.group_scroll()

    def display_find_create_options(self):
        find_button = ctk.CTkButton(self.UI_Frame, text="Find Group", font=("Helvetica", 12), command=self.group_scroll)
        find_button.grid(row=0, column=0, padx=10, pady=10)

        create_button = ctk.CTkButton(self.UI_Frame, text="Create Group", font=("Helvetica", 12), command=self.show_group_form)
        create_button.grid(row=0, column=1, padx=10, pady=10)

def main():
    root = ctk.CTk()
    app = PartyFoodPlanner(root)
    root.mainloop()
    app.conn.close()


