import platform
import os
from re import sub
import subprocess
import os.path
from tabnanny import check

# Sets global variable to determine whether path seperators are \ or /
if platform.system() == "Windows":
    PATH_SEPERATOR = "\\"
else:
    PATH_SEPERATOR = '/'
    

INSTALL_DIR = "..{}gameservers{}".format(PATH_SEPERATOR, PATH_SEPERATOR)

def check_steamcmd() -> int:
    command = "steamcmd"
    
    process = subprocess.run(args = f"{command} +quit" , capture_output=True, check=True, shell=True)
    if process.stderr[0:len(command)] == f"{command}:" or process.stderr[0:len(command)+1] == f"'{command}'":
        print("Error: steamcmd not installed")
        return 1
    
    
    return 0

def install_server(steam_appname: str, steam_appid: int) -> int:
    os.system()
    
    return 0

check_steamcmd()