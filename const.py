from enum import Enum

class Status(Enum):
    OPEN = 'Open'
    CLOSED = 'Closed'
    ON = 'On'
    OFF = 'Off'

class Mode(Enum):
    ARM = 0
    HOME = 1
    DISARM = 2

class Device(Enum):
    TYPE_WINDOW_SENSOR = 'Fensterkontakt'
    TYPE_DOOR_SENSOR = 'Türkontakt'
    TYPE_KEY_PAD = 'Keypad'
    TYPE_MOTION_DETECTOR = 'Bewegungsmelder'
    TYPE_SMOKE_DETECOR = 'Rauchmelder'
    TYPE_WATER_DETECTOR = 'Wassermelder'
    TYPE_POWER_SWITCH = 'Steckdose'
    TYPE_SIRENE = 'Sirene'

SWITCH_TYPES = [Device.TYPE_POWER_SWITCH]
BINARY_SENSOR_TYPES = [Device.TYPE_DOOR_SENSOR, Device.TYPE_WINDOW_SENSOR]
TYPE_SENSOR = [Device.TYPE_SMOKE_DETECOR, Device.TYPE_WATER_DETECTOR, Device.TYPE_MOTION_DETECTOR]
