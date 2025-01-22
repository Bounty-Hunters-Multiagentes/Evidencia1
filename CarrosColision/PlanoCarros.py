#Autor: Ivan Olmos Pineda
#Curso: Multiagentes - Graficas Computacionales


import math
import agentpy as ap
import numpy as np
# Visualization
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import IPython
from IPython.display import display, HTML

import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Se carga el archivo de la clase Car
import sys
sys.path.append('..')
from Carro import Car
from Basura import Basura

import numpy as np
import math
import random

from nbconvert import PythonExporter
import nbformat
import sys
from pathlib import Path


screen_width = 500
screen_height = 500
#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=300.0
EYE_Y=200.0
EYE_Z=300.0
CENTER_X=0
CENTER_Y=0
CENTER_Z=0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500
#Dimension del plano
DimBoard = 200

pygame.init()

cars = []
ncars = 5

basuras = []
nbasuras = 5


rounds = None
initial_position = None


def execute_notebook_code(notebook_path):
    """
    Import and execute code from a Jupyter notebook while handling imports and context properly.
    
    Args:
        notebook_path (str): Path to the .ipynb file
    """
    # Convert path to absolute path
    notebook_path = Path(notebook_path).resolve()
    
    # Add notebook's directory to Python path to handle relative imports
    notebook_dir = str(notebook_path.parent)
    if notebook_dir not in sys.path:
        sys.path.append(notebook_dir)
    
    # Read and convert notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = nbformat.read(f, as_version=4)
    
    # Convert to Python code
    exporter = PythonExporter()
    python_code, _ = exporter.from_notebook_node(notebook_content)
    
    # Create a new module namespace
    module_name = notebook_path.stem
    module = type(sys)(module_name)
    module.__file__ = str(notebook_path)
    
    # Execute in the module namespace
    exec(python_code, module.__dict__)
    
    # Add module to sys.modules
    sys.modules[module_name] = module
    
    return module

def simulate_game():
    global initial_position
    global rounds
    # Import the notebook as a module
    simulation_module = execute_notebook_code('../agentpy/mainSimulation.ipynb')
    
    # Now you can access classes and functions defined in the notebook
    BoxWarehouseModel = simulation_module.BoxWarehouseModel
    
    parameters = {
        'steps': 100,
        'n': 20,
        'm': 20,
        'total_boxes': 50,
    }
    
    model = BoxWarehouseModel(parameters)
    results = model.run()
    rounds = model.rounds
    
    # for round in rounds:
    #     print("New Test Round")
    #     for move in round:
    #         print(move)
    initial_position = model.initial_position
    # print(model.initial_position)

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis en rojo
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis en verde
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis en azul
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)


def load_texture(image_path):
    texture_surface = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
    width, height = texture_surface.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    #Seteamos los parametros de la textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Seteamos esto para que la textura se aplique con el color original
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

    # Upload the texture to OpenGL
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

    return texture_id

def init_basura_objects(initial_position):
    """Inicializa los objetos basura en posiciones aleatorias"""
    rows, columns = initial_position.board_dimensions
    scale_factor_x = 400 / columns  # Scale factor for x-axis (columns)
    scale_factor_y = 400 / rows     # Scale factor for y-axis (rows)
    
    for box in initial_position.box_positions:
        print(box)
        scaled_x = (box[1] - columns / 2) * scale_factor_x
        scaled_z = (box[0] - rows / 2) * scale_factor_y
        position = [scaled_x, 2.0, scaled_z] # Y = 2.0 para que esté ligeramente elevado sobre el plano
        
        try:
            basura = Basura(position, "../Assets/rubik.png")
            basuras.append(basura)
        except Exception as e:
            print(f"Error al crear objeto basura: {e}")
        

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()

    # Permitimos el uso de texturas
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ground_texture)

    # Dibujamos el plano gris
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3d(-DimBoard, 0, -DimBoard)
    glTexCoord2f(1, 0); glVertex3d(DimBoard, 0, -DimBoard)
    glTexCoord2f(1, 1); glVertex3d(DimBoard, 0, DimBoard)
    glTexCoord2f(0, 1); glVertex3d(-DimBoard, 0, DimBoard)
    glEnd()

    glDisable(GL_TEXTURE_2D)

    if are_movements_done(cars):
        # Si ya no hay movimientos, obtenemos el siguiente movimiento de la simulación
        pass
    # Dibujamos carros y los actualizamos
    for car in cars:
        car.draw()
        car.update()
    
    # Dibujamos objetos basura
    for basura in basuras:
        basura.draw()

def initialize_cars(DimBoard, ncars):
    """
    Initialize the cars and place them based on the initial positions of agents.

    Args:
        DimBoard: The OpenGL board dimension (e.g., 200x200).
        ncars: Number of cars to initialize.

    Returns:
        List of initialized Car objects.
    """
    # Extract board dimensions and scale factor
    rows, columns = initial_position.board_dimensions
    scale_factor_x = 400 / columns  # Scale factor for x-axis (columns)
    scale_factor_y = 400 / rows     # Scale factor for y-axis (rows)

    cars = []

    for i in range(ncars):
        car = Car(DimBoard, 1.0, 5.0)  # Initialize car
        if i < len(initial_position.agents):
            agent_id, initial_pos = initial_position.agents[i]

            # Center the agent grid around (0, 0) of the OpenGL board
            # Map the agent position from grid [0,0] to [columns-1, rows-1]
            # to the OpenGL range [-400/2, 400/2]

            # Compute scaled x and z positions for OpenGL coordinates
            scaled_x = (initial_pos[1] - columns / 2) * scale_factor_x
            scaled_z = (initial_pos[0] - rows / 2) * scale_factor_y

            # Update car position
            car.Position = [scaled_x, car.scale, scaled_z]

        cars.append(car)

    # Link cars for collision detection
    for car in cars:
        car.getCars(cars)
        car.getBoxes(basuras)
        
    return cars


def are_movements_done(cars):
    for car in cars:
        if car.is_moving:
            return False
    return True

#Cargamos textura
def Init():
    global ground_texture
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Cars")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Cargamos textura
    try:
        ground_texture = load_texture("../Assets/asphalt-texture.png")
    except pygame.error as e:
        print(f"Failed to load texture: {e}")
        pygame.quit()
        sys.exit()
    
    # Inicializamos objetos basura
    
    simulate_game()

    global cars 
    global initial_position
    
    init_basura_objects(initial_position)
    # Iniciamos carros
    cars = initialize_cars(DimBoard, ncars)
    print("these are the cars")
    
    for car in cars:
        print (car.Position)
    # print(cars)
    """
    for i in range(ncars):
        cars.append(Car(DimBoard, 1.0, 5.0))
    for car in cars:
        car.getCars(cars)
    """
    """
    -200 A 200 EN X y Y
    """
    
done = False
Init()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    display()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()