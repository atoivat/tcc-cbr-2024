#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import (  # type: ignore
    ColorSensor,
    InfraredSensor,
    Motor,
    UltrasonicSensor,
)
from pybricks.hubs import EV3Brick  # type: ignore
from pybricks.iodevices import Ev3devSensor  # type: ignore
from pybricks.parameters import Button, Color, Port, Stop  # type: ignore
from pybricks.tools import DataLog, wait  # type: ignore

import constants as const

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

from core.utils import ev3_print, get_hostname

brick_name_to_sensors_and_functions = {
    "lilo": [
        ("S1", ColorSensor, Port.S1, lilo_lego_ev3_color_p1_decision_tree),
        ("S2", ColorSensor, Port.S2, lilo_lego_ev3_color_p2_decision_tree),
        ("S3", ColorSensor, Port.S3, lilo_lego_ev3_color_p3_decision_tree),
        ("S4", ColorSensor, Port.S4, lilo_lego_ev3_color_p4_decision_tree),
    ],
    "stitch": [
        ("S3-ht-nxt", Ev3devSensor, Port.S3, stitch_ht_nxt_color_v2_p3_decision_tree)
    ],
}


def test_calibration():

    brick = EV3Brick()
    sensor_info = brick_name_to_sensors_and_functions[get_hostname()]

    sensors = []
    for _, s_class, s_port, _ in sensor_info:
        sensors.append(s_class(s_port))

    while True:
        for (s_name, s_class, s_port, s_function), sensor in zip(sensor_info, sensors):
            if "ht-nxt" in s_name:
                ev3_print(s_port, "-", s_function(*sensor.read("NORM")), ev3=brick)
            else:
                ev3_print(s_port, "-", s_function(*sensor.rgb()), ev3=brick)

        wait(100)
        brick.screen.clear()


if __name__ == "__main__":
    test_calibration()
