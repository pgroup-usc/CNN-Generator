"""
complete the entire tree: draw the edges
"""
from logf.printf import printf
import numpy as np
import math

import PIL.ImageDraw as ID
import PIL.ImageFont as IF
import pdb

def connect_nodes(img_draw, from_idx, to_idx, unit, fill="black", width=1, is_dir=False, label="", label_fill="black"):
    import draw.tree.macro as macro
    r = macro.NODE_SCALE*unit
    dx = abs(macro.nodes[from_idx][0] - macro.nodes[to_idx][0])
    dy = abs(macro.nodes[from_idx][1] - macro.nodes[to_idx][1])
    l = math.sqrt(dx*dx + dy*dy)
    x_ctr, y_ctr = (macro.nodes[from_idx] + macro.nodes[to_idx])/2
    if macro.nodes[from_idx][0] > macro.nodes[to_idx][0]:
        x0 = x_ctr + (l-2*r)*dx/(2*l)
        x1 = x_ctr - (l-2*r)*dx/(2*l)
    else:
        x1 = x_ctr + (l-2*r)*dx/(2*l)
        x0 = x_ctr - (l-2*r)*dx/(2*l)
    if macro.nodes[from_idx][1] > macro.nodes[to_idx][1]:
        y0 = y_ctr + (l-2*r)*dy/(2*l)
        y1 = y_ctr - (l-2*r)*dy/(2*l)
    else:
        y1 = y_ctr + (l-2*r)*dy/(2*l)
        y0 = y_ctr - (l-2*r)*dy/(2*l)
    import draw.font as f
    import draw.tree.element as elem
    unit_width=macro.NODE_SCALE*unit
    elem.write_txt(img_draw, label, x_ctr,y_ctr, unit_width, label_fill)
    img_draw.line([x0,y0,x1,y1], fill=fill, width=width)
