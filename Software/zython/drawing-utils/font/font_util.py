"""
directory should be relative to the "draw" package
"""

from logf.printf import printf

import PIL.Image as I
import PIL.ImageFont as IF
import pdb

FONT = "draw/font/UbuntuMono/UbuntuMono-R.ttf"

def adjust_font_size(unit_width, font=FONT):
    """
    adjust the font size based on the width requirement. --> measured per char
    """
    char = "A"
    fontsize=1
    ft = IF.truetype(font, fontsize)
    while ft.getsize(char)[0] < unit_width:
        fontsize += 1
        ft = IF.truetype(font, fontsize)
    ft = IF.truetype(font, fontsize-1)
    return ft, fontsize
