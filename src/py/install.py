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
    

INSTALL_DIR = "..{}..{}gameservers{}".format(PATH_SEPERATOR, PATH_SEPERATOR, PATH_SEPERATOR)


# Returns 1 if steamcmd not installed and on path else returns 0
# attempts to run the shell command "steamcmd +quit" 
# if the stderr contains command not found output then it prints Error and returns 1 else it returns 0
def check_steamcmd() -> int:
    command = "steamcmd"
    
    process = subprocess.run(args = f"{command} +quit" , capture_output=True, check=True, shell=True)
    # Checks to see if the standard linux or windows shell response in stderr for when command is not found occurs
    if "not found" in process.stderr or "not recognized" in process.stderr:
        print("Error: steamcmd command not found.")
        print("       Likely steamcmd is not installed on your system.")
        print("       https://developer.valvesoftware.com/wiki/SteamCMD")
        return 1
    
    if "ulimit" in process.stderr:
        process = subprocess.run(args="ulimit -n 2048", check = True, shell=True)
    
    return 0

# install game server steam_appid in dir with steam_appname as name of dir
def install_server(steam_appname: str, steam_appid: int) -> int:
    if check_steamcmd() == 1:
        return 1;
    
    path = f"{INSTALL_DIR}{PATH_SEPERATOR}{steam_appname}"
    
    try:
        os.makedirs(path, exist_ok=True)
        print("Success: Created directory %s" %path)
    except:
        print("Error: unable to create directory %s" %path)
        return 1
    
    flags = "+force_install_dir {} +login {} {} +app_update {} validate +quit".format(path, STEAM_USER, STEAM_PASS, steam_appid)
    process = subprocess.run(args=f"steamcmd {flags}", capture_output=True, check=True, shell=True)
    
    return 0

check_steamcmd()