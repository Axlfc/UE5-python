import script
import importlib


# Description: This function is used to reload the script
def reload(scriptname):
    print("Script " + str(scriptname) + " reloaded")
    importlib.reload(scriptname)


reload(script)
