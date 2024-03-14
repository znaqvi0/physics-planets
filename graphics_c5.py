import random

from vectors import *
import pygame as p
import sys  # most commonly used to turn the interpreter off (shut down your game)
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
scale = 0.05e-9
r_scale = scale  # 500e-9


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


space_balls = []


def make_objs(n):
    r = 7.4e12
    total_m = 2e30
    rand = lambda x: random.uniform(-x, x)
    rand_vec = lambda x: Vec(rand(x), rand(x), rand(x))
    for i in range(n):
        sb = SpaceBall(rand_vec(r),
                       norm(rand_vec(1)) * random.uniform(0, 100e3), total_m / n, 3e11*1.5)
        while sb.pos.x ** 2 + sb.pos.y ** 2 + sb.pos.z ** 2 > r ** 2:
            sb.pos = rand_vec(r)
        space_balls.append(sb)


make_objs(10)
print(space_balls[0].m)
for thing in space_balls:
    thing.check_orbit = False
    # thing.pos.z = 0
    # thing.v.z = 0

initial = SpaceBall(Vec(), Vec(), 0, 0)
current_focus = initial
running = False
dragging = False
t = 0
dt = 1e4
while True:
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
        elif event.type == p.MOUSEBUTTONDOWN:
            dragging = True
        elif event.type == p.MOUSEBUTTONUP:
            dragging = False
    if dragging:
        mouse_move = p.mouse.get_rel()
        x0 += mouse_move[0]
        y0 += mouse_move[1]
        origin = x0, y0
    screen.fill((0, 0, 0))  # comment/uncomment to enable/disable trail

    for obj in space_balls:
        draw_ball(obj)

    if running:
        for i in range(1):  # steps multiple times every frame
            update_list_with_collision(space_balls, dt)
            # print(objects)
            t += dt
            # test_planet = earth
            # print(test_planet.lowest_pos_pos0_difference, t / 3600 / 24)
            # if test_planet.orbit_time is not None:
            #     print(test_planet.orbit_time/3600/24)
        # x0, y0 = -current_focus.pos.x * scale + WIDTH / 2, current_focus.pos.y * scale + HEIGHT / 2


            # print(obj.a)
    days, hours, minutes, seconds = time_convert(t)
    # %2.0f means 2 place values before decimal and 0 after
    text = font.render("%2.0f days %2.0f hours %2.0f minutes %2.0f seconds" % (days, hours, minutes, seconds), True, (255, 255, 255), (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (25, 25)
    screen.blit(text, text_rect)
    p.display.flip()
    # p.time.Clock().tick(100)  # caps frame rate at 100
