from tkinter import *

#создание интерфейса
root = Tk()
root.geometry('600x600')
# область для рисования
canvas_frame = Frame(root)
canvas = Canvas(root, width=600, height=600, background='grey') # устанавливаем размер и цвет фона
canvas.place(relx = 0, rely = 0)

# старатовая позциия частицы и радиус
start_x = 300
start_y = 300
radius = 35
# текущая позиция и шаг изменения положения по y
cur_x = start_x
cur_y = start_y
step_y = 15
# создаем окружность
circle = canvas.create_oval(start_x, start_y, start_x + radius, start_y + radius, fill='white')

# функция перемещения круга
def move_circle():
    global cur_y, start_y, radius, step_y
    cur_y += step_y # смещение позиции
    canvas.move(circle, 0, step_y) # смещение на форме
    # если достигли границ, либо начальной позиции, меняем направление
    if (cur_y <= start_y) or (cur_y + radius >= 600):
        step_y *= -1
    canvas.after(50, move_circle) # следующее движение

canvas.after(50, move_circle) # первое перемещение круга
root.mainloop()
