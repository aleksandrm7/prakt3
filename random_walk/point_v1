from tkinter import *
from random import randint

#создание интерфейса
root = Tk()
root.geometry('600x600')
# область для рисования
canvas_frame = Frame(root)
canvas = Canvas(root, width=600, height=600, background='grey') # устанавливаем размер и цвет фона
canvas.place(relx = 0, rely = 0)

# старатовая позциия точки и радиус
start_x = 300
start_y = 300
radius = 5
# текущая позиция и шаг по обоим координатам
cur_x = start_x
cur_y = start_y
step = 5
# создаем точку (окружность)
point = canvas.create_oval(start_x, start_y, start_x + radius, start_y + radius, fill='white')

# функция перемещения точки
def move_point():
    global cur_x, cur_y, radius, step

    # случайное направление
    direction = randint(0, 3)
    if direction == 0: # 0 - влево
        new_x = cur_x - step
        new_y = cur_y
        canvas.move(point, -step, 0)  # смещение на форме
    elif direction == 1: # 1 - вправо
        new_x = cur_x + step
        new_y = cur_y
        canvas.move(point, step, 0)
    elif direction == 2: # 2 - вверх
        new_x = cur_x
        new_y = cur_y - step
        canvas.move(point, 0, -step)
    else: # вниз
        new_x = cur_x
        new_y = cur_y + step
        canvas.move(point, 0, step)
    canvas.create_line(cur_x, cur_y, new_x, new_y, fill="white", width=2) # линия траектории
    cur_x, cur_y = new_x, new_y # обновляем текущие координаты
    canvas.after(100, move_point) # следующее движение

canvas.after(100, move_point()) # первое перемещение точки
root.mainloop()
