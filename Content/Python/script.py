import unreal
import sys
import socket
import importlib

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


def reload(text):
    importlib.reload(text)

def main():

    #showPaths(gamePaths)
    pass
    

main()

