from enum import Enum

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