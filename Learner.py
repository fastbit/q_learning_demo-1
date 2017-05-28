__author__ = 'philippe'
import World
import threading
import time
import matplotlib.pyplot as plt

discount = 1
actions = World.actions
states = []
Q = {}
plot_x = []
plot_y = []
plt.plot([], [])
plt.ion()
plt.show()

for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

for state in states:
    temp = {}
    for action in actions:
        #temp[action] = 0.1
	temp[action] = 10
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp

for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)


def do_action(action):
    s = World.player
    r = -World.score
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score
    return s, action, r, s2


def max_Q(s):
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc
    World.set_cell_score(s, a, Q[s][a])


def run():
	global discount
	time.sleep(0.001)
	alpha = 1
	t = 1
	while True:
		# Pick the right action
		s = World.player
		max_act, max_val = max_Q(s)
		(s, a, r, s2) = do_action(max_act)

		# Update Q
		max_act, max_val = max_Q(s2)
		inc_Q(s, a, 1, r + discount * max_val)
		
		# Check if the game has restarted
		t += 1.0
		score = World.score
		if World.has_restarted():
			World.restart_game()
			time.sleep(0.001)
			t = 1.0
			plot_x.append(World.iteration)
			plot_y.append(score)
			plt.plot(plot_x, plot_y, color="black")
			plt.draw()

		# Update the learning rate
		alpha = pow(t, -0.1)

		# MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
		time.sleep(0)

t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()
