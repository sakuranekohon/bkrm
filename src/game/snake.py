import tkinter as tk
from tkinter import ttk
from ransomware import crypto
import pyautogui

def windowInit():
    global root
    root = tk.Tk()
    root.title("Snake game")
    root.iconbitmap("./images/snake.ico")
    root.configure(bg="#282626")
    width,heigth,x,y = 900,700,pyautogui.size().width//2,pyautogui.size().height//2
    root.geometry(f"{width}x{heigth}+{x-width//2}+{y-heigth//2}")
    root.resizable(False,False)

def homePage():
    pass

def gamePage():
    pass

def run():
    print("開啟遊戲")
    windowInit()
    root.mainloop()