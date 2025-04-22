"""
Robô de quatro rodas omnidirecionais
"""

from pybricks.hubs import EV3Brick
from pybricks.tools import StopWatch
from pybricks.parameters import Port, Button

from core.utils import wait_button_pressed, ev3_print, ev3_draw, PIDValues, get_hostname
from core.network import Bluetooth
from core.decision_color_sensor import DecisionColorSensor
from pybricks.ev3devices import Motor, UltrasonicSensor, InfraredSensor
from pybricks.tools import wait

from core.utils import PIDControl

import constants as const
import math


class Direction:
    FRONT = 1
    FRONT_RIGHT = 2
    RIGHT = 3
    BACK_RIGHT = 4
    BACK = 5
    BACK_LEFT = 6
    LEFT = 7
    FRONT_LEFT = 8

    @staticmethod
    def get_all():
        return [
            Direction.FRONT,
            Direction.FRONT_RIGHT,
            Direction.RIGHT,
            Direction.BACK_RIGHT,
            Direction.BACK,
            Direction.BACK_LEFT,
            Direction.LEFT,
            Direction.FRONT_LEFT,
        ]

    @classmethod
    def get_relative_direction(cls, initial, offset: int):
        _all = cls.get_all()
        return _all[(_all.index(initial) + offset) % len(_all)]


class OmniRobot:
    """Classe que representa um robô de 4 rodas omnidirecionais"""

    def __init__(
        self,
        wheel_diameter=6.5,
        wheel_length=10,
        wheel_width=18,
        motor_front_left: Port = None,
        motor_front_right: Port = None,
        motor_back_left: Port = None,
        motor_back_right: Port = None,
        motor_claw_lift: Port = None,
        motor_claw_gripper: Port = None,
        color_front_left: DecisionColorSensor = None,
        color_front_right: DecisionColorSensor = None,
        color_back_left: DecisionColorSensor = None,
        color_back_right: DecisionColorSensor = None,
        color_side: DecisionColorSensor = None,
        infra_claw: Port = None,
        ultra_back: Port = None,
        ultra_front: Port = None,
        server_name: str = None,
        turn_correction=const.LILO_TURN_CORRECTION,
        debug=True,
    ):

        # Ev3
        self.ev3 = EV3Brick()
        self.watch = StopWatch()
        self.name = get_hostname()

        # Rodas
        self.wheel_diameter = wheel_diameter
        self.wheel_length = wheel_length
        self.wheel_width = wheel_width

        # Motores
        if motor_front_left is not None:
            self.motor_front_left = Motor(motor_front_left)
        if motor_front_right is not None:
            self.motor_front_right = Motor(motor_front_right)
        if motor_back_left is not None:
            self.motor_back_left = Motor(motor_back_left)
        if motor_back_right is not None:
            self.motor_back_right = Motor(motor_back_right)
        if motor_claw_gripper is not None:
            self.motor_claw_gripper = Motor(motor_claw_gripper)
        if motor_claw_lift is not None:
            self.motor_claw_lift = Motor(motor_claw_lift)

        # Sensores
        if color_front_left is not None:
            self.color_front_left = color_front_left
        if color_front_right is not None:
            self.color_front_right = color_front_right
        if color_back_left is not None:
            self.color_back_left = color_back_left
        if color_back_right is not None:
            self.color_back_right = color_back_right
        if infra_claw is not None:
            self.infra_claw = InfraredSensor(infra_claw)
        if ultra_back is not None:
            self.ultra_back = UltrasonicSensor(ultra_back)
        if ultra_front is not None:
            self.ultra_front = UltrasonicSensor(ultra_front)
        if color_side is not None:
            self.color_side = color_side

        # Comunicação bluetooth
        if server_name:
            self.bluetooth = Bluetooth(ev3=self.ev3, server_name=server_name)

        self.debug = debug

        self.turn_correction = turn_correction

        # Orientação (N, S, L, O, ou None caso o robô ainda não tenha se encontrado)
        self.orientation = None

        # Marca a direção para a qual é o movimento padrão do robô omidirecional
        # Se 1, os movimentos serão considerando a frente do robô a parte que tem a garra.
        # Se -1, os movimentos serão considerando a frente do robô a parte que não tem a garra.
        self.moving_direction_sign = 1

        # Printa a voltagem e corrente atual da bateria:
        self.ev3_print("Bat. V:", self.ev3.battery.voltage(), "mV")
        self.ev3_print("Bat. C:", self.ev3.battery.current(), "mA")

    def robot_axis_to_motor_degrees(self, angle):
        """
        Grau relativo ao eixo do robô -> grau nas rodas (motores) do robô

        Considera um possível fator de correção
        """
        # Converte graus reais para graus correspondentes na roda
        robot_diameter = (self.wheel_length**2 + self.wheel_width**2) ** (1 / 2)
        return angle * (robot_diameter / self.wheel_diameter) * self.turn_correction

    def cm_to_motor_degrees(self, cm: float):
        """Distância em centímetros -> grau nas rodas (motores) do robô"""
        return cm * (360 / (math.pi * self.wheel_diameter))

    def motor_degrees_to_cm(self, degrees: float):
        """Grau nas rodas (motores) do robô -> distância em centímetros"""
        return degrees * (math.pi * self.wheel_diameter / 360)

    def abs_wheels_angle(self):

        return (
            abs(self.motor_front_left.angle())
            + abs(self.motor_front_right.angle())
            + abs(self.motor_back_left.angle())
            + abs(self.motor_back_right.angle())
        ) / 4

    def reset_wheels_angle(self, angle=0):
        """Reseta o ângulo das rodas"""
        self.motor_front_left.reset_angle(angle)
        self.motor_front_right.reset_angle(angle)
        self.motor_back_left.reset_angle(angle)
        self.motor_back_right.reset_angle(angle)

    def get_all_motors(self):
        return [
            self.motor_front_left,
            self.motor_front_right,
            self.motor_back_left,
            self.motor_back_right,
        ]

    def stop(self):
        """Desliga motores de locomoção."""
        motors = self.get_all_motors()
        for motor in motors:
            motor.dc(0)

        for motor in motors:
            motor.stop()

        for motor in motors:
            motor.hold()

    def get_motors_direction_signs(self, robot_direction: Direction):
        """
        Retorna os sinais de movimento dos motores dependendo da direção que o robô deve se movendo.

        Ordem de retorno:
            Dianteiro Esquerdo,
            Dianteiro Direito,
            Posterior Esquerdo,
            Posterior Direito
        """
        map_robot_direction_to_motor_signs = {
            Direction.FRONT: (-1, -1, 1, 1),
            Direction.FRONT_RIGHT: (-1, 0, 0, 1),
            Direction.RIGHT: (-1, 1, -1, 1),
            Direction.BACK_RIGHT: (0, 1, -1, 0),
            Direction.BACK: (1, 1, -1, -1),
            Direction.BACK_LEFT: (1, 0, 0, -1),
            Direction.LEFT: (1, -1, 1, -1),
            Direction.FRONT_LEFT: (0, -1, 1, 0),
        }
        return map_robot_direction_to_motor_signs[robot_direction]

    def get_sensors_towards_direction(self, direction: Direction):
        """Retorna os 2 sensores de cor que estão mais ao extremo do robô, na direção passada"""
        if direction in (
            Direction.FRONT_LEFT,
            Direction.FRONT_RIGHT,
            Direction.BACK_LEFT,
            Direction.BACK_RIGHT,
        ):
            raise ValueError("Direction must be a straight direction")

        map_robot_direction_to_sensors = {
            Direction.FRONT: (self.color_front_left, self.color_front_right),
            Direction.RIGHT: (self.color_front_right, self.color_back_right),
            Direction.BACK: (self.color_back_right, self.color_back_left),
            Direction.LEFT: (self.color_back_left, self.color_front_left),
        }
        return map_robot_direction_to_sensors[direction]

    def pid_walk(
        self,
        cm,
        speed=40,
        obstacle_function=None,
        off_motors=True,
        direction: Direction = Direction.FRONT,
    ):
        """
        Anda em linha reta com controle PID entre os motores.

        Retorna se viu obstáculos e quantos porcento do movimento foi realizado até a saída da função.

        Exemplos:
            False, 0.7
            True, 1
        """
        degrees = self.cm_to_motor_degrees(cm)
        if degrees == 0:
            return True, 1

        pid_controls = [PIDControl(const.PID_WALK_VALUES) for _ in range(3)]

        initial_angles = [motor.angle() for motor in self.get_all_motors()]
        motor_angle_average = 0

        has_seen_obstacle = False
        while abs(motor_angle_average) < abs(degrees):
            if obstacle_function is not None and obstacle_function():
                has_seen_obstacle = True
                break

            motor_angle_average = motor_angle_average = (
                abs(self.motor_front_left.angle() - initial_angles[0])
                + abs(self.motor_front_right.angle() - initial_angles[1])
                + abs(self.motor_back_left.angle() - initial_angles[2])
                + abs(self.motor_back_right.angle() - initial_angles[3])
            ) / 4

            self.loopless_pid_walk(
                pid_controls=pid_controls,
                vel=speed,
                direction=direction,
                initials=initial_angles,
            )

        if off_motors:
            self.stop()
        return has_seen_obstacle, abs(motor_angle_average) / abs(degrees)

    def loopless_pid_walk(
        self,
        pid_controls: list[PIDControl],  # 3 instâncias de PIDControl
        vel=60,
        direction: Direction = Direction.FRONT,
        initials=[0, 0, 0, 0],
    ):
        """
        Controle PID entre os motores sem um loop específico.
        Feita pra ser colocada dentro de um loop em outra função, passando os
        novos parâmetros (prev_elapsed_time, i_share, prev_error) devidamente
        inicializados a cada iteração.
        """

        if direction in (
            Direction.FRONT_LEFT,
            Direction.FRONT_RIGHT,
            Direction.BACK_LEFT,
            Direction.BACK_RIGHT,
        ):
            raise ValueError("Direction must be a straight direction")

        fl_sign, *direction_signs = self.get_motors_direction_signs(direction)
        # Usa o motor dianteiro esquerdo como alvo, os outros 4 o seguem
        target = (self.motor_front_left.angle() - initials[0]) * fl_sign

        corrections = []
        for pid_control, direction_sign, motor, initial in zip(
            pid_controls, direction_signs, self.get_all_motors()[1:], initials[1:]
        ):
            current = (motor.angle() - initial) * direction_sign
            corrections.append(pid_control.compute(lambda: current - target))

        speeds = [fl_sign * vel] + [
            sign * (vel - correction)
            for sign, correction in zip(direction_signs, corrections)
        ]
        self.motor_front_left.dc(speeds[0])
        self.motor_front_right.dc(speeds[1])
        self.motor_back_left.dc(speeds[2])
        self.motor_back_right.dc(speeds[3])

    def pid_turn(
        self,
        angle,
        pid: PIDValues = const.PID_TURN_VALUES,
        stop_condition_function=None,
    ):
        """
        Curva com controle PID.
        - Angulo relativo ao eixo do robô.
        - Angulo negativo: curva p / esquerda
        - Angulo positivo: curva p / direita
        """
        motor_degrees = self.robot_axis_to_motor_degrees(angle)
        fr_sign, fl_sign, br_sign, bl_sign = self.get_motors_direction_signs(
            robot_direction=Direction.FRONT
        )

        initial_angle = [
            self.motor_front_left.angle(),
            self.motor_front_right.angle(),
            self.motor_back_left.angle(),
            self.motor_back_right.angle(),
        ]

        target_angle = [
            self.motor_front_left.angle() + (motor_degrees * fl_sign),
            self.motor_front_right.angle() - (motor_degrees * fr_sign),
            self.motor_back_left.angle() + (motor_degrees * bl_sign),
            self.motor_back_right.angle() - (motor_degrees * br_sign),
        ]

        prev_errors = [(i - t) for i, t in zip(initial_angle, target_angle)]
        i_share = [0, 0, 0, 0]
        prev_elapsed_time = self.watch.time()
        while True:
            errors = [
                self.motor_front_left.angle() - target_angle[0],
                self.motor_front_right.angle() - target_angle[1],
                self.motor_back_left.angle() - target_angle[2],
                self.motor_back_right.angle() - target_angle[3],
            ]

            for i in range(4):
                if errors[i] < 30:
                    i_share[i] += errors[i]

            wait(1)
            elapsed_time = self.watch.time()

            d_share = [
                (e - p) / (elapsed_time - prev_elapsed_time)
                for e, p in zip(errors, prev_errors)
            ]
            prev_elapsed_time = elapsed_time
            prev_errors = errors

            pid_corrections = [
                e * pid.kp + i * pid.ki + d * pid.kd
                for e, i, d in zip(errors, i_share, d_share)
            ]

            # Limitante de velocidade
            speeds = [
                min(75, max(-75, pid_correction)) for pid_correction in pid_corrections
            ]

            for motor, speed in zip(self.get_all_motors(), speeds):
                motor.dc(-speed)

            distances = [
                motor.angle() - initial
                for motor, initial in zip(self.get_all_motors(), initial_angle)
            ]

            # self.ev3_print(
            #     distances, [motor.speed() for motor in self.get_all_motors()]
            # )
            if (
                all([abs(e) <= const.PID_TURN_ACCEPTABLE_DEGREE_DIFF for e in errors])
                or (
                    all(
                        [
                            abs(m.speed()) <= const.PID_TURN_MIN_SPEED
                            for m in self.get_all_motors()
                        ]
                    )
                    and all(
                        [abs(d) > const.MIN_DEGREES_CURVE_THRESHOLD for d in distances]
                    )
                )
                or (stop_condition_function is not None and stop_condition_function())
            ):
                break
        self.stop()

    def wait_button(self, button=Button.CENTER):
        return wait_button_pressed(ev3=self.ev3, button=button)

    def ev3_print(
        self,
        *args,
        clear=False,
        font="Lucida",
        size=16,
        bold=False,
        x=0,
        y=0,
        background=None,
        end="\n",
        **kwargs,
    ):
        ev3_print(
            *args,
            ev3=self.ev3,
            clear=clear,
            font=font,
            size=size,
            bold=bold,
            x=x,
            y=y,
            background=background,
            end=end,
            **kwargs,
        )

    def ev3_draw(
        self,
        *args,
        x=0,
        y=0,
        background=False,
        line=0,
        clear=False,
        font="Lucida",
        size=16,
        bold=False,
        **kwargs,
    ):
        ev3_draw(
            *args,
            ev3=self.ev3,
            x=x,
            y=y,
            background=background,
            line=line,
            clear=clear,
            font=font,
            size=size,
            bold=bold,
            **kwargs,
        )

    def align(
        self,
        direction: Direction = Direction.FRONT,
        speed=40,
        pid: PIDValues = const.ALIGN_VALUES,
    ):
        sensors = self.get_sensors_towards_direction(direction)
        all_signs = self.get_motors_direction_signs(direction)
        all_motors = self.get_all_motors()
        pids = [PIDControl(pid) for _ in range(2)]

        initial_colors = [sensor.color() for sensor in sensors]
        initial_reflections = [sensor.rgb()[2] for sensor in sensors]
        has_seen = [False, False]

        error = [0, 0]
        targets = [0, 0]
        speeds = [0, 0]
        speeds_stops = 0
        while True:
            for i, sensor in enumerate(sensors):
                # self.ev3_print("S:", i)
                if not has_seen[i] and sensor.color() != initial_colors[i]:
                    has_seen[i] = True
                    targets[i] = (sensor.rgb()[2] + initial_reflections[i]) / 2

                if has_seen[i]:
                    error[i] = sensor.rgb()[2] - targets[i]
                    correction = pids[i].compute(lambda: error[i])
                    speeds[i] = min(75, max(-75, correction))
                else:
                    speeds[i] = speed

            all_speeds = two_axis_into_four_motors_speeds(
                speeds[0], speeds[1], direction
            )

            for motor, sign, motor_speed in zip(all_motors, all_signs, all_speeds):
                motor.dc(sign * motor_speed)

            if all([s <= 20 for s in speeds]):
                speeds_stops += 1
            else:
                speeds_stops = 0

            if all(has_seen) and (
                all([abs(e) <= 15 for e in error]) or speeds_stops > 10
            ):

                break
        self.stop()

    def start_claw(
        self, open_angle=None, closed_angle=None, high_angle=None, low_angle=None
    ):
        if open_angle is None:
            self.claw_open_angle = self.motor_claw_gripper.run_until_stalled(
                speed=-300, duty_limit=35
            )
            self.ev3_print("Open angle:", self.claw_open_angle)
        else:
            self.claw_open_angle = open_angle

        if closed_angle is None:
            self.claw_closed_angle = self.motor_claw_gripper.run_until_stalled(
                speed=300, duty_limit=45
            )
            self.ev3_print("Closed angle:", self.claw_closed_angle)
        else:
            self.claw_closed_angle = closed_angle

        if high_angle is None:
            self.claw_high_angle = self.motor_claw_lift.run_until_stalled(
                speed=-300, duty_limit=20
            )
            self.ev3_print("High_angle:", self.claw_high_angle)
        else:
            self.claw_high_angle = high_angle

        if low_angle is None:
            self.claw_low_angle = self.motor_claw_lift.run_until_stalled(
                speed=300, duty_limit=15
            )
            self.ev3_print("Low angle:", self.claw_low_angle)
        else:
            self.claw_low_angle = low_angle

        self.claw_mid_angle = self.claw_low_angle - const.STITCH_CLAW_MID_TO_LOW_DIFF

    def line_follower(
        self,
        sensor,
        loop_condition_function,
        speed=60,
        direction: Direction = Direction.FRONT,
        pid: PIDValues = const.LINE_FOLLOWER_VALUES,
        side: str = "R",
        error_function=None,
    ):
        """
        Segue uma linha com um sensor de cor.
        """
        if side == "R":
            side = 1
        elif side == "L":
            side = -1
        else:
            raise ValueError("Apenas 'R' ou 'L'")

        if error_function is None:
            error_function = (
                lambda: sensor.reflection() - const.LINE_FOLLOW_TARGET_REFLECTION
            )

        error = 0
        error_i = 0
        prev_error = 0
        d_error = 0

        all_motors = self.get_all_motors()
        motor_signs = self.get_motors_direction_signs(direction)
        while loop_condition_function():
            error = error_function()
            error_i += error
            d_error = error - prev_error
            prev_error = error

            pid_correction = pid.kp * error + pid.ki * error_i + pid.kd * d_error

            # self.ev3_print(error, pid_correction, [speed, speed])
            all_speeds = two_axis_into_four_motors_speeds(
                speed + pid_correction * side, speed - pid_correction * side, direction
            )
            for motor, sign, motor_speed in zip(all_motors, motor_signs, all_speeds):
                motor.dc(sign * (motor_speed))

        self.stop()


def two_axis_into_four_motors_speeds(speed_left, speed_right, direction: Direction):
    """
    Converte a velocidade de dois "motores" (baseada em dois eixos) em quatro motores, de acordo com a direção. Desconsidera possíveis sinais.
    """
    if direction == Direction.FRONT:
        return speed_left, speed_right, speed_left, speed_right
    elif direction == Direction.BACK:
        return speed_right, speed_left, speed_right, speed_left
    elif direction == Direction.LEFT:
        return speed_right, speed_right, speed_left, speed_left
    elif direction == Direction.RIGHT:
        return speed_left, speed_left, speed_right, speed_right
    else:
        ValueError("Direção inválida")
