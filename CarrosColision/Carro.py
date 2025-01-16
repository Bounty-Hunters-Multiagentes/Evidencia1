#Autor: Ivan Olmos Pineda


import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import random
import math

class Car:
    def __init__(self, dim, vel, Scale):
        # Car body points (cube without top)
        self.body_points = np.array([
            # Bottom vertices
            [-1.0, -0.5, 1.0],  [1.0, -0.5, 1.0],   [1.0, -0.5, -1.0],  [-1.0, -0.5, -1.0],
            # Top vertices
            [-1.0, 0.5, 1.0],   [1.0, 0.5, 1.0],    [1.0, 0.5, -1.0],   [-1.0, 0.5, -1.0]
        ])
        
        self.scale = Scale
        self.radio = math.sqrt(self.scale*self.scale + self.scale*self.scale)
        self.DimBoard = dim
        
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
        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[2]*self.Direction[2])
        self.Direction[0] /= m
        self.Direction[2] /= m
        
        # Set velocity
        self.Direction[0] *= vel
        self.Direction[2] *= vel
        
        self.collision = False
        self.Cars = []
        glutInit()


    def getCars(self, NCars):
        self.Cars = NCars

    def update(self):
        self.CollitionDetection()
        if self.collision == False:
            new_x = self.Position[0] + self.Direction[0]
            new_z = self.Position[2] + self.Direction[2]
            
            if(abs(new_x) <= self.DimBoard):
                self.Position[0] = new_x
            else:
                self.Direction[0] *= -1.0
                self.Position[0] += self.Direction[0]
            
            if(abs(new_z) <= self.DimBoard):
                self.Position[2] = new_z
            else:
                self.Direction[2] *= -1.0
                self.Position[2] += self.Direction[2]

    def drawWheels(self):
    # Draw four wheels - raised higher (-0.3 instead of -0.5)
        wheel_positions = [
            [-1.0, -0.3, 0.7],   # Front left
            [1.0, -0.3, 0.7],    # Front right
            [-1.0, -0.3, -0.7],  # Back left
            [1.0, -0.3, -0.7]    # Back right
        ]
        
        glColor3f(0.4, 0.4, 0.4)  # Grey color for wheels
        for wheel_pos in wheel_positions:
            glPushMatrix()
            glTranslatef(wheel_pos[0], wheel_pos[1], wheel_pos[2])
            
            # Draw wheel as a solid sphere
            # Parameters: radius, slices, stacks
            glutSolidSphere(0.3, 20, 20)
            
            glPopMatrix()

    def drawCube(self):
        # Draw bottom face (black)
        glColor3f(0.0, 0.0, 0.0)  # Black
        glBegin(GL_QUADS)
        glVertex3fv(self.body_points[0])
        glVertex3fv(self.body_points[1])
        glVertex3fv(self.body_points[2])
        glVertex3fv(self.body_points[3])
        glEnd()
        
        # Draw back face
        glColor3f(1.0, 1.0, 1.0)  # White
        glBegin(GL_QUADS)
        glVertex3fv(self.body_points[2])
        glVertex3fv(self.body_points[3])
        glVertex3fv(self.body_points[7])
        glVertex3fv(self.body_points[6])
        glEnd()
        
        # Draw left side face
        glBegin(GL_QUADS)
        glVertex3fv(self.body_points[3])
        glVertex3fv(self.body_points[0])
        glVertex3fv(self.body_points[4])
        glVertex3fv(self.body_points[7])
        glEnd()
        
        # Draw right side face
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
        angle = math.atan2(self.Direction[2], self.Direction[0])
        glRotatef(math.degrees(angle), 0, 1, 0)
        
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