# Autor: Bounty Hunters
# Curso: Multiagentes - Graficas Computacionales


# Se carga el archivo de la clase Car
import sys

import pygame

# Visualization
from IPython.display import display
from objects import Camera

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *

sys.path.append("..")
import contextlib
import io
import sys
from pathlib import Path

import nbformat
from Basura import Basura
from Carro import Car
from constants import (
    ANIMATION_SAVE_PATH,
    ASPHALT_ASSET,
    BASE_Y,
    COLUMNS,
    DISCARGE_Y,
    NB_PATH,
    ROWS,
    RUBRIK_ASSET,
    X_MAX,
    X_MIN,
    Y_MAX,
    Y_MIN,
    Z_MAX,
    Z_MIN,
    DimBoard,
    screen_height,
    screen_width,
    toggle_camera_view,
)
from nbconvert import PythonExporter


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
    with open(notebook_path, "r", encoding="utf-8") as f:
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
    # Import the notebook as a module
    simulation_module = execute_notebook_code(NB_PATH)

    # Now you can access classes and functions defined in the notebook
    BoxWarehouseModel = simulation_module.BoxWarehouseModel
    show_animation_func = simulation_module.show_animation

    parameters = {
        "steps": 100,
        "n": COLUMNS,
        "m": ROWS,
        "total_boxes": 50,
        "discharge_side": 4,
        "sergio_agents": 0,
        "rodrigo_agents": 5,
        "pepe_agents": 0,
        "oscar_agents": 0,
        "hector_agents": 0,
        "random_agents": 0,
        "seed": 22,
    }

    model = BoxWarehouseModel(parameters)
    model.run()
    # for round in rounds:
    #     print("New Test Round")
    #     for move in round:
    #         print(move)
    # print(model.initial_position)

    # ignore the stdout of these lines (output errors are expected)
    f = io.StringIO()
    with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
        animation = show_animation_func(parameters)
        animation_html = animation.to_jshtml()

    with open(ANIMATION_SAVE_PATH, "w") as f:
        f.write(animation_html)

    return model


def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    # X axis en rojo
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN, 0.0, 0.0)
    glVertex3f(X_MAX, 0.0, 0.0)
    glEnd()
    # Y axis en verde
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, Y_MIN, 0.0)
    glVertex3f(0.0, Y_MAX, 0.0)
    glEnd()
    # Z axis en azul
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, Z_MIN)
    glVertex3f(0.0, 0.0, Z_MAX)
    glEnd()
    glLineWidth(1.0)


def load_texture(image_path):
    texture_surface = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
    width, height = texture_surface.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Seteamos los parametros de la textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Seteamos esto para que la textura se aplique con el color original
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

    # Upload the texture to OpenGL
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

    return texture_id


def map_coords(x, z):
    # Center the agent grid around (0, 0) of the OpenGL board
    # Map the agent position from grid [0,0] to [columns-1, rows-1]
    # to the OpenGL range [-400/2, 400/2]
    board_size = DimBoard * 2
    scale_factor_x = board_size / COLUMNS  # Scale factor for x-axis (columns)
    scale_factor_z = board_size / ROWS  # Scale factor for y-axis (rows)

    scaled_x = (x - COLUMNS / 2) * scale_factor_x
    scaled_z = (z - ROWS / 2) * scale_factor_z

    return scaled_x, scaled_z


def initialize_basuras(initial_position):
    """Inicializa los objetos basura en posiciones aleatorias"""
    basuras = []

    for box in initial_position.box_positions:
        position = [
            box[1],
            BASE_Y,
            box[0],
        ]

        try:
            basura = Basura(position, RUBRIK_ASSET, map_coords)
            basuras.append(basura)
            Basura.place_box(basura, box[0], box[1])
        except Exception as e:
            print(f"Error al crear objeto basura: {e}")

    return basuras


def pick_decision(robot_position, direction):
    # print("pd:", direction)
    # print("robot_position:", robot_position)
    if direction == "up":
        robot_position[0] -= 1
        return robot_position
    elif direction == "down":
        robot_position[0] += 1
        return robot_position
    elif direction == "left":
        robot_position[1] -= 1
        return robot_position
    elif direction == "right":
        robot_position[1] += 1
        return robot_position


def initialize_cars(DimBoard, initial_position):
    """
    Initialize the cars and place them based on the initial positions of agents.

    Args:
        DimBoard: The OpenGL board dimension (e.g., 200x200).
        initial_position: the state of the initial positions in the simulation.

    Returns:
        List of initialized Car objects.
    """
    # Extract board dimensions and scale factor
    cars = []

    for i in range(len(initial_position.agents)):
        agent_id, initial_pos = initial_position.agents[i]

        car = Car(
            DimBoard, 1.0, 5.0, id=agent_id, map_coords=map_coords
        )  # Initialize car

        # Update car position
        car.set_position([initial_pos[1], car.scale, initial_pos[0]])
        car.rotatedir("up")

        cars.append(car)

    # Link cars for collision detection
    for car in cars:
        car.getCars(cars)
        car.getBoxes(basuras)

    return cars


def initialize_discharge_cells(initial_position):
    discharge_cells = initial_position.discharge_positions
    cell_size_x = (DimBoard * 2) / COLUMNS
    cell_size_z = (DimBoard * 2) / ROWS

    discharge_data = []
    for x, z in discharge_cells:
        scaled_x, scaled_z = map_coords(x, z)
        discharge_data.append(
            {
                "x": scaled_x + cell_size_x / 2,
                "z": scaled_z + cell_size_z / 2,
                "size_x": cell_size_x,
                "size_z": cell_size_z,
                "color": (0.0, 1.0, 0.0, 0.3),  # verdesin y un poco transparente
            }
        )

    return discharge_data


def draw_discharge_cells(discharge_cells_data):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    for cell in discharge_cells_data:
        glColor4f(*cell["color"])
        glBegin(GL_QUADS)
        glVertex3f(
            cell["x"] - cell["size_x"] / 2, DISCARGE_Y, cell["z"] - cell["size_z"] / 2
        )
        glVertex3f(
            cell["x"] + cell["size_x"] / 2, DISCARGE_Y, cell["z"] - cell["size_z"] / 2
        )
        glVertex3f(
            cell["x"] + cell["size_x"] / 2, DISCARGE_Y, cell["z"] + cell["size_z"] / 2
        )
        glVertex3f(
            cell["x"] - cell["size_x"] / 2, DISCARGE_Y, cell["z"] + cell["size_z"] / 2
        )
        glEnd()

    glDisable(GL_BLEND)


def update_movements(round_index, cars, memo):
    """Actualiza los movimientos de los carros en cada ronda de la simulación"""

    if are_movements_done(cars) and round_index not in memo:
        memo[round_index] = True
        if round_index < len(rounds):
            round = rounds[round_index]
            for move in round:
                for car in cars:
                    if car.id == move.agent_id:
                        if move.action == "pick_up":
                            pick_cell = pick_decision(
                                [move.cell[0], move.cell[1]], move.looking_direction
                            )

                            pick_cell = [int(c) for c in pick_cell]
                            Basura.pick_box(car, pick_cell[0], pick_cell[1])

                            # print(f"Agent {car.id} picked up box at {pick_cell}")
                        if move.action == "stack":
                            place_cell = pick_decision(
                                [move.cell[0], move.cell[1]], move.looking_direction
                            )
                            Basura.place_box(car.basura, place_cell[0], place_cell[1])
                            car.basura = None

                        car.move(move.cell[1], move.cell[0])
                        car.rotatedir(move.looking_direction)
                        break
            round_index += 1

        else:
            pass
            # print("SIMULATION FINISHED")

    return round_index


def display(round_index, cars, basuras, ground_texture, discharge_cells_data, memo):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()

    # Permitimos el uso de texturas
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ground_texture)

    # Dibujamos el plano gris
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glTexCoord2f(1, 0)
    glVertex3d(DimBoard, 0, -DimBoard)
    glTexCoord2f(1, 1)
    glVertex3d(DimBoard, 0, DimBoard)
    glTexCoord2f(0, 1)
    glVertex3d(-DimBoard, 0, DimBoard)
    glEnd()

    glDisable(GL_TEXTURE_2D)

    # Dibujamos carros y los actualizamos
    for car in cars:
        car.draw()
        # car.update()
        car.update_new()

    # Dibujamos objetos basura
    # basuras[0].target_reference = cars[0]
    for basura in basuras:
        basura.update()

    # Dibujamos discharge cells
    draw_discharge_cells(discharge_cells_data)

    return update_movements(round_index, cars, memo)


def are_movements_done(cars):
    for car in cars:
        if car.is_moving:
            return False
    return True


def load_camera(camera: Camera):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(camera.FOVY, screen_width / screen_height, camera.ZNEAR, camera.ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        camera.EYE_X,
        camera.EYE_Y,
        camera.EYE_Z,
        camera.CENTER_X,
        camera.CENTER_Y,
        camera.CENTER_Z,
        camera.UP_X,
        camera.UP_Y,
        camera.UP_Z,
    )


# Cargamos textura
def Init(camera):
    print("Running agentpy simulation...")
    model = simulate_game()

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Cars")

    load_camera(camera)

    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Cargamos textura
    try:
        ground_texture = load_texture(ASPHALT_ASSET)
    except pygame.error as e:
        print(f"Failed to load texture: {e}")
        pygame.quit()
        sys.exit()

    initial_position = model.initial_position
    rounds = model.rounds

    # Iniciamos carros
    cars = initialize_cars(DimBoard, initial_position)

    # Iniciamos basuras
    basuras = initialize_basuras(initial_position)

    # Iniciamos celdas de descarga
    discharge_cells_data = initialize_discharge_cells(initial_position)

    # for car in cars:
    #     print(car.Position)

    return cars, basuras, rounds, ground_texture, screen, discharge_cells_data


def debug(cars, boxes):
    print("********** DEBUG **********")
    print("********** car Positions **********")
    for car in cars:
        print(car.Position)

    print("********** Box Positions **********")

    for box in boxes:
        print(box.Position)

    print("********** Box Positions (Basura) **********")

    print(Basura.boxes_positions)
    for key, value in Basura.boxes_positions.items():
        for box in value:
            print(box.target_reference.Position)

    print("\n\n")


if __name__ == "__main__":
    MANUAL_IT = True
    done = False
    round_index = 0
    cars = []
    basuras = []
    camera = Camera()
    memo = {}
    cars, basuras, rounds, ground_texture, screen, discharge_cells_data = Init(camera)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                # Toggle top view and perspective view
                if event.key == pygame.K_t:
                    toggle_camera_view(camera)
                    load_camera(camera)
                if event.key == pygame.K_RIGHT and are_movements_done(cars):
                    round_index += 1
                if event.key == pygame.K_LEFT and are_movements_done(cars):
                    round_index -= 1
                if event.key == pygame.K_d:
                    debug(cars, basuras)

        round_index = min(max(round_index, 0), len(rounds) - 1)

        if MANUAL_IT:
            display(
                round_index, cars, basuras, ground_texture, discharge_cells_data, memo
            )
        else:
            round_index = display(
                round_index, cars, basuras, ground_texture, discharge_cells_data, memo
            )

        pygame.display.set_caption(f"OpenGL: Cars (t = {round_index+1}/{len(rounds)})")

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()
