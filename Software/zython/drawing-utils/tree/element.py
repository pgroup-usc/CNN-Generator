"""
directory should be relative to the "draw" package.
"""
from logf.printf import printf
import numpy as np

import PIL.ImageDraw as ID
import PIL.ImageFont as IF
import pdb

def write_txt(img_draw, txt, x,y, unit_width, color):
    """
    x,y are the center of txt
    """
    import draw.font as f
    font, _ = f.font_util.adjust_font_size(unit_width)
    dx, dy = font.getsize(txt)
    x -= dx/2
    y -= dy/2
    img_draw.text([x,y], txt, fill=color, font=font)


def draw_node(img_draw, idx, x,y, unit, fill="white", outline="black",
        label="", label_color="black"):
    import draw.tree.macro as macro
    r = macro.NODE_SCALE*unit
    img_draw.ellipse([x-r, y-r, x+r, y+r], fill=fill, outline=outline)
    write_txt(img_draw, label, x,y, r, label_color)
    macro.nodes[idx] = np.array((x,y))


def draw_subtree(img_draw, idx, x, y, unit, 
        node_fill="white", tree_fill="#ADD8E6", 
        node_outline="black", tree_outline="black",
        node_label="", tree_label="",
        n_label_col="black", t_label_col="black"):
    import draw.tree.macro as macro
    node_r = macro.NODE_SCALE*unit
    tri_bottom = 4*unit
    tri_height = 5*unit
    # draw subtree root
    draw_node(img_draw, idx, x,y, unit, fill=node_fill, outline=node_outline, label=node_label, label_color=n_label_col)
    #img_draw.ellipse([x-node_r, y-node_r, x+node_r, y+node_r], fill=node_fill, outline=node_outline)
    # draw tree (triangle)
    tri_pts = [0.]*6
    tri_pts[0] = x
    tri_pts[1] = y + node_r
    tri_pts[2] = tri_pts[0] - tri_bottom/2
    tri_pts[3] = tri_pts[1] + tri_height
    tri_pts[4] = tri_pts[0] + tri_bottom/2
    tri_pts[5] = tri_pts[3]
    img_draw.polygon(tri_pts, fill=tree_fill, outline=tree_outline)
   
