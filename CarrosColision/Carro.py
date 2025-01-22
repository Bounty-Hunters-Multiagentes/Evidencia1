# Autor: Bounty Hunters


import math
import random

import numpy as np

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *


class Car:
    def __init__(self, dim, vel, Scale, id):
        # Car body points (cube without top)
        self.body_points = np.array(
            [
                # Bottom vertices
                [-1.0, -0.5, 1.0],
                [1.0, -0.5, 1.0],
                [1.0, -0.5, -1.0],
                [-1.0, -0.5, -1.0],
                # Top vertices
                [-1.0, 0.5, 1.0],
                [1.0, 0.5, 1.0],
                [1.0, 0.5, -1.0],
                [-1.0, 0.5, -1.0],
            ]
        )

        self.scale = Scale  # + 2
        self.radio = math.sqrt(self.scale * self.scale + self.scale * self.scale)
        self.DimBoard = dim
        self.id = id

        # Initialize random position
        self.Position = []
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        self.Position.append(self.scale)
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))

        # Initialize random direction
        self.Direction = []
        self.Direction.append(random.random())
        self.Direction.append(self.scale)
        self.Direction.append(random.random())

        # Normalize direction vector
        m = math.sqrt(
            self.Direction[0] * self.Direction[0]
            + self.Direction[2] * self.Direction[2]
        )
        self.Direction[0] /= m
        self.Direction[2] /= m

        # Set velocity
        self.Direction[0] *= vel
        self.Direction[2] *= vel

        self.collision = False
        self.Cars = []
        self.Boxes = []
        glutInit()

        # Animation properties
        self.target_position = None
        self.target_rotation = None
        self.current_rotation = 0.0
        self.is_moving = False
        self.animation_speed = 1.0  # unidades por frame
        self.rotation_speed = 10.0  # grados por frame

    def getCars(self, NCars):
        self.Cars = NCars

    def getBoxes(self, NBoxes):
        self.Boxes = NBoxes

    def move(self, target_x, target_z):
        self.target_position = [
            target_x,  # * self.scale,
            self.Position[1],
            target_z,  # * self.scale,
        ]
        self.is_moving = True

        dx = self.target_position[0] - self.Position[0]
        dz = self.target_position[2] - self.Position[2]
        length = math.sqrt(dx * dx + dz * dz)
        if length > 0:
            self.Direction[0] = (dx / length) * self.animation_speed
            self.Direction[2] = (dz / length) * self.animation_speed

    def rotatedir(self, direction):
        rotation_map = {
            "up": 0.0,
            "right": 90.0,
            "down": 180.0,
            "left": 270.0,
        }

        if direction in rotation_map:
            self.target_rotation = rotation_map[direction]

    def update_new(self):
        if self.target_rotation is not None:
            diff = (self.target_rotation - self.current_rotation + 180) % 360 - 180
            if abs(diff) < self.rotation_speed:
                self.current_rotation = self.target_rotation
                self.target_rotation = None
            else:
                self.current_rotation += math.copysign(self.rotation_speed, diff)
                self.current_rotation %= 360

        if self.target_position and self.is_moving:
            dx = self.target_position[0] - self.Position[0]
            dz = self.target_position[2] - self.Position[2]
            distance = math.sqrt(dx * dx + dz * dz)

            if distance < self.animation_speed:
                # ya llegamos, ya no te muevas
                self.Position = self.target_position
                self.is_moving = False
                self.target_position = None
            else:
                # nos movemos
                new_x = self.Position[0] + self.Direction[0]
                new_z = self.Position[2] + self.Direction[2]

                # checar que no se nos vaya
                # if abs(new_x) <= self.DimBoard:
                self.Position[0] = new_x
                # if abs(new_z) <= self.DimBoard:
                self.Position[2] = new_z

    def update(self):
        self.CollitionDetection()
        if self.collision == False:
            new_x = self.Position[0] + self.Direction[0]
            new_z = self.Position[2] + self.Direction[2]

            if abs(new_x) <= self.DimBoard:
                self.Position[0] = new_x
            else:
                self.Direction[0] *= -1.0
                self.Position[0] += self.Direction[0]

            if abs(new_z) <= self.DimBoard:
                self.Position[2] = new_z
            else:
                self.Direction[2] *= -1.0
                self.Position[2] += self.Direction[2]

    def drawWheels(self):
        wheel_positions = [
            [-1.0, -0.3, 0.7],  # Front left
            [1.0, -0.3, 0.7],  # Front right
            [-1.0, -0.3, -0.7],  # Back left
            [1.0, -0.3, -0.7],  # Back right
        ]

        glColor3f(0.4, 0.4, 0.4)  # Color gris
        for wheel_pos in wheel_positions:
            glPushMatrix()
            glTranslatef(wheel_pos[0], wheel_pos[1], wheel_pos[2])

            # Parameters: radius, slices, stacks
            glutSolidSphere(0.3, 20, 20)

            glPopMatrix()

    def drawCube(self):
        # bottom face (black)
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3fv(self.body_points[0])
        glVertex3fv(self.body_points[1])
        glVertex3fv(self.body_points[2])
        glVertex3fv(self.body_points[3])
        glEnd()

        # Front face
        glColor3f(0.8, 0.6, 0.8)  # Morado
        glBegin(GL_QUADS)
        glVertex3fv(self.body_points[2])
        glVertex3fv(self.body_points[3])
        glVertex3fv(self.body_points[7])
        glVertex3fv(self.body_points[6])
        glEnd()

        # left side face
        glBegin(GL_QUADS)
        glVertex3fv(self.body_points[3])
        glVertex3fv(self.body_points[0])
        glVertex3fv(self.body_points[4])
        glVertex3fv(self.body_points[7])
        glEnd()

        # right side face
        glBegin(GL_QUADS)
        glVertex3fv(self.body_points[1])
        glVertex3fv(self.body_points[2])
        glVertex3fv(self.body_points[6])
        glVertex3fv(self.body_points[5])
        glEnd()

    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(self.scale, self.scale, self.scale)

        # Calculate rotation angle based on direction

        # TASK - Cuando se implemente el agente, reemplazar lo posterior con:
        glRotatef(self.current_rotation, 0, 1, 0)
        # angle = math.atan2(self.Direction[2], self.Direction[0])
        # glRotatef(math.degrees(angle), 0, 1, 0)

        self.drawCube()
        self.drawWheels()

        glPopMatrix()

    def CollitionDetection(self):
        for obj in self.Cars:
            if self != obj:
                d_x = self.Position[0] - obj.Position[0]
                d_z = self.Position[2] - obj.Position[2]
                d_c = math.sqrt(d_x * d_x + d_z * d_z)
                if d_c - (self.radio + obj.radio) < 0.0:
                    self.Direction[0] *= -1.0
                    self.Direction[2] *= -1.0

        for obj in self.Boxes:
            if self != obj:
                d_x = self.Position[0] - obj.Position[0]
                d_z = self.Position[2] - obj.Position[2]
                d_c = math.sqrt(d_x * d_x + d_z * d_z)
                if d_c - (self.radio + 5) < 0.0:
                    self.Direction[0] *= -1.0
                    self.Direction[2] *= -1.0
