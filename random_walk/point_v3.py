from tkinter import *
from random import randint

# считать значение приоритетного значения из слайдера
def set_prior_direction(value):
    prior_scale.set(value)

# считать значнеие множителя шага для приоитетного направления из слайдера
def set_prior_mult(value):
    mult_scale.set(value)

#создание интерфейса
root = Tk()
root.geometry('600x600')
# область для рисования
canvas_frame = Frame(root)
canvas = Canvas(root, width=600, height=500, background='grey') # устанавливаем размер и цвет фона
canvas.place(x = 0, y = 100)

# рамка (Frame) с виджетами для приоритетного направления
direction_frame = LabelFrame(root, text='Приоритетное направление', width = 600, height=100)

# слайдер для приоитетного направления
prior_scale = IntVar() # переменная для хранения направления из слайдера
scale_direction = Scale(direction_frame, label='Направление', variable = prior_scale, from_=0, to=3, orient=HORIZONTAL, length=200, showvalue=0, tickinterval=1, resolution=1, command=set_prior_direction)
scale_direction.place(x = 10, y = 1)
prior_scale.set(0) # начальное приоритетное направление - влево
lbl_info = Label(root, text='0 - влево, 1 - вправо, 2 - вверх, 3 - вниз')
lbl_info.place(x = 10, y = 75)
# слайдер для "силы притяжения" - множителя шага
mult_scale = IntVar() # переменная для хранения множителя
scale_mult = Scale(direction_frame, label='Множитель шага (сила притяжения)', variable = mult_scale, from_=1, to=5, orient=HORIZONTAL, length=240, showvalue=0, tickinterval=1, resolution=1, command=set_prior_mult)
scale_mult.place(x = 300, y = 1)
mult_scale.set(1) # начальный множитель

direction_frame.place(x = 0, y = 0)

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

    offset = step # смещение точки
    # случайное направление
    direction = randint(0, 7)
    if direction > 3: # 50% на приоритетное направление
        direction = prior_scale.get()
        offset *= mult_scale.get() # смещение умножаем на заданный шаг для приоритетного
    if direction == 0: # 0 - влево
        new_x = cur_x - offset
        new_y = cur_y
        canvas.move(point, -offset, 0)  # смещение на форме
    elif direction == 1: # 1 - вправо
        new_x = cur_x + offset
        new_y = cur_y
        canvas.move(point, offset, 0)
    elif direction == 2: # 2 - вверх
        new_x = cur_x
        new_y = cur_y - offset
        canvas.move(point, 0, -offset)
    else: # вниз
        new_x = cur_x
        new_y = cur_y + offset
        canvas.move(point, 0, offset)
    canvas.create_line(cur_x, cur_y, new_x, new_y, fill="white", width=2) # линия траектории
    cur_x, cur_y = new_x, new_y # обновляем текущие координаты
    canvas.after(100, move_point) # следующее движение

canvas.after(100, move_point()) # первое перемещение точки
root.mainloop()
