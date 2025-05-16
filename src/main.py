#!/usr/bin/env pybricks-micropython

import time

from pybricks.ev3devices import ColorSensor
from pybricks.iodevices import Ev3devSensor
from pybricks.parameters import Button, Color, Port
from pybricks.tools import wait

import constants as const
from core.decision_color_sensor import DecisionColorSensor
from core.robot import Direction, OmniRobot
from core.utils import PIDValues, get_hostname

if const.MAP_COLOR_CALIBRATION == "OFICIAL":
    from decision_trees.oficial.lilo_lego_ev3_color_1 import (
        lilo_lego_ev3_color_p1_decision_tree,
    )
    from decision_trees.oficial.lilo_lego_ev3_color_2 import (
        lilo_lego_ev3_color_p2_decision_tree,
    )
    from decision_trees.oficial.lilo_lego_ev3_color_3 import (
        lilo_lego_ev3_color_p3_decision_tree,
    )
    from decision_trees.oficial.lilo_lego_ev3_color_4 import (
        lilo_lego_ev3_color_p4_decision_tree,
    )
    from decision_trees.oficial.stitch_ht_nxt_color_v2_4 import (
        stitch_ht_nxt_color_v2_p4_decision_tree,
    )
elif const.MAP_COLOR_CALIBRATION == "HOME":
    from decision_trees.home.lilo_lego_ev3_color_1 import (
        lilo_lego_ev3_color_p1_decision_tree,
    )
    from decision_trees.home.lilo_lego_ev3_color_2 import (
        lilo_lego_ev3_color_p2_decision_tree,
    )
    from decision_trees.home.lilo_lego_ev3_color_3 import (
        lilo_lego_ev3_color_p3_decision_tree,
    )
    from decision_trees.home.lilo_lego_ev3_color_4 import (
        lilo_lego_ev3_color_p4_decision_tree,
    )
    from decision_trees.home.stitch_ht_nxt_color_v2_3 import (
        stitch_ht_nxt_color_v2_p3_decision_tree,
    )
elif const.MAP_COLOR_CALIBRATION == "TEST":
    from decision_trees.test.lilo_lego_ev3_color_1 import (
        lilo_lego_ev3_color_p1_decision_tree,
    )
    from decision_trees.test.lilo_lego_ev3_color_2 import (
        lilo_lego_ev3_color_p2_decision_tree,
    )
    from decision_trees.test.lilo_lego_ev3_color_3 import (
        lilo_lego_ev3_color_p3_decision_tree,
    )
    from decision_trees.test.lilo_lego_ev3_color_4 import (
        lilo_lego_ev3_color_p4_decision_tree,
    )
    from decision_trees.test.stitch_ht_nxt_color_v2_4 import (
        stitch_ht_nxt_color_v2_p4_decision_tree,
    )

from domain.boarding import (
    manouver_to_get_passenger,
    passenger_boarding,
    passenger_unboarding,
)
from domain.gripper_server import (
    close_claw,
    lower_claw,
    mid_claw,
    open_claw,
    raise_claw,
    server_main,
    transmit_signal,
)
from domain.localization import forward_avoiding_places, localization_routine
from domain.pathfinding import Graph, get_target_for_passenger, map_matrix
from domain.pathfollowing import move_from_position_to_targets, pathfollowing_control

testing_targets = [0, 13, 26, 2, 15, 28, 4, 17, 30]


def lilo_main(lilo: OmniRobot):
    lilo.ev3_print("CLIENT READY")
    lilo.ev3_print("PRESS TO START")
    lilo.wait_button()

    lilo.ev3_print(lilo.bluetooth.start())
    lilo.ev3_print("GO!")
    lilo.bluetooth.message("CLAW_HIGH")
    lilo.bluetooth.message()

    # Inicialização do mapa
    map_graph = Graph(map_matrix)

    #
    # Localização inicial
    #
    localization_routine(lilo)

    n = 0

    while True:
        #
        # Coleta de passageiros
        #
        passenger_info, boarding_position = passenger_boarding(lilo)
        lilo.orientation = "N"  # TODO: deixar na lógica de localização
        lilo.moving_direction_sign = 1
        lilo.ev3_print("Age:", passenger_info[0])
        lilo.ev3_print("Col:", passenger_info[1])

        #
        # Pathfinding e movimentação (obstáculos)
        #
        target = get_target_for_passenger(*passenger_info)

        delivered_position = move_from_position_to_targets(
            lilo, map_graph, boarding_position[0], target
        )

        #
        # Desembarque de passageiros
        #
        passenger_unboarding(lilo)

        #
        # Retorno a zona de embarque
        #
        move_from_position_to_targets(
            lilo, map_graph, delivered_position, [boarding_position[1]]
        )
        manouver_to_get_passenger(lilo)
        n += 1


def test_navigation_lilo(lilo: OmniRobot):

    lilo.bluetooth.start()

    passenger_info = passenger_boarding(lilo)

    return

    map_graph = Graph(map_matrix)

    lilo.orientation = "N"
    initial_position = 5
    target_position = 26

    current_position = move_from_position_to_target(
        lilo, map_graph, initial_position, target_position
    )
    lilo.wait_button()
    move_from_position_to_target(lilo, map_graph, current_position, initial_position)


def test_bt_lilo(lilo: OmniRobot):
    lilo.bluetooth.start()
    while True:
        lilo.ev3_print("Press request button:")
        pressed = lilo.wait_button(
            [Button.UP, Button.LEFT, Button.RIGHT, Button.DOWN, Button.CENTER]
        )
        button_to_request = {
            Button.UP: "CLAW_HIGH",
            Button.LEFT: "CLAW_OPEN",
            Button.RIGHT: "CLAW_CLOSE",
            Button.DOWN: "CLAW_LOW",
            Button.CENTER: "CLAW_MID",
        }
        lilo.ev3_print(pressed)
        lilo.bluetooth.message(button_to_request[pressed])

        # while Button.CENTER not in lilo.ev3.buttons.pressed():
        #     lilo.ev3_print(lilo.bluetooth.message(should_wait=False))

        # lilo.bluetooth.message("STOP")


def test_claw_grip(stitch: OmniRobot):
    stitch.start_claw(0, 78, -220, 0)
    while True:
        mid_claw(stitch)
        wait(1000)
        close_claw(stitch)
        raise_claw(stitch)
        wait(1000)
        lower_claw(stitch)
        open_claw(stitch)
        stitch.wait_button()


def test_unboarding(robot: OmniRobot):
    robot.bluetooth.start()

    wait(100)

    robot.bluetooth.message("CLAW_CLOSE")
    robot.bluetooth.message()

    robot.bluetooth.message("CLAW_HIGH")
    robot.bluetooth.message()

    passenger_unboarding(robot)


def test_pid_align_lilo(robot: OmniRobot):
    while True:
        for direction in Direction.get_all():
            if direction % 2 != 0:  # apenas as 4 direções principais
                robot.align(direction=direction, pid=PIDValues(kp=1, ki=0, kd=0.5))
                robot.wait_button()


def gerar_timestamp():
    t = time.localtime()
    # Formata: ano, mês, dia, hora, minuto, segundo
    timestamp = "{:04d}{:02d}{:02d}_{:02d}{:02d}{:02d}".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    return timestamp


def test_movements_case_1(robot: OmniRobot):

    file_string = "test_" + gerar_timestamp() + ".txt"

    with open(file_string, "w+") as logfile:
        testing_dir = Direction.FRONT
        DISTANCE = 150

        print("Bat. V:", robot.ev3.battery.voltage(), "mV", file=logfile)
        print("Bat. C:", robot.ev3.battery.current(), "mA", file=logfile)

        iteration = 0
        while iteration < 10:
            iteration += 1
            # robot.wait_button()
            robot.pid_walk(
                DISTANCE, speed=const.LILO_FORWARD_SPEED, direction=testing_dir
            )
            robot.stop()

            log = (
                str(iteration)
                + " FWD: "
                + "{:.2f}".format(
                    robot.motor_degrees_to_cm(robot.motor_front_right.angle())
                )
                + "cm"
            )
            robot.ev3_print(log)
            print(log, file=logfile)

            # robot.wait_button()
            robot.pid_walk(
                DISTANCE,
                speed=const.LILO_FORWARD_SPEED,
                direction=Direction.get_relative_direction(testing_dir, 4),
            )
            log_backwards = (
                str(iteration)
                + " BCK: "
                + "{:.2f}".format(
                    robot.motor_degrees_to_cm(robot.motor_front_right.angle())
                )
                + "cm"
            )
            robot.ev3_print(log_backwards)
            print(log_backwards, file=logfile)
            robot.stop()


def test_movements_case_2(robot: OmniRobot):
    testing_dir_sign = 1
    while True:
        robot.wait_button()
        for _ in range(4):
            robot.pid_turn(90 * testing_dir_sign)
        robot.stop()


def test_movements_case_3(robot: OmniRobot):
    testing_dir_sign = 1
    while True:
        robot.wait_button()
        for _ in range(4):
            robot.pid_walk(
                60, speed=const.LILO_FORWARD_SPEED, direction=const.LILO_FORWARD_SPEED
            )
            robot.pid_turn(90 * testing_dir_sign)


def main(hostname):
    if hostname == "lilo":
        lilo_main(
            OmniRobot(
                motor_front_left=Port.B,
                motor_front_right=Port.C,
                motor_back_left=Port.A,
                motor_back_right=Port.D,
                color_front_left=DecisionColorSensor(
                    ColorSensor(Port.S1), lilo_lego_ev3_color_p1_decision_tree
                ),
                color_front_right=DecisionColorSensor(
                    ColorSensor(Port.S4), lilo_lego_ev3_color_p4_decision_tree
                ),
                color_back_left=DecisionColorSensor(
                    ColorSensor(Port.S2), lilo_lego_ev3_color_p2_decision_tree
                ),
                color_back_right=DecisionColorSensor(
                    ColorSensor(Port.S3), lilo_lego_ev3_color_p3_decision_tree
                ),
                server_name="stitch",
            )
        )
    elif hostname == "stitch":
        server_main(
            OmniRobot(
                color_side=DecisionColorSensor(
                    Ev3devSensor(Port.S3), stitch_ht_nxt_color_v2_p3_decision_tree
                ),
                infra_claw=Port.S1,
                ultra_back=Port.S4,
                ultra_front=Port.S2,
                motor_claw_lift=Port.A,
                motor_claw_gripper=Port.B,
                server_name="stitch",
            )
        )


if __name__ == "__main__":
    main(get_hostname())
