"""
Centralização de definição de constantes.

Devem estar nesse módulo:
    - Definição de variáveis constantes (e que obviamente não devem ser alteradas em
        execução)
    - Comentários sobre o que significam as constantes
    - Constantes com nomes bem significativos

Não devem estar nesse módulo:
    - Qualquer tipo de código além de declaração de constantes
    - Variáveis globais utilizadas para controle de algoritmos (que sofrem alterações em
        execução)
"""

import json
import math

from core.utils import PIDValues, get_hostname

LOG_TO_FILE = True


def load_json_file():
    with open("pid_const.json", "r") as file:
        data = json.load(file)
    return data


const_map = load_json_file()
hostname = get_hostname()

# Constantes PID

PID_WALK_VALUES = PIDValues.from_list(const_map[hostname]["pid_walk"])
PID_TURN_VALUES = PIDValues.from_list(const_map[hostname]["pid_turn"])
ALIGN_VALUES = PIDValues.from_list(const_map[hostname]["align"])
LINE_FOLLOWER_VALUES = PIDValues.from_list(const_map[hostname]["line_follower"])
LINE_FOLLOWER_AVOIDING_PLACES = PIDValues(kp=1.5, ki=0, kd=1)

# Dimensões do robô
WHEEL_DIAMETER = 6.7
WHEEL_DIST = 16.1
WHEEL_LENGTH = WHEEL_DIAMETER * math.pi

ROBOT_SIZE = 15  # considerando a distância dos sensores de cor da frente até a parte de trás do robô
ROBOT_SIZE_HALF = ROBOT_SIZE / 2


STITCH_CLAW_MID_TO_LOW_DIFF = 10


# Curvas com PID
PID_TURN_ACCEPTABLE_DEGREE_DIFF = 3
PID_TURN_MIN_SPEED = 5
MIN_DEGREES_CURVE_THRESHOLD = 30

# Comunicação Bluetooth
SERVER_NAME = "sandy"


# Distâncias
OMNI_WALK_DISTANCE_CORRECTION = 0.8
OMNI_SIDE_ALING_PERCENTAGE = 0.53


# Obstáculos
OBSTACLE_DISTANCE = 150
SANDY_OBSTACLE_DISTANCE = 80
OBSTACLE_DISTANCE_TO_CELL = 13
OBSTACLE_ALIGN_DISTANCE = 7.5

LINE_FOLLOW_TARGET_REFLECTION = 30
SANDY_LINE_FOLLOW_TARGET_REFLECTION = 20

ROBOT_SPEED = 55


if get_hostname() in ("lilo", "stitch"):
    CELL_DISTANCE = 30
    CELL_DISTANCE_TO_PARK = 24
    CELL_DISTANCE_TO_BOARDING = 16.5
    LINE_TO_CELL_CENTER_DISTANCE = 5
else:
    CELL_DISTANCE = 27.5
    CELL_DISTANCE_TO_PARK = 22
    CELL_DISTANCE_TO_BOARDING = 16.5
    LINE_TO_CELL_CENTER_DISTANCE = 11


# Localização Sandy
SANDY_ORIGIN_VERTEX = 31
SANDY_BOARDING_VERTEX = [6]

DIST_COLOR_AFTER_ALIGN = 0.5
SPEED_COLOR_AFTER_ALIGN = 30

OMNI_LINE_FOLLOWER_BLUE_TARGET = 30


LILO_FORWARD_SPEED = 47
LILO_TURN_CORRECTION = 1.35


MAP_COLOR_CALIBRATION = "HOME"  # OFICIAL, HOME, TEST
