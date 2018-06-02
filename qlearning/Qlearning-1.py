import pyglet, random, math, time 
from game import boat, canav
from pyglet.gl import *


game_window = pyglet.window.Window(800, 600)
#main_batch = pyglet.graphics.Batch()
t = False
r = 1
s = []
p = 0
boat_ship = boat.Player(x=400, y=30)
#car_ship = boat.Player(x=400, y=-300)
game_window.push_handlers(boat_ship.key_handler)

@game_window.event
def on_draw():
    global p, s
    game_window.clear()
    print("2")
    canav_c = canav.canav()
    boat_ship.draw()
    if p != 0:
        glBegin(GL_LINE_STRIP)
        gl.glColor4f(0.9, 0.1, 0.1, 1.0)
        for x, y, z in s:
            glVertex2f(x, y)
        glEnd()

    #car_ship.draw()

def reset():
    global t, r
    boat_ship.x, boat_ship.y = 400,30
    boat_ship.rotation = 0
    t = True
    r = -1000

def step(action):
    boat_ship.rotation = action
    radians = 90 - action 
    angle_radians = math.radians(radians)
    force_x = math.cos(angle_radians) * 10
    force_y = math.sin(angle_radians) * 10
    px = boat_ship.x + force_x
    py = boat_ship.y + force_y
    boat_ship.x, boat_ship.y = px, py   
    print(boat_ship.x, boat_ship.y)
    #car_ship.draw()
    #time.sleep(1)
    visualx = boat_ship.x - 350
    visualy = boat_ship.y - 30
    return (visualx, visualy)

def greedy(actions, qfunc, x, y):
    amax = 0
    key = "%d_%d_%d" % (x, y, actions[0])
    qmax = qfunc[key]
    for i in range(len(actions)): 
        key = "%d_%d_%d" % (x, y, actions[i])
        q = qfunc[key]
        if qmax < q:
            qmax = q
            amax = i
    return actions[amax]

def epsilon_greedy(actions, qfunc, x, y, epsilon):
    amax = 0
    key = "%d_%d_%d"%(x, y, actions[0])
    qmax = qfunc[key]
    for i in range(len(actions)):    
        key = "%d_%d_%d"%(x, y, actions[i])
        q = qfunc[key]
        if qmax < q:
            qmax = q
            amax = i
    
    pro = [0.0 for i in range(len(actions))]
    pro[amax] += 1-epsilon
    for i in range(len(actions)):
        pro[i] += epsilon/len(actions)

    r = random.random()
    s = 0.0
    for i in range(len(actions)):
        s += pro[i]
        if s>= r: return actions[i]
    return actions[len(actions)-1]

def update():
    #pyglet.clock.unschedule(update)
    #print(1)
    global r, t
    #boat_ship.y += 10
    #boat_ship.update(dt)
    boat_ship.contact()
    if boat_ship.rotation == 0:
        if (boat_ship.x-boat_ship.width/2) < 350:
            reset()
        if (boat_ship.y+boat_ship.height/2) > 350:
            reset()
        if (boat_ship.x+boat_ship.width/2) > 450 and (boat_ship.y-boat_ship.height/2) < 250:
            reset()
        if (boat_ship.x+boat_ship.width/2) > 800:
            reset()

    if boat_ship.rotation == 90:
        if (boat_ship.x-boat_ship.height/2) < 350:
            reset()
        if (boat_ship.y+boat_ship.width/2) > 350:
            reset()
        if (boat_ship.x+boat_ship.height/2) > 450 and (boat_ship.y-boat_ship.width/2) < 250:
            reset()
        if (boat_ship.x+boat_ship.height/2) > 800:
            reset()

    if boat_ship.x ==760:
        r = 1000
        t = True
        boat_ship.x, boat_ship.y = 400,30
        boat_ship.rotation = 0

def qlearning(num = 1):
    #boat_ship.x, boat_ship.y = 400,100
    #boat_ship.rotation = 90
    #pyglet.clock.unschedule(qlearning)
    global t, r
    actions = [0, 90]
    states = []
    i = 0
    while i < 470:
        j = 0
        while j < 340 :
            states.append((i, j))
            j += 10
        i += 10
    qfunc = dict()
    for x,y in states:
        for a in actions:
            key = "%d_%d_%d" % (x, y, a)
            qfunc[key] = 0
    for l in range(1000):
        x, y = 50, 0
        a = 0
        t = False
        r = 1
        count = 0
        while False == t and count < 500:
            #on_draw()
            key = "%d_%d_%d" % (x, y, a)
            x1, y1 = step(a)
            update()          
            a1 = greedy(actions, qfunc, x1, y1)
            key1 = "%d_%d_%d" % (x1, y1, a1)
            qfunc[key] = qfunc[key] + 0.3*(r + 0.8 * qfunc[key1]-qfunc[key])
            x, y = x1, y1
            a = epsilon_greedy(actions, qfunc, x, y, 0.2)
            count += 1
    print(qfunc)
    return qfunc, actions, states

def upwd(dt):
    pyglet.clock.unschedule(upwd)
    #step(0)
    global t,s
    for i in range(1):
        #boat_ship.x, boat_ship.y = 400, 30
        x, y = (boat_ship.x-350), (boat_ship.y-30)
        #boat_ship.rotation = 0
        t = False
        count = 0
        while False == t and count<100:
            a1 = greedy(actions, qfunc, x, y)
            s.append((x+350,y+30,a1))
            #print(x, y, a1)
            #time.sleep(1)
            #key = "%d_%d_%d" % (x, y, a1)
            x1, y1 = step(a1)
            #boat_ship.x, boat_ship.y = 500, 300 
            #glBegin(GL_LINE_STRIP)
            #gl.glColor4f(0.9, 0.1, 0.1, 1.0)
            #glVertex2f(x+350, y+30)
            #glVertex2f(x1+350, y1+30)
            #glEnd()
            update()
            x, y = x1, y1
            count +=1
        #boat_ship.x, boat_ship.y = 500, 30

def shiyan(dt):
    #pyglet.clock.unschedule(shiyan)
    global p
    #win = pyglet.window.Window()
    p += 1
    if len(s) > p:
        boat_ship.x, boat_ship.y, boat_ship.rotation = s[p]


def newwindow(dt):
    pyglet.clock.unschedule(newwindow)
    #win = pyglet.window.Window(800, 600)
    #win.set_size(1200, 800)
    #game_window._recreate('800')
    game_window.set_size(800,600)
    ''''@win.event
    def on_draw():
        game_window.clear()
        # print("2")
        canav_c = canav.canav()
        boat_ship.draw()'''


if __name__ == "__main__":
    #pyglet.clock.schedule_interval(update, 1/120.0)
    qfunc, actions, states = qlearning()
    pyglet.clock.schedule_interval(upwd, 0.1)
    pyglet.clock.schedule_interval(shiyan, 0.2)
    #pyglet.clock.schedule_interval(newwindow, 5)
    pyglet.app.run()
    #qfunc = qlearning()