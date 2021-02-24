import time
import random
import textwrap

from PIL import Image, ImageFont, ImageDraw 
from appscript import app, mactypes
import subprocess

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

def set_desktop_background(filename):
    subprocess.Popen(SCRIPT%filename, shell=True)


wallpaper_filename = "zhihu-wallpaper"
wallpaper_path = f"./{wallpaper_filename}.png"

quotes = [
    "Live to the point of tears.",
    "To be ignorant of what occurred before you were born is to remain always a child. For what is the worth of human life, unless it is woven into the life of our ancestors by the records of history?",
    "Read at every wait; read at all hours; read within leisure; read in times of labor; read as one goes in; read as one goest out. The task of the educated mind is simply put: read to lead.",
    "If we are not ashamed to think it, we should not be ashamed to say it.",
    "If you're ever behind on commitments to other people, you must commit to working 14 hours a day on those commitments until you've caught up."
]

def main():
    wallpaper = Image.open(wallpaper_path).convert('RGBA')

    quote = random.choice(quotes)
    quote_index = quotes.index(quote)
    quote = textwrap.fill(quote, width=70)

    font = ImageFont.truetype('/System/Library/Fonts/SFCompact.ttf', 50)

    wallpaper_editable = ImageDraw.Draw(wallpaper)
    wallpaper_editable.text((15,15), quote, (255, 255, 255), font=font)

    filename = f"/Users/thomaspelm/projects/quote-to-wallpaper-generator/{wallpaper_filename}_{quote_index}_{time.time()}.png"
    wallpaper.save(filename)

    # Set Mac desktop wallpaper
    set_desktop_background(filename)
    #app('Finder').desktop_picture.set(mactypes.File(filename))


if __name__ == "__main__":
    main()