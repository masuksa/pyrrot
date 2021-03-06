This is a collection of scripts I use to manage my wallpapers.
This is made for my usage in mind, and hasn't been tested much by others, but it might interest you.
If you've got any suggestion or issue, please let me know.

I personnally use Archlinux, and more importantly i3wm.
These scripts may not work on other window managers.

## What does it do ?

The `wallpaper.py` script sets you wallpaper from a json file listing all your wallpapers with a few attributes.
Wallpapers may be any file supported by feh (jpeg and non-animated png and gif).
Animated gif or vidéo support for live-wallpapers will be supported later using xwinwrap.
(I should also make a script to aut-generate such a json file if you just want to use a list of images without selection by tags or colors for instance.)

`mpd-wallpaper` will allow you to set your wallpaper with the cover of the current music you're listening to with your mpd server.
It requires `wallpaper.py`.

## Usage

1. Edit wallpaper.conf according to your needs.
2. Setup a cron job to run wallpaper.py to change the wallpaper regularly. Mine is `*/5 * * * * DISPLAY=:0 /home/user/scripts/wallpaper/wallpaper.py`
3. Setup a systemd task for the mpd part (optional). See the `mpd-wallpaper.service.example`.
 Of course if you prefer not to run the scripts with cron or systemd, you're free to use them as you want.

## Prerequisites

Python 3.7 for the mpd script, Python 3.5 for the wallpaper.py, pywal and feh.
Linux (it might work on some BSD or macOS but it may need some tweaks, and it hasn't been tested at all)
