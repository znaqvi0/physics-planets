from data import *
from engine import *
space_balls = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
dt = 100000*2.5/10
for thing in space_balls:
    thing.check_orbit = False


def get_quadrant(ball):
    pos = ball.pos - sun.pos
    if pos.x > 0:
        ball_quadrant = 1 if pos.y > 0 else 4
    else:
        ball_quadrant = 2 if pos.y > 0 else 3
    return ball_quadrant


def get_angle(x, y):
    angle = math.atan2(y, x)
    if angle < 0:
        angle += 2*math.pi
    return angle


def aligned():
    min_angle = 10000
    max_angle = -10000

    for ball in space_balls[1:]:
        pos = ball.pos - sun.pos
        angle = get_angle(pos.y, pos.x)
        if angle < min_angle:
            min_angle = get_angle(pos.y, pos.x)
        if angle > max_angle:
            max_angle = get_angle(pos.y, pos.x)
    if math.degrees(max_angle - min_angle) < 80:
        return True
    return False


t = 0
last_printed = 0
while True:
    update_list_rk4(space_balls, dt)
    t += dt
    elapsed = t / 3600 / 24 / 365.25
    if int(elapsed) % 20 == 0:
        if int(elapsed) != last_printed:
            print(int(elapsed))
            last_printed = int(elapsed)
    if aligned():
        print("%.2f years until next alignment" % elapsed)
        break
