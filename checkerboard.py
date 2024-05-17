# from collections import namedtuple
#
# Chessman = namedtuple('Chessman', 'Name Value Color')
# Point = namedtuple('Point', 'X Y')
#
# BLACK_CHESSMAN = Chessman('黑子', 1, (45, 45, 45))
# WHITE_CHESSMAN = Chessman('白子', 2, (219, 219, 219))
#
# offset = [(1, 0), (0, 1), (1, 1), (1, -1)]
#
#
# class Checkerboard:
#     def __init__(self, line_points):
#         self._line_points = line_points
#         self._checkerboard = [[0] * line_points for _ in range(line_points)]
#
#     def _get_checkerboard(self):
#         return self._checkerboard
#
#     checkerboard = property(_get_checkerboard)
#
#     # 判断是否可落子
#     def can_drop(self, point):
#         return self._checkerboard[point.Y][point.X] == 0
#
#     def drop(self, chessman, point):
#         """
#         落子
#         :param chessman:
#         :param point:落子位置
#         :return:若该子落下之后即可获胜，则返回获胜方，否则返回 None
#         """
#         print(f'{chessman.Name} ({point.X}, {point.Y})')
#         self._checkerboard[point.Y][point.X] = chessman.Value
#
#         if self._win(point):
#             print(f'{chessman.Name}获胜')
#             return chessman
#
#     # 判断是否赢了
#     def _win(self, point):
#         cur_value = self._checkerboard[point.Y][point.X]
#         for os in offset:
#             if self._get_count_on_direction(point, cur_value, os[0], os[1]):
#                 return True
#
#     def _get_count_on_direction(self, point, value, x_offset, y_offset):
#         count = 1
#         for step in range(1, 5):
#             x = point.X + step * x_offset
#             y = point.Y + step * y_offset
#             if 0 <= x < self._line_points and 0 <= y < self._line_points and self._checkerboard[y][x] == value:
#                 count += 1
#             else:
#                 break
#         for step in range(1, 5):
#             x = point.X - step * x_offset
#             y = point.Y - step * y_offset
#             if 0 <= x < self._line_points and 0 <= y < self._line_points and self._checkerboard[y][x] == value:
#                 count += 1
#             else:
#                 break
#
#         return count >= 5


from collections import namedtuple

Chessman = namedtuple('Chessman', 'Name Value Color')
Point = namedtuple('Point', 'X Y')

BLACK_CHESSMAN = Chessman('黑子', 1, (45, 45, 45))
WHITE_CHESSMAN = Chessman('白子', 2, (219, 219, 219))

offset = [(1, 0), (0, 1), (1, 1), (1, -1)]


class Checkerboard:
    def __init__(self, line_points):
        self._line_points = line_points
        self._checkerboard = [[0] * line_points for _ in range(line_points)]
        self._history_stack = []  # 用来记录下棋历史，以便悔棋

    def _get_checkerboard(self):
        return self._checkerboard

    checkerboard = property(_get_checkerboard)

    # 判断是否可落子
    def can_drop(self, point):
        return self._checkerboard[point.Y][point.X] == 0

    def drop(self, chessman, point):
        """
        落子
        :param chessman: 落子的棋子
        :param point: 落子位置
        :return: 若该子落下之后即可获胜，则返回获胜方，否则返回 None
        """
        print(f'{chessman.Name} ({point.X}, {point.Y})')
        self._checkerboard[point.Y][point.X] = chessman.Value
        self._history_stack.append((point, chessman))  # 记录每次落子的位置和棋子

        if self._win(point):
            print(f'{chessman.Name}获胜')
            return chessman

    # 悔棋操作
    def regret(self):
        if len(self._history_stack) >= 2:
            last_point2, _ = self._history_stack.pop()
            last_point1, _ = self._history_stack.pop()
            self._checkerboard[last_point2.Y][last_point2.X] = 0
            self._checkerboard[last_point1.Y][last_point1.X] = 0
            print(f'悔棋：位置 ({last_point1.X}, {last_point1.Y}) 和 ({last_point2.X}, {last_point2.Y}) 的棋子被移除')
            return last_point1, last_point2
        else:
            print("棋数不足,无法悔棋")
            return None, None

    # 判断是否赢了
    def _win(self, point):
        cur_value = self._checkerboard[point.Y][point.X]
        for os in offset:
            if self._get_count_on_direction(point, cur_value, os[0], os[1]):
                return True

    def _get_count_on_direction(self, point, value, x_offset, y_offset):
        count = 1
        # 向一个方向延伸
        for step in range(1, 5):
            x = point.X + step * x_offset
            y = point.Y + step * y_offset
            if 0 <= x < self._line_points and 0 <= y < self._line_points and self._checkerboard[y][x] == value:
                count += 1
            else:
                break
        # 向相反方向延伸
        for step in range(1, 5):
            x = point.X - step * x_offset
            y = point.Y - step * y_offset
            if 0 <= x < self._line_points and 0 <= y < self._line_points and self._checkerboard[y][x] == value:
                count += 1
            else:
                break

        return count >= 5

        # 悔棋操作

