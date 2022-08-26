#! /usr/bin/python
"""
This is the main script that pyrrot should launch.

It is currently in the process of being cleaned and refactored.
"""

## TODO
#
# * If the song is paused (for more than x seconds), use a "normal" wallpaper
# * CONFIG_FILE override

from os.path import expanduser, abspath, dirname
import subprocess

from pyrrot_wallpaper.wallpaper_metadata import WallpaperMetadata
from pyrrot_wallpaper.config import SelectionMode, WallpaperConfig

def set_wallpaper(wallpaper, wallpaper_config: WallpaperConfig, feh_options=("--bg-fill",)):
    """
    wallpaper: dict object for the wallpaper
    """
    if wallpaper_config.selection_mode == SelectionMode.ALBUMART:
        file = wallpaper_config.music["albumart_file"]
    else:
        file = expanduser(dirname(wallpaper_config.metadata_file)) + "/" + wallpaper["file"]

    subprocess.run(["feh", file] + [fopt for fopt in feh_options], check=True)

    # setting theme
    print("Theme update : ")
    print(wallpaper_config.theme["do_update_theme"])
    if not wallpaper_config.theme["do_update_theme"]:
        return
    if wallpaper_config.theme["use_static_theme"]:
        subprocess.run(["wal", "--theme", wallpaper_config.theme["default_theme"]], check=True)
        print("Tata")
    elif "theme" in wallpaper:
        subprocess.run(["wal", "--theme", wallpaper["theme"]], check=True)
        print("Tete")
    else:
        # bug when for covers, see https://github.com/dylanaraps/pywal/issues/429
        # cache is not reset, so we have to do it by hand first
        subprocess.run(["wal", "-c"], check=True)
        subprocess.run(["wal", "-i", file, "-n"], check=True)
        print("Tutu")
    # fixing powerline colors
    subprocess.run([abspath(expanduser(wallpaper_config.theme["powerline_colours"]))], check=True)
    print("Toto")
    return

if __name__ == '__main__':
    wallpaper_config = WallpaperConfig(expanduser("~") + "/.config/pyrrot/pyrrot.config")

    if wallpaper_config.debug:
        print(f"Mode: {wallpaper_config.selection_mode}")

    wallpaperMetdata = WallpaperMetadata(
        expanduser(dirname(wallpaper_config.metadata_file)),
        expanduser(wallpaper_config.metadata_file)
        )

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
    if wallpaper_config.selection_mode == SelectionMode.ALBUMART:
        pic = {
                'file': expanduser(wallpaper_config.music["albumart_file"])
                }
        set_wallpaper(pic, wallpaper_config, feh_options=("--bg-center",))
    else:
        set_wallpaper(wallpaperMetdata.select_single_wallpaper(wallpaper_config), wallpaper_config)
