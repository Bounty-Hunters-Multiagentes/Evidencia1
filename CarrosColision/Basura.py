import numpy as np
import pygame

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *


# Clase para el cubo Basura
class Basura:
    def __init__(self, position, texture_file):
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
        self.Position = position  # Posición fija en el plano
        self.texture = self.load_texture(texture_file)

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

    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5, 5, 5)
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
