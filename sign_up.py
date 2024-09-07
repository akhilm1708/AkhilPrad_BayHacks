from tkinter import *
from tkinter import messagebox
import sqlite3

root = Tk()
conn = sqlite3.connect("party.db")
root.geometry("500x500")

def new_frame():
    Login_frame.pack_forget()  # Use pack_forget instead of destroy
    Success_Label = Label(root, text="welcome", font=("Helvetica", 16, "bold"))
    Success_Label.pack(expand=True)

def submit():
    my_username = Username_Entry.get()
    my_password = Password_Entry.get()
    conn.execute("INSERT INTO info (username, password) VALUES(?, ?)", (my_username, my_password))
    conn.commit()  # Ensure changes are saved to the database

    if len(my_username) >= 4 and len(my_password) >= 4:
        messagebox.showinfo(title = "Success", message = "Details saved!")

    else:
        messagebox.showerror("The username and password must be above 4 characters")

def sign_up():
    global Username_Entry, Password_Entry, Login_frame
    Login_frame = Frame(root)
    Login_frame.pack(expand=True)

    #Title
    Title_Label = Label(Login_frame, text = "NutriFest", font = ("Helvetica", 30, "bold"))
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

    Submit_button = Button(Login_frame, text="Next", fg="black", bg="white", command=submit, font=("Helvetica", 16, "bold"))
    Submit_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__": 
    sign_up()

