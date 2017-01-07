__author__ = 'philippe'
from Tkinter import *
import numpy as np
master = Tk()

iteration = 1
triangle_size = 0.1
cell_score_min = -0.2
cell_score_max = 0.2
Width = 15
(x, y) = (50, 50)
position = [[0 for i in range(x)] for j in range(y)]
colorscore = [[0 for i in range(x)] for j in range(y)]
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*Width, height=y*Width)
player = (0, y-1)
score = 1
restart = False
walk_reward = -0.04

# Generate a random set of walls

number_of_walls = 500
walls = []

for i in range(number_of_walls):
	
	while True:
		wall_x = np.random.randint(0, x)
		wall_y = np.random.randint(0, y)
		if (wall_x, wall_y) not in walls and (wall_x, wall_y) not in player:
			break
	
	walls.append((wall_x, wall_y))

# Generate random set of red rectangles
	
number_of_red = 100
specials = []

for i in range(number_of_red):
	
	while True:
		red_x = np.random.randint(0, x)
		red_y = np.random.randint(0, y)
		
		if (red_x, red_y) not in walls and (red_x, red_y) not in player and (red_x, red_y) not in specials:
			break
	
	specials.append((red_x, red_y, "red", -1))

# Generate random green rectangle

while True:
	green_x = np.random.randint(0, x)
	green_y = np.random.randint(0, y)
	
	if (green_x, green_y) not in walls and (green_x, green_y) not in player and (green_x, green_y) not in specials:
		break
	
specials.append((green_x, green_y, "green", 1))	

cell_scores = {}

def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)


def render_grid():
    global specials, walls, Width, x, y, player, position
    for i in range(x):
        for j in range(y):
            position[i][j] = board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

render_grid()


def set_cell_score(state, action, val):
	global cell_score_min, cell_score_max
	triangle = cell_scores[state][action]
	green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
	green = hex(green_dec)[2:]
	red = hex(255-green_dec)[2:]
	if len(red) == 1:
		red += "0"
	if len(green) == 1:
		green += "0"
	color = "#" + red + green + "00"
	#board.itemconfigure(triangle, fill=color)


def try_move(dx, dy):
	global player, x, y, score, walk_reward, me, restart, iteration
	if restart == True:
		restart_game()
	new_x = player[0] + dx
	new_y = player[1] + dy
	score += walk_reward
	if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
		color_visited(new_x, new_y)
		board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
		player = (new_x, new_y)
	for (i, j, c, w) in specials:
		if new_x == i and new_y == j:
			score -= walk_reward
			score += w
			if score > 0:
				print iteration, " -- Success! score: ", score
			else:
				print iteration, " -- Fail! score: ", score
			restart = True
			iteration += 1
			#color_reset()
			return
    #print "score: ", score

def color_visited(new_x, new_y):
	colorscore[new_x][new_y] += 1
	colorind = colorscore[new_x][new_y]
	colorspeed = 0.001
	colorvalue  = 255
	colorvalue2 = 255
	colorvalue = int(round(max(0, -(colorspeed*colorind**2)+255), 0))
	if colorvalue == 0:
		colorind -= 505
		colorvalue2 = int(round(max(0, -(colorspeed*colorind**2)+255), 0))
	colorvalue  = format(colorvalue,  '02x')
	colorvalue2 = format(colorvalue2, '02x')
	coloritem = "#" + colorvalue + colorvalue2 + "ff"
	board.itemconfigure(position[new_x][new_y], fill=coloritem, tag="visited")
	
def color_reset():
	for item in board.find_withtag("visited"):
		board.itemconfigure(item, fill="white")
	
def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player, score, me, restart
    player = (0, y-1)
    score = 1
    restart = False
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="orange", width=1, tag="me")

board.grid(row=0, column=0)


def start_game():
    master.mainloop()
