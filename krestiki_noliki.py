# функция проверки координаты
def vvod_koodinat(x):
    st = -1
    while st < 0:
        kl = input("Введите номер колонки:")
        st = input("Введите номер столбца:")
        if not (kl.isdigit() and st.isdigit()):
            print("Вы ввели некорректную координату! Повторите снова!")
            st = -1
        elif (int(kl) < 0 or int(kl) > x - 1) or (int(st) < 0 or int(st) > x - 1):
            print("Вы ввели некорректную координату! Повторите снова!")
            st = -1
        else:
            kl, st = int(kl), int(st)
            return kl, st


# функция печати поля
def print_board(x, game_board):
    print("")
    print(' ', *range(len(game_board)), sep='  ')
    for i in range(x):
        print(i, *game_board[i], sep='  ')
    print("")


# функция проверки победителя
def winner_test(x, game_board):
    # проверка заполнения колонок
    for Kol in range(x):
        if all(game_board[Kol][Stolb] == game_board[Kol][Stolb + 1] and
               game_board[Kol][Stolb] != '-' for Stolb in range(x - 1)):
            if game_board[Kol][0] == "X":
                print(f"Игрок 1 победил, заполнив первым колонку № {Kol} !!!")
                return 'win'
            else:
                print(f"Игрок 2 победил, заполнив первым колонку № {Kol} !!!")
                return 'win'

    # проверка заполнения столбцов
    for Stolb in range(x):
        if all(game_board[Kol][Stolb] == game_board[Kol + 1][Stolb] and
               game_board[Kol][Stolb] != '-' for Kol in range(x - 1)):
            if game_board[0][Stolb] == "X":
                print(f"Игрок 1 победил, заполнив первым столбец № {Stolb} !!!")
                return 'win'
            else:
                print(f"Игрок 2 победил, заполнив первым столбец № {Stolb} !!!")
                return 'win'

    # проверка диагонали cверху вниз, слева направо
    if all(game_board[0][0] == game_board[Kol][Kol] and game_board[0][0] != '-' for Kol in range(x)):
        if game_board[0][0] == "X":
            print(f"Игрок 1 победил, заполнив первым диагональ сверху вниз, слева направо !!!")
            return 'win'
        else:
            print(f"Игрок 2 победил, заполнив первым диагональ сверху вниз, слева направо !!!")
            return 'win'

    #  проверка диагонали cверху вниз, справа налево
    if all(game_board[0][x - 1] == game_board[Kol][x - 1 - Kol] and
           game_board[0][x - 1] != '-' for Kol in range(x)):
        if game_board[0][x - 1] == "X":
            print(f"Игрок 1 победил, заполнив диагональ сверху вниз, справа налево !!!")
            return 'win'
        else:
            print(f"Игрок 2 победил, заполнив диагональ сверху вниз, справа налево !!!")
            return 'win'

    # проверка на ничью
    if all(all(game_board[Kol][Stolb] != '-' for Stolb in range(x)) for Kol in range(x)):
        print("Игра закончилась ничьей !!!")
        return 'win'


# НАЧАЛО
print("*" * 5, " Игра Крестики-нолики для любого заданного пользователем размера игрового поля", "*" * 5)

v = 0
while v <= 0:
    v = input("Введите размерность игрового поля (положительноe число):")
    if not v.isdigit() or v == "0":
        print("Вы ввели некорректное значение! Повторите снова!")
        v = 0
    else:
        v = int(v)

# cоздание и первая печать игрового поля (при размерности поля более 11 коряво показывает столбцы, исправлять не стал)
game_board_start = [["-" for i in range(v)] for a in range(v)]
print("Игровое поле готово! Наслаждайтесь игрой!")
print_board(v, game_board_start)

igroki = (("1", "крестик", "X"), ("2", "нолик", "0"))
test = ""
while True:
    for i in range(2):
        while True:
            print(f"Ход игрока {igroki[i][0]} '{igroki[i][1]}':")
            k, s = vvod_koodinat(v)
            # проверка занятости ячейки: если занята, вернуться в начало
            if game_board_start[k][s] == '-':
                game_board_start[k][s] = igroki[i][2]
                print_board(v, game_board_start)
                break
            else:
                print("Вы выбрали занятую ячейку! Повторите снова!")
                continue
        test = winner_test(v, game_board_start)
        if test == 'win':
            break
    if test == 'win':
        break
