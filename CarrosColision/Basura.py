# Autor: Bounty Hunters

import math

import numpy as np
import pygame

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *


# Clase para el cubo Basura
class Basura:
    boxes_positions = {}

    def __init__(self, position, texture_file, map_coords):
        # Vertices del cubo
        self.points = np.array(
            [
                [-1.0, -1.0, 1.0],
                [1.0, -1.0, 1.0],
                [1.0, -1.0, -1.0],
                [-1.0, -1.0, -1.0],
                [-1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0],
                [1.0, 1.0, -1.0],
                [-1.0, 1.0, -1.0],
            ]
        )
        self.Direction = [0, 0, 0]
        self.Position = position  # Posición fija en el plano
        self.texture = self.load_texture(texture_file)
        self.animation_speed = 0.1
        self.target_reference = None
        self.map_coords = map_coords
        self.scale = 5

    def load_texture(self, texture_file):
        # Cargar imagen como textura
        texture_surface = pygame.image.load(texture_file)
        texture_data = pygame.image.tostring(texture_surface, "RGB", True)
        width, height = texture_surface.get_size()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            width,
            height,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            texture_data,
        )
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return texture_id

    def update(self):
        if self.target_reference and self.target_reference.Position:
            # Compute vector direction

            target_position = self.target_reference.Position

            dx = target_position[0] - self.Position[0]
            dz = target_position[2] - self.Position[2]
            length = math.sqrt(dx * dx + dz * dz)

            if length > 0:
                self.Direction[0] = (dx / length) * self.animation_speed
                self.Direction[2] = (dz / length) * self.animation_speed

            dx = target_position[0] - self.Position[0]
            dz = target_position[2] - self.Position[2]
            distance = math.sqrt(dx * dx + dz * dz)

            # Compute new position
            if distance < self.animation_speed:
                # ya llegamos, ya no te muevas
                self.Position = target_position
                self.is_moving = False
            else:
                # nos movemos
                new_x = self.Position[0] + self.Direction[0]
                new_z = self.Position[2] + self.Direction[2]

                # checar que no se nos vaya
                # if abs(new_x) <= self.DimBoard:
                self.Position[0] = new_x
                # if abs(new_z) <= self.DimBoard:
                self.Position[2] = new_z

        self.draw()

    def draw(self):
        x, z = self.map_coords(self.Position[0], self.Position[2])
        x += self.scale * 2
        z += self.scale * 2

        glPushMatrix()
        glTranslatef(x, self.Position[1], z)
        glScaled(self.scale, self.scale, self.scale)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glEnable(GL_TEXTURE_2D)

        glBegin(GL_QUADS)
        # Cara frontal
        glTexCoord2f(0, 0)
        glVertex3fv(self.points[0])
        glTexCoord2f(1, 0)
        glVertex3fv(self.points[1])
        glTexCoord2f(1, 1)
        glVertex3fv(self.points[5])
        glTexCoord2f(0, 1)
        glVertex3fv(self.points[4])

        # Cara trasera
        glTexCoord2f(0, 0)
        glVertex3fv(self.points[3])
        glTexCoord2f(1, 0)
        glVertex3fv(self.points[2])
        glTexCoord2f(1, 1)
        glVertex3fv(self.points[6])
        glTexCoord2f(0, 1)
        glVertex3fv(self.points[7])

        # Cara izquierda
        glTexCoord2f(0, 0)
        glVertex3fv(self.points[0])
        glTexCoord2f(1, 0)
        glVertex3fv(self.points[4])
        glTexCoord2f(1, 1)
        glVertex3fv(self.points[7])
        glTexCoord2f(0, 1)
        glVertex3fv(self.points[3])

        # Cara derecha
        glTexCoord2f(0, 0)
        glVertex3fv(self.points[1])
        glTexCoord2f(1, 0)
        glVertex3fv(self.points[5])
        glTexCoord2f(1, 1)
        glVertex3fv(self.points[6])
        glTexCoord2f(0, 1)
        glVertex3fv(self.points[2])

        # Cara superior
        glTexCoord2f(0, 0)
        glVertex3fv(self.points[4])
        glTexCoord2f(1, 0)
        glVertex3fv(self.points[5])
        glTexCoord2f(1, 1)
        glVertex3fv(self.points[6])
        glTexCoord2f(0, 1)
        glVertex3fv(self.points[7])

        # Cara inferior
        glTexCoord2f(0, 0)
        glVertex3fv(self.points[0])
        glTexCoord2f(1, 0)
        glVertex3fv(self.points[1])
        glTexCoord2f(1, 1)
        glVertex3fv(self.points[2])
        glTexCoord2f(0, 1)
        glVertex3fv(self.points[3])
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
