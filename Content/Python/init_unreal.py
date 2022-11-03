import importlib
import subprocess
import pkg_resources
import material_tools
import material_instance_tools
import unreal


# Description: This function is used to reload the script
def reload(scriptname):
    print("Script " + str(scriptname) + " reloaded")
    importlib.reload(scriptname)


# Description: With this function we force to upgrade pip and function to install packages for python3 in unreal.
def pip_install(package):
    query = []
    pythonpath = '"C:\\Program Files/Epic Games/UE_5.0/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"'
    query.append(pythonpath)
    upgradepipquery = query.copy()
    upgradepipquery.append('-m pip install --upgrade pip')
    query.append('-m pip install ' + package)

    querystring = ""
    upgradepipstring = ""
    final_query = []
    pip_query = []

    for i in range(len(upgradepipquery)):
        pip_query.append(upgradepipquery[i])
        upgradepipstring += " " + upgradepipquery[i]

    for i in range(len(query)):
        final_query.append(query[i])
        querystring += " " + query[i]

    # Always upgrade pip to the latest version
    subprocess.run(upgradepipstring, shell=True)
    subprocess.run(querystring, shell=True)


# Description: We can use this function to uninstall pip packages from python3 unreal.
# This function make crash Unreal Engine... Use with precaution. We recommend uninstalling pip packages manually.
# start "C:\Program Files/Epic Games/UE_5.0/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" "-m pip uninstall packageName"
def pip_uninstall(package):
    query = []
    pythonpath = '"C:\\Program Files/Epic Games/UE_5.0/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"'
    query.append(pythonpath)
    query.append('-m pip uninstall ' + package)
    querystring = ""
    final_query = []

    for i in range(len(query)):
        final_query.append(query[i])
        querystring += " " + query[i]
    subprocess.run(querystring, shell=True)


# Capturing installed pip packages
installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
installed_packages_names_list = []
for installedPackage in range(len(installed_packages_list)):
    installed_packages_names_list.append(installed_packages_list[installedPackage].split("=")[0])


# If we haven't installed the necessary pip packages, we force to do so.
pipPackages = ["python-magic-bin"]
for pippackage in pipPackages:
    if pippackage not in installed_packages_names_list:
        pip_install(pippackage)


import script
reload(script)
reload(material_tools)
reload(material_instance_tools)


# Unreal classes
abstractnavdata = unreal.AbstractNavData
actor = unreal.Actor
aicontroller = unreal.AIController
ambientsound = unreal.AmbientSound
animationeditorpreviewactor = unreal.AnimationEditorPreviewActor
animationthumbnailskeletalmeshactor = unreal.AnimationThumbnailSkeletalMeshActor
aractor = unreal.ARActor
archvischaracter = unreal.ArchVisCharacter
aroriginactor = unreal.AROriginActor
arskylight = unreal.ARSkyLight
audiovolume = unreal.AudioVolume
blockingvolume = unreal.BlockingVolume
boxreflectioncapture = unreal.BoxReflectionCapture
# bpskysphere = unreal.BP_Sky_Sphere
cableactor = unreal.CableActor
cameraactor = unreal.CameraActor
camerablockingvolume = unreal.CameraBlockingVolume
camerarigcrane = unreal.CameraRig_Crane
camerarigrail = unreal.CameraRig_Rail
camerashakesourceactor = unreal.CameraShakeSourceActor
character = unreal.Character
cinecameraactor = unreal.CineCameraActor
combinedtransformgizmoactor = unreal.CombinedTransformGizmoActor
controlrigcontrolactor = unreal.ControlRigControlActor
culldistancevolume = unreal.CullDistanceVolume
datasmitharealightactor = unreal.DatasmithAreaLightActor
datasmithlmportedsequencesactor = unreal.DatasmithImportedSequencesActor
datasmithsceneactor = unreal.DatasmithSceneActor
decalactor = unreal.DecalActor
defaultpawn = unreal.DefaultPawn
directionallight = unreal.DirectionalLight
documentationactor = unreal.DocumentationActor
dynamicmeshactor = unreal.DynamicMesh
eqstestingpawn = unreal.EQSTestingPawn
exponentialheightfog = unreal.ExponentialHeightFog
fieldsystemactor = unreal.FieldSystemActor
functionalaitest = unreal.FunctionalAITest
functionaltest = unreal.FunctionalTest
functionaluiscreenshottest = unreal.FunctionalUIScreenshotTest
gizmoactor = unreal.GizmoActor
# geometrycollectiondebugdrawactor = unreal.GeometryCollectionDebugDrawActor
# geometrycollectionrenderlevelsetactor = unreal.GeometryCollectionRenderLevelSetActor
# editgrabbablesmallcube = unreal.Grabbable_SmallCube
hierarchicallodvolume = unreal.HierarchicalLODVolume
instancedplacementpartitionactor = unreal.InstancedPlacementPartitionActor
internaltoolframeworkactor = unreal.InternalToolFrameworkActor
intervalgizmoactor = unreal.IntervalGizmoActor
killzvolume = unreal.KillZVolume
landscapemeshproxyactor = unreal.LandscapeMeshProxyActor
levelbounds = unreal.LevelBounds
levelinstance = unreal.LevelInstance
levelsequenceactor = unreal.LevelSequenceActor
levelsequencemediacontroller = unreal.LevelSequenceMediaController
levelstreamingvolume = unreal.LevelStreamingVolume
levelvariantsetsactor = unreal.LevelVariantSetsActor
lightmasscharacterindirectdetailvolume = unreal.LightmassCharacterIndirectDetailVolume
lightmassimportancevolume = unreal.LightmassImportanceVolume
lightmassportal = unreal.LightmassPortal
lightweightinstancemanager = unreal.LightWeightInstanceManager
lightweightinstancestaticmeshmanager = unreal.LightWeightInstanceStaticMeshManager
manipulator = unreal.Manipulator
materialinstanceactor = unreal.MaterialInstanceActor
matineeactor = unreal.MatineeActor
# menu = unreal.Menu
meshmergecullingvolume = unreal.MeshMergeCullingVolume
navlinkproxy = unreal.NavLinkProxy
navsystemconfigoverride = unreal.NavSystemConfigOverride
navigationtestingactor = unreal.NavigationTestingActor
navmeshboundsvolume = unreal.NavMeshBoundsVolume
navmodifiervolume = unreal.NavModifierVolume
niagaraperfbaselineactor = unreal.NiagaraPerfBaselineActor
niagarapreviewgrid = unreal.NiagaraPreviewGrid
note = unreal.Note
packedlevelactor = unreal.PackedLevelActor
paincausingvolume = unreal.PainCausingVolume
papercharacter = unreal.PaperCharacter
papergroupedspriteactor = unreal.PaperGroupedSpriteActor
papertilemapactor = unreal.PaperTileMapActor
pawn = unreal.Pawn
physicsconstraintactor = unreal.PhysicsConstraintActor
physicsthruster = unreal.PhysicsThruster
physicsvolume = unreal.PhysicsVolume
# pistol = unreal.Pistol
planarreflection = unreal.PlanarReflection
playerstart = unreal.PlayerStart
pointlight = unreal.PointLight
postprocessvolume = unreal.PostProcessVolume
precomputedvisibilityoverridevolume = unreal.PrecomputedVisibilityOverrideVolume
precomputedvisibilityvolume = unreal.PrecomputedVisibilityVolume
recastnavmesh = unreal.RecastNavMesh
# projectile = unreal.Projectile
previewgeometryactor = unreal.PreviewGeometryActor
previewmeshactor = unreal.PreviewMeshActor
propertyeditortestactor = unreal.PropertyEditorTestActor
radialforceactor = unreal.RadialForceActor
rectlight = unreal.RectLight
resonanceaudiodirectivityvisualizer = unreal.ResonanceAudioDirectivityVisualizer
runtimevirtualtexturevolume = unreal.RuntimeVirtualTextureVolume
scenecapture2d = unreal.SceneCapture2D
scenecapturecube = unreal.SceneCaptureCube
screenshotfunctionaltest = unreal.ScreenshotFunctionalTest
sequencerecordergroup = unreal.SequenceRecorderGroup
sequencerkeyactor = unreal.SequencerKeyActor
sequencermeshtrail = unreal.SequencerMeshTrail
serverstatreplicator = unreal.ServerStatReplicator
skyatmosphere = unreal.SkyAtmosphere
skylight = unreal.SkyLight
staticmeshactor = unreal.StaticMeshActor
spherereflectioncapture = unreal.SphereReflectionCapture
splinemeshactor = unreal.SplineMeshActor
spotlight = unreal.SpotLight
switchactor = unreal.SwitchActor
targetpoint = unreal.TargetPoint
templatesequenceactor = unreal.TemplateSequenceActor
textrenderactor = unreal.TextRenderActor
triggerbox = unreal.TriggerBox
triggercapsule = unreal.TriggerCapsule
triggersphere = unreal.TriggerSphere
triggervolume = unreal.TriggerVolume
variantmanagertestactor = unreal.VariantManagerTestActor
visualloggerfiltervolume = unreal.VisualLoggerFilterVolume
volumetriccloud = unreal.VolumetricCloud
volumetriclightmapdensityvolume = unreal.VolumetricLightmapDensityVolume
vreditoravataractor = unreal.VREditorAvatarActor
vreditorbaseactor = unreal.VREditorBaseActor
vreditordockablecamerawindow = unreal.VREditorDockableCameraWindow
vreditordockablewindow = unreal.VREditorDockableWindow
vreditorfloatingcameraui = unreal.VREditorFloatingCameraUI
vreditorfloatingui = unreal.VREditorRadialFloatingUI
vreditorradialfloatingui = unreal.VREditorRadialFloatingUI
vreditorteleporter = unreal.VREditorTeleporter
# vrpawn = unreal.VRPawn
# vrspectator = unreal.VRSpectator
# vrteleportvisualizer = unreal.VRTeleportVisualizer
winddirectionalsource = unreal.WindDirectionalSource
worldpartitionvolume = unreal.WorldPartitionVolume
internaltoolframeworkactor = unreal.InternalToolFrameworkActor
