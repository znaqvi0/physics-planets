import datetime
import sys  # most commonly used to turn the interpreter off (shut down your game)

import pygame as p

from data import *

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


# scale = 1e-9
# r_scale=500e-9


def ball_xy(ball):
    # print(float(origin[0] + ball.pos.x / scale), float(origin[1] - ball.pos.y / scale))
    return float(origin[0] + ball.pos.x * scale), float(origin[1] - ball.pos.y * scale)


def draw_ball(ball):
    # print(earth.r/scale)
    p.draw.circle(screen, ball.color, ball_xy(ball), max(ball.r * r_scale, 1))


def time_convert(t):
    days = t / 3600 / 24
    hours = days % 1 * 24
    minutes = hours % 1 * 60
    seconds = minutes % 1 * 60
    return int(days), int(hours), int(minutes), int(seconds)


# space_balls = []
space_balls = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, moon]
for ball in [sun, jupiter, saturn, uranus, neptune]:
    ball.r /= 5
sun.r /= 20
# earth.r /= 100
# moon.r /= 100
# sun.r /= 40
initial = SpaceBall(Vec(), Vec(), 0, 0)
current_focus = initial
running = False
sub_challenge = 1
if sub_challenge == 1:
    space_balls = [sun, SpaceBall(Vec(-2.972015400432158E+09, 4.073504769556730E+09, -1.489219177682864E+09) * 1000,
                                  Vec(7.133079985050709E-01, 5.539892657262223E-01, 1.036258353889948E-01) * 1000,
                                  2.2e14, 1)]  # mystery
    sun.check_orbit = False
    for ball in space_balls[2:]:
        ball.check_orbit = False
comet = space_balls[1]


def update_fixed_sun():
    comet.f = comet.force_from(sun)
    comet.update(dt)


def update_rk4():
    v = comet.v
    vy_sign_before = math.copysign(1, v.y)
    f = comet.force_from(sun)
    m = comet.m
    k1v = f/m
    k1x = v

    v_mid1 = v+dt*k1v/2
    sb_mid1 = SpaceBall(comet.pos + v_mid1*dt/2, v_mid1, m, 1)
    f = sb_mid1.force_from(sun)
    k2v = f/m  # v derivative at midpoint 1
    k2x = v_mid1  # pos derivative at midpoint 1

    v_mid2 = v+dt*k2v/2
    sb_mid2 = SpaceBall(comet.pos + v_mid2*dt/2, v_mid2, m, 1)
    f = sb_mid2.force_from(sun)
    k3v = f / m
    k3x = v_mid2

    v_end = v+dt*k3v
    sb_end = SpaceBall(comet.pos + v_end*dt, v_end, m, 1)
    f = sb_end.force_from(sun)
    k4v = f / m
    k4x = v_end

    comet.v += (k1v + 2 * k2v + 2 * k3v + k4v)*dt/6
    comet.pos += (k1x + 2 * k2x + 2 * k3x + k4x)*dt/6
    comet.t += dt
    comet.orbit_update(vy_sign_before)


dragging = False
t = 0
# dt = 10000
dt = 60000
sun.pos = Vec()
sun.v = Vec()
while True:
    for event in p.event.get():
        if event.type == p.QUIT:  # this refers to clicking on the "x"-close
            p.quit()
            sys.exit()
        elif event.type == p.KEYDOWN:
            screen.fill((0, 0, 0))
            if event.key == p.K_SPACE:
                running = True
                time_start_computation = time.time_ns()
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
        elif event.type == p.MOUSEBUTTONDOWN:
            dragging = True
            current_focus = None
        elif event.type == p.MOUSEBUTTONUP:
            dragging = False

    if dragging:
        mouse_move = p.mouse.get_rel()
        x0 += mouse_move[0]
        y0 += mouse_move[1]
        origin = x0, y0
        screen.fill((0, 0, 0))
    # screen.fill((0, 0, 0))  # comment/uncomment to enable/disable trail
    if current_focus is not None:
        origin = -current_focus.pos.x * scale + WIDTH / 2, current_focus.pos.y * scale + HEIGHT / 2

    # screen.fill((0, 0, 0))  # comment/uncomment to enable/disable trail
    for obj in space_balls:
        draw_ball(obj)
    if running:
        for i in range(100):  # steps multiple times every frame
            # update_fixed_sun()
            update_rk4()
            # print(objects)
            t += dt
            if comet.printed_orbit:
                print((time.time_ns() - time_start_computation) / 1e9)
                running = False
                break
            # dt = 0.1/mag(comet.a)
            # if mag(comet.pos) < 0.4*700e9:
            #     dt = 20
            #     comet.color=(255,0,0)
            # else:
            #     dt = 200*2
            # test_planet = earth
            # print(test_planet.lowest_pos_pos0_difference, t / 3600 / 24)
            # if test_planet.orbit_time is not None:
            #     print(test_planet.orbit_time/3600/24)
        # origin = -current_focus.pos.x * scale + WIDTH / 2, current_focus.pos.y * scale + HEIGHT / 2

        # print(((t/3600)/24)/365)
        # print(objects[0].v)
        # print(objects[0].t)
        # print(sun)
        # print(math.degrees(earth.angle) - math.degrees(earth.initial_angle))
    days, hours, minutes, seconds = time_convert(t)
    # %2.0f means 2 place values before decimal and 0 after
    text = font.render("%2.0f days %2.0f hours %2.0f minutes %2.0f seconds" % (days, hours, minutes, seconds), True,
                       (255, 255, 255), (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (25, 25)
    screen.blit(text, text_rect)

    date_start = datetime.datetime.strptime("11/11/23", "%m/%d/%y")
    date_end = date_start + datetime.timedelta(days=t / 3600 / 24)
    string_date = str(date_end)
    text2 = font.render(string_date, True, (255, 255, 255), (0, 0, 0))
    text_rect2 = text2.get_rect()
    text_rect2.topleft = (25, 50)
    screen.fill((0, 0, 0), rect=text_rect2)
    screen.blit(text2, text_rect2)

    p.display.flip()
    # p.time.Clock().tick(100)  # caps frame rate at 100
