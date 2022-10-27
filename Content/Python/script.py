import unreal
import sys
import socket
import importlib

classes = ["SoundWave", "Material", "MaterialInstanceConstant", "MaterialFunction", "Texture2D", "StaticMesh", "SkeletalMesh", "ObjectRedirector", "PhysicsAsset", "Skeleton", "UserDefinedEnum", "TextureRenderTarget2D", "Blueprint", "SoundCue", "WidgetBlueprint", "HapticFeedbackEffect_Curve", "MapBuildDataRegistry", "NiagaraParameterCollection", "NiagaraSystem"]


EAL = unreal.EditorAssetLibrary
# EUL = unreal.EditorUtilityLibrary
EAS = unreal.EditorActorSubsystem

world = unreal.World

hostname = socket.gethostname()

IPaddress = socket.gethostbyname(hostname)


# Description: This function is used to print a warning in unreal log.
def warning(text):
    return unreal.log_warning(text)


# Description: This function is used to print an error in unreal log.
def error(text):
    return unreal.log_error(text)


# Description: This function is used to print in unreal log.
def log(text):
    return unreal.log(text)


def processPaths():
    unrealPaths = []
    for p in sys.path:
        unrealPaths.append(p)
    return unrealPaths


def showPaths(gPaths):
    for path in range(len(gPaths)):
        print(gPaths[path])

gamePaths = processPaths()


def reload(scriptName):
    print("Script " + str(scriptName) + " reloaded")
    importlib.reload(scriptName)


# Print paths of all assets under project root directory
def processAssetPaths():
    assets = []
    gamePath = '/Game'
    assetPaths = EAL.list_assets(gamePath)

    for assetPath in assetPaths:
        assets.append(assetPath)
    return assets

assetPaths = processAssetPaths()

def getAllActors():
    actors = []
    allActors = unreal.get_editor_subsystem(EAS).get_all_level_actors()

    for actor in allActors:
        actors.append(actor)
    return actors

allActorsPath = getAllActors()


def getAssetClass(classType):
    assets = []
    gamePath = '/Game'
    assetPaths = EAL.list_assets(gamePath)

    for assetPath in assetPaths:
        assetData = EAL.find_asset_data(assetPath)
        assetClass = assetData.asset_class
        if classType == assetClass:
            assets.append(assetData.get_asset())
    return assets

soundWaveActors = getAssetClass(classes[0])

def main():
    #showPaths(gamePaths)
    pass
    

main()
