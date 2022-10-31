import importlib
import subprocess
import pkg_resources
import material_tools
import material_instance_tools


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
<<<<<<< HEAD
reload(script)
reload(material_tools)
reload(material_instance_tools)
=======
import importlib


# Description: This function is used to reload the script
def reload(scriptname):
    print("Script " + str(scriptname) + " reloaded")
    importlib.reload(scriptname)


reload(script)
>>>>>>> 87fb193d282e5200d26af3b38278a14c60dc8ea8
