from enum import Enum, auto

class KnowledgeType(Enum):
    BEAST = 1
    CULTURE = 2
    PLANE = 3
    PLANEWING = 4
    PLANEFUEL = 5
    LIGHTHOUSE = 6
    QUEST_ARARIEL = 7
    ISLAND_SINK = 8

class Knowledge(Enum):
    KnowsOfBeast = (KnowledgeType.BEAST,1)
    SeenBeast = (KnowledgeType.BEAST,2)
    FoughtBeast = (KnowledgeType.BEAST,3)
    DefeatedBeast = (KnowledgeType.BEAST,4)
    
    VisitedVillage = (KnowledgeType.CULTURE,1)
    LearnedLanguage = (KnowledgeType.CULTURE,2)
    LearnedVillageName = (KnowledgeType.CULTURE,3)
    LearnedVillageHistory = (KnowledgeType.CULTURE,4)
    VillagersAcceptYou = (KnowledgeType.CULTURE,5) #Preregs max QUEST_ARARIEL & LIGHTHOUSE
    
    ExaminedPlane = (KnowledgeType.PLANE,1)
    FixedPlane = (KnowledgeType.PLANE,2) #Prereqs max PLANEWING & PLANEFUEL

    CollectedWingMaterial = (KnowledgeType.PLANEWING,1)
    AttachedWing = (KnowledgeType.PLANEWING,2)

    LearnedPlaneFuelMaterial = (KnowledgeType.PLANEFUEL,1)
    CollectedFuelMaterial = (KnowledgeType.PLANEFUEL,2)
    AddedFuelToPlane = (KnowledgeType.PLANEFUEL,3)

    VisitedLighthouse = (KnowledgeType.LIGHTHOUSE,1)
    LearnedLighthouseHistory = (KnowledgeType.LIGHTHOUSE,2)
    FixedLighthouse = (KnowledgeType.LIGHTHOUSE,3)

    LearnedOfTearOfArariel = (KnowledgeType.QUEST_ARARIEL,1)
    LocatedTearOfArariel = (KnowledgeType.QUEST_ARARIEL,2)
    CollectedTearOfArariel = (KnowledgeType.QUEST_ARARIEL,3)
    ReturnedTearOfArariel = (KnowledgeType.QUEST_ARARIEL,4)

    KnowsOfIslandRumbling = (KnowledgeType.ISLAND_SINK,1)
    IslandRumbledOnce = (KnowledgeType.ISLAND_SINK,2)
    IslandRumbledTwice = (KnowledgeType.ISLAND_SINK,3)
    IslandRumbledThrice = (KnowledgeType.ISLAND_SINK,4)
    IslandSinking = (KnowledgeType.ISLAND_SINK,5)

class GameTime(Enum):    
    MIDNIGHT = 0
    DAWN = 1
    MORNING = 2
    NOON = 3
    EVENING = 4
    DUSK = 5

class Rooms(Enum):
    PLANECRASH = 'RoomPlaneCrash("Plane Crash")'
    VILLAGE = 'RoomVillage("Village")'
    CROSSROADS = 'RoomCrossroads("Crossroads")'
    LIGHTHOUSE = 'RoomLighthouse("Lighthouse")'
    BEACH = 'RoomBeach("Beach")'
    CAVEENTRANCE = 'RoomCaveEntrance("Cave Entrance")'
    CAVEEXIT = 'RoomCaveExit("Cave Exit")'    
    CLIFFS = 'RoomCliffs("Cliffs")'
    FOREST = 'RoomForest("Forest")'
    VILLAGEINSIDE = 'RoomVillageInside("Inside the village")'
    CASTLEINSIDE = 'RoomCastleInside("Inside the castle in village")'
    LABORATORYINSIDE = 'RoomLaboratoryInside("Inside the village; right house")'
    CAVEINSIDE = 'RoomCaveInside("Inside the cave")'
    CAVE1 = 'RoomCave1Inside("Upper Cave")'
    ARARIELJEWEL = 'RoomArarielDialogue("Arariel jewel dialog")'
    EAGLEDIALOG = 'RoomEagleDialogue("Lighthouse eagle dialog")'

class Actions(Enum):
    BluePotion = auto()
    RedPotion = auto()
    YellowPotion = auto()
    ChasedBirds = auto()
    MetEagle = auto()
