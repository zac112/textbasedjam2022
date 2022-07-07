from enum import Enum, auto

class KnowledgeType(Enum):
    BEAST = auto()
    CULTURE = auto()
    PLANE = auto()
    PLANEWHEEL = auto()
    PLANEFUEL = auto()
    PLANEHOSE = auto()
    LIGHTHOUSE = auto()
    QUEST_ARARIEL = auto()
    ISLAND_SINK = auto()
    LANGUAGE = auto()

class Knowledge(Enum):
    KnowsOfBeast = (KnowledgeType.BEAST,1)
    SeenBeast = (KnowledgeType.BEAST,2)
    FoughtBeast = (KnowledgeType.BEAST,3) #Requires sword
    DefeatedBeast = (KnowledgeType.BEAST,4)

    LearnedLanguage = (KnowledgeType.LANGUAGE,1)
    
    VisitedVillage = (KnowledgeType.CULTURE,1)    
    LearnedVillageName = (KnowledgeType.CULTURE,2)
    LearnedVillageHistory = (KnowledgeType.CULTURE,3) #Prereqs KnowsofBeast
    VillagersAcceptYou = (KnowledgeType.CULTURE,4) #Preregs max QUEST_ARARIEL & LIGHTHOUSE
    
    ExaminedPlane = (KnowledgeType.PLANE,1)
    FixedPlane = (KnowledgeType.PLANE,2) #Prereqs max PLANEWING & PLANEFUEL & PLANEHOSE

    CollectedWheelMaterial = (KnowledgeType.PLANEWHEEL,1)
    AttachedWheel = (KnowledgeType.PLANEWHEEL,2)
    
    CollectedFuelMaterial = (KnowledgeType.PLANEFUEL,1)
    AddedFuelToPlane = (KnowledgeType.PLANEFUEL,2)

    FoundFuelHose = (KnowledgeType.PLANEHOSE,1)
    AttachedFuelHose = (KnowledgeType.PLANEHOSE,2)

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
    SHOPKEEPERDIALOG = 'RoomShopkeeperDialogue("Town shopkeeper; left house")'
    #shopkeeper; steal hose for plane

class Actions(Enum):
    BluePotion = auto()
    RedPotion = auto()
    YellowPotion = auto()
    ChasedBirds = auto()
    MetEagle = auto()
    EagleQuest = auto() #axe
    SwordBought = auto() #lose axe, gain sword
