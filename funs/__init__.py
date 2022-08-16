import random
import numpy as np
from colorama import Back, Fore, Style

# -------- init board
class ColorsMap:
    map = {'r': Back.RED, 'b': Back.BLUE, 'g': Back.GREEN, 'y': Back.YELLOW}

def init_board(ncol: int = 18, nrow: int = 18):
    avail_colors = ('r', 'b', 'g', 'y')
    random_colors = random.choices(avail_colors, k=ncol * nrow)
    return np.array(random_colors).reshape(ncol, nrow)


# -------- print functions

def print_row(row, colors_map: dict, dummy_char: str = "   "):
    out = ''
    for clr in row:
        out = out + colors_map[clr] + dummy_char
    print(out + Style.RESET_ALL, end="\n")

def print_board(board, colors_map):
    board = np.copy(board)
    rows, columns = board.shape
    for i in range(rows):
        print_row(row=board[i, ], colors_map=colors_map)


# ------ coloring functions

def get_colored_points(board, color: str):

    row, col = board.shape

    arr = np.where(board == color, 0, -1)

    # directions
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    # queue
    queue = []

    color_matched = []

    # insert the top right corner.
    queue.append((0, 0))

    # until queue is empty
    while len(queue) > 0:
        # print("queue is: %s" % queue)
        p = queue[0]
        queue.pop(0)

        # destination is reached.
        if p == (row - 1, col - 1):
            return color_matched

        # check all four directions
        for i in range(4):

            # using the direction array
            a = p[0] + directions[i][0]
            b = p[1] + directions[i][1]

            # not blocked and valid
            if (a >= 0 and b >= 0 and a < row and b < col and arr[a][b] != -1 and arr[p] != -1):
                queue.append((a, b))
                color_matched.append((a, b))

        # mark as visited
        arr[p[0]][p[1]] = -1

    return color_matched


def color_board(board: np.ndarray, color: str):
    board_new = np.copy(board)

    starting_color = board_new[(0, 0)]

    # get all points with current color from starting point (0, 0)
    colored_points = get_colored_points(board_new, color=starting_color)

    board_new[(0, 0)] = color

    for xy in colored_points:
        board_new[xy] = color
    return board_new

# ------------ game

def validate_color(x: str):
    colors = ColorsMap()
    return x in colors.map.keys()


def user_input(msg: str):
    selected_color = input(msg)
    colors = ColorsMap()
    if not validate_color(selected_color):
        print(Back.YELLOW + Fore.BLACK +
              "Invalid input. Select from: %s." % [x for x in colors.map.keys()] +
              Style.RESET_ALL, end="\n")
        return user_input(msg)
    else:
        return selected_color


def is_game_completed(board: np.ndarray) -> bool:
    if len(list(np.unique(board))) == 1:
        print(Back.GREEN + "\t\t!!! YOU WON !!!\t\t" + Style.RESET_ALL, end="\n")
        return True
    else:
        return False


def you_lost() -> bool:
    print("\n" + Back.RED + "\t\tYOU LOST :(\t\t" + Style.RESET_ALL, end="\n")
    return False


def start_game(board: np.ndarray, colors_map: dict, imax: int = 21):
    if board is None:
        board = init_board()
    print("Your board is:")
    print_board(board, colors_map)
    for i in range(imax):
        selected_color = user_input("(Round #%s/%s) Select color:\n" % (i, imax))
        board = color_board(board, selected_color)
        print_board(board, colors_map)
        if is_game_completed(board):
            return True
    return you_lost()


# ------ game class

class Game:
    def __init__(self, max_iteration = 21, nrow: int = 18, ncol: int = 18):
        self.max_iteration = max_iteration
        self.__ncol = ncol
        self.__nrow = nrow
        self.__board = init_board(self.__ncol, self.__nrow)
        self.__colors_map = ColorsMap().map

    def print(self):
        print_board(self.__board, self.__colors_map)
    def user_won(self):
        return is_game_completed(self.__board)
    def start(self):
        print("Your board is:")
        self.print()
        for i in range(self.max_iteration):
            selected_color = user_input("(Round #%s/%s) Select color:\n" % (i, self.max_iteration))
            self.__board = color_board(self.__board, selected_color)
            self.print()
            if self.user_won():
                return True
        return you_lost()








