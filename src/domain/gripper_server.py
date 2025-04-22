from pybricks.parameters import Button

from core.robot import OmniRobot


def server_main(robot: OmniRobot):
    # robot.start_claw()
    robot.start_claw(0, 78, -250, 0)
    robot.ev3_print("SERVER READY")
    robot.bluetooth.start()
    robot.ev3_print("GO!")

    while True:
        request = robot.bluetooth.message()
        robot.ev3_print(request)
        if request == "ULTRA_FRONT":
            transmit_signal(robot, robot.ultra_front.distance)
        elif request == "ULTRA_BACK":
            transmit_signal(robot, robot.ultra_back.distance)
        elif request == "ULTRA_CLAW":
            transmit_signal(robot, robot.infra_claw.distance)
        elif request == "COLOR_SIDE":
            transmit_signal(robot, robot.color_side.color)
        elif request == "CLAW_LOW":
            lower_claw(robot)
            robot.ev3_print("Claw low")
        elif request == "CLAW_HIGH":
            raise_claw(robot)
            robot.ev3_print("Claw high")
        elif request == "CLAW_MID":
            mid_claw(robot)
            robot.ev3_print("Claw mid")
        elif request == "CLAW_OPEN":
            open_claw(robot)
            robot.ev3_print("Claw open")
        elif request == "CLAW_CLOSE":
            close_claw(robot)
            robot.ev3_print("Claw closed")
        elif request.startswith("PRINT:"):
            robot.ev3_print(request[5:])
        robot.bluetooth.message(None, force_send=True)
        robot.ev3_print("Request finished")
        # robot.ev3_print(robot.ultra_claw.distance(), robot.ultra_front.distance())


def open_claw(robot: OmniRobot):
    robot.motor_claw_gripper.dc(0)
    robot.motor_claw_gripper.run_target(300, target_angle=robot.claw_open_angle)


def close_claw(robot: OmniRobot):

    direction_sign = (
        -1 if robot.motor_claw_gripper.angle() - robot.claw_closed_angle > 0 else 1
    )

    while (
        abs(robot.motor_claw_gripper.angle() - robot.claw_closed_angle) > 10
        and not robot.motor_claw_gripper.stalled()
    ):
        robot.motor_claw_gripper.run(300 * direction_sign)
    robot.motor_claw_gripper.hold()


def raise_claw(robot: OmniRobot):
    robot.motor_claw_lift.run_target(200, target_angle=robot.claw_high_angle)


def lower_claw(robot: OmniRobot):
    robot.motor_claw_lift.run_target(200, target_angle=robot.claw_low_angle)


def mid_claw(robot: OmniRobot):
    robot.motor_claw_lift.run_target(200, target_angle=robot.claw_mid_angle)


def transmit_signal(robot: OmniRobot, signal_function):
    robot.ev3_print("Transmitindo:")
    robot.bluetooth.message(signal_function(), force_send=True)
    while robot.bluetooth.message(should_wait=False) != "STOP":
        robot.bluetooth.message(signal_function(), force_send=True)
    robot.bluetooth.message(None, force_send=True)
    robot.ev3_print("Transmissao encerrada")
