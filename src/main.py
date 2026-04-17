'''
Hienas Sapecas 2D Turtle game, created exclusively by Gabriel Garib Gomes

'''

# imports
import turtle as t
from math import sqrt
import random as r


# start screen and initial settings
t.title("Hienas sapecas 2D")  # tab name
t.setup(1160, 940)  # defines screen size
t.bgpic('./sprites/startscreen.gif')  # add a start screen
t.hideturtle()

# adds the sprites
screen = t.Screen()
screen.addshape('./sprites/hyena.gif')
screen.addshape('./sprites/dreher_enemy.gif')
screen.addshape('./sprites/ecobier.gif')
screen.addshape('./sprites/coke_shot.gif')
screen.addshape('./sprites/coisa.gif')
screen.addshape('./sprites/intencion_enemy.gif')

# creates shot turtle
shot = t.Turtle()
shot.hideturtle()
shot.shape("./sprites/coke_shot.gif")
shot.penup()
shot.speed(0)

# creates character turtle
hyena = t.Turtle()
hyena.hideturtle()
hyena.penup()

# creates boss turtle
boss = t.Turtle()
boss.hideturtle()
boss.penup()
boss.speed(0)

# variable that stores game start information
started = False

# screen limits
margin_error = 50
limits = [[], []]
top = screen.window_height() // 2 - margin_error
bottom = -screen.window_height() // 2 + margin_error
left = -screen.window_width() // 2 + margin_error
right = screen.window_width() // 2 - margin_error

# protagonist data
hyena_dict = {
    'x': left,
    'y': 0,
    'lives': 3,
    'step': 30
}

# shot data
shot_dict = {
    'x': None,
    'y': None,
    'flag': True,
    'step': 20
}

# variable that stores the phase number
phase = 1

# draws the character
def draw_hyena():
    hyena.shape('./sprites/hyena.gif')
    hyena.speed(0)
    hyena.penup()
    hyena.setx(left)
    hyena.showturtle()

# creates arena and starts the game
def start_game():
    global started
    t.bgpic('./sprites/container_bar_background1.gif')
    create_enemies_dict(3)
    draw_hyena()
    draw_lives()
    draw_enemies()
    animate_enemies()
    
    started = True


# closes the game (when pressing 'q')
def close_game():
    t.bye()

# character animations (if position is greater than limit + margin of error, the function is not called when pressing the key)

def move_up():
    global hyena_dict  # allows updating the dictionary globally
    new_position_y = hyena_dict['y'] + hyena_dict['step']
    if hyena_dict['y'] < top and check_ellipse_collision(hyena_dict['x'], new_position_y, shape_format):
        hyena.sety(new_position_y)
        hyena_dict['y'] = hyena.ycor()  # updates character's y position in the dictionary


def move_down():
    global hyena_dict  # allows updating the dictionary globally
    new_position_y = hyena_dict['y'] - hyena_dict['step']
    if hyena_dict['y'] > bottom and check_ellipse_collision(hyena_dict['x'], new_position_y, shape_format):
        hyena.sety(new_position_y)
        hyena_dict['y'] = hyena.ycor()  # updates character's y position in the dictionary

def move_left():
    global hyena_dict  # allows updating the dictionary globally
    new_position_x = hyena_dict['x'] - hyena_dict['step']
    
    if hyena_dict['x'] > left and check_ellipse_collision(new_position_x, hyena_dict['y'], shape_format):
        hyena.setx(new_position_x)
        hyena_dict['x'] = hyena.xcor()  # updates character's x position in the dictionary

def move_right():
    global hyena_dict  # allows updating the dictionary globally
    new_position_x = hyena_dict['x'] + hyena_dict['step']
    if hyena_dict['x'] < right and check_ellipse_collision(new_position_x, hyena_dict['y'], shape_format):
        hyena.setx(new_position_x)
        hyena_dict['x'] = hyena.xcor()  # updates character's x position in the dictionary


# function that checks if a point is inside the ellipse (with margin of error for sprite=200)
def check_ellipse_collision(posx, posy, shape):
    if len(shape) == 4:
        elp = shape  # phase1
        if ((posx - elp[0]) ** 2) / (elp[2] ** 2) + ((posy - elp[1]) ** 2) / (elp[3] ** 2) <= 1 + (200 / elp[2]) ** 2:  # ellipse equation
            return False
        else:
            return True
    elif len(shape) == 3:  # phase2
        circ = shape
        if ((posx - circ[0]) ** 2) + ((posy - circ[1]) ** 2) <= circ[2] ** 2:
            return False
        else:
            return True


# defines the phase format as an ellipse
shape_format = (0, 20, 345, 225)

# Calculates the distance between two points using the Pythagorean Theorem
def calculate_distance(x1, y1, x2, y2):
    distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

# enemy data
enemies_data = []

# create_enemies_dict with args 2,3 arguments serve to generate enemies with position
def create_enemies_dict(num_enemies):
    global phase
    for _ in range(num_enemies):
        enemy = {'x': r.randint(-500, 500),
                'y': r.randint(-400, 400),
                'step': 20,
                }
        enemies_data.append(enemy)
    if phase == 1:
        phase = 2  # variable that allows moving to phase 2 once enemies are eliminated

enemies_list = []

# variable that defines the phase 1 sprite
sprite = './sprites/intencion_enemy.gif'

# draws the enemies
# pulls the number of enemies from the enemies_data list
def draw_enemies():
    global enemy_counter  # variable used for loops of all enemies
    for enemy_counter in range(len(enemies_data)):
        enemy = t.Turtle()
        enemy.speed(0)
        enemy.penup()
        enemy.shape(sprite)
        enemies_list.append(enemy)
        enemy.goto(enemies_data[enemy_counter]['x'], enemies_data[enemy_counter]['y'])

# boss data
def create_boss_dict():
    global boss_dict
    boss_dict = {'x': 0,
                  'y': 0,
                  'step': 5
                }

# draws the boss
def draw_boss():
    boss.showturtle()
    boss.penup()
    boss.shape('./sprites/coisa.gif')
    boss.goto(boss_dict['x'], boss_dict['y'])

# enemy movement
def chase():
    global enemy_counter  # avoids the error: local variable 'enemy_counter' referenced before assignment
    for enemy in enemies_list:
        enemy.setheading(enemy.towards(hyena) + r.uniform(-50, 50))
        if enemy_counter >= len(enemies_data):  # fixes the error of decreasing list length inside the loop
            enemy_counter -= 1
        distance = calculate_distance(hyena_dict['x'], hyena_dict['y'], enemies_data[enemy_counter]['x'], enemies_data[enemy_counter]['y'])
        if distance > 20:
            enemy.forward(enemies_data[enemy_counter]['step'])
            enemies_data[enemy_counter]['x'] = enemy.xcor()  # updates x position in dictionary
            enemies_data[enemy_counter]['y'] = enemy.ycor()  # updates y position in dictionary

# configures character lives
def lose_life():
    global hyena_dict
    for i in range(len(enemies_list)):
        if i >= len(enemies_list):  # fixes the error of decreasing list length inside the loop
            i -= 1
        if enemies_list[i].distance(hyena) < margin_error and enemies_list[i].isvisible():
            hyena_dict['lives'] -= 1
            lives[hyena_dict['lives']].hideturtle()
            enemies_list[i].hideturtle()
            enemies_list.remove(enemies_list[i])
        if hyena_dict['lives'] == 0:
            hyena_dict['step'] = 0
            game_over()
            break

# determines game over
def game_over():
    hyena.hideturtle()
    boss.hideturtle()
    for enemy in enemies_list:
        enemy.hideturtle()
    for life in lives:
        life.hideturtle()
    screen.bgpic('./sprites/gameover.gif')


# animates the enemies
def animate_enemies():
    lose_life()
    chase()
    eliminate_enemy()
    start_phase_2()
    screen.update()
    screen.ontimer(animate_enemies, 100)

# draws character lives
def draw_lives():
    global lives
    lives = []
    for i in range(4):
        heart = t.Turtle()
        heart.hideturtle()
        heart.penup()
        heart.shape('./sprites/ecobier.gif')
        heart.speed(0)
        heart.goto(left + ((i) * 50), top)
        heart.showturtle()
        lives.append(heart)
    heart.hideturtle()

# function that determines enemy death if hit by shots
def eliminate_enemy():
    global shot_dict
    for i in range(len(enemies_list)):
        if i >= len(enemies_list):
            i -= 1
        if enemies_list[i].distance(shot) < margin_error and shot.isvisible():
            enemies_list[i].hideturtle()
            enemies_list.remove(enemies_list[i])
            shot.hideturtle()
            shot_dict['flag'] = True


# functions assigned to keys
def shoot_up():
    if started and shot_dict['flag']:
        shot.goto(hyena_dict['x'], hyena_dict['y'] + margin_error)
        move_shot_up()

def shoot_down():
    if started and shot_dict['flag']:
        shot.goto(hyena_dict['x'], hyena_dict['y'] - margin_error)
    move_shot_down()

def shoot_left():
    if started and shot_dict['flag']:
        shot.goto(hyena_dict['x'] - margin_error, hyena_dict['y'])
    move_shot_left()

def shoot_right():
    if started and shot_dict['flag']:
        shot.goto(hyena_dict['x'] + margin_error, hyena_dict['y'])
    move_shot_right()

# shot animation upwards
def move_shot_up():
    global shot_dict
    shot_dict['flag'] = False
    shot.showturtle()
    shot_dict['x'], shot_dict['y'] = shot.xcor(), shot.ycor()
    y = shot_dict['y'] + shot_dict['step']
    shot.sety(y)
    shot_dict['y'] = shot.ycor()
    # Checking collision with borders and obstacles
    if shot.ycor() > top or not check_ellipse_collision(shot_dict['x'], shot_dict['y'], shape_format):
        shot.hideturtle()
        shot_dict['flag'] = True
        return
    screen.ontimer(move_shot_up, 20)

# shot animation downwards
def move_shot_down():
    global shot_dict
    shot_dict['flag'] = False
    shot.showturtle()
    shot_dict['x'], shot_dict['y'] = shot.xcor(), shot.ycor()
    y = shot_dict['y'] - shot_dict['step']
    shot.sety(y)
    shot_dict['y'] = shot.ycor()
    # Checking collision with borders and obstacles
    if shot.ycor() < bottom or not check_ellipse_collision(shot_dict['x'], shot_dict['y'], shape_format):
        shot.hideturtle()
        shot_dict['flag'] = True
        return
    screen.ontimer(move_shot_down, 20)

# shot animation to the right
def move_shot_right():
    global shot_dict
    shot_dict['flag'] = False
    shot.showturtle()
    shot_dict['x'], shot_dict['y'] = shot.xcor(), shot.ycor()
    x = shot_dict['x'] + shot_dict['step']
    shot.setx(x)
    shot_dict['x'] = shot.xcor()
    # Checking collision with borders and obstacles
    if shot.xcor() > right or not check_ellipse_collision(shot_dict['x'], shot_dict['y'], shape_format):
        shot.hideturtle()
        shot_dict['flag'] = True
        return
    screen.ontimer(move_shot_right, 20)

# shot animation to the left, can only shoot when shot finishes
def move_shot_left():
    global shot_dict
    shot_dict['flag'] = False
    shot.showturtle()
    shot_dict['x'], shot_dict['y'] = shot.xcor(), shot.ycor()
    x = shot_dict['x'] - shot_dict['step']
    shot.setx(x)
    shot_dict['x'] = shot.xcor()
    # Checking collision with borders and obstacles
    if shot.xcor() < left or not check_ellipse_collision(shot_dict['x'], shot_dict['y'], shape_format):
        shot.hideturtle()
        shot_dict['flag'] = True
        return
    screen.ontimer(move_shot_left, 20)

# starts second phase and ends the game
def start_phase_2():
    global shape_format, hyena_dict, phase, sprite
    if enemies_list == [] and hyena_dict['lives'] != 0 and phase == 2:
        phase = 0
        hyena_dict['lives'] = 1  # determines damage from phase 2 enemies
    sprite = './sprites/dreher_enemy.gif'
    t.bgpic('./sprites/life_background2.gif')
    shape_format = (-10, 10, 280)
    hyena.goto(left, 0)
    hyena_dict['x'] = hyena.xcor()
    hyena_dict['y'] = hyena.ycor()
    enemies_data.clear()
    create_enemies_dict(6)
    draw_enemies()
    create_boss_dict()
    draw_boss()
    if enemies_list == [] and phase == 0:
        for i in range(200):
            if boss.distance(hyena) < margin_error * 3:  # easter egg death by boss
                game_over()
            boss.goto(0, i * boss_dict['step'])  # boss leaving the screen
            if boss.xcor() == 0 and boss.ycor() > 700:  # if boss leaves the screen the game ends
                you_won()
                return


# function that determines what happens if you beat the game
def you_won():
    if enemies_list == []:
        boss.hideturtle()
        hyena.hideturtle()
        for life in lives:
            life.hideturtle()
        shot.hideturtle()
        screen.bgcolor('black')
        screen.bgpic('./sprites/youwon.gif')
        return
    screen.ontimer(you_won, 800)

# Reads keys pressed on keyboard
screen.listen()
screen.onkey(start_game, 'p')
screen.onkey(close_game, "q")
screen.onkeypress(move_up, "Up")
screen.onkeypress(move_down, "Down")
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkey(shoot_up, "w")
screen.onkey(shoot_down, "s")
screen.onkey(shoot_right, "d")
screen.onkey(shoot_left, "a")

# keeps the canvas open
t.mainloop()