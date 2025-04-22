import math

from pybricks.parameters import Color  # type: ignore

import constants as const
from core.robot import Direction, OmniRobot
from core.utils import PIDControl, PIDValues
from domain.localization import forward_avoiding_places
from domain.pathfinding import main

boarding_vertices = [(31, 32), (24, 25), (18, 19), (11, 12), (5, 6)]


def passenger_unboarding(robot: OmniRobot):
    """
    Rotina de desembarque de passageiro
    """
    if robot.moving_direction_sign == -1:
        robot.pid_turn(180)
        robot.moving_direction_sign = 1

    robot.align()
    robot.stop()

    robot.pid_walk(1.5, 35)

    pid_controls = [PIDControl(const.PID_WALK_VALUES) for _ in range(3)]
    initial_angles = [motor.angle() for motor in robot.get_all_motors()]
    if robot.color_front_left.color() == Color.YELLOW:
        while robot.color_front_right.color() != Color.YELLOW:
            robot.loopless_pid_walk(
                pid_controls, 40, direction=Direction.LEFT, initials=initial_angles
            )
    elif robot.color_front_right.color() == Color.YELLOW:
        while robot.color_front_left.color() != Color.YELLOW:
            robot.loopless_pid_walk(
                pid_controls, 40, direction=Direction.RIGHT, initials=initial_angles
            )

    robot.align(direction=Direction.BACK)
    robot.bluetooth.message("CLAW_LOW")
    robot.bluetooth.message()
    robot.pid_walk(20, 40)

    robot.ev3.speaker.beep()

    robot.bluetooth.message("CLAW_OPEN")
    robot.bluetooth.message()

    robot.pid_walk(20, 40, direction=Direction.BACK)
    robot.stop()
    robot.bluetooth.message("CLAW_HIGH")
    robot.bluetooth.message()


def manouver_to_get_passenger(robot: OmniRobot):
    if robot.moving_direction_sign == -1:
        robot.pid_turn(90)
    else:
        robot.pid_turn(-90)

    robot.align(Direction.BACK, speed=40)
    robot.pid_walk(const.ROBOT_SIZE_HALF, speed=40, direction=Direction.FRONT)


def passenger_boarding(robot: OmniRobot):
    robot.bluetooth.message("CLAW_OPEN")
    robot.bluetooth.message()

    robot.bluetooth.message("CLAW_MID")
    robot.bluetooth.message()

    robot.align(direction=Direction.RIGHT, speed=50)

    robot.bluetooth.message("COLOR_SIDE")

    initial_angle_left = robot.motor_front_left.angle()

    def condition_function():
        color = robot.bluetooth.message(should_wait=False)
        return color is None or color == Color.WHITE

    robot.line_follower(
        sensor=robot.color_front_right,
        loop_condition_function=condition_function,
    )
    passenger_color = robot.bluetooth.message(should_wait=False)
    robot.ev3_print("PASSENGER:", passenger_color)

    pid_controls = [PIDControl(const.PID_WALK_VALUES) for _ in range(3)]
    initial_angles = [motor.angle() for motor in robot.get_all_motors()]
    while robot.bluetooth.message(should_wait=False) is None:
        robot.loopless_pid_walk(
            pid_controls, 35, direction=Direction.BACK, initials=initial_angles
        )
    robot.stop()

    for pid in pid_controls:
        pid.reset()
    initial_angles = [motor.angle() for motor in robot.get_all_motors()]
    while robot.bluetooth.message(should_wait=False) is not None:
        if passenger_color is None:
            passenger_color = robot.bluetooth.message(should_wait=False)
        robot.loopless_pid_walk(
            pid_controls, 35, direction=Direction.BACK, initials=initial_angles
        )
    robot.ev3_print("PASSENGER:", passenger_color)

    robot.stop()
    robot.bluetooth.message("STOP")

    robot.pid_walk(cm=3, direction=Direction.FRONT)
    robot.stop()
    robot.pid_walk(cm=5, direction=Direction.LEFT)
    robot.pid_turn(90)
    robot.align(speed=50)

    robot.pid_walk(cm=4, direction=Direction.FRONT, speed=35)

    robot.bluetooth.message("CLAW_CLOSE")
    robot.bluetooth.message()
    robot.ev3_print("CLAW_CLOSE")

    robot.bluetooth.message("CLAW_HIGH")
    robot.bluetooth.message()
    robot.ev3_print("CLAW_HIGH")

    # Média de 3 leituras
    robot.bluetooth.message("ULTRA_CLAW")
    distances = []
    for _ in range(3):
        distances.append(robot.bluetooth.message())
    robot.bluetooth.message("STOP")
    distance_front = sum(distances) / len(distances)

    adult_or_child = (
        "ADULT" if passenger_color == Color.RED or distance_front < 5 else "CHILD"
    )
    robot.ev3_print(adult_or_child, ":", distance_front, distances)

    robot.pid_walk(cm=8, direction=Direction.BACK)
    robot.pid_turn(-90)

    # Média de 3 leituras
    robot.bluetooth.message("ULTRA_CLAW")
    for _ in range(3):
        distances.append(robot.bluetooth.message())
    robot.bluetooth.message("STOP")
    distance_front = sum(distances) / len(distances)

    robot.ev3_print("P. DIST.:", distance_front, distances)

    forward_avoiding_places(robot, direction=Direction.BACK)

    robot.pid_walk(cm=3)

    return ((adult_or_child, passenger_color), boarding_vertices[0])
