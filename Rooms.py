from enum import Enum
from Room import *

class Rooms(Enum):
    PLANECRASH = RoomPlaneCrash("Plane crash")
    VILLAGE = RoomVillage("Village")
    CROSSROADS = RoomCrossroads("Crossroads")
    LIGHTHOUSE = RoomLighthouse("Lighthouse")
    BEACH = RoomBeach("Beach")
    CAVEENTRANCE = RoomCaveEntrance("Cave Entrance")
    CAVE = RoomCave("Cave")
    CAVEEXIT = RoomCaveExit("Cave Exit")
    CLIFFS = RoomCliffs("Cliffs")
    FOREST = RoomForest("Forest")
