import customtkinter as ctk
from tkinter import messagebox, Menu
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
        # Create a menu bar
        menubar = Menu(self.root)

        # Create a 'Settings' menu
        settings_menu = Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Change Theme", command=self.open_theme_selection)

        # Add 'Settings' menu to the menu bar
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # Create a 'Home' menu
        home_menu = Menu(menubar, tearoff=0)
        home_menu.add_command(label="Home", command=self.show_home_page)

        # Add 'Home' menu to the menu bar
        menubar.add_cascade(label="Home", menu=home_menu)

        # Set the menu bar to the root window
        self.root.config(menu=menubar)

    def open_theme_selection(self):
        # Create a new top-level window for theme selection
        theme_window = ctk.CTkToplevel(self.root)
        theme_window.title("Select Theme")
        theme_window.geometry("450x450")

        theme_label = ctk.CTkLabel(theme_window, text="Select Theme:", font=("Helvetica", 12, 'bold'))
        theme_label.pack(pady=10)

        theme_options = ["Light", "Dark", "System"]
        theme_dropdown = ctk.CTkOptionMenu(theme_window, values=theme_options, command=self.change_theme)
        theme_dropdown.pack(pady=10)

    def change_theme(self, choice):
        """Change the theme of the application."""
        ctk.set_appearance_mode(choice)  # Change between "Light", "Dark", "System"
        self.root.update_idletasks()

    def clear_frame(self, frame):
        """Clear all widgets from a frame."""
        for widget in frame.winfo_children():
            widget.destroy()

    def group_scroll(self):
        # Clear both frames before loading new content
        self.clear_frame(self.UI_Frame)
        self.clear_frame(self.Display_Frame)

        # Add a 'Back to Home' button
        back_button = ctk.CTkButton(self.UI_Frame, text="Back to Home", command=self.show_home_page)
        back_button.grid(row=0, column=0, padx=10, pady=10)

        # Search field for entering a group name
        search_label = ctk.CTkLabel(self.UI_Frame, text="Search Group Name:", font=("Helvetica", 12, 'bold'))
        search_label.grid(row=1, column=0, padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(self.UI_Frame, placeholder_text="Enter group name")
        self.search_entry.grid(row=1, column=1, padx=10, pady=5)

        search_button = ctk.CTkButton(self.UI_Frame, text="Find Group", command=self.find_group)
        search_button.grid(row=1, column=2, padx=10, pady=5)

        # Label to show group details
        self.details_label = ctk.CTkLabel(self.UI_Frame, text="", font=("Helvetica", 12))
        self.details_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def find_group(self):
        group_name = self.search_entry.get()

        # Check if the group exists in the database
        cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]

        if group_name in tables:
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

        # Assume we are checking the first user's allergies (could be extended for multiple users)
        first_user = rows[0]
        user_id, first_name, last_name, group_name, favfood, alg1, alg2, details = first_user

        if not alg1 or not alg2:
            # Prompt user to enter allergy info
            self.prompt_allergy_update(group_name, user_id, alg1, alg2)
        else:
            # Display table contents if allergies are present
            self.display_table_contents(group_name)
            self.details_label.configure(text=f"Group '{group_name}' found. You have access to the party.")

    def prompt_allergy_update(self, group_name, user_id, alg1, alg2):
        # Prompt the user to enter allergy information
        def update_allergies():
            new_alg1 = alg1_entry.get()
            new_alg2 = alg2_entry.get()

            # Update the database with new allergy information
            self.conn.execute(f"UPDATE {group_name} SET alg1 = ?, alg2 = ? WHERE id = ?", (new_alg1, new_alg2, user_id))
            self.conn.commit()

            messagebox.showinfo("Updated", "Allergy information updated successfully!")
            self.display_table_contents(group_name)

        # Create a new top-level window for allergy update
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
        # Clear the Display_Frame before showing new table contents
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
                label_text = f"{col_value}"
                label = ctk.CTkLabel(self.Display_Frame, text=label_text, font=("Helvetica", 12))
                label.grid(row=row_num, column=col_num, padx=5, pady=3, sticky="w")

    def show_group_form(self):
        # Clear both frames before showing the form
        self.clear_frame(self.UI_Frame)
        self.clear_frame(self.Display_Frame)

        # Add a 'Back to Home' button
        back_button = ctk.CTkButton(self.UI_Frame, text="Back to Home", command=self.show_home_page)
        back_button.grid(row=0, column=0, padx=10, pady=10)

        Title = ctk.CTkLabel(self.UI_Frame, text="Create New Group", text_color="blue", font=("Helvetica", 15, 'bold'))
        Title.grid(row=1, column=0, columnspan=2, pady=10)

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
        self.show_home_page()

    def display_find_create_options(self):
        find_button = ctk.CTkButton(self.UI_Frame, text="Find Group", font=("Helvetica", 12), command=self.group_scroll)
        find_button.grid(row=1, column=0, padx=10, pady=10)

        create_button = ctk.CTkButton(self.UI_Frame, text="Create Group", font=("Helvetica", 12), command=self.show_group_form)
        create_button.grid(row=1, column=1, padx=10, pady=10)

    def show_home_page(self):
        # Clear both frames before showing the home page
        self.clear_frame(self.UI_Frame)
        self.clear_frame(self.Display_Frame)

        # Display "Find or Create" options on the home page
        self.display_find_create_options()

def main():
    root = ctk.CTk()
    app = PartyFoodPlanner(root)
    root.mainloop()
    app.conn.close()

if __name__ == "__main__":
    main()
