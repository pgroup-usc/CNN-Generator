import numpy as np
from logf.printf import printf

import PIL.Image as I
import PIL.ImageDraw as ID
import PIL.ImageFont as IF

import draw.font.font_util as ft

from functools import reduce
from math import ceil
import pdb


class plot_curve:
    def __init__(self, f_list, func_data, unit_x, unit_y, output_file):
        """
        f_list: a list of files with points to plot
        func_data: lambda function to be applied to the input file
        """
        self.data = {}
        for f in f_list:
            with open(f) as f_:
                l_raw = f_.readlines()
                # pdb.set_trace()
                self.data[f.split('/')[-1]] = list(map(lambda _: func_data(_), l_raw))
        self.unit_x = unit_x
        self.unit_y = unit_y
        self.output_file = output_file
        self.color_set = ['red','blue','green','black']
        
    def _normalize(self):
        for k in self.data:
            m = min(self.data[k])
            self.data[k] = [i-m for i in self.data[k]]

    def plot(self):
        self._normalize()
        max_x = reduce(lambda mx,k: (len(self.data[k])>mx) and len(self.data[k]) or mx, self.data, 0)
        max_y = reduce(lambda mx,k: (max(self.data[k])>mx) and max(self.data[k]) or mx, self.data, 0)
        W = ceil(max_x*self.unit_x)
        H = ceil(max_y*self.unit_y)
        self.img = I.new('RGB', (W, H), 'white')
        self.draw = ID.Draw(self.img)
        # draw lines
        font, _ = ft.adjust_font_size(self.unit_x)
        line_label_y_off = 0
        for li, ln in enumerate(self.data):
            ln_col = self.color_set[li%len(self.color_set)]
            w = len(self.data[ln])*self.unit_x
            for i,x in enumerate(range(self.unit_x, w, self.unit_x)):
                x0 = x-self.unit_x
                x1 = x
                y0 = H-(self.data[ln][i-1])*self.unit_y
                y1 = H-(self.data[ln][i])*self.unit_y
                self.draw.line([x0,y0,x1,y1], fill=ln_col)
            # add name to the plotted line
            dx, dy = font.getsize(ln)
            self.draw.text([W-dx,H-dy-line_label_y_off], ln, fill=ln_col, font=font)
            line_label_y_off += dy

    def save(self):
        if self.img is None:
            printf('img has not been drawn yet')
            exit()
        else:
            self.img.save(self.output_file, 'PNG')
