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
    FixedSword = (KnowledgeType.BEAST,3)
    FoughtBeast = (KnowledgeType.BEAST,4)
    DefeatedBeast = (KnowledgeType.BEAST,5)

    LearnedLanguage = (KnowledgeType.LANGUAGE,1)
    
    VisitedVillage = (KnowledgeType.CULTURE,1)    
    LearnedVillageName = (KnowledgeType.CULTURE,2)
    LearnedVillageHistory = (KnowledgeType.CULTURE,3)
    VillagersAcceptYou = (KnowledgeType.CULTURE,4) #Preregs max QUEST_ARARIEL & LIGHTHOUSE
    
    ExaminedPlane = (KnowledgeType.PLANE,1)
    FixedPlane = (KnowledgeType.PLANE,2) #Prereqs max PLANEWING & PLANEFUEL & PLANEHOSE

    FoundWheelMaterial = (KnowledgeType.PLANEWHEEL,1)
    CollectedWheelMaterial = (KnowledgeType.PLANEWHEEL,2)
    AttachedWheel = (KnowledgeType.PLANEWHEEL,3)
    
    FoundFuelMaterial = (KnowledgeType.PLANEFUEL,1)
    CollectedFuelMaterial = (KnowledgeType.PLANEFUEL,2)
    AddedFuelToPlane = (KnowledgeType.PLANEFUEL,3)

    FoundFuelHose = (KnowledgeType.PLANEHOSE,1)
    CollectedFuelHose = (KnowledgeType.PLANEHOSE,2)
    AttachedFuelHose = (KnowledgeType.PLANEHOSE,3)

    VisitedLighthouse = (KnowledgeType.LIGHTHOUSE,1)
    LearnedLighthouseHistory = (KnowledgeType.LIGHTHOUSE,2)
    FixedLighthouse = (KnowledgeType.LIGHTHOUSE,3)

    LearnedOfTearOfArariel = (KnowledgeType.QUEST_ARARIEL,1)
    LocatedTearOfArariel = (KnowledgeType.QUEST_ARARIEL,2)
    CollectedTearOfArariel = (KnowledgeType.QUEST_ARARIEL,3)
    ReturnedTearOfArariel = (KnowledgeType.QUEST_ARARIEL,4)

class GameTime(Enum):    
    MIDNIGHT = 60
    DAWN = 90
    MORNING = 150
    NOON = 210
    EVENING = 270
    DUSK = 300

class Rooms(Enum):
    MAINMENU = 'MainMenu("Main menu")'
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
    FORESTINSIDE = 'RoomForestInside("Forest")'
    BEASTDIALOG = 'RoomBeastDialogue("Beast fight")'

class Actions(Enum):
    BluePotion = auto()
    RedPotion = auto()
    YellowPotion = auto()
    ChasedBirds = auto()
    MetEagle = auto()
    EagleQuest = auto() 
    SwordBought = auto()
    AskedHoseFromShopkeeper = auto()
    StoleHoseFromShopkeeper = auto()
    StoleSwordFromShopkeeper = auto()
    TradedAxeToShopkeeper = auto()
    StoleAxeFromShopkeeper = auto()
    TradedTearToShopkeeper = auto()
    StoleTearFromShopkeeper = auto()
    GaveTearToKing = auto()
    ClimbedDownCliff = auto()
    FoundFuel = auto()

class Items(Enum):
    Tear = auto()
    Axe = auto()
    Sword = auto()
    SwordOfArariel = auto()
    Fuel = auto()
    Wheels = auto()
    Hose = auto()
    Wood = auto()
    Lightbead = auto()
    
class GameEnd(Enum):
    LOSE = 0
    WIN = 1
    QUIT = 2
