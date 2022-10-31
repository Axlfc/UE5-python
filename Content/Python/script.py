import unreal
import sys
import os
import socket
import magic

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


# assetClasses = ["SoundWave", "Material", "MaterialInstanceConstant", "MaterialFunction", "Texture2D", "StaticMesh",
# "SkeletalMesh", "ObjectRedirector", "PhysicsAsset", "Skeleton", "UserDefinedEnum", "TextureRenderTarget2D",
# "Blueprint", "SoundCue", "WidgetBlueprint", "HapticFeedbackEffect_Curve", "MapBuildDataRegistry",
# "NiagaraParameterCollection", "NiagaraSystem"]

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
                # print(str(staticMesh.get_name()) + " has " + str(len(sectiondata[0])) + " vertices, ",
                # str(int(len(sectiondata[1])/3)) + " triangles in LOD (" + str(i) + ")" )
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
        # print(str(staticMesh.get_name()) + " LOD triangles:\t" + str(staticmeshtricount),
        # " with " + str(staticmeshreductions) + "% reductions")

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


# For mimetypes we use python-magic-bin

mime = magic.Magic(mime=True)


def build_import_task(filename, destination_path, destination_name, options=None):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', False)
    task.set_editor_property('destination_name', destination_name)
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', filename)
    task.set_editor_property('replace_existing', False)
    task.set_editor_property('save', False)
    task.set_editor_property('options', options)
    return task


def build_staticmesh_import_options():
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_textures", False)
    options.set_editor_property("import_materials", True)
    options.set_editor_property("import_as_skeletal", False)  # StaticMesh
    options.static_mesh_import_data.set_editor_property("import_translation", unreal.Vector(0.0, 0.0, 0.0))
    options.static_mesh_import_data.set_editor_property("import_rotation", unreal.Rotator(0.0, 0.0, 0.0))
    options.static_mesh_import_data.set_editor_property("import_uniform_scale", 1.0)
    options.static_mesh_import_data.set_editor_property("combine_meshes", True)
    options.static_mesh_import_data.set_editor_property("generate_lightmap_u_vs", True)
    options.static_mesh_import_data.set_editor_property("auto_generate_collision", True)
    return options


def build_skeletalmesh_import_options():
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_textures", True)
    options.set_editor_property("import_materials", True)
    options.set_editor_property("import_as_skeletal", True)  # SkeletalMesh
    options.skeletal_mesh_import_data.set_editor_property("import_translation", unreal.Vector(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property("import_rotation", unreal.Rotator(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property("import_uniform_scale", 1.0)
    options.skeletal_mesh_import_data.set_editor_property("import_morph_targets", True)
    options.skeletal_mesh_import_data.set_editor_property("update_skeleton_reference_pose", False)
    return options


def build_animation_import_options(skeletonpath):
    options = unreal.FbxImportUI()
    options.set_editor_property("import_animations", True)
    options.skeleton = unreal.load_asset(skeletonpath)
    options.anim_sequence_import_data.set_editor_property("import_translation", unreal.Vector(0.0, 0.0, 0.0))
    options.anim_sequence_import_data.set_editor_property("import_rotation", unreal.Rotator(0.0, 0.0, 0.0))
    options.anim_sequence_import_data.set_editor_property("import_uniform_scale", 1.0)
    options.anim_sequence_import_data.set_editor_property("animation_length",
                                                          unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    options.anim_sequence_import_data.set_editor_property("remove_redundant_keys", False)
    return options


def execute_import_tasks(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    for task in tasks:
        for path in task.get_editor_property("imported_object_paths"):
            print("Imported:\t" + str(path))


currentGameImportsDir = unreal.Paths.game_source_dir().replace("../../../../../../",
                                                               "C:\\\\").replace("Source", "Content/Imports")
fontsPath = unreal.Paths.game_source_dir().replace("../../../../../../",
                                                   "C:\\\\").replace("Source", "Content/Fonts")
soundPath = unreal.Paths.game_source_dir().replace("../../../../../../",
                                                   "C:\\\\").replace("Source", "Content/Sound")
texturesPath = unreal.Paths.game_source_dir().replace("../../../../../../",
                                                      "C:\\\\").replace("Source", "Content/Textures")
videosPath = unreal.Paths.game_source_dir().replace("../../../../../../",
                                                    "C:\\\\").replace("Source", "Content/Videos")
wordsPath = unreal.Paths.game_source_dir().replace("../../../../../../",
                                                   "C:\\\\").replace("Source", "Content/Words")
skeletalmeshPath = unreal.Paths.game_source_dir().replace("../../../../../../",
                                                          "C:\\\\").replace("Source", "Content/SkeletalMeshes")
staticmeshPath = unreal.Paths.game_source_dir().replace("../../../../../../",
                                                        "C:\\\\").replace("Source", "Content/StaticMeshes")
animationsPath = unreal.Paths.game_source_dir().replace("../../../../../../",
                                                        "C:\\\\").replace("Source", "Content/Animations")


def import_animation(skeleton):
    mytask = []
    for file in os.listdir(currentGameImportsDir):
        fileextension = file.split(".")[1]
        filepath = (currentGameImportsDir + file).replace("\\\\", "/")
        if fileextension == "fbx":
            prefix = file.split("_")[0]
            if prefix == "AN":
                # Input a path to a skeleton to import the animation
                mytask.append(build_import_task(filepath, soundPath, file, build_animation_import_options(skeleton)))

    execute_import_tasks(mytask)


def import_assets():
    mytasks = []
    for file in os.listdir(currentGameImportsDir):
        fileextension = file.split(".")[1]
        filepath = (currentGameImportsDir + file).replace("\\\\", "/")
        mimefile = mime.from_file(filepath)
        mimetype = mimefile.split("/")[0]
        prefix = file.split("_")[0]
        # We assume files are correctly named as SK_ or SM_ (SkeletalMesh or StaticMesh) inside Imports
        if fileextension == "fbx":
            if prefix == "SK":
                mytasks.append(build_import_task(filepath, soundPath, file, build_skeletalmesh_import_options()))
            elif prefix == "SM":
                mytasks.append(build_import_task(filepath, soundPath, file, build_staticmesh_import_options()))
        else:
            if mimetype == "audio":
                mytasks.append(build_import_task(filepath, soundPath, file))
            elif mimetype == "font":
                mytasks.append(build_import_task(filepath, fontsPath, file))
            elif mimetype == "image":
                mytasks.append(build_import_task(filepath, texturesPath, file))
            elif mimetype == "text":
                mytasks.append(build_import_task(filepath, wordsPath, file))
            elif mimetype == "video":
                mytasks.append(build_import_task(filepath, videosPath, file))

    execute_import_tasks(mytasks)


# unreal.Package
def get_package_from_path(packagepath):
    return unreal.load_asset(packagepath)


def get_all_dirty_packages():
    packages = unreal.Array(unreal.Package)
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
        packages.append(x)
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages():
        packages.append(x)
    return packages


def save_all_dirty_packages(showdialog=False):
    if showdialog:
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(save_map_packages=True,
                                                                           save_content_packages=True)
    else:
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(save_map_packages=True, save_content_packages=True)


def save_packages(packages=[], showdialog=False):
    if showdialog:
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(packages, only_dirty=False)  # May not work.
    else:
        unreal.EditorLoadingAndSavingUtils.save_packages(packages, only_dirty=False)


def save_asset(assetpath):
    EAL.save_asset(assetpath, only_if_is_dirty=False)


def save_directory(directorypath):
    EAL.save_directory(directorypath, only_if_is_dirty=False, recursive=True)


def create_directory(directorypath):
    EAL.make_directory(directorypath)


def duplicate_directory(directorypath, duplicateddirectorypath):
    return EAL.duplicate_directory(directorypath, duplicateddirectorypath)


def delete_directory(directorypath):
    EAL.delete_directory(directorypath)


def directory_exists(directorypath):
    return EAL.does_directory_exist(directorypath)


def rename_directory(directorypath, renameddirectorypath):
    EAL.rename_directory(directorypath, renameddirectorypath)


def duplicate_asset(assetpath, duplicatedassetpath):
    return EAL.duplicate_asset(assetpath, duplicatedassetpath)


def delete_asset(assetpath):
    EAL.delete_asset(assetpath)


def asset_exists(assetpath):
    return EAL.does_asset_exist(assetpath)


def rename_asset(assetpath, renamedassetpath):
    EAL.rename_asset(assetpath, renamedassetpath)


def main():
    # showPaths(gamePaths)
    pass


main()
