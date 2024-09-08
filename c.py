import customtkinter as ctk

class YourCustomClass:
    def __init__(self, root):
        self.root = root
        
        # Example of creating a button
        self.button = ctk.CTkButton(root, text="Example Button", command=self.example_command)
        self.button.pack()
    
    def example_command(self):
        print("Button clicked")
