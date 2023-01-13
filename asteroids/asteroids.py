import pygame, sys, os, random, math
from pygame.locals import *
import configure as st
import classes as cl

pygame.mixer.pre_init()
pygame.init()
fps = pygame.time.Clock()

window = pygame.display.set_mode((st.WIDTH, st.HEIGHT), 0, 34)
pygame.display.set_caption('Asteroids Rain')

"""Класс корабля"""


class Ship:
    def __init__(self, pos, vel, angle, image, thrust_image, info):
        self.pos = [pos[0] - 45, pos[1] - 45]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.thrust_image = thrust_image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward = [0, 0]

    def shoot(self):
        global a_missile

        missile_pos = [self.pos[0] + 40 + self.radius * self.forward[0],
                       self.pos[1] + 40 + self.radius * self.forward[1]]

        missile_vel = [self.vel[0] + 6 * self.forward[0], self.vel[1] + 6 * self.forward[1]]
        missile_group.add(cl.Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info))

    def set_thrust(self, thrust):

        self.thrust = thrust

    def get_position(self):
        return (int(self.pos[0] + self.radius), int(self.pos[1] + self.radius))

    def get_radius(self):
        return self.radius

    def draw(self, canvas):

        if self.thrust:
            canvas.blit(cl.rotate(self.thrust_image, self.angle), self.pos)
        else:
            canvas.blit(cl.rotate(self.image, self.angle), self.pos)

    def update(self):
        acc = 0.5
        fric = acc / 20

        self.angle += self.angle_vel

        self.forward = cl.angle_to_vector(math.radians(self.angle))

        if self.thrust:
            self.vel[0] += self.forward[0] * acc
            self.vel[1] += self.forward[1] * acc

        self.vel[0] *= (1 - fric)
        self.vel[1] *= (1 - fric)

        self.pos[0] = (self.pos[0] + self.vel[0]) % (st.WIDTH - self.radius)
        self.pos[1] = (self.pos[1] + self.vel[1]) % (st.HEIGHT - self.radius)

    def set_angle_vel(self, vel):
        self.angle_vel = vel


"""Функция, нарезающая спрайты взрыва"""


def load_sliced_sprites(w, h, filename):
    images = []
    master_image = pygame.image.load(os.path.join('images', filename)).convert_alpha()

    master_width, master_height = master_image.get_size()
    for i in range(int(master_width / w)):
        images.append(master_image.subsurface((i * w, 0, w, h)))
    return images


"""Изображение заставки"""
splash = pygame.image.load(os.path.join('images', 'splash.png'))

"""Статический фон"""
nebula = pygame.image.load(os.path.join('images', 'background.png'))

"""Динамический фон"""
debris = pygame.image.load(os.path.join('images', 'dynamic.png'))

"""Изображение корабля"""
ship_image = pygame.image.load(os.path.join('images', 'ship.png'))
ship_info = cl.ImageInfo([45, 45], [90, 90], 45)

"""Изображение корабля при ускорении"""
thrusted_ship_image = pygame.image.load(os.path.join('images', 'ship_2.png'))
thrusted_ship_info = cl.ImageInfo([45, 45], [90, 90], 45)

"""Изображение астероидов"""
rock_image = pygame.image.load(os.path.join('images', 'asteroid.png'))
rock_info = cl.ImageInfo([45, 45], [90, 90], 45)

"""Изображение ракеты"""
missile_image = pygame.image.load(os.path.join('images', 'shot.png'))
missile_info = cl.ImageInfo([5, 5], [10, 10], 5, 50)

"""Изображения взрыва"""
explosion_images = load_sliced_sprites(128, 128, 'boom.png')
explosion_info = cl.ImageInfo([64, 64], [128, 128], 64, 24, True)

Board = Ship([st.WIDTH // 2, st.HEIGHT // 2], [0, 0], 0, ship_image, thrusted_ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])


def process_sprite_group(canvas):
    for rock in rock_group:
        rock.draw(canvas)
        rock.update()

    for missile in list(missile_group):
        missile.draw(canvas)
        if missile.update():
            missile_group.remove(missile)

    for explosion in explosion_group:
        explosion.draw(canvas)


def group_collide(group, other_object):
    counter = len(group)

    for element in list(group):
        if element.collide(other_object):
            explosion_group.add(cl.Sprite(
                [element.get_position()[0] - 3 * element.radius, element.get_position()[1] - 3 * element.radius],
                [0, 0], 0, 0, explosion_images, explosion_info))
            group.remove(element)

    return counter - len(group)


def group_group_collide(first_group, second_group):
    counter = 0

    for element in list(first_group):
        if group_collide(second_group, element) > 0:
            counter += 1
            first_group.remove(element)

    return counter


"""Функция отображения(отрисовки)"""


def draw(canvas):
    """Отображение фона"""
    canvas.fill(st.BLACK)
    canvas.blit(nebula, (0, 0))
    canvas.blit(debris, (st.time * .3, 0))
    canvas.blit(debris, (st.time * .3 - st.WIDTH, 0))
    "Если игра запущенна"
    if st.started:
        """Отображение корабля"""
        Board.draw(canvas)

        """Отображение астероидов и ракет"""
        process_sprite_group(canvas)

        Board.update()

        """Проверка столкновения корабля с астероидом"""
        if group_collide(rock_group, Board) > 0:
            """Проверка на количество жизней"""
            if st.lives > 1:  # Если при столкновении более одной жизни, то количество оставшихся убавляется на 1
                st.lives -= 1
            else:  # Если при столкновении жизни закончились, то игра останавливается
                st.lives = 0
                st.started = False

        hits = group_group_collide(missile_group, rock_group)
        if hits > 0:
            st.score += hits * 1;  # В случае попадания ракеты в астероид, прибавляеся одно очко
    else:  # Если игра не запущена, то отображается заставка
        canvas.blit(splash, (st.WIDTH // 2 - 200, st.HEIGHT // 2 - 100))

    """Отображение жизней"""
    myfont1 = pygame.font.SysFont("Arial", 25)
    label1 = myfont1.render("Lives : " + str(st.lives), 1, (42, 242, 2))
    canvas.blit(label1, (50, 20))

    """Отображение счёта"""
    myfont2 = pygame.font.SysFont("Arial", 25)
    label2 = myfont2.render("Score : " + str(st.score), 1, (42, 242, 2))
    canvas.blit(label2, (670, 20))


"""Обработчик нажатия клавиш"""


def keydown(event):
    if event.key == K_LEFT or event.key == K_a:  # При нажатии стелки влево, либо клавиши A
        Board.set_angle_vel(st.ang_vel)  # Корабль делает поворот влево
    if event.key == K_RIGHT or event.key == K_d:  # При нажатии стрелки вправо, либо клавиши D
        Board.set_angle_vel(-st.ang_vel)  # Корабль делает поворот вправо
    if event.key == K_UP or event.key == K_w:  # При нажатии стрелт вверх, либо клавиши W
        Board.set_thrust(True)  # Корабль делает ускорение
    if event.key == K_SPACE:  # При нажатии пробела
        Board.shoot()  # Корабль производит выстрел ракетой


"""Обработчик отпускания клавиши"""


def keyup(event):
    if event.key in (K_LEFT, K_RIGHT, K_a, K_d):  # Если была отпущена одна из клавиш: влево, вправо, A, D
        Board.set_angle_vel(0)  # Корабль перестаёт делать вращение (Угловая ск-ть становится 0)
    if event.key in (K_UP, K_w):  # Если была отпущена одна из клавиш: вверх, W
        Board.set_thrust(False)  # Корабль прекращает ускорение и постепено останавливается


def timer():
    if st.time <= st.WIDTH:
        st.time += 1
        if st.time % 60 == 0:
            rock_spawner()
    else:
        st.time = 0


def rock_spawner():
    global rock_group, started

    if len(rock_group) < 12 and st.started:

        while 1:
            random_pos = [random.randrange(0, st.WIDTH), random.randrange(0, st.HEIGHT)]

            if cl.dist(random_pos, Board.get_position()) <= rock_info.get_radius() + 2 * Board.get_radius():
                continue
            else:
                rock_pos = random_pos
                break

        increase = st.score / 100

        rock_vel = [random.random() * (3 + increase) - (1 + increase),
                    random.random() * (3 + increase) - (1 + increase)]
        rock_avel = random.random() * 6 - 1
        rock_group.add(cl.Sprite(rock_pos, rock_vel, 0, rock_avel, rock_image, rock_info))


def click(event):
    global started, lives, score, rock_group, missile_group, Board

    if event.button == 1 and event.pos[0] in range(st.WIDTH // 2 - 200, st.WIDTH // 2 + 200) and event.pos[1] in range(
            st.HEIGHT // 2 - 150, st.HEIGHT // 2 + 150) and not st.started:
        st.started = True
        st.lives = st.lives_start
        st.score = st.score_start
        rock_group = set([])
        missile_group = set([])


while True:

    draw(window)

    timer()

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == MOUSEBUTTONDOWN:
            click(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps.tick(60)
