from tkinter import ttk

def run():
    style = ttk.Style()
    
    homeFont = ("Comic Sans MS", 30, "bold")
    style.configure("homeBTN.TButton",
                    foreground="#000000",
                    background="#FFFFFF",
                    font=homeFont)
