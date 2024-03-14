from data import *

t = 0
dt = 10000  # 27639 at dt=50, 27597.56 found in 1230 seconds at dt=10
sub_challenge = 1
if sub_challenge == 1:
    space_balls = [sun, SpaceBall(Vec(-2.972015400432158E+09, 4.073504769556730E+09, -1.489219177682864E+09) * 1000,
                                  Vec(7.133079985050709E-01, 5.539892657262223E-01, 1.036258353889948E-01) * 1000,
                                  2.2e14, 1)]
    sun.check_orbit = False
    for ball in space_balls[2:]:
        ball.check_orbit = False

comet = space_balls[1]


# no other planets: 27617.95 days at 250/30 in 57.4653341 seconds
# 27612.75 days at 250/25 in 53.546482 seconds
# 27589.09 days 397.69014 at 100/2
# 27604.41 days 58.2773883 at 250/17
# 27588.37 days 150.1148863 at 500/2
# 27591.49 days 72.4438507
# 27598.4 days 52.4218968 at 250/10 smaller dt change radius
# 27593 in 61

def update_fixed_sun():
    comet.f = comet.force_from(sun)
    comet.update(dt)


def update_rk4():
    v = comet.v
    pos = comet.pos
    vy_sign_before = math.copysign(1, v.y)
    f = comet.force_from(sun)
    m = comet.m
    k1v = f/m
    k1x = v

    v_mid1 = v+dt*k1v/2
    sb_mid1 = SpaceBall(pos + v_mid1*dt/2, v_mid1, m, 1)
    f = sb_mid1.force_from(sun)
    k2v = f/m  # v derivative at midpoint 1
    k2x = v_mid1  # pos derivative at midpoint 1

    v_mid2 = v+dt*k2v/2
    sb_mid2 = SpaceBall(pos + v_mid2*dt/2, v_mid2, m, 1)
    f = sb_mid2.force_from(sun)
    k3v = f / m
    k3x = v_mid2

    v_end = v+dt*k3v
    sb_end = SpaceBall(pos + v_end*dt, v_end, m, 1)
    f = sb_end.force_from(sun)
    k4v = f / m
    k4x = v_end

    comet.v += (k1v + 2 * k2v + 2 * k3v + k4v)*dt/6
    comet.pos += (k1x + 2 * k2x + 2 * k3x + k4x)*dt/6
    comet.t += dt
    comet.orbit_update(vy_sign_before)


sun.v = Vec()
sun.pos = Vec()  # 27615.87 days 53.9312686 seconds, 27595.33 days 160.7122475, 27592.22 days 245.6779038
start_time = time.time_ns()
while not comet.printed_orbit:
    update_rk4()
    # update_list(space_balls, dt)  # 27849 with faster_update 250 dt, 27639.18 with 50 dt
    # t += dt
    # if mag(comet.pos) < 0.4 * 700e9:
    #     dt = 3  # 50 27616
    # else:
    #     dt = 250  # 500
print((time.time_ns() - start_time) / 1e9)
# conversion to year, month, day: int(days/365.25) year, int((years % 1) * 12) month, round((months % 1) * 30.437) day
