import platform
import os

def plat():
    return platform.system()

def process_pythonversion(platf):
    if platf == "Linux":
        # If customizer installation exists
        if os.path.isdir('~/.customizer/bin/chatGPT'):
            return "~/.customizer/bin/chatGPT/bin/python3"
        else:
            return "python3"

    elif platf == "Windows":
        return "python"

    elif platf == "Darwin":
        return "python3"

    return process_pythonversion(plat())


def main():
    return process_pythonversion(plat())


if __name__ == '__main__':
    main()