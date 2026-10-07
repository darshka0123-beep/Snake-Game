from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 125
SPACE_SIZE = 100
BODY_PARTS = 4
WORM_COLOR = "#E31196"
CUPCAKE_COLOR = "#F40B0B"
BACKGROUND_COLOR = "#000000"
NORMAL_SPEED = 125
BOOST_SPEED = 50
is_boosted = False

class Worm:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=WORM_COLOR, tag="worm")
            self.squares.append(square)




class Cupcake:

    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) -1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=CUPCAKE_COLOR, tag="cupcake")





def next_turn(worm, cupcake):
    x, y = worm.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE


    worm.coordinates.insert(0,(x,y))

    square = canvas.create_rectangle(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill=WORM_COLOR)

    worm.squares.insert(0, square)

    if x == cupcake.coordinates[0] and y == cupcake.coordinates[1]:

        global score

        score+=1

        label.config(text="Score:{}".format(score))
        canvas.delete("cupcake")
        cupcake = Cupcake()


    else: 
        del worm.coordinates[-1]
        canvas.delete(worm.squares[-1])
        del worm.squares[-1]

    if check_collisions(worm):
        game_over()
    else:
        current_speed = BOOST_SPEED if is_boosted else NORMAL_SPEED
        game_loop = window.after(current_speed, next_turn, worm, cupcake)


def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction =='right':
        if direction != 'left':
            direction = new_direction

    elif new_direction =='up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

    

def check_collisions(worm):
    x, y, = worm.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y>= GAME_HEIGHT:
        return True

    for body_part in worm.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
        



def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height()/2, font=('Helvetica', 70), text="Game Over :(", fill="red", tag="gameover")

def restart_game(event=None):
    global score, direction, worm, cupcake, is_game_over

    canvas.delete(ALL)
    score = 0
    direction = 'down'
    is_game_over = False
    label.config(text=f"Score: {score}")

    worm = Worm()
    cupcake = Cupcake()
    next_turn(worm, cupcake)

def start_boost(event):
    global is_boosted
    is_boosted = True

def stop_boost(event):
    global is_boosted
    is_boosted = False

window = Tk()
window.title("Cupcake Game!!")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('console', 40))
label.pack()

restart_btn = Button(window, text="Restart", font=('console', 20), command=restart_game)
restart_btn.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2)) - 50

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction("up"))
window.bind('<Down>', lambda event: change_direction("down"))
window.bind('<a>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))
window.bind('<KeyPress-space>', start_boost)
window.bind('<KeyRelease-space>', stop_boost)

worm = Worm()
cupcake = Cupcake()

next_turn(worm, cupcake)

window.mainloop() 

window.bind('<r>', restart_game)
