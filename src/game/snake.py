import tkinter as tk
from tkinter import ttk
#from ransomware import crypto
import pyautogui
from PIL import Image, ImageTk

def styles():
    style = ttk.Style()
    
    style.configure("homeBTN.TButton",
                    foreground="#000000",
                    background="#FFFFFF",
                    font=("Comic Sans MS", 20, "bold"))
    
    style.configure("gameLabel.TLabel",
                    foreground="#FFFFFF",
                    background="#282626",
                    font=("Comic Sans MS", 24))
    
    style.configure("pauseLabel.TLabel",
                    foreground="#000000",
                    background="#D9D9D9",
                    font=("Comic Sans MS", 20, "bold"))
    
    style.configure("pauseBTN.TButton",
                    foreground="#000000",
                    background="#D9D9D9",
                    font=("Comic Sans MS", 20, "bold"))

def windowInit():
    global root
    root = tk.Tk()
    root.title("Snake game")
    root.iconbitmap("./images/snake.ico")
    root.configure(bg="#282626")
    width,heigth,x,y = 900,700,pyautogui.size().width//2,pyautogui.size().height//2
    root.geometry(f"{width}x{heigth}+{x-width//2}+{y-heigth//2}")
    root.resizable(False,False)

    homePage()

def clearWindow():
    for widget in root.winfo_children():
        widget.destroy()

def homePage():
    global img
    def play():
        gamePage()
    def exit():
        root.destroy()

    clearWindow()

    letfFrame = tk.Frame(root,width=250,height=700,bg="#282626")
    rightFrame = tk.Frame(root,width=650,height=700,bg="#FFFFFF")

    letfFrame.pack(side="left",fill="both")
    rightFrame.pack(side="right")
    root.update_idletasks()

    playBTN = ttk.Button(letfFrame,text="Play",style="homeBTN.TButton",command=play)
    exitBTN = ttk.Button(letfFrame,text="Exit",style="homeBTN.TButton",command=exit)
    padxV,padyV = 20,20
    playBTN.pack(side="top",padx=padxV,pady=padyV)
    exitBTN.pack(side="bottom",padx=padxV,pady=padyV)
    
    img = Image.open("./images/snake.png")
    img = img.resize((rightFrame.winfo_width(),rightFrame.winfo_height()))
    img = ImageTk.PhotoImage(img)
    imageLabel = ttk.Label(rightFrame,image=img)
    imageLabel.image = img
    imageLabel.pack()
    
def gamePage():
    clearWindow()
    
    scoreLabel = ttk.Label(root,text="Score:0",style="gameLabel.TLabel")
    gameCanve = tk.Canvas(root,width=800,height=600,bg="#32EBFF")
    scoreLabel.pack(padx=50,pady=5,anchor="nw")
    gameCanve.pack(padx=50,pady=(5,25))

    for x in range(0,800,40):
        gameCanve.create_line(x,0,x,600,width=2,fill="#FFFFFF")
    for y in range(0,600,40):
        gameCanve.create_line(0,y,800,y,width=2,fill="#FFFFFF")

    pauseFrame = tk.Frame(root,width=450,height=300,bg="#FFFFFF")
    pauseFrame.place(x=225,y=200)
    pTitle = ttk.Label(pauseFrame,text="Game Pause",style="pauseLabel.TLabel")
    pCancel = ttk.Button(pauseFrame,text="Cancel",style="pauseBTN.TButton")

def run():
    print("Game start")
    windowInit()
    styles()
    root.mainloop()

if __name__ == "__main__":
    run()