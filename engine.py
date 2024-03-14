import copy

from vectors import *

# dt = 1000  # 1000 for c2, 0.1 for c4, 1e4 for c5
G = 6.67e-11


class SpaceBall:
    def __init__(self, position, velocity, mass, radius, color=(255, 255, 255), check_orbit=True, does_drag=False):
        self.v = velocity
        self.pos = position
        self.pos0 = copy.deepcopy(position)
        self.v0 = copy.deepcopy(velocity)
        self.a = Vec()
        self.f = Vec()
        self.r = radius
        self.m = mass
        self.color = color
        self.t = 0
        self.check_orbit = check_orbit
        self.does_drag = does_drag
        self.orbit_time = None
        self.orbit_start = None
        self.orbit_end = None
        self.num_vel_direction_changes = 0
        self.printed_orbit = False

    def __repr__(self):
        return f"ball\n\tpos = {self.pos}\n\tvel = {self.v}\n\tacc = {self.a}\n\tm = {self.m}"

    def move(self, dt):
        self.pos += self.v * dt
        self.a = self.f / self.m
        self.v += self.a * dt

    def distance_to(self, other):
        return mag(other.pos - self.pos)

    def colliding_with(self, other):
        return self.distance_to(other) <= (self.r + other.r)/3.0

    def force_from(self, other):
        r = other.pos - self.pos
        # return (G * self.m * other.m / (mag(r) ** 2)) * norm(r)
        return (G * self.m * other.m / (r.x**2+r.y**2+r.z**2)) * norm(r)  # avoids sqrt operation in mag()

    def orbit_update(self, vy_sign_before):
        if self.check_orbit:
            if not self.printed_orbit:
                if vy_sign_before != math.copysign(1, self.v.y):
                    # print("hello")
                    self.num_vel_direction_changes += 1
                    if self.num_vel_direction_changes == 1:
                        self.orbit_start = self.t
                    elif self.num_vel_direction_changes == 3:
                        self.orbit_end = self.t
                        self.orbit_time = self.orbit_end - self.orbit_start
                        print(f"{round(self.orbit_time / 3600 / 24, 2)} days")
                        self.printed_orbit = True

    def update(self, dt):
        vy_sign_before = math.copysign(1, self.v.y)
        self.move(dt)
        self.t += dt
        self.orbit_update(vy_sign_before)

    def future_force(self, objects, dt, v, index):
        pos = self.pos + v*dt  # future position based on v and current position
        sb = SpaceBall(pos, v, self.m, 1)  # copy of self at future position to use in future force calculation
        f = sum([sb.force_from(thing2) for thing2 in objects if objects.index(thing2) != index], Vec())  # sum forces
        return f

    def update_rk4(self, dt, list_start, list_mid, list_end, index):
        # index: index of planet in all lists (to skip over in force calculation)
        # v for vel and x for pos in k value var names
        v = self.v  # velocity at start = k1x
        m = self.m
        vy_sign_before = math.copysign(1, v.y)  # used to check orbit

        f = self.future_force(list_start, 0, v, index)  # find force to use in finding acc=k1v
        k1v = f / m  # acc estimate initial
        k1x = v  # v estimate initial

        v_mid1 = v + k1v * dt / 2  # uses k1v to find v estimate at midpoint 1
        f = self.future_force(list_mid, dt / 2, v_mid1, index)
        k2v = f / m  # acc estimate at midpoint 1
        k2x = v_mid1  # v estimate at midpoint 1

        v_mid2 = v + k2v * dt / 2  # uses k2v to find v estimate at midpoint 2
        f = self.future_force(list_mid, dt / 2, v_mid2, index)
        k3v = f / m  # acc estimate at midpoint 2
        k3x = v_mid2  # v estimate at midpoint 2

        v_end = v + k3v * dt  # uses k3v to find v estimate at end
        f = self.future_force(list_end, dt, v_end, index)
        k4v = f / m  # acc estimate at end
        k4x = v_end  # v estimate at end

        # rk4 uses 4 slope estimates instead of 1 (euler)
        self.v += (k1v + 2 * k2v + 2 * k3v + k4v) * dt / 6  # update v using weighted avg of all acc estimates
        self.pos += (k1x + 2 * k2x + 2 * k3x + k4x) * dt / 6  # update pos using weighted avg of all v estimates
        self.t += dt
        self.orbit_update(vy_sign_before)


def update_list_rk4(objects, dt):
    list_start = update_list_return(objects, 0)  # list of planets at start of interval
    list_mid = update_list_return(objects, dt / 2)  # list of updated planets at midpoint of interval
    list_end = update_list_return(objects, dt)  # list of updated planets at end of interval
    for i in range(len(objects)):
        objects[i].update_rk4(dt, list_start, list_mid, list_end, i)


def update_list_return(list, dt):
    objects = [SpaceBall(thing.pos, thing.v, thing.m, 1) for thing in list]
    for obj in objects:
        obj.check_orbit = False
    update_pairs(objects, dt)
    return objects


def update_list(objects, dt):
    for thing1 in objects:
        thing1.f = sum((thing1.force_from(thing2) for thing2 in objects if thing2 != thing1), Vec())
    for thing in objects:
        thing.update(dt)


def update_pairs(objects, dt):
    n = len(objects)
    for i in range(n):
        # since everything from 0 to i has already calculated everything, j only needs to be > i
        for j in range(i + 1, n):
            obj_i = objects[i]
            obj_j = objects[j]
            force = obj_i.force_from(obj_j)
            obj_i.f += force
            obj_j.f -= force
    for thing in objects:
        thing.update(dt)
        thing.f = Vec()


def update_pairs_with_collision(objects, dt):
    n = len(objects)
    remove = []
    for i in range(n):
        for j in range(i + 1, n):
            # print(i,j)
            thing1 = objects[i]
            thing2 = objects[j]
            if thing2.colliding_with(thing1):
                total_v = 4.0 / 3 * math.pi * thing1.r ** 3 + 4.0 / 3 * math.pi * thing2.r ** 3
                new_r = (3 * total_v / (4 * math.pi)) ** (1.0 / 3)
                (bigger, smaller) = (thing1, thing2) if thing1.m > thing2.m else (thing2, thing1)
                bigger.v = (thing1.m * thing1.v + thing2.m * thing2.v) / (thing1.m + thing2.m)
                bigger.r = new_r
                if bigger.m == smaller.m:
                    bigger.pos = (bigger.pos + smaller.pos) / 2
                bigger.m += smaller.m
                # if smaller in objects:
                    # objects.remove(smaller)
                remove.append(smaller)
            else:
                force = thing1.force_from(thing2)
                thing1.f += force
                thing2.f -= force
    for thing in remove:
        if thing in objects:
            objects.remove(thing)
    for thing in objects:
        thing.update(dt)
        thing.f = Vec()


def update_with_drag(objects, dt, drag_force):
    for thing1 in objects:
        thing1.f = sum((thing1.force_from(thing2) for thing2 in objects if thing2 != thing1), Vec())
        if thing1.does_drag:
            thing1.f += drag_force
    for thing in objects:
        thing.update(dt)


def faster_update_list(objects, dt):
    for thing1 in objects:
        # force = Vec()
        # for thing2 in objects:
        #     if thing2 != thing1:
        #         force += thing1.force_from(thing2)
        force = sum((thing1.force_from(thing2) for thing2 in objects if thing2 != thing1), Vec())
        thing1.f = force
        thing1.update(dt)


def update_list_with_collision(objects, dt):
    for thing1 in objects:
        force = Vec()
        for thing2 in objects:
            if thing2 != thing1:
                if thing2.colliding_with(thing1):
                    total_v = 4.0/3*math.pi*thing1.r**3 + 4.0/3*math.pi*thing2.r**3
                    new_r = (3*total_v/(4*math.pi))**(1.0/3)
                    (bigger, smaller) = (thing1, thing2) if thing1.m > thing2.m else (thing2, thing1)
                    bigger.v = (thing1.m * thing1.v + thing2.m * thing2.v)/(thing1.m + thing2.m)
                    bigger.r = new_r
                    if bigger.m == smaller.m:
                        bigger.pos = (bigger.pos + smaller.pos)/2
                    bigger.m += smaller.m
                    if smaller in objects:
                        objects.remove(smaller)
                else:
                    force += thing1.force_from(thing2)
        thing1.f = force
    for thing in objects:
        thing.update(dt)
        # print(thing)
