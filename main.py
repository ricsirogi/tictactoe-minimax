import tkinter as tk
import time
import re
import copy


class GameWindow():
    def __init__(self) -> None:
        self.tiles: list[list["Tile"]] = [[], [], []]
        self.tiles_display: list[list[tk.Button]] = [[], [], []]
        self.current_player = "X"
        self.GENERAL_FONT = ("Consolas", 80)
        self.depth = 9

        self.XWinsRegex = r"^(XXX[XO_]{6})|([XO_]{3}XXX[XO_]{3})|([XO_]{6}XXX)|(X[XO_]{2}X[XO_]{2}X[XO_]{2})|([XO_]X[XO_]{2}X[XO_]{2}X[XO_])|([XO_]{2}X[XO_]{2}X[XO_]{2}X)|(X[XO_]{3}X[XO_]{3}X)|([XO_]{2}X[XO_]X[XO_]X[XO_]{2})$"
        self.OWinsRegex = r"^(OOO[XO_]{6})|([XO_]{3}OOO[XO_]{3})|([XO_]{6}OOO)|(O[XO_]{2}O[XO_]{2}O[XO_]{2})|([XO_]O[XO_]{2}O[XO_]{2}O[XO_])|([XO_]{2}O[XO_]{2}O[XO_]{2}O)|(O[XO_]{3}O[XO_]{3}O)|([XO_]{2}O[XO_]O[XO_]O[XO_]{2})$"

        self.window = tk.Tk()
        self.window.title("Tic Tac Toe OP")
        self.window.bind("<Escape>", lambda _: self.reset())
        for row in range(3):
            for column in range(3):
                self.tiles[row].append(Tile(row, column))
                self.tiles_display[row].append(tk.Button(
                    self.window, text="_", font=self.GENERAL_FONT, width=3, command=lambda row=row, column=column: self.clicked(row, column)))
                self.tiles_display[row][column].grid(row=row, column=column)

        self.window.mainloop()

    def reset(self):
        for row in range(3):
            for column in range(3):
                self.tiles[row][column].value = "_"
                self.tiles_display[row][column].config(text="_")
        self.current_player = "X"

    def clicked(self, row: int, column: int):
        if self.tiles[row][column].value != "_" or self.terminal(self.tiles):
            return
        self.tiles[row][column].value = self.current_player
        self.tiles_display[row][column].config(text=self.current_player)
        if self.current_player == "X":
            self.current_player = "O"
            if self.terminal(self.tiles):
                return
            start_time = time.time()
            bot = self.Minimax(self.tiles, self.depth)[1]
            print("Computer thinking time:", time.time() - start_time)
            self.clicked(bot[0], bot[1])
        else:
            self.current_player = "X"

    def Minimax(self, board: list[list["Tile"]], depth: int, alpha: float = float("-inf"), beta: float = float("inf")) -> tuple[float, tuple[int, int, str]]:
        if self.terminal(board) or depth == 0:
            return (self.value(board), None)  # type:ignore

        next_player = self.player(board)
        if next_player == "X":
            best_value = float("-inf")
            best_action: Tile = None  # type:ignore
            for action in self.actions(board):
                value, _ = self.Minimax(self.result(board, action), depth-1, alpha, beta)
                if value > best_value:
                    best_value = value
                    best_action = action
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value, best_action

        if next_player == "O":
            best_value = float("inf")
            best_action: tuple[int, int, str] = None  # type:ignore
            for action in self.actions(board):
                value, _ = self.Minimax(self.result(board, action), depth-1, alpha, beta)
                if value < best_value:
                    best_value = value
                    best_action = action
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value, best_action
        else:
            return (0, None)  # type:ignore

    def actions(self, board: list[list["Tile"]]) -> list[tuple[int, int, str]]:
        actions = []
        player_symbol = self.player(board)
        for row in board:
            for tile in row:
                if tile.value == "_":
                    actions.append((tile.row, tile.column, player_symbol))
        return actions

    def player(self, board: list[list["Tile"]]) -> str:
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

    def result(self, board: list[list["Tile"]], action: tuple[int, int, str]) -> list[list["Tile"]]:
        new_board = copy.deepcopy(board)
        new_board[action[0]][action[1]].value = action[2]
        return new_board

    def terminal(self, board: list[list["Tile"]]) -> bool:
        board_str = self.board_to_str(board)

        if re.search(self.XWinsRegex, board_str) or re.search(self.OWinsRegex, board_str) or "_" not in board_str:
            return True
        return False

    def value(self, board: list[list["Tile"]]) -> int:
        if re.search(self.XWinsRegex, self.board_to_str(board)):
            return 1
        elif re.search(self.OWinsRegex, self.board_to_str(board)):
            return -1
        else:
            return 0

    def board_to_str(self, board: list[list["Tile"]]) -> str:
        board_str = ""
        for row in board:
            for tile in row:
                board_str += tile.value
        return board_str

    def print_board(self, board: list[list["Tile"]]) -> None:
        row = 0
        for column in range(9):
            if column % 3 == 0:
                row += 1
                print()
            print(board[row - 1][column % 3].value, end=" ")


class Tile():
    def __init__(self, row: int, column: int, value: str = "_") -> None:
        self.row: int = row
        self.column: int = column
        self.value: str = value


if __name__ == "__main__":
    app = GameWindow()
