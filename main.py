import tkinter as tk
import re


class GameWindow():
    def __init__(self) -> None:
        self.tiles: list[list[Tile]] = [[], [], []]
        self.tiles_display: list[list[tk.Button]] = [[], [], []]
        self.current_player = "X"
        self.GENERAL_FONT = ("Consolas", 20)

        self.XWinsRegex = " /(XXX[XO_]{6})|([XO_]{3}XXX[XO_]{3})|([XO_]{6}XXX)|(X[XO_]{2}X[XO_]{2}X[XO_]{2})|([XO_]X[XO_]{2}X[XO_]{2}X[XO_])|([XO_]{2}X[XO_]{2}X[XO_]{2}X)|(X[XO_]{3}X[XO_]{3}X)|([XO_]{2}X[XO_]X[XO_]X[XO_]{2})/g"
        self.OWinsRegex = " /(OOO[XO_]{6})|([XO_]{3}OOO[XO_]{3})|([XO_]{6}OOO)|(O[XO_]{2}O[XO_]{2}O[XO_]{2})|([XO_]O[XO_]{2}O[XO_]{2}O[XO_])|([XO_]{2}O[XO_]{2}O[XO_]{2}O)|(O[XO_]{3}O[XO_]{3}O)|([XO_]{2}O[XO_]O[XO_]O[XO_]{2})/g"

        self.window = tk.Tk()

        for row in range(3):
            for column in range(3):
                self.tiles[row].append(Tile(row, column))
                self.tiles_display[row].append(tk.Button(
                    self.window, text="_", font=self.GENERAL_FONT, command=lambda row=row, column=column: self.clicked(row, column)))
                self.tiles_display[row][column].grid(row=row, column=column)

        self.window.mainloop()

    def clicked(self, row: int, column: int):
        if self.tiles[row][column].value != "_":
            return
        self.tiles[row][column].value = self.current_player
        self.tiles_display[row][column].config(text=self.current_player)
        if self.current_player == "X":
            self.current_player = "O"
            bot = self.Minimax(self.tiles, 6)[1]
            self.clicked(bot.row, bot.column)
        else:
            self.current_player = "X"

    def Minimax(self, board: list[list["Tile"]], depth: int) -> tuple[float, "Tile"]:
        if self.terminal(board) or depth == 0:
            return (self.value(board), None)  # type:ignore

        if self.player(board) == "MAX":
            best_value = float("-inf")
            best_action: Tile = None  # type:ignore
            for action in self.actions(board):
                value, _ = self.Minimax(self.result(board, action), depth-1)
                if value > best_value:
                    best_value = value
                    best_action = action
            return best_value, best_action

        if self.player(board) == "MIN":
            best_value = float("inf")
            best_action: Tile = None  # type:ignore
            for action in self.actions(board):
                value, _ = self.Minimax(self.result(board, action), depth-1)
                if value < best_value:
                    best_value = value
                    best_action = action
            return best_value, best_action

        else:
            return (0, None)  # type:ignore

    def actions(self, board: list[list["Tile"]]) -> list["Tile"]:
        actions = []
        for row in board:
            for tile in row:
                if tile.value == "_":
                    next_player = self.player(board)
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

    def player(self, board: list[list["Tile"]]) -> str:
        x = 0
        o = 0
        for row in board:
            for tile in row:
                if tile.value == "X":
                    x += 1
                elif tile.value == "O":
                    o += 1
        if x > o:
            return "MIN"
        elif o == x:
            return "MAX"
        else:
            return "ERROR"

    def result(self, board: list[list["Tile"]], action: "Tile"):
        board[action.row][action.column].value = action.value
        return board

    def terminal(self, board: list[list["Tile"]]) -> bool:
        board_str = ""
        for row in board:
            for tile in row:
                board_str += tile.value
        if re.search(self.XWinsRegex, board_str) or re.search(self.OWinsRegex, board_str) or "_" not in board_str:
            return True
        else:
            return False

    def value(self, board: list[list["Tile"]]) -> int:
        board_str = ""
        for row in board:
            for tile in row:
                board_str += tile.value

        if re.search(self.XWinsRegex, board_str):
            return 1
        elif re.search(self.OWinsRegex, board_str):
            return -1
        else:
            return 0


class Tile():
    def __init__(self, row: int, column: int) -> None:
        self.row: int = row
        self.column: int = column
        self.value: str = "_"


if __name__ == "__main__":
    app = GameWindow()
