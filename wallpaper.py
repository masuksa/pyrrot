#! /usr/bin/python

##
# Requires Python3.5 for subprocess

## TODO
#
# * If the song is paused (for more than x seconds), use a "normal" wallpaper
# * CONFIG_FILE override

import sys
import json
from os.path import expanduser, abspath, dirname
import subprocess
import random
import configparser

CONFIG_FILE = expanduser("~") + "/.config/pyrrot/pyrrot.config"
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

print("config: {}".format(CONFIG_FILE))

if config["global"]["debug"] == "true":
    print("Mode: {}".format(config["global"]["mode"]))

INCLUDE_TAGS =      [tag.strip() for tag in config["wallpaper"]["include_tags"].strip("[]").split(',')]
INCLUDE_COLOURS =   [colour.strip() for colour in config["wallpaper"]["include_colours"].strip("[]").split(',')]
INCLUDE_FILES =     [filename.strip() for filename in config["wallpaper"]["include_files"].strip("[]").split(',')]
EXCLUDE_TAGS =      [tag.strip() for tag in config["wallpaper"]["exclude_tags"].strip("[]").split(',')]
EXCLUDE_COLOURS =   [colour.strip() for colour in config["wallpaper"]["exclude_colours"].strip("[]").split(',')]
EXCLUDE_FILES =     [filename.strip() for filename in config["wallpaper"]["exclude_files"].strip("[]").split(',')]
if '' in INCLUDE_TAGS:
    INCLUDE_TAGS.remove('')
if '' in INCLUDE_COLOURS:
    INCLUDE_COLOURS.remove('')
if '' in INCLUDE_FILES:
    INCLUDE_FILES.remove('')
if '' in EXCLUDE_TAGS:
    EXCLUDE_TAGS.remove('')
if '' in EXCLUDE_COLOURS:
    EXCLUDE_COLOURS.remove('')
if '' in EXCLUDE_FILES:
    EXCLUDE_FILES.remove('')
if config["global"]["debug"] == "true":
    print("Included tags :")
    print(INCLUDE_TAGS)
    print("Included colours :")
    print(INCLUDE_COLOURS)
    print("Included files :")
    print(INCLUDE_FILES)
    print("Excluded tags :")
    print(EXCLUDE_TAGS)
    print("Excluded colours :")
    print(EXCLUDE_COLOURS)
    print("Excluded files :")
    print(EXCLUDE_FILES)

def get_all_tags(infos):
    """
    return: dict tag: count
    """
    res = {}
    for x in infos:
        for t in x["tags"]: 
            if res.has_key(t):
                res[t] = res[t] + 1
            else:
                res[t] = 1
    return res

def get_wallpapers_with_tags(infos, tags):
    res = []
    for x in infos:
        for t in x["tags"]: 
            if t in tags:
                res.append(x)
                break
    return res

def get_wallpapers_with_colours(infos, colours):
    res = []
    for x in infos:
        for t in x["colours"]: 
            if t in colours:
                res.append(x)
                break
    return res

def set_wallpaper(wallpaper, feh_options=["--bg-fill"]):
    """
    wallpaper: dict object for the wallpaper
    """
    if wallpaper is None: return
    if config["global"]["mode"] == "albumart":
        file = config["global"]["albumart"]
    else:
        file = expanduser(dirname(config["global"]["picture_infos"])) + "/" + wallpaper["file"]

    subprocess.run(["feh", file] + feh_options)

    # setting theme
    print("Theme update : ")
    print(config.getboolean("global", "update_theme"))
    if not config.getboolean("global", "update_theme"):
        return
    if config.getboolean("wallpaper", "use_static_theme"):
        subprocess.run(["wal", "--theme", config["wallpaper"]["default_theme"]])
        print("Tata")
    elif "theme" in wallpaper:
        subprocess.run(["wal", "--theme", wallpaper["theme"]])
        print("Tete")
    else:
        # bug when for covers, see https://github.com/dylanaraps/pywal/issues/429
        # cache is not reset, so we have to do it by hand first
        subprocess.run(["wal", "-c"])
        subprocess.run(["wal", "-i", file, "-n"])
        print("Tutu")
    # fixing powerline colors
    subprocess.run([abspath(expanduser(config["wallpaper"]["powerline_colors"]))])
    print("Toto")
    return


# TODO check that image file exists

def select_wallpaper(infos):
    """Return selected wallpaper object"""
    selected_pictures = []

    if config["global"]["mode"] != "selection":
        selected_pictures = infos
    else:
        for pic in infos:
            excluded = False
            for tag in EXCLUDE_TAGS:
                if tag in pic["tags"]:
                    excluded = True
                    break
            for colour in EXCLUDE_COLOURS:
                if colour in pic["colours"]:
                    excluded = True
                    break
            for f in EXCLUDE_FILES:
                if f in pic["file"]:
                    excluded = True
                    break
            if not excluded:
                if len(INCLUDE_TAGS) == 0:
                    selected_pictures.append(pic)
                else:
                    for tag in pic["tags"]:
                        if tag in INCLUDE_TAGS and pic not in selected_pictures:
                            selected_pictures.append(pic)
                            break
                if len(INCLUDE_COLOURS) > 0:
                    selected_pictures.append(pic)
                else:
                    for colour in pic["colours"]:
                        if colour in INCLUDE_COLOURS and pic not in selected_pictures:
                            selected_pictures.append(pic)
                            break
                if len(INCLUDE_FILES) > 0:
                    selected_pictures.append(pic)
                else:
                    if pic["file"] in INCLUDE_FILES and pic not in selected_pictures:
                        selected_pictures.add(pic)

    if len(selected_pictures) == 0:
        print("There is no wallpaper matching your criteria.")
        return
    pic = random.choice(selected_pictures)
    print(json.dumps(pic, sort_keys=True, indent=4))
    return pic
        

if __name__ == '__main__':
    with open(expanduser(config["global"]["picture_infos"]), 'r') as f:
        t = f.read()

    infos = json.loads(t)

    """
    # TODO : use argparse or something like this
    flag_tags = False
    flag_pinfo = False
    flag_ptags = False
    for arg in sys.argv:
        if flag_tags:
            TAGS = arg.split(',')
            for i in range(len(TAGS)):
                TAGS[i] = TAGS[i].strip(' ')
            flag_tags = False
        if arg == "--tags":
            flag_tags = True
        if arg == "--pinfos":
            flag_pinfo = True
        if arg == "--ptags":
            flag_ptags = True
        if arg == "--albumart":
            USE_ALBUMART = True

    if flag_ptags:
        all_tags = print_all_tags(infos)
        all_tags.sort()
        for t in all_tags:
            print(t)
    elif flag_pinfo:
        print(TAGS)
        for pic in get_wallpapers_with_tags(infos):
            print(pic["name"])
    elif USE_ALBUMART:
        pic = {}
        set_wallpaper(pic);
    else:
        set_wallpaper(select_wallpaper(infos))
    """
    if config["global"]["mode"] == "albumart":
        pic = {
                'file': expanduser(config["global"]["albumart"])
                }
        set_wallpaper(pic, feh_options=["--bg-center"]);
    else:
        set_wallpaper(select_wallpaper(infos))

