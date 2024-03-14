import datetime
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
scale = 1e-9
r_scale = 500e-9


def ball_xy(ball):
    # print(float(origin[0] + ball.pos.x / scale), float(origin[1] - ball.pos.y / scale))
    return float(origin[0] + ball.pos.x * scale), float(origin[1] - ball.pos.y * scale)


def draw_ball(ball):
    # print(earth.r/scale)
    p.draw.circle(screen, ball.color, ball_xy(ball), max(ball.r * r_scale, 1))


# space_balls = []
space_balls = [sun, earth, moon]
for ball in [sun, jupiter, saturn, uranus, neptune]:
    ball.r /= 5
sun.r /= 20
earth.r /= 100
moon.r /= 100
# sun.r /= 40
initial = SpaceBall(Vec(), Vec(), 0, 0)
current_focus = earth
running = False
t = 0
dt = 1000 / 2
for ball in space_balls:
    ball.check_orbit = False


def time_convert(t):
    days = t / 3600 / 24
    hours = days % 1 * 24
    minutes = hours % 1 * 60
    seconds = minutes % 1 * 60
    return int(days), int(hours), int(minutes), int(seconds)


def get_angle(x, y):
    angle = math.atan2(y, x)
    if angle < 0:
        angle += 2 * math.pi
    return angle


def eclipse():
    moon_pos = moon.pos - sun.pos
    earth_pos = earth.pos - sun.pos
    moon_angle = get_angle(moon_pos.y, moon_pos.x)
    earth_angle = get_angle(earth_pos.y, earth_pos.x)
    if abs(moon_angle - earth_angle) < math.radians(0.035):
        moon.color = (0, 255, 0)
        if abs(moon.pos.z - earth.pos.z) < moon.r + earth.r:
            return True
        # earth_xy_dist = mag(Vec(earth_pos.x, earth_pos.y))
        # moon_xy_dist = mag(Vec(moon_pos.x, moon_pos.y))
        # earth_angle_z = math.atan2(earth_pos.z, earth_xy_dist)
        # moon_angle_z = math.atan2(moon_pos.z, moon_xy_dist)
        # if abs(moon_angle_z - earth_angle_z) < math.radians(0.00004247333):
        #     return True
    else:
        moon.color = (255, 255, 255)
        return False


last_printed = ""
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
            if event.key == p.K_3:
                current_focus = earth
            if event.key == p.K_0:
                current_focus = initial

    screen.fill((0, 0, 0))  # comment/uncomment to enable/disable trail
    for obj in space_balls:
        draw_ball(obj)

    if running:
        for i in range(10):  # steps multiple times every frame
            update_list_rk4(space_balls, dt)
            t += dt
            if eclipse():
                if moon.distance_to(sun) > earth.distance_to(sun):
                    e_type = "lunar"
                else:
                    e_type = "solar"
                # print("%.2f days until" % (t/3600/24), e_type, "eclipse")
                date_start = datetime.datetime.strptime("11/11/23", "%m/%d/%y")
                date_end = date_start + datetime.timedelta(days=t / 3600 / 24)
                string_date = e_type + " eclipse on " + date_end.strftime(
                    '%B %d %Y hour %H')  # can add %A for day of week
                if string_date.split("hour")[0] != last_printed.split("hour")[0]:
                    print(string_date)
                    last_printed = string_date

        origin = -current_focus.pos.x * scale + WIDTH / 2, current_focus.pos.y * scale + HEIGHT / 2
        p.draw.line(screen, (255, 255, 255), ball_xy(sun), ball_xy(earth), 1)
        # p.draw.line(screen, (255, 255, 255), ball_xy(sun), ball_xy(earth), 1)

    days, hours, minutes, seconds = time_convert(t)
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
