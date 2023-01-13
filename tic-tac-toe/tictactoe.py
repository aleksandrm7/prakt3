from tkinter import *
from tkinter import messagebox, font

# Создание интерфейса

field_width = 450
field_height = 450

turn = 1  # обозначение хода: 1 - крестики, -1 - нолики
turns_left = 9  # сколько ходов осталось
# матрица для хранения значений клеток поля. изначально заполнена пробелами, при игре заполняется X и 0
field_matrix = []
field_matrix.append([' '] * 3)
field_matrix.append([' '] * 3)
field_matrix.append([' '] * 3)

root = Tk()
root.geometry('450x500')
root.title('Крестики-нолики')
# Игровое поле
canvas = Canvas(root, width=field_width, height=field_height, background='grey')  # Устанавливаем размер и цвет фона
canvas.place(relx = 0, rely = 0)


# Линии разметки поля
def draw_field_lines():
    canvas.create_line(field_width / 3, 0, field_width / 3, field_height, fill='black', width=3)
    canvas.create_line((field_width / 3) * 2, 0, (field_width / 3) * 2, field_height, fill='black', width=3)
    canvas.create_line(0, field_height / 3, field_width, field_height / 3, fill='black', width=3)
    canvas.create_line(0, (field_height / 3) * 2, field_width, (field_height / 3) * 2, fill='black', width=3)

# Нарисовать крестик в ячейке поля, соответствующей i, j
def draw_cross(i, j):
    cross_len = field_width / 3 - 20 # ширина крестика
    # Координаты концов линий
    start_x = field_width / 3 * j + 10
    start_y = field_height / 3 * i + 10
    end_x = start_x + cross_len
    end_y = start_y + cross_len
    canvas.create_line(start_x, start_y, end_x, end_y, fill='blue', width=5)
    canvas.create_line(start_x, end_y, end_x, start_y, fill='blue', width=5)

# Нарисовать нолик в ячейке поля, соответсвующей i, j
def draw_zero(i, j):
    zero_len = field_width / 3 - 20
    start_x = field_width / 3 * j + 10
    start_y = field_height / 3 * i + 10
    end_x = start_x + zero_len
    end_y = start_y + zero_len
    canvas.create_oval(start_x, start_y, end_x, end_y, outline='orange', width=5)

# Получить индексы ячейки поля из координат мыши при клике
def get_click_coords(event):
    i = event.y // (field_height // 3)
    j = event.x // (field_width // 3)
    return int(i), int(j)

# Проверить победу (заполенние клеток строки или столбца или диагонали тремя символами)
def check_win(row, col):
    global turn
    # Текущий символ для проверки линиии
    if turn == 1:
        symbol = 'X'
    else:
        symbol = '0'
    # Проверка строки
    win = True  # Есть ли победа
    for j in range(3):
        if field_matrix[row][j] != symbol:
            win = False
    # Проверка столбца
    if not win:
        win = True
        for i in range(3):
            if field_matrix[i][col] != symbol:
                win = False
    # Если совпадают координаты, проверяем главную диагональ
    if not win and row == col:
        win = True
        for i in range(3):
            if field_matrix[i][i] != symbol:
                win = False
    # Если побочная диагональ, првоеряем ее
    if not win and col == 2 - row:
        win = True
        for i in range(3):
            if field_matrix[i][2-i] != symbol:
                win = False
    if win: # При победе возвращаем обозначение хода игрока
        return turn
    else: # При отсутствии победы - 0
        return 0

# Сделать ход
def make_turn(event):
    global turn, turns_left
    if turns_left <= 0:  # Если ходов не осталось, ничего не делаем
        return
    i, j = get_click_coords(event)  # Получаем координаты ячейки
    if field_matrix[i][j] == ' ':  # Если ячейка не занята
        if turn == 1:  # Если ход крестиков
            draw_cross(i, j)
            field_matrix[i][j] = 'X'
        else:  # Иначе рисуем нолик
            draw_zero(i, j)
            field_matrix[i][j] = '0'
        turns_left -= 1  # Минус один ход
        winner = check_win(i, j)  # Проверяем победу игрока
        if winner == 1:
            messagebox.showinfo('Игра завершена', 'Игра завершена! Победитель: крестики')
            turns_left = 0
        elif winner == -1:
            messagebox.showinfo('Игра завершена', 'Игра завершена! Победитель: нолики')
            turns_left = 0
        elif turns_left == 0:  # Если ходы кончились, объялвяется ничья
            messagebox.showinfo('Игра завершена', 'Игра завершилась ничьей!')
        turn *= -1  # Смена хода

# Начать новую игру - очистить поле и сбросить количество ходов
def start_game():
    global turns_left, turn
    canvas.delete('all')
    draw_field_lines()  # Наносим разметку
    # Очищаем матрицу поля
    for i in range(3):
        for j in range(3):
            field_matrix[i][j] = ' '
    turns_left = 9
    turn = 1

# Привязываем к полю событие клика мыши - выполнение хода
canvas.bind('<Button-1>', make_turn) # Клик левой кнопкой мыши
# Кнопка для начала новой игры
btn_game = Button(root, text="НОВАЯ ИГРА", width=15, font=font.Font(family='Helvetica', size=11), bg='lightgreen', command=start_game)
btn_game.place(x = 150, y = 460)

root.mainloop()
