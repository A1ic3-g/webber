from pysteamcmdwrapper import SteamCMD, SteamCMDException
import env_vars
import os
from sqlalchemy.exc import IntegrityError
import re
from .models import Mod 
from . import db


def steam_install():
    steam = SteamCMD(env_vars.STEAMCMD_DIR)
    steam.install()

def game_install():
    try:
        steam = SteamCMD(env_vars.STEAMCMD_DIR)
        steam.app_update(233780,os.path.join(os.getcwd(),env_vars.SERVER_DIR),validate=True)
    except SteamCMDException:
        print("ERROR: SteamCMD exception installing game")

def mod_install(mod_id: int, mod_name = None, n_tries = 10):
    """Installs a mod using its mod id
        mod_id = steam workshop mod ID
        n_tries = number of times to attempt to install the mod if it times out the first time
                  default is 10
                  
        adds the mod to the modlist database
        adds symlink between mod_id folder and mod_name folder"""

        
    steam = SteamCMD(env_vars.STEAMCMD_DIR)
    
    try:
        steam.workshop_update(
            app_id=107410, 
            workshop_id=mod_id,
            n_tries=n_tries, 
            install_dir=os.path.join(os.getcwd(), env_vars.SERVER_DIR, "workshop")
        )
        
    except SteamCMDException:
        print(f"Error Installing mod {mod_id}")
        return

    # Create the folder name from the mod name defined in the modpack file 
    if mod_name is None:
        mod_name = f"@{mod_id}"
    else:
        # regex to replace all special characters in the modname 
        mod_name = re.sub(r"[^0-9a-zA-Z@-]", "-")
        mod_name = f"@{mod_name.lower()}"
    

    
    mod = Mod( mod_id = mod_id, mod_name= mod_name)
    db.session.add(mod)
    try:
        db.commit()
    except IntegrityError:
        db.session.rollback()
        print("Error: Mod already in database")

    try:
        # create symlink between workshop dir and gamedir
        os.symlink(os.path.join(os.getcwd(), env_vars.SERVER_DIR, "workshop", mod_id),
                    os.path.join(os.getcwd(), env_vars.SERVER_DIR, mod_name))
    except OSError:
        print("Error: failed to create symlink between workshop dir and mod dir")
        


def mod_update(mod_id: int, n_tries=10):
    """Updates a mod with a given mod_id
        mod_id = steam workshop mod id
        n_tries = number of times to attempt to install the mod if it times out the first time
                  default is 10"""
    steam = SteamCMD(env_vars.STEAMCMD_DIR)
    
    try:
        steam.workshop_update(
            app_id=107410, 
            workshop_id=mod_id,
            n_tries=n_tries,
            install_dir=os.path.join(os.getcwd(), env_vars.SERVER_DIR, "workshop"),
            validate=True, 
        )
    except SteamCMDException:
        print(f"Error updating mod {mod_id}")

def mod_unistall(mod_id: int):
    """Removes the mod from the server with a given workshop id
    Removes symlink and mod folder
    Removes mod from the database"""

    # get mod details from the database
    # to get the name of the mod symlink
    mod = Mod.query.get(mod_id)

    # remove symlink
    try:
        remove_symlink(os.path.join(os.getcwd(), env_vars.SERVER_DIR, mod.mod_name))
    except OSError:
        print(f"Error: symlink {mod.mod_name} not found")
    
    # remove mod
    try:
        os.rmdir(os.path.join(os.cwd(), env_vars.SERVER_DIR, "workshop", mod_id))
    except OSError:
        print(f"Error: mod workshop folder not found for {mod_id}")


    # remove database entry
    db.session.delete(mod)
    db.session.commit()


def remove_symlink(path:str):
    """OS agnostic method to remove a symlink to a folder"""
    if(os.path.isdir(path)):
        os.rmdir(path)
    else:
        os.unlink(path)