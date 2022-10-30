import unreal
import sys
import os
# import subprocess
import pkg_resources
import socket


EAL = unreal.EditorAssetLibrary
# EUL = unreal.EditorUtilityLibrary
EAS = unreal.EditorActorSubsystem
# ESML = unreal.EditorStaticMeshLibrary
PML = unreal.ProceduralMeshLibrary


world = unreal.World

hostname = socket.gethostname()

ipaddress = socket.gethostbyname(hostname)


# Description: This function is used to print a warning in unreal log
def warning(text):
    return unreal.log_warning(text)


# Description: This function is used to print an error in unreal log
def error(text):
    return unreal.log_error(text)


# Description: This function is used to print in unreal log
def log(text):
    return unreal.log(text)


# Description: This function is used to process all unreal paths
def process_paths():
    unrealpaths = []
    for p in sys.path:
        unrealpaths.append(p)
    return unrealpaths


gamePaths = process_paths()


# Description: This function is used to print any list (mainly paths)
def show(x):
    for path in range(len(x)):
        print(x[path])


# Description: Returns the paths of all assets under project root directory
def process_asset_paths():
    assets = []
    gamepath = '/Game'
    assetpaths = EAL.list_assets(gamepath)

    for assetpath in assetpaths:
        assets.append(assetpath)
    return assets


assetPaths = process_asset_paths()


# Description: Returns a list of all game actors
def get_all_actors():
    actors = []
    allactors = unreal.get_editor_subsystem(EAS).get_all_level_actors()

    for actor in allactors:
        actors.append(actor)
    return actors


allActorsPath = get_all_actors()


# Description: Returns the class of the asset
def get_asset_class(classtype):
    assets = []
    gamepath = '/Game'
    assetpaths = EAL.list_assets(gamepath)

    for assetpath in assetpaths:
        assetdata = EAL.find_asset_data(assetpath)
        assetclass = assetdata.asset_class
        if classtype == assetclass:
            assets.append(assetdata.get_asset())
    return assets


# assetClasses = ["SoundWave", "Material", "MaterialInstanceConstant", "MaterialFunction", "Texture2D", "StaticMesh", "SkeletalMesh", "ObjectRedirector", "PhysicsAsset", "Skeleton", "UserDefinedEnum", "TextureRenderTarget2D", "Blueprint", "SoundCue", "WidgetBlueprint", "HapticFeedbackEffect_Curve", "MapBuildDataRegistry", "NiagaraParameterCollection", "NiagaraSystem"]

soundWaveActors = get_asset_class("SoundWave")
materialActors = get_asset_class("Material")
materialInstanceConstantActors = get_asset_class("MaterialInstanceConstant")
materialFunctionActors = get_asset_class("MaterialFunction")
texture2DActors = get_asset_class("Texture2D")
skeletalMeshActors = get_asset_class("SkeletalMesh")
objectRedirectorActors = get_asset_class("ObjectRedirector")
physicsAssetActors = get_asset_class("PhysicsAsset")
skeletonActors = get_asset_class("Skeleton")
userDefinedEnumActors = get_asset_class("UserDefinedEnum")
textureRenderTarget2DActors = get_asset_class("TextureRenderTarget2D")
blueprintActors = get_asset_class("Blueprint")
soundCueActors = get_asset_class("SoundCue")
widgetBlueprintActors = get_asset_class("WidgetBlueprint")
hapticFeedbackEffect_CurveActors = get_asset_class("HapticFeedbackEffect_Curve")
mapBuildDataRegistryActors = get_asset_class("MapBuildDataRegistry")
niagaraParameterCollectionActors = get_asset_class("NiagaraParameterCollection")
niagaraSystemActors = get_asset_class("NiagaraSystem")
staticMeshActors = get_asset_class("StaticMesh")


# Description: Returns asset import data of the staticMesh actors
def get_staticmesh_data():
    assetsimportdata = []

    for staticMesh in staticMeshActors:
        assetimportdata = staticMesh.get_editor_property("asset_import_data")
        assetsimportdata.append(assetimportdata)
    return assetsimportdata


staticMeshData = get_staticmesh_data()


# Level Of Detail (LOD)
lod_groups = ["LevelArchitecture", "SmallProp", "LargeProp", "Deco", "Vista", "Foliage", "HighDetail"]


# Description: This function is used to print the LOD (Level of Detail) of the staticMesh actors
def check_staticmesh_lod():
    for staticMesh in staticMeshActors:
        assetimportdata = staticMesh.get_editor_property("asset_import_data")

        lodgroupinfo = staticMesh.get_editor_property("lod_group")
        if lodgroupinfo == "None":
            warning("No LOD group (" + str(staticMesh.get_num_lods()) + ") assigned to " + str(staticMesh.get_name()))
            log("PATH:\t" + str(assetimportdata))


# Description: Returns the LOD (Level of Detail) of the staticMesh actors
def get_staticmesh_lod_data():
    for staticMesh in staticMeshActors:
        staticmeshtricount = []
        numlods = staticMesh.get_num_lods()
        staticmeshlod = []
        
        for i in range(numlods):
            lodtricount = 0
            numsections = staticMesh.get_num_sections(i)
            
            for j in range(numsections):
                sectiondata = PML.get_section_from_static_mesh(staticMesh, i, j)
                # print(str(staticMesh.get_name()) + " has " + str(len(sectiondata[0])) + " vertices, " + str(int(len(sectiondata[1])/3)) + " triangles in LOD (" + str(i) + ")" )
                lodtricount += len(sectiondata[1])/3
            staticmeshtricount.append(int(lodtricount))
        staticmeshreductions = [100]
        
        for k in range(1, len(staticmeshtricount)):
            staticmeshreductions.append(int(staticmeshtricount[k] / staticmeshtricount[0] * 100))
        
            # Level of Detail 1
            try:
                loddata = staticMesh.get_name(), staticmeshtricount[1]
            except:
                warning("No LOD assigned to " + str(staticMesh.get_name()) + " using LOD 0")
                loddata = staticMesh.get_name(), staticmeshtricount[0]
            staticmeshlod.append(loddata)
        # print(str(staticMesh.get_name()) + " LOD triangles:\t" + str(staticmeshtricount) + " with " + str(staticmeshreductions) + "% reductions")

        return staticmeshlod


lodsdata = get_staticmesh_lod_data()


# Description: Returns the number of repetitions of staticMesh actors
def get_staticmesh_instance_counts():
    staticmeshinstanceactors = []
    staticmeshactorcounts = []
    
    for levelActor in allActorsPath:
        if levelActor.get_class().get_name() == "StaticMeshActor":
            staticmeshcomponent = levelActor.static_mesh_component
            staticmesh = staticmeshcomponent.static_mesh
            staticmeshinstanceactors.append(staticmesh.get_name())
    processedactors = []
    for staticmeshactor in staticmeshinstanceactors:
        if staticmeshactor not in processedactors:
            actorcounts = staticmeshactor, staticmeshinstanceactors.count(staticmeshactor)
            staticmeshactorcounts.append(actorcounts)
            processedactors.append(staticmeshactor)
    
    staticmeshactorcounts.sort(key=lambda a: a[1], reverse=True)
    
    aggregatetricounts = []
    
    for i in range(len(staticmeshactorcounts)):
        for j in range(len(lodsdata)):
            if staticmeshactorcounts[i][0] == lodsdata[j][0]:
                aggregatetricount = staticmeshactorcounts[i][0], staticmeshactorcounts[i][0] * lodsdata[j][1]
                aggregatetricounts.append(aggregatetricount)
                
    aggregatetricounts.sort(key=lambda a: a[1], reverse=True)
    return aggregatetricounts


staticMeshInstanceCounts = get_staticmesh_instance_counts()


# Description: This function is used to print the materials and textures associated to the staticMesh actors
def check_material_information_smc():
    for levelActor in allActorsPath:
        if levelActor.get_class().get_name() == "StaticMeshActor":
            staticmeshcomponent = levelActor.static_mesh_component
            print("Actor:\t" + levelActor.get_name())
            materials = staticmeshcomponent.get_materials()
            for material in materials:
                print(material.get_name())
                try:
                    for item in material.texture_parameter_values:
                        print(item)
                except:
                    pass
                print("_____")


# Description: This function is used to print the materials and textures associated to the staticMesh actors
def get_all_properties(unrealclass=None):
    return unreal.get_all_properties(unrealclass)


# Description: Returns a list with all staticMesh components
def show_staticmesh_components():
    staticmeshcomponents = []
    for component in dir(unreal.StaticMeshComponent):
        staticmeshcomponents.append(component)
    return staticmeshcomponents


allComponentsStaticMesh = show_staticmesh_components()


# Description: Returns a list with all fbx
def process_fbx_paths():
    fbxfilepaths = []

    for staticMesh in staticMeshActors:
        assetimportdata = staticMesh.get_editor_property("asset_import_data")
        if assetimportdata.extract_filenames():
            fbxfilepaths.append(assetimportdata.extract_filenames())
    return fbxfilepaths


fbxPaths = process_fbx_paths()


# Description: Is used to cast objects into a certain class
# object_to_cast: obj unreal.Object : The object you want to cast
# object_class: obj unreal.Class : The class you want to cast the object into
def cast(objecttocast=None, objectclass=None):
    try:
        return objectclass.cast(objecttocast)
    except:
        return None


# Description: With this function we generate a string to upgrade pip package manager of python3 unreal.

def pip_upgrade(package):
    pythonPath = "\"C:\\Program Files/Epic Games/UE_5.0/Engine/Binaries/ThirdParty/Python3/Win64/python.exe\""
    comm = "start " + pythonPath + " \"-m pip install "
    print("Run:\t" + comm + "--upgrade pip\" to upgrade pip")
    print("Run:\t" + comm + "nameofpackage\" to install package")
    # query = comm + package + "\""
    # subprocess.run(query, shell=True)


# Description: We use this function to install pip packages into python3 unreal.
def pip_install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])


# Capturing installed pip packages
installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
installed_packages_names_list = []
for installedPackage in range(len(installed_packages_list)):
    installed_packages_names_list.append(installed_packages_list[installedPackage].split("=")[0])


# If we haven't installed necessary pip packages, we do so.
pipPackages = ["python-magic-bin"]
for pippackage in pipPackages:
    if pippackage not in installed_packages_names_list:
        pip_install(pippackage)


# For mimetypes we use python-magic-bin
import magic
mime = magic.Magic(mime=True)


def build_import_task(filename, destination_path, destination_name):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', False)
    task.set_editor_property('destination_name', destination_name)
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', filename)
    task.set_editor_property('replace_existing', False)
    task.set_editor_property('save', False)
    return task


def execute_import_tasks(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    #for task in tasks:
        #for path in task.get_editor_property("imported_object_paths"):
            #print("Imported:\t" + str(path))


# def auto_import_assets():
currentGameImportsDir = unreal.Paths.game_source_dir().replace("../../../../../../", "C:\\\\").replace("Source", "Content/Imports")
fontsPath = unreal.Paths.game_source_dir().replace("../../../../../../", "C:\\\\").replace("Source", "Content/Fonts")
soundPath = unreal.Paths.game_source_dir().replace("../../../../../../", "C:\\\\").replace("Source", "Content/Sound")
texturesPath = unreal.Paths.game_source_dir().replace("../../../../../../", "C:\\\\").replace("Source", "Content/Textures")
videosPath = unreal.Paths.game_source_dir().replace("../../../../../../", "C:\\\\").replace("Source", "Content/Videos")
wordsPath = unreal.Paths.game_source_dir().replace("../../../../../../", "C:\\\\").replace("Source", "Content/Words")


def import_assets():
    myTasks = []
    for file in os.listdir(currentGameImportsDir):
        filePath = (currentGameImportsDir + file).replace("\\\\", "/")
        mimefile = mime.from_file(filePath)
        mimetype = mimefile.split("/")[0]

        if mimetype == "audio":
            myTasks.append(build_import_task(filePath, soundPath, file))
        elif mimetype == "font":
            myTasks.append(build_import_task(filePath, fontsPath, file))
        elif mimetype == "image":
            myTasks.append(build_import_task(filePath, texturesPath, file))
        elif mimetype == "text":
            myTasks.append(build_import_task(filePath, wordsPath, file))
        elif mimetype == "video":
            myTasks.append(build_import_task(filePath, videosPath, file))
        else:
            pass
    execute_import_tasks(myTasks)


def main():
    # showPaths(gamePaths)
    pass


main()
