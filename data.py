import time

import requests

from engine import SpaceBall
from vectors import *

id_dict = {"sun": 10, "mercury": 199, "venus": 299, "earth": 399, "mars": 499, "jupiter": 599, "saturn": 699,
           "uranus": 799, "neptune": 899, "moon": 301}


def get_data(planet):
    data = requests.get(
        f"https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='{id_dict[planet]}'&OBJ_DATA='YES'&MAKE_EPHEM"
        "='YES'&EPHEM_TYPE='VECTOR'&CENTER='500@0'&START_TIME='2023-11-11'&STOP_TIME='2023-11-12"
        "'&STEP_SIZE='1%20d'&QUANTITIES='1,9,20,23,24,29'").text
    # __________________mass______________
    m_data = data.split("Mass")[1].split("\n")[0]
    unwanted_m_strs = ["~", ",", "+-"]
    for unwanted in unwanted_m_strs:
        m_data = m_data.replace(unwanted, " ")
    m_pow_10 = float(m_data.split("10^")[1].split(" ")[0])
    m_units = "kg" if "kg" in m_data.split("10^")[1].split(" ")[1] else "g"
    if m_units == "g":
        m_pow_10 -= 3
    m_number = m_data.split("=")[1].split(" ")
    m_number = float([num for num in m_number if num != ""][0])
    mass = m_number * 10 ** m_pow_10
    # ____________________radius__________________
    # print(data)
    r_data = data.lower().split("mean radius")[1].split("\n")[0]
    for unwanted in unwanted_m_strs:
        r_data = r_data.replace(unwanted, " ")
    r_data = r_data.split("=")[1].split(" ")
    radius = float([num for num in r_data if num != ""][0]) * 1000
    # print(radius)
    # ____________________pos, vel________________
    data = data.split("$$SOE")[1].split("$$EOE")[0].split("TDB")[1].split("LT")[0]
    unwanted_strs = ["X =", "Y =", "Z =", "VX=", "VY=", "VZ=", "\n"]
    for unwanted in unwanted_strs:
        data = data.replace(unwanted, "")
    data = [float(num) * 1000 for num in data.split(" ") if num != ""]
    data_dict = {'x': data[0], 'y': data[1], 'z': data[2], 'vx': data[3], 'vy': data[4], 'vz': data[5], 'm': mass,
                 'r': radius}
    data_vec = {'pos': Vec(data_dict['x'], data_dict['y'], data_dict['z']),
                'v': Vec(data_dict['vx'], data_dict['vy'], data_dict['vz']),
                'm': data_dict['m'],
                'r': data_dict['r']}
    return data_vec


time_start = time.time_ns()
# print(requests.get(
#         f"https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='MB'&OBJ_DATA='YES'&MAKE_EPHEM"
#         "='YES'&EPHEM_TYPE='VECTOR'&CENTER='500@0'&START_TIME='2023-11-11'&STOP_TIME='2023-11-12"
#         "'&STEP_SIZE='1%20d'&QUANTITIES='1,9,20,23,24,29'").text)
time_end = time.time_ns()
print("using the nasa api wasted %.0f ms of your life" % ((time_end - time_start) / 1e6))


# sun_mass, sun_radius = 1988500e24, 696500e3
# mercury_mass, mercury_radius = 3.302e23, 2440e3
# venus_mass, venus_radius = 48.685e23, 6051.84e3
# earth_mass, earth_radius = 5.97219e24, 6371.01e3
# mars_mass, mars_radius = 6.4171e23, 3389.92e3
# jupiter_mass, jupiter_radius = 189818722e22 * 1e-3, 69911e3
# saturn_mass, saturn_radius = 5.6834e26, 58232e3
# uranus_mass, uranus_radius = 86.813e24, 25362e3
# neptune_mass, neptune_radius = 102.409e24, 24624e3
def spaceball_from_data(data, color):
    return SpaceBall(data['pos'], data['v'], data['m'], data['r'], color)


sun = spaceball_from_data(get_data("sun"), (255, 255, 0))
mercury = spaceball_from_data(get_data("mercury"), (183, 184, 185))
venus = spaceball_from_data(get_data("venus"), (255, 198, 73))
earth = spaceball_from_data(get_data("earth"), (40, 122, 184))
mars = spaceball_from_data(get_data("mars"), (156, 46, 53))
jupiter = spaceball_from_data(get_data("jupiter"), (169, 63, 73))
saturn = spaceball_from_data(get_data("saturn"), (250, 229, 191))
uranus = spaceball_from_data(get_data("uranus"), (79, 208, 231))
neptune = spaceball_from_data(get_data("neptune"), (75, 112, 221))
moon = spaceball_from_data(get_data("moon"), (200, 200, 200))
