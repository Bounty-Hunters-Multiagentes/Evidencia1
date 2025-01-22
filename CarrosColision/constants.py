from objects import Camera

# Variables para dibujar los ejes del sistema

X_MIN = -500
X_MAX = 500
Y_MIN = -500
Y_MAX = 500
Z_MIN = -500
Z_MAX = 500

ANGLE_STEP = 5

# Ventana de pygame
screen_width = 500
screen_height = 500

# Dimension del plano
DimBoard = 200
COLUMNS = 20
ROWS = 20

# File paths
NB_PATH = "../agentpy/mainSimulation.ipynb"
RUBRIK_ASSET = "../Assets/rubik.png"
ASPHALT_ASSET = "../Assets/asphalt-texture.png"


def toggle_camera_view(camera: Camera):
    if camera.UP_Y == 1:
        # Top view config
        camera.UP_Y = 0
        camera.UP_Z = -1
        camera.EYE_X = 0
        camera.EYE_Y = 400
        camera.EYE_Z = 0
    else:
        # Front view config
        camera.UP_Y = 1
        camera.UP_Z = 0
        camera.EYE_X = 200
        camera.EYE_Y = 200
        camera.EYE_Z = 300
