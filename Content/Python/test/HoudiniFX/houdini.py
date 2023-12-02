import sys
sys.path.append("C:/Program Files/Side Effects Software/Houdini 19.5.435/houdini/python3.9libs")
sys.path.append("C:/Program Files/Side Effects Software/Houdini 19.5.435/python39/lib")
sys.path.append("C:/Users/1vrv/AppData/Roaming/Python/Python39/site-packages")
sys.path.append("C:/Program Files/Side Effects Software/Houdini 19.5.435/python39/lib/site-packages")
import os
from os import environ
from os.path import join
import pip
import subprocess


def enableHouModule():
    '''Set up the environment so that "import hou" works.'''
    try:
        import hou
    except ImportError:
        # Add $HFS/houdini/python2.6libs to sys.path so Python can find the
        # hou module.
        lib_path = join(environ['HFS'], "python", "lib", "python%d.%d" % (sys.version_info[:2]))
        hou_path = join(environ['HFS'], "houdini", "python%d.%dlibs" % (sys.version_info[:2]))
        paths = [lib_path, hou_path]
        for path in paths:
            if not path in sys.path:
                sys.path.append(path)
enableHouModule()


'''# Install pip in Houdini
def install_pip():
    os.popen('python get-pip.py').read()


# Install individual package with pip in Houdini
def install_pip_package(pippackagename):
    pip._internal.main(['install', pippackagename])


# Install list of packages with pip in Houdini
def install_pip_packages(pippackagenames):
    for pippackage in pippackagenames:
        install_pip_package(pippackage)

'''

def pip_install(package):
    query = []
    pythonpath = '"C:\\Program Files\\Side Effects Software\\Houdini 19.5.435\\bin\\hython"'
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
    print(querystring)
    subprocess.run(querystring, shell=True)


# Get Houdini environment variable
def get_scene_name():
    return hou.expandString("$HIPNAME")


# TODO: RF Scene file operations
def scene_file_operations():
    sceneRoot = hou.node('/obj')

    # Save current scene as file
    hou.hipFile.save('C:/temp/myScene_001.hipnc')

    # Export selected node to a file
    sceneRoot.saveChildrenToFile(hou.selectedNodes(), [], 'C:/temp/nodes.hipnc')

    # Import file to the scene
    sceneRoot.loadChildrenFromFile('C:/temp/nodes.hipnc')


# TODO: test Get node code
def get_node_as_code(nodepath, nodename):
    nodefullpath = nodepath + "/" + nodename
    input("get nde")
    node = hou.node(nodefullpath)
    input("XD")
    return node.asCode()


def get_node(nodepath, nodename):
    nodefullpath = nodepath + "/" + nodename
    return hou.node(nodefullpath)


# Get node from the scene
def get_node_content(nodepath, nodename):
    nodefullpath = nodepath + "/" + nodename
    node = hou.node(nodefullpath)
    node = hou.selectedNodes()[0]
    return node.children()


# Get node upstream connections
def get_node_upstream_connections(node):
    return node.inputAncestors()


# TODO: RF Create node in the scene
def create_node_in_scene():
    # Get scene root node
    OBJ = hou.node('/obj/')
    # Create Geometry node in scene root
    geometry = OBJ.createNode('geo')
    # Create transform node inside geo1
    geometry = hou.node('/obj/geo1')
    xform = geometry.createNode('xform')
    xform.moveToGoodPosition()  # Align new node

    # Create new transform node linked to existing transform
    xformNew = xform.createOutputNode('xform')


# Delete node
def delete_node(node):
    node.destroy()


# Delete parameter expression (chennal, animation)
def delete_parameter_expression(node, parameterName):
    node.parm(parameterName).deleteAllKeyframes()


# Copy node to another location
def copy_node_to_another_location(node, parentpath):
    parent = hou.node(parentpath)
    hou.copyNodesTo(node, parent)

# TODO: RF Get parameters
def get_parameters():
    node = hou.selectedNodes()[0]

    # get translate X
    node.parm('tx').eval()
    hou.parm('/obj/geo1/tx').eval()
    hou.ch('/obj/geo1/tx')

    # Get string parameter without token evaluation
    node = hou.node('/obj/geometry/fileCache')
    print()
    node.parm('file').eval()
    print()
    node.parm('file').rawValue()
    # >> C:/temp/myFile.1.bgeo.sc
    # >> $HIP/myFile.$F.bgeo.sc


# TODO: RF Set parameters
def set_parameters():
    node = hou.selectedNodes()[0]

    # set translate XYZ
    node.parmTuple('t').set([0, 1, 0])
    hou.parm('/obj/geo1/tx').set(2)

    # Set parameters for selected Remesh SOP
    remesh = hou.selectedNodes()[0]
    remesh.setParms({'group': 'myGroup', 'element_sizing1': 1, 'iterations': 2})


# Get Translate X keyframes of selected node
def get_translate_x_keyframes():
    node = hou.selectedNodes()[0]
    node.parm('tx').keyframes()


# Run hscript command form Python
def run_hscript():
    hou.hscript('Redshift_openIPR')


# Return list of all parameters names for input node object
def get_all_node_parameters_names(node):
    allParameters = [param.name() for param in node.parms()]
    return allParameters


# TODO: RF Connect nodes
def connect_nodes(node):
    # Create transform nodes
    xform_A = hou.node('/obj/geo1/transform1')
    xform_B = hou.node('/obj/geo1/transform2')
    # Connect transform_A to transform_B
    xform_B.setInput(0, xform_A)

    # Create merge
    merge = node.createNode('merge')
    # Connect xforms to a merge
    merge.setNextInput(xform_A)
    merge.setNextInput(xform_B)

    # Get node inputs
    merge.inputs()
    # Get node outputs
    merge.outputs()


# Get groups
def get_groups():
    node = hou.selectedNodes()[0]
    groups = [g.name() for g in node.geometry().primGroups()]
    print(groups)


# Create "Material Surface Builder" in SHOP context, dive inside.
def create_material_surface_builder():
    shader = hou.node('/shop/vopmaterial1/lambert1')
    out = hou.node('/shop/vopmaterial1/surface_output')
    out.setNamedInput('Cf', shader, 'clr')  # Set connection by name
    out.setNamedInput(0, shader, 0)  # Set connection by parameter index

    # List all inputs for node 'surface_output'
    print(out.inputNames())


def extractVop(listOfChildrens):
    for node in listOfChildrens:
        if node.type().name() == 'vopsurface':
            return node


# Filter node.children() output
def filter_node_children_output():
    selectedNode = hou.selectedNodes()
    return extractVop(selectedNode.children())


def list_comprehensions():
    selectedNode = hou.selectedNodes()
    return [node for node in selectedNode.children() if node.type().name() == 'vopsurface']

def main():
    # TODO: import hou module
    nodepath = '/obj/geo1'
    nodename = 'mynode'
    nodefullpath = nodepath + '/' + nodename

    # If we haven't installed the necessary pip packages, we force to do so.
    pipPackages = ["python-setuptools", "python-dotdenv"]
    for pippackage in pipPackages:
        pip_install(pippackage)

    from dotenv import load_dotenv
    load_dotenv()

    # Capturing installed pip packages
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
    installed_packages_names_list = []
    for installedPackage in range(len(installed_packages_list)):
        installed_packages_names_list.append(installed_packages_list[installedPackage].split("=")[0])

    #install_pip_package("python3-dotenv")

    get_node_as_code(nodepath, nodename)
    input("hola")



if __name__ == '__main__':
    main()