import time
from pulseapi import *
import copy
import math
from io_board import IOBoard

ip = '7.7.7.3'
port = 23000
timeout = 0.1
io = IOBoard(ip=ip, port=port, timeout=timeout)
host = "192.168.0.178:8081"
robot = RobotPulse(host)
Rotation = [math.pi, 0, 0]
SPEED = 1
new_tool_info = tool_info(position([0, 0, 0.057], [0, 0, 0]), name="soska")


class Play:
    """
    В ходе стажировки в компани была поставлена задача реалтзовать 
    алгортм игры "Djenga".
    Был реалтзованн класс Play на вход подаёстя высота блока игры h,
    координаты места построения start_cord, количесво урвней башни  quantity_levels,
    смещение по оси у delta_y, координаты места положения блоков place_balka
    """

    def __init__(self, h, start_cord, quantity_levels, delta_y, place_balka):
        self.height = h
        self.start_cord = start_cord
        self.quantity = quantity_levels
        self.delta_y = delta_y
        self.cord_balka = place_balka

    def get_start_cord(self):
        """
        В этом методе вычесляются кординаты
        места построения
        :return: 
        """
        start = copy.deepcopy(self.start_cord)
        start[2] = start[2] + self.height
        return start

    def get_cord_level_Y(self):
        """
        Вычесляются координаты балок которые 
        ложатся паралельно
        :return: 
        """
        rez_cord = []
        for i in range(int(self.quantity / 2)):
            z_cord = copy.deepcopy(self.get_start_cord()[2]) + (2 * i * self.height)
            for j in range(3):
                y_cord = copy.deepcopy(self.get_start_cord()[1])
                y_cord = y_cord + (j * self.delta_y)
                prom = [self.get_start_cord()[0], y_cord, z_cord]
                rez_cord.append(prom)
        return rez_cord

    def get_cord_level_X(self):
        """
        Вычесление координат перпендекулярных 
        балок
        :return: 
        """
        rez_cord = []
        start_cord = copy.deepcopy(self.get_start_cord())
        start_cord[0] = start_cord[0] + 0.024
        start_cord[1] = start_cord[1] + self.delta_y / 2
        start_cord[2] = start_cord[2] + 0.013
        for i in range(int(self.quantity / 2)):
            z_cord = copy.deepcopy(start_cord[2]) + (2 * i * self.height)
            for j in range(3):
                x_cord = copy.deepcopy(start_cord[0])
                x_cord = x_cord + (j * self.delta_y)
                prom = [x_cord, start_cord[1], z_cord]
                rez_cord.append(prom)
        return rez_cord

    def combinate_XY(self):
        """
        В методе объединятся кординаты
        x_level and y_level
        :return: 
        """
        rez = []
        for i in range(len(self.create_level_cord_Y())):
            rez.append(self.create_level_cord_Y()[i])
            rez.append(self.create_level_cord_X()[i])
        return rez

    def build_Tower_first(self):
        """
        В этом методе происходит построение
        башни 
        :return: 
        """
        number = 0
        for i in range(len(self.combinate_XY())):
            cord = copy.deepcopy(self.start_cord)
            cord[2] = 0.35
            for j in range(len(self.combinate_XY()[i])):
                robot.set_position(position(cord, Rotation), SPEED, motion_type=MT_JOINT)
                self.get_balka(number)
                number += 1
                robot.set_position(position(cord, Rotation), SPEED, motion_type=MT_JOINT)
                if i % 2 == 0:
                    robot.set_position(position(cord, Rotation), SPEED, motion_type=MT_JOINT)
                    robot.await_motion()
                    io.set_digital_output(1, 'HIGH')
                    robot.await_motion()
                    prom_cord = copy.deepcopy(self.combinate_XY()[i][j])
                    prom_cord[2] = prom_cord[2] + 0.05
                    robot.set_position(position(prom_cord, Rotation), SPEED,
                                       motion_type=MT_JOINT)
                    robot.set_position(position(self.combinate_XY()[i][j], Rotation), SPEED, motion_type=MT_JOINT)
                    robot.await_motion()
                    # io.set_digital_output(1, 'LOW')

                else:
                    robot.set_position(position(cord, [math.pi, 0, math.pi / 2]), SPEED, motion_type=MT_JOINT)
                    time.sleep(3)
                    robot.await_motion()
                    # io.set_digital_output(1, 'HIGH')
                    robot.await_motion()
                    prom_cord = copy.deepcopy(self.combinate_XY()[i][j])
                    prom_cord[2] = prom_cord[2] + 0.05
                    robot.set_position(position(prom_cord, Rotation), SPEED, motion_type=MT_JOINT)
                    robot.set_position(position(self.combinate_XY()[i][j], [math.pi, 0, math.pi / 2]), SPEED,
                                       motion_type=MT_JOINT)
                    robot.await_motion()
                    # io.set_digital_output(1, 'LOW')

    def get_cord_bloks(self):
        """
        В жтом методе вычесляются координаты
        каждой балки для построения
        :return: 
        """
        cord = copy.deepcopy(self.cord_balka)
        center_cord = [cord[0] - 0.0375, cord[1] + 0.012, cord[2] + 0.013]
        z_const = cord[2] + 0.013
        rez_cord = []
        prom = []
        level_1 = []
        level_2 = []
        level_3 = []
        level_4 = []
        level_5 = []
        for i in range(12):
            y_cord = copy.deepcopy(center_cord[1])
            y_cord = y_cord + (i * 0.025)
            prom.clear()
            for j in range(5):
                z_cord = copy.deepcopy(z_const)
                z_cord = z_cord + (j * 0.013)
                prom_2 = [center_cord[0], y_cord, z_cord]
                if j == 0:
                    level_1.append(prom_2)
                elif j == 1:
                    level_2.append(prom_2)
                elif j == 2:
                    level_3.append(prom_2)
                elif j == 3:
                    level_4.append(prom_2)
                elif j == 4:
                    level_5.append(prom_2)
                if len(level_5) == 12:
                    rez_cord.append(level_1)
                    rez_cord.append(level_2)
                    rez_cord.append(level_3)
                    rez_cord.append(level_4)
                    rez_cord.append(level_5)
        return rez_cord

    def generate_list_cord(self):
        """
        Объединение координат 
        блков в единый список
        :return: 
        """
        rez = []
        cord_work = self.get_cord_bloks()
        for i in range(len(cord_work)):
            for j in range(len(cord_work[i])):
                rez.append(cord_work[i][j])
        return rez

    def get_balka(self, number):
        """
        Захват балок для построения
        с метса нахождения 
        :return: 
        """
        working_cord = self.generate_list_cord()
        prom_cord = copy.deepcopy(working_cord[number])
        prom_cord[2] = prom_cord[2] + 0.06
        robot.set_position(position(prom_cord, Rotation), SPEED, motion_type=MT_JOINT)
        time.sleep(0.5)
        robot.set_position(position(working_cord[number], Rotation), SPEED, motion_type=MT_LINEAR)
        robot.await_motion()
        # io.set_digital_output(1, 'HIGH')
        robot.await_motion()
        robot.set_position(position(prom_cord, Rotation), SPEED, motion_type=MT_LINEAR)
