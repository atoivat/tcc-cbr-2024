#!/usr/bin/env pybricks-micropython
import json

from pybricks.ev3devices import ColorSensor  # type: ignore
from pybricks.hubs import EV3Brick  # type: ignore
from pybricks.parameters import Button, Port  # type: ignore
from pybricks.tools import StopWatch, wait  # type: ignore

import constants as const
from core.decision_color_sensor import DecisionColorSensor
from core.display import calibration_menu, screen
from core.robot import Direction, OmniRobot, Robot
from core.utils import PIDControl, PIDValues, get_hostname
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
from decision_trees.oficial.sandy_lego_ev3_color_3 import (
    sandy_lego_ev3_color_p3_decision_tree,
)
from decision_trees.oficial.sandy_lego_ev3_color_4 import (
    sandy_lego_ev3_color_p4_decision_tree,
)
from decision_trees.oficial.stitch_ht_nxt_color_v2_4 import (
    stitch_ht_nxt_color_v2_p4_decision_tree,
)
from domain.boarding import passenger_boarding, passenger_unboarding
from domain.localization import localization_routine
from domain.pathfinding import Graph, get_target_for_passenger, map_matrix
from domain.pathfollowing import pathfollowing_control

robot = None
showed_data = None

if get_hostname() == "lilo":
    robot = OmniRobot(
        motor_front_left=Port.B,
        motor_front_right=Port.C,
        motor_back_left=Port.A,
        motor_back_right=Port.D,
        color_front_left=DecisionColorSensor(
            ColorSensor(Port.S3), lilo_lego_ev3_color_p3_decision_tree
        ),
        color_front_right=DecisionColorSensor(
            ColorSensor(Port.S2), lilo_lego_ev3_color_p2_decision_tree
        ),
        color_back_left=DecisionColorSensor(
            ColorSensor(Port.S1), lilo_lego_ev3_color_p1_decision_tree
        ),
        color_back_right=DecisionColorSensor(
            ColorSensor(Port.S4), lilo_lego_ev3_color_p4_decision_tree
        ),
    )
elif get_hostname() == "sandy":
    robot = Robot(
        wheel_diameter=const.WHEEL_DIAMETER,
        wheel_distance=const.WHEEL_DIST,
        motor_r=Port.B,
        motor_l=Port.C,
        infra_side=Port.S1,
        ultra_feet=Port.S2,
        color_right=DecisionColorSensor(
            ColorSensor(Port.S3), sandy_lego_ev3_color_p3_decision_tree
        ),
        color_left=DecisionColorSensor(
            ColorSensor(Port.S4), sandy_lego_ev3_color_p4_decision_tree
        ),
    )


def main():

    header = ["KP", "KI", "KD"]
    file_name = "pid_const.json"

    while True:

        selected_options, showed_data = calibration_menu(
            file_name, header, robot, clear=True
        )
        selected_function, kp, ki, kd = selected_options

        values = [kp, ki, kd]

        screen(showed_data, selected=None, clear=True, robot=robot)

        watch = StopWatch()

        while watch.time() < 3000:
            if selected_function == "align":
                robot.align(pid=PIDValues(kp, ki, kd))
            elif selected_function == "pid_walk":
                robot.pid_walk(100, pid=PIDValues(kp, ki, kd))
            elif selected_function == "pid_turn":
                robot.reset_wheels_angle()
                robot.pid_turn(90, pid=PIDValues(kp, ki, kd))
                print(robot.abs_wheels_angle())
            elif selected_function == "line_follower":
                robot.line_follower(50, side="R", pid=PIDControl(PIDValues(kp, ki, kd)))

        robot.stop()

        screen(
            showed_data + ["Save parameters?"], selected=None, robot=robot, clear=True
        )

        wait(1000)

        button = robot.wait_button(
            [Button.UP, Button.DOWN, Button.CENTER, Button.LEFT, Button.RIGHT]
        )

        if button == Button.CENTER:
            with open(file_name, "r") as file:
                data = json.load(file)
            data[robot.name][selected_function] = values
            print(data)
            with open(file_name, "w") as file:
                json.dump(data, file, indent=4)
            screen(showed_data + ["Saved!"], selected=None, robot=robot, clear=True)

            robot.wait_button(
                [Button.UP, Button.DOWN, Button.CENTER, Button.LEFT, Button.RIGHT]
            )
        else:
            screen(showed_data + ["Not saved!"], selected=None, robot=robot, clear=True)


main()
