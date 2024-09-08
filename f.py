import tkinter as tk
import customtkinter as ctk
from c import YourCustomClass  # Ensure this is imported after Tkinter is initialized

def main():
    root = tk.Tk()
    root.title("Your App Title")
    
    # Initialize customtkinter
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    # Create an instance of your main application class
    app = YourCustomClass(root)
    
    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
