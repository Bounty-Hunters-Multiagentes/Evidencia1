from dataclasses import dataclass, field


@dataclass
class Camera:
    FOVY: float = field(default=60.0)
    ZNEAR: float = field(default=0.01)
    ZFAR: float = field(default=900.0)

    EYE_X: float = field(default=0.0)
    EYE_Y: float = field(default=400.0)
    EYE_Z: float = field(default=0.0)
    CENTER_X: float = field(default=0)
    CENTER_Y: float = field(default=0)
    CENTER_Z: float = field(default=0)
    UP_X: float = field(default=0)
    UP_Y: float = field(default=0)
    UP_Z: float = field(default=-1)
