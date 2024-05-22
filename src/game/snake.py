import tkinter as tk
from tkinter import ttk
import pyautogui
from PIL import Image, ImageTk
import random

CELL_SIZE = 20
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
GRID_WIDTH = CANVAS_WIDTH // CELL_SIZE
GRID_HEIGHT = CANVAS_HEIGHT // CELL_SIZE

class SnakeGame:
    def __init__(self, canvas, score_label):
        self.canvas = canvas
        self.score_label = score_label
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = 'Up'
        self.running = True
        self.paused = False
        self.score = 0
        self.food = self.create_food()

        self.pause_frame = None
        self.create_pause_menu()
        self.update_game()

    def create_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def change_direction(self, event):
        if event.keysym in ['Up', 'Down', 'Left', 'Right']:
            if (self.direction == 'Up' and event.keysym != 'Down') or \
               (self.direction == 'Down' and event.keysym != 'Up') or \
               (self.direction == 'Left' and event.keysym != 'Right') or \
               (self.direction == 'Right' and event.keysym != 'Left'):
                self.direction = event.keysym

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == 'Up':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'Left':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + 1, head_y)

        self.snake = [new_head] + self.snake[:-1]

    def check_collisions(self):
        head_x, head_y = self.snake[0]
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT or (head_x, head_y) in self.snake[1:]:
            self.running = False

    def check_food(self):
        if self.snake[0] == self.food:
            self.snake.append(self.snake[-1])
            self.food = self.create_food()
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")

    def draw_elements(self):
        self.canvas.delete(tk.ALL)
        for x, y in self.snake:
            self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE, fill='green')
        food_x, food_y = self.food
        self.canvas.create_rectangle(food_x * CELL_SIZE, food_y * CELL_SIZE, food_x * CELL_SIZE + CELL_SIZE, food_y * CELL_SIZE + CELL_SIZE, fill='red')

    def toggle_pause(self, event=None):
        self.paused = not self.paused
        if self.paused:
            self.show_pause_menu()
        else:
            self.hide_pause_menu()
            self.update_game()

    def create_pause_menu(self):
        self.pause_frame = tk.Frame(self.canvas, width=450, height=300, bg="#FFFFFF")
        pTitle = ttk.Label(self.pause_frame, text="Game Paused", style="pauseLabel.TLabel",anchor="center")
        pTitle.pack(pady=(0,10),fill="x")
        pResume = ttk.Button(self.pause_frame, text="Resume", style="pauseBTN.TButton", command=self.toggle_pause)
        pResume.pack(padx=10,pady=10)
        pBack = ttk.Button(self.pause_frame, text="Back", style="pauseBTN.TButton", command=self.back_to_home)
        pBack.pack(padx=10,pady=10)

    def show_pause_menu(self):
        self.pause_frame.place(x=175, y=150)
        self.pause_frame.tkraise()

    def hide_pause_menu(self):
        self.pause_frame.place_forget()

    def back_to_home(self):
        self.canvas.destroy()
        homePage()

    def update_game(self):
        if self.running and not self.paused:
            self.move_snake()
            self.check_collisions()
            self.check_food()
            self.draw_elements()
            self.canvas.after(100, self.update_game)
        elif not self.running:
            self.canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, text="Game Over", fill="white", font=('Arial', 24))

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
    root.title("Snake Game")
    root.iconbitmap("./images/snake.ico")
    root.configure(bg="#282626")
    width, height, x, y = 900, 700, pyautogui.size().width // 2, pyautogui.size().height // 2
    root.geometry(f"{width}x{height}+{x-width//2}+{y-height//2}")
    root.resizable(False, False)

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

    leftFrame = tk.Frame(root, width=250, height=700, bg="#282626")
    rightFrame = tk.Frame(root, width=650, height=700, bg="#FFFFFF")

    leftFrame.pack(side="left", fill="both")
    rightFrame.pack(side="right")
    root.update_idletasks()

    playBTN = ttk.Button(leftFrame, text="Play", style="homeBTN.TButton", command=play)
    exitBTN = ttk.Button(leftFrame, text="Exit", style="homeBTN.TButton", command=exit)
    padxV, padyV = 20, 20
    playBTN.pack(side="top", padx=padxV, pady=padyV)
    exitBTN.pack(side="bottom", padx=padxV, pady=padyV)
    
    img = Image.open("./images/snake.png")
    img = img.resize((rightFrame.winfo_width(), rightFrame.winfo_height()))
    img = ImageTk.PhotoImage(img)
    imageLabel = ttk.Label(rightFrame, image=img)
    imageLabel.image = img
    imageLabel.pack()

def gamePage():
    clearWindow()
    
    scoreLabel = ttk.Label(root, text="Score: 0", style="gameLabel.TLabel")
    gameCanvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="#32EBFF")
    scoreLabel.pack(padx=50, pady=5, anchor="nw")
    gameCanvas.pack(padx=50, pady=(5, 25))

    snake_game = SnakeGame(gameCanvas, scoreLabel)
    root.bind("<KeyPress>", snake_game.change_direction)
    root.bind("<Escape>", snake_game.toggle_pause)  # 綁定 'Esc' 鍵以切換暫停狀態

def run():
    print("Game start")
    windowInit()
    styles()
    root.mainloop()

# if __name__ == "__main__":
#     run()
