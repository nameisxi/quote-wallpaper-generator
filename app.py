import time
import random
import textwrap

import pandas as pd
from PIL import Image, ImageFont, ImageDraw 
from appscript import app, mactypes
import subprocess


wallpaper_filename = "zhihu-wallpaper2"
wallpaper_path = f"./{wallpaper_filename}.png"
max_line_length = 80

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

def set_desktop_background(filename):
    subprocess.Popen(SCRIPT%filename, shell=True)

def combine_lines(quote):
    try:
        counter = 0
        while True:
            sentences = quote.splitlines(True)
            for j, sentence in enumerate(sentences):
                if counter == len(sentences): return quote
                if j > 0 and (len(sentence) + len(sentences[j-1])) < max_line_length:
                    quote = quote.replace(sentences[j-1], sentences[j-1].replace("\n", ""))
                    counter = 0
                    break
                else:
                    counter += 1
                
        return quote
    except:
        return quote

def split_to_newline(quote):
    quote = quote.replace(".", ".\n").replace("!", "!\n").replace("?", "?\n")
    quote = combine_lines(quote)

    sentences = quote.splitlines(True)
    for i, sentence in enumerate(sentences):
        if len(sentence) > max_line_length:
            quote = quote.replace(sentence, sentence.replace(":", ":\n").replace(";", ";\n"))
    quote = combine_lines(quote)

    sentences = quote.splitlines(True)
    for i, sentence in enumerate(sentences):
        if len(sentence) > max_line_length:
            quote = quote.replace(sentence, sentence.replace(",", ",\n"))
    quote = combine_lines(quote)

    sentences = quote.splitlines(True)
    for sentence in sentences:
        quote = quote.replace(sentence, sentence.lstrip())

    return quote

def main():
    wallpaper = Image.open(wallpaper_path).convert('RGBA')
    quotes = pd.read_csv("./goodreads_quotes_export.csv")
    font = ImageFont.truetype('/System/Library/Fonts/SFCompact.ttf', 40)

    quote = quotes.sample(n=1)

    quote_text = split_to_newline(quote['Quote'].values[0]) 
    quote_text = f"{quote_text}\n- {quote['Author'].values[0]}"

    wallpaper_editable = ImageDraw.Draw(wallpaper)
    wallpaper_editable.text((575,1), quote_text, (255, 255, 255), font=font)

    filename = f"/Users/thomaspelm/projects/quote-to-wallpaper-generator/wallpapers/{wallpaper_filename}_{quote['Goodreads Quote Id'].values[0]}_{time.time()}.png"
    wallpaper.save(filename)

    # Set Mac desktop wallpaper
    set_desktop_background(filename)


if __name__ == "__main__":
    main()