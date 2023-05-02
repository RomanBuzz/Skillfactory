from random import randint
import re

delimiters = r"[\n\t .,]+"


# Собственный тип данных "Точка"
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


# Собственные классы исключений
class GameBoardExceptions(Exception):
    pass


class OutOfBoardError(GameBoardExceptions):
    def __str__(self):
        return "Вы стреляете за пределы поля! Измените координату!"


class OccupiedPossitionError(GameBoardExceptions):
    def __str__(self):
        return "Запрещено стрелять в одну и ту же клетку несколько раз! Измените координату!"


# Для проверки размещения корабля за пределами доски или на занятой ячейке
class WrongShipLocationError(GameBoardExceptions):
    pass


# Класс для представления корабля, принимающий в себя набор точек (координат) на игровой доске
class Ship:
    def __init__(self, bow, ln, dr):
        # начальная точка корабля
        self.bow = bow
        # длина корабля
        self.ln = ln
        # направление корабля: 0 - по вертикали вниз, 1 - по горизонтали вправо
        self.dr = dr
        self.health = ln

    # свойство position возвращает место расположения всех точек корабля
    @property
    def position(self):
        ship_position = []
        for i in range(self.ln):
            point_x = self.bow.x
            point_y = self.bow.y

            if self.dr == 0:
                point_x += i

            elif self.dr == 1:
                point_y += i

            ship_position.append(Point(point_x, point_y))

        return ship_position

    # проверка попадания в корабль
    def hit(self, shot):
        return shot in self.position


# Класс доски, принимающей набор кораблей
class GameBoard:
    def __init__(self, hidden=False, size=6):
        self.hidden = hidden
        self.size = size
        self.dead_ships = 0
        self.board = [["0"] * size for _ in range(size)]
        self.occupied = []
        self.ships = []

    # Печать игрового поля
    def __str__(self):
        prnt = "  |" if self.size < 10 else "   |"
        for i in range(self.size):
            prnt += f" {i + 1} |" if self.size < 10 else f" {i + 1} |"
        for kol in range(self.size):
            prnt += f"\n{kol + 1} |" if self.size < 10 or kol + 1 >= 10 else f"\n{kol + 1}  |"
            for stolb in range(self.size):
                prnt += f" {self.board[kol][stolb]} |" if stolb + 1 < 10 else f"  {self.board[kol][stolb]} |"

        if self.hidden:
            prnt = prnt.replace("■", "O")
        return prnt

    # Проверяем находится ли точка за пределами доски
    def out_of_board(self, pos):
        return not ((0 <= pos.x < self.size) and (0 <= pos.y < self.size))

    # Корабли должны находится на расстоянии минимум одной клетки друг от друга
    def near_ship(self, ship, near_open=False):
        for p in ship.position:
            for ax in range(-1, 2):
                for ay in range(-1, 2):
                    pos = Point(p.x + ax, p.y + ay)
                    if not (self.out_of_board(pos)) and pos not in self.occupied:
                        self.occupied.append(pos)
                        if near_open:
                            self.board[pos.x][pos.y] = "T"

    # Ставим корабль на доску
    def add_ship(self, ship):
        for pos in ship.position:
            if self.out_of_board(pos) or pos in self.occupied:
                raise WrongShipLocationError()
        for pos in ship.position:
            self.board[pos.x][pos.y] = "■"
            self.occupied.append(pos)
        self.ships.append(ship)
        self.near_ship(ship)

    # Делаем выстрел
    def shot(self, pos):
        if self.out_of_board(pos):
            raise OutOfBoardError()

        if pos in self.occupied:
            raise OccupiedPossitionError()

        self.occupied.append(pos)

        for ship in self.ships:
            if ship.hit(pos):
                ship.health -= 1
                self.board[pos.x][pos.y] = "X"
                if ship.health == 0:
                    self.dead_ships += 1
                    self.near_ship(ship, True)
                    print("Потопил!")
                    # второй ход не нужен
                    return False
                else:
                    print("Ранил!")
                    # второй ход нужен
                    return True

        self.board[pos.x][pos.y] = "T"
        print("Промазал!")
        # второй ход не нужен
        return False

    def begin(self):
        self.occupied = []


class Players:
    def __init__(self, game_board, opponent_board):
        self.game_board = game_board
        self.opponent_board = opponent_board

    def ask_coord(self):
        raise NotImplementedError()

    def player_step(self):
        while True:
            try:
                target = self.ask_coord()
                shoot = self.opponent_board.shot(target)
                # Если ранил, то возвращает True, тогда попавший стреляет еще раз
                return shoot
            except GameBoardExceptions as err:
                print(err)


class CompPlayer(Players):
    def ask_coord(self):
        pos = Point(randint(0, self.opponent_board.size - 1), randint(0, self.opponent_board.size - 1))
        print(f"Выстрел компьютера: {pos.x + 1} {pos.y + 1}")
        return pos


class UserPlayer(Players):
    def ask_coord(self):
        while True:
            pos = re.split(delimiters, input(f"Ваш ход! Введите координаты: Строка, Столбец!\n"))
            if len(pos) != 2:
                print("Необходимо ввести 2 координаты! Повторите!")
                continue

            x, y = pos

            try:
                x, y = int(x), int(y)
            except ValueError:
                print("Необходимо ввести 2 целых числа! Повторите!")
                continue

            return Point(x - 1, y - 1)


class GameLogic:
    def __init__(self, size=6):
        self.size = size
        self.ship_lens = []
        user_board = self.create_board()
        comp_board = self.create_board()
        comp_board.hidden = True
        self.user = UserPlayer(user_board, comp_board)
        self.comp = CompPlayer(comp_board, user_board)

    def create_ship(self):
        self.ship_lens = []
        ship_size = self.size // 2
        if ship_size >= 4:
            ship_size -= 1
        if ship_size > 6:
            ship_size = 6
        kol_ships = 1
        for i in range(ship_size):
            for _ in range(kol_ships):
                self.ship_lens.append(ship_size - i)
            if i == 1:
                kol_ships += 1
            kol_ships += 1
        board = GameBoard(size=self.size)
        attempts = 0
        for lens in self.ship_lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Point(randint(0, self.size-1), randint(0, self.size-1)), lens, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except WrongShipLocationError:
                    pass
        board.begin()
        return board

    def create_board(self):
        board = None
        while board is None:
            board = self.create_ship()
        return board

    def play_game(self):
        step = 0
        while True:
            print("-" * 5, "Поле пользователя:", "-" * 5)
            print(self.user.game_board)
            print("-" * 5, "Поле Компьютера:", "-" * 5)
            print(self.comp.game_board)
            if step % 2 == 0:
                print("-" * 5, "Ход пользователя:", "-" * 5)
                shoot = self.user.player_step()
            else:
                print("-" * 5, "Ход Компьютера:", "-" * 5)
                shoot = self.comp.player_step()
            # Повторить ход, если ранен
            if shoot:
                step -= 1

            if self.comp.game_board.dead_ships == len(self.ship_lens):
                print("-" * 5, "!!! Пользователь победил !!!", "-" * 5)
                break

            if self.user.game_board.dead_ships == len(self.ship_lens):
                print("-" * 5, "!!! Компьютер победил !!!", "-" * 5)
                break
            step += 1


# НАЧАЛО
print("*" * 5, " Игра Морской бой для любого заданного пользователем размера игрового поля ", "*" * 5)
print("*" * 5, " Формат ввода: Номер строки, Номер столбца ", "*" * 5)

b_size = 0
while b_size <= 2:
    b_size = input(f"Введите размерность игрового поля (число от 3 до 99):\n")
    try:
        b_size = int(b_size)
    except ValueError:
        print("Необходимо ввести целое числа! Повторите!")
        b_size = 0
        continue
    if b_size <= 2 or b_size >= 100:
        print("Вы ввели некорректное значение! Повторите снова!")
        b_size = 0
        continue

game = GameLogic(b_size)
game.play_game()
