#! /usr/bin/python

# Need Python 3.7

import subprocess
from time import sleep
from os.path import expanduser, abspath
import configparser
import time


CONFIG_FILE = expanduser("~") + "/scripts/wallpaper/wallpaper.config"
config = configparser.ConfigParser()
config.read(CONFIG_FILE)


def extract_albumart(prev_songfile, prev_t):
    config.read(CONFIG_FILE)
    # TODO: with shell = True : less unicode problems, but then the songfile is incorrect
    songfile = subprocess.run(["mpc", "--format", "%file%", "current"], capture_output=True, text=True).stdout
    songfile = abspath(expanduser(config["global"]["music_dir"])) + "/" + songfile.strip("\n")
    if config["global"]["debug"] == "true": print("Songfile: " + songfile)
    if prev_songfile == songfile and time.time() - prev_t < config["mpd"]["song_interval"]: return (songfile, time.time())
    subprocess.run(["rm", config["global"]["albumart"]])
    if config["global"]["debug"] == "true": print("albumart file: " + config["global"]["albumart"])
    # TODO : it doesn't work for Jyc Row Orchestral Compilation vol. 2
    subprocess.run(["ffmpeg", "-i", songfile, "-an", "-vcodec", "copy", config["global"]["albumart"], "-y", "-loglevel", "quiet"], text = True)
    # TODO : if image set, get width, height, and maybe rescale it

    if config["global"]["mode"] == "albumart":
        sleep(1) # else, the cover in /tmp/cover.sh might not have been set already
        if config["global"]["debug"] == "true": print("Song has changed")
        subprocess.run([config["global"]["wallpaper_script"]])
    return (songfile, time.time())

if __name__ == "__main__":
    prev_songfile = ""
    prev_t = time.time()
    while subprocess.run(["mpc", "idle", "player"]):
        songfile, prev_t = extract_albumart(prev_songfile, prev_t)
