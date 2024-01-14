import re

XWinsRegex = r"^(XXX[XO_]{6})|([XO_]{3}XXX[XO_]{3})|([XO_]{6}XXX)|(X[XO_]{2}X[XO_]{2}X[XO_]{2})|([XO_]X[XO_]{2}X[XO_]{2}X[XO_])|([XO_]{2}X[XO_]{2}X[XO_]{2}X)|(X[XO_]{3}X[XO_]{3}X)|([XO_]{2}X[XO_]X[XO_]X[XO_]{2})$"
OWinsRegex = r"^(OOO[XO_]{6})|([XO_]{3}OOO[XO_]{3})|([XO_]{6}OOO)|(O[XO_]{2}O[XO_]{2}O[XO_]{2})|([XO_]O[XO_]{2}O[XO_]{2}O[XO_])|([XO_]{2}O[XO_]{2}O[XO_]{2}O)|(O[XO_]{3}O[XO_]{3}O)|([XO_]{2}O[XO_]O[XO_]O[XO_]{2})$"


def player(board: list[list["Tile"]]) -> str:
    o, x = 0, 0
    for row in board:
        for tile in row:
            if tile.value == "O":
                o += 1
            elif tile.value == "X":
                x += 1
    if x > o:
        return "O"
    elif o == x:
        return "X"
    else:
        return "ERROR"


def actions(board: list[list["Tile"]]) -> list["Tile"]:
    actions = []
    for row in board:
        for tile in row:
            if tile.value == "_":
                next_player = player(board)
                if next_player == "MAX":
                    symbol = "X"
                elif next_player == "MIN":
                    symbol = "O"
                else:
                    return []
                return_tile = Tile(tile.row, tile.column)
                return_tile.value = symbol
                actions.append(return_tile)
    return actions


def result(board: list[list["Tile"]], action: "Tile"):
    board[action.row][action.column].value = action.value
    return board


def terminal(board: list[list["Tile"]]) -> bool:
    board_str = board_to_str(board)

    if re.search(XWinsRegex, board_str) or re.search(OWinsRegex, board_str) or "_" not in board_str:
        return True
    return False


def value(board: list[list["Tile"]]) -> int:
    if re.search(XWinsRegex, board_to_str(board)):
        return 1
    elif re.search(OWinsRegex, board_to_str(board)):
        return -1
    else:
        return 0


def board_to_str(board: list[list["Tile"]]) -> str:
    board_str = ""
    for row in board:
        for tile in row:
            board_str += tile.value
    return board_str


class Tile():
    def __init__(self, row: int, column: int, value: str = "_") -> None:
        self.row = row
        self.column = column
        self.value = value


b: list[list[Tile]] = [[], [], []]
b[0].append(Tile(0, 0, "X"))
b[0].append(Tile(0, 1, "_"))
b[0].append(Tile(0, 2, "_"))
b[1].append(Tile(1, 0, "_"))
b[1].append(Tile(1, 1, "_"))
b[1].append(Tile(1, 2, "_"))
b[2].append(Tile(2, 0, "_"))
b[2].append(Tile(2, 1, "_"))
b[2].append(Tile(2, 2, "_"))

print(player(b))

"""acts = [a for a in actions(b)]
act = acts[4]
r = result(b, act)
"""
row = 0
for column in range(9):
    if column % 3 == 0:
        row += 1
        print()
    print(b[row - 1][column % 3].value, end=" ")
"""
for act in acts:
    pass
    # print(act.row, act.column, act.value)"""
