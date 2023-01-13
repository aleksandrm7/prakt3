import math
import pygame
import configure as st


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def rotate(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        if sound:
            sound.play()
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.pos = [pos[0] + self.radius, pos[1] + self.radius]

    def collide(self, other_object):
        if dist(self.pos, other_object.get_position()) <= self.radius + other_object.get_radius():
            return True
        else:
            return False

    def get_position(self):
        return [int(self.pos[0]), int(self.pos[1])]

    def get_radius(self):
        return self.radius

    def draw(self, canvas):

        if self.animated:
            self.age += 1
            if self.age < 14:
                canvas.blit(self.image[self.age], self.pos)
        else:
            canvas.blit(rotate(self.image, self.angle),
                        (int(self.pos[0] - self.radius), int(self.pos[1] - self.radius)))

    def update(self):
        self.angle += self.angle_vel

        self.pos[0] = (self.pos[0] + self.vel[0]) % st.WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % st.HEIGHT

        self.age += 1

        if self.age < self.lifespan:
            return False
        else:
            return True


def angle_to_vector(ang):
    return [math.cos(ang), -math.sin(ang)]


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
