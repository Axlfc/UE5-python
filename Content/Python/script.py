import unreal
import sys
import socket
import importlib


EAL = unreal.EditorAssetLibrary
# EUL = unreal.EditorUtilityLibrary
EAS = unreal.EditorActorSubsystem
#ESML = unreal.EditorStaticMeshLibrary
PML = unreal.ProceduralMeshLibrary


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
    

def reload(scriptName):
    print("Script " + str(scriptName) + " reloaded")
    importlib.reload(scriptName)


def processPaths():
    unrealPaths = []
    for p in sys.path:
        unrealPaths.append(p)
    return unrealPaths


def show(x):
    for path in range(len(x)):
        print(x[path])

gamePaths = processPaths()


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


# assetClasses = ["SoundWave", "Material", "MaterialInstanceConstant", "MaterialFunction", "Texture2D", "StaticMesh", "SkeletalMesh", "ObjectRedirector", "PhysicsAsset", "Skeleton", "UserDefinedEnum", "TextureRenderTarget2D", "Blueprint", "SoundCue", "WidgetBlueprint", "HapticFeedbackEffect_Curve", "MapBuildDataRegistry", "NiagaraParameterCollection", "NiagaraSystem"]

soundWaveActors = getAssetClass("SoundWave")
materialActors = getAssetClass("Material")
materialInstanceConstantActors = getAssetClass("MaterialInstanceConstant")
materialFunctionActors = getAssetClass("MaterialFunction")
texture2DActors = getAssetClass("Texture2D")
skeletalMeshActors = getAssetClass("SkeletalMesh")
objectRedirectorActors = getAssetClass("ObjectRedirector")
physicsAssetActors = getAssetClass("PhysicsAsset")
skeletonActors = getAssetClass("Skeleton")
userDefinedEnumActors = getAssetClass("UserDefinedEnum")
textureRenderTarget2DActors = getAssetClass("TextureRenderTarget2D")
blueprintActors = getAssetClass("Blueprint")
soundCueActors = getAssetClass("SoundCue")
widgetBlueprintActors = getAssetClass("WidgetBlueprint")
hapticFeedbackEffect_CurveActors = getAssetClass("HapticFeedbackEffect_Curve")
mapBuildDataRegistryActors = getAssetClass("MapBuildDataRegistry")
niagaraParameterCollectionActors = getAssetClass("NiagaraParameterCollection")
niagaraSystemActors = getAssetClass("NiagaraSystem")
staticMeshActors = getAssetClass("StaticMesh")


def getStaticMeshData():
    assetsImportData = []

    for staticMesh in staticMeshActors:
        assetImportData = staticMesh.get_editor_property("asset_import_data")
        assetsImportData.append(assetImportData)
    return assetsImportData

staticMeshData = getStaticMeshData()


# Level Of Detail (LOD)
lod_groups = ["LevelArchitecture", "SmallProp", "LargeProp", "Deco", "Vista", "Foliage", "HighDetail"]
def checkStaticMeshLod():
    for staticMesh in staticMeshActors:
        assetImportData = staticMesh.get_editor_property("asset_import_data")

        lodGroupInfo = staticMesh.get_editor_property("lod_group")
        if lodGroupInfo == "None":
            warning("No LOD group (" + str(staticMesh.get_num_lods()) + ") assigned to " + str(staticMesh.get_name()))
            log("PATH:\t" + str(assetImportData))


def getStaticMeshLodData():
    for staticMesh in staticMeshActors:
        staticMeshTriCount = []
        numLods = staticMesh.get_num_lods()
        staticMeshLod = []
        
        for i in range(numLods):
            LodTriCount = 0
            numSections = staticMesh.get_num_sections(i)
            
            for j in range(numSections):
                sectionData = PML.get_section_from_static_mesh(staticMesh, i, j)
                #print(str(staticMesh.get_name()) + " has " + str(len(sectionData[0])) + " vertices, " + str(int(len(sectionData[1])/3)) + " triangles in LOD (" + str(i) + ")" )
                LodTriCount += len(sectionData[1])/3
            staticMeshTriCount.append(int(LodTriCount))
        staticMeshReductions = [100]
        
        for k in range(1, len(staticMeshTriCount)):
            staticMeshReductions.append(int(staticMeshTriCount[i] / staticMeshTriCount[0] * 100))
        
        # Level of Detail 1
        try:
            LodData = staticMesh.get_name(), staticMeshTriCount[1]
        except:
            warning("No LOD assigned to " + str(staticMesh.get_name()) + " using LOD 0")
            LodData = staticMesh.get_name(), staticMeshTriCount[0]
        staticMeshLod.append(LodData)
        # print(str(staticMesh.get_name()) + " LOD triangles:\t" + str(staticMeshTriCount) + " with " + str(staticMeshReductions) + "% reductions")

    return staticMeshLod

lodData = getStaticMeshLodData()


def getStaticMeshInstanceCounts():
    staticMeshInstanceActors = []
    staticMeshActorCounts = []
    
    for levelActor in allActorsPath:
        if levelActor.get_class().get_name() == "StaticMeshActor":
            staticMeshComponent = levelActor.static_mesh_component
            staticMesh = staticMeshComponent.static_mesh
            staticMeshInstanceActors.append(staticMesh.get_name())
    processedActors = []
    for staticMeshActor in staticMeshInstanceActors:
        if staticMeshActor not in processedActors:
            actorCounts = staticMeshActor, staticMeshInstanceActors.count(staticMeshActor)
            staticMeshActorCounts.append(actorCounts)
            processedActors.append(staticMeshActor)
    
    staticMeshActorCounts.sort(key = lambda a: a[1], reverse = True)
    
    aggregateTriCounts = []
    
    for i in range(len(staticMeshActorCounts)):
        for j in range(len(lodData)):
            if staticMeshActorCounts[i][0] == lodData[j][0]:
                aggregateTriCount = staticMeshActorCounts[i][0], staticMeshActorCounts[i][0] * lodData[j][1]
                aggregateTriCounts.append(aggregateTriCount)
                
    aggregateTriCounts.sort(key = lambda a: a[1], reverse = True)
    return aggregateTriCounts

staticMeshInstanceCounts = getStaticMeshInstanceCounts()


def checkMaterialInformationSMC():
    for levelActor in allActorsPath:
        if levelActor.get_class().get_name() == "StaticMeshActor":
            staticMeshComponent = levelActor.static_mesh_component
            print("Actor:\t" + levelActor.get_name())
            materials = staticMeshComponent.get_materials()
            for material in materials:
                print(material.get_name())
                try:
                    for item in material.texture_parameter_values:
                        print(item)
                except:
                    pass
                print("_____")



def showStaticMeshComponents():
    staticMeshComponents = []
    for item in dir(unreal.StaticMeshComponent):
        staticMeshComponents.append(item)
    return staticMeshComponents

allComponentsStaticMesh = showStaticMeshComponents()


def processFbxPaths():
    fbxFilePaths = []

    for staticMesh in staticMeshActors:
        assetImportData = staticMesh.get_editor_property("asset_import_data")
        if assetImportData.extract_filenames():
            fbxFilePaths.append(assetImportData.extract_filenames())
    return fbxFilePaths

fbxPaths = processFbxPaths()


def main():
    #showPaths(gamePaths)
    pass
    

main()

