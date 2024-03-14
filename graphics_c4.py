import sys  # most commonly used to turn the interpreter off (shut down your game)

import pygame as p

from data import *
from engine import *

# Initializes pygame - see documentation
p.init()

# Constants - sets the size of the window
WIDTH = 800
HEIGHT = 800

screen = p.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))
p.display.set_caption('window')

font = p.font.SysFont('Monocraft', 20)


origin = x0, y0 = WIDTH / 2, HEIGHT / 2  # This is the new origin
scale = 0.8e-10  # 1e-9 for only inner planets
r_scale = 200e-9  # 500e-9 for only inner planets
scale = 300e-9 * 1.2 ** 20
# r_scale=500e-9
r_scale = scale


def ball_xy(ball):
    # print(float(origin[0] + ball.pos.x / scale), float(origin[1] - ball.pos.y / scale))
    return float(origin[0] + ball.pos.x * scale), float(origin[1] - ball.pos.y * scale)


def draw_ball(ball):
    # print(earth.r/scale)
    p.draw.circle(screen, ball.color, ball_xy(ball), max(ball.r * r_scale, 1))


def time_convert(t):
    days = t/3600/24
    hours = days % 1 * 24
    minutes = hours % 1 * 60
    seconds = minutes % 1 * 60
    return int(days), int(hours), int(minutes), int(seconds)


def get_drag(asteroid, cd):
    h = asteroid.pos.x - earth.r
    if h > 25000:
        T = -131.21 + 0.00299*h
        p = 2.488*((T+273.1)/216.6)**-11.388
        asteroid.color = (255, 255, 255)
    elif h > 11000:
        T = -56.46
        p = 22.65*math.exp(1.73-0.000157*h)
        asteroid.color = (0, 255, 0)
    elif h > 0:
        T = 15.04 - 0.00649*h
        p = 101.29*((T+273.1)/288.08)**5.256
        asteroid.color = (255, 0, 0)
    rho = p/(0.2869*(T+273.1))
    # print(rho)
    A = math.pi * asteroid.r ** 2  # front facing area
    v = asteroid.v  # velocity of ball wrt air
    return -0.5 * cd * rho * A * mag(v) ** 2 * norm(v)


# space_balls = []
sub_challenge = 2
if sub_challenge == 1:
    asteroid = SpaceBall(Vec(), Vec(), 1, 1)
    space_balls = [venus, asteroid]
    asteroid.pos.x = 15*space_balls[0].r*2

elif sub_challenge == 2:
    asteroid = SpaceBall(Vec(), Vec(-10889.052), 12000, 10, (255, 255, 255), False, True)
    space_balls = [earth, asteroid]
    asteroid.pos.x = 120000 + earth.r
space_balls[0].pos = Vec()
space_balls[0].v = Vec()
# for ball in [sun, jupiter, saturn, uranus, neptune]:
#     ball.r /= 5
# sun.r /= 20
# earth.r /= 100
# moon.r /= 100
# sun.r /= 40
initial = SpaceBall(Vec(), Vec(), 0, 0)
current_focus = SpaceBall(Vec(earth.r), Vec(), 0, 0) if sub_challenge == 2 else initial
running = False
t = 0
dt = 0.0001 if sub_challenge == 2 else 0.1
printed_vel = False
max_drag = 0
while True:
    origin = -current_focus.pos.x * scale + WIDTH / 2, current_focus.pos.y * scale + HEIGHT / 2
    # screen.fill((0, 0, 0))  # comment/uncomment to enable/disable trail
    for obj in space_balls:
        draw_ball(obj)
    for event in p.event.get():
        if event.type == p.QUIT:  # this refers to clicking on the "x"-close
            p.quit()
            sys.exit()
        elif event.type == p.KEYDOWN:
            screen.fill((0, 0, 0))
            if event.key == p.K_SPACE:
                running = True
            if event.key == p.K_UP:
                scale *= 1.2
                r_scale *= 1.2
            if event.key == p.K_DOWN:
                scale /= 1.2
                r_scale /= 1.2
            focus_dict = {
                p.K_1: mercury,
                p.K_2: venus,
                p.K_3: earth,
                p.K_4: mars,
                p.K_5: jupiter,
                p.K_6: saturn,
                p.K_7: uranus,
                p.K_8: neptune,
                p.K_0: initial}
            if event.key in focus_dict:
                current_focus = focus_dict[event.key]


    if running:
        for i in range(100):  # steps multiple times every frame
            if sub_challenge == 1:
                update_pairs_with_collision(space_balls, dt)
            elif sub_challenge == 2:
                drag_force = get_drag(asteroid, 0.5)
                max_drag = max(drag_force.x, max_drag)
                if asteroid.pos.x - earth.pos.x < asteroid.r + earth.r:
                    print(asteroid.v.x)
                    break
                update_with_drag(space_balls, dt, drag_force)
                # print("%.5f drag %.5f m/s" % (drag_force.x, asteroid.v.x))
                print(drag_force, asteroid.v, asteroid.a, max_drag)
            # print(objects)
            t += dt
            if sub_challenge == 1:
                if not printed_vel:
                    # +120000 only for earth and venus
                    if space_balls[0].distance_to(space_balls[1]) <= space_balls[0].r + space_balls[1].r + 120000:
                        print("%.3f m/s" % space_balls[1].v.x)
                        printed_vel = True


        # print(asteroid.pos)
        for obj in space_balls:
            draw_ball(obj)

    days, hours, minutes, seconds = time_convert(t)
    # %2.0f means 2 place values before decimal and 0 after
    text = font.render("%2.0f days %2.0f hours %2.0f minutes %2.0f seconds" % (days, hours, minutes, seconds), True,
                       (255, 255, 255), (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (25, 25)
    screen.blit(text, text_rect)
    p.display.flip()
    # p.time.Clock().tick(100)  # caps frame rate at 100
