import numpy as np
from math import ceil, floor
from logf.printf import printf

import PIL.Image as I
import PIL.ImageDraw as ID
import PIL.ImageFont as IF

import draw.font.font_util as ft

from functools import reduce
import pdb

class scheduler:
    def __init__(self, op_path, unit_x, unit_y):
        """
        unit_x: length of one time unit
        unit_y: vertical separation for time overlapped jobs
        """
        self.op_path = op_path
        self.unit_x = unit_x
        self.unit_y = unit_y
        self.jobs = []
        self.img = None
        self.draw = None
        self.job_height_scale = 0.6 # scale in terms of unit_y
        

    def add_job(self, start, end, color):
        """
        start / end are in terms of time units
        """
        self.jobs += [(start, end, color)]
    
    def _draw_axis(self, ax_y, axis_len, axis_col, width, idx_l):
        assert self.draw is not None
        ax_x0 = self.unit_x
        ax_x_end = ceil((axis_len+2)*self.unit_x)
        ax_x1 = ax_x_end - 0.4*self.unit_x
        self.draw.line([ax_x0, ax_y, ax_x1, ax_y], fill=axis_col, width=width)
        # mark
        for x in range(ax_x0, ax_x_end, self.unit_x):
            y0 = ax_y - self.unit_y*0.1
            y1 = ax_y + self.unit_y*0.1
            self.draw.line([x,y0,x,y1], fill=axis_col)
        font, _ = ft.adjust_font_size(self.unit_x*0.2)
        # label
        for i,l in enumerate(idx_l):
            x_ctr = (i+1)*self.unit_x
            y_up = ax_y + self.unit_y*0.1
            dx, dy = font.getsize(str(l))
            self.draw.text([x_ctr-dx/2,y_up], str(l), fill=axis_col, font=font)
        # arrow
        x0 = ax_x1
        x1 = ax_x1 - 0.15*self.unit_x
        x2 = x1
        y0 = ax_y
        y1 = y0 + self.unit_y*0.15
        y2 = y0 - self.unit_y*0.15
        self.draw.polygon((x0,y0,x1,y1,x2,y2), fill=axis_col)
        
 

    
    def drawing(self, axis_col='black', width=1):
        max_end_time = max([j[1] for j in self.jobs])
        min_start_time = min([j[0] for j in self.jobs])
        axis_len = max_end_time - min_start_time
        # assign jobs to tracks: compound layout
        track = [None] * len(self.jobs)
        for jb in self.jobs:
            for ti, tk in enumerate(track):
                if tk is None:
                    track[ti] = (jb,)
                    break
                else:
                    is_ok = True
                    for jtk in tk:
                        if not ((jtk[1]<=jb[0]) or (jtk[0]>=jb[1])):
                            # has overlapped already
                            is_ok = False
                            break
                    if is_ok:
                        track[ti] += (jb,)
                        break
        num_track = reduce(lambda _1,_2: _1+(_2 is not None), track, 0)
        # draw
        self.img = I.new('RGB', (ceil((axis_len+2)*self.unit_x), ceil((num_track+2)*self.unit_y)), 'white')
        self.draw = ID.Draw(self.img)
        ax_y  = (num_track+1)*self.unit_y
        self._draw_axis(ax_y, axis_len, axis_col, width, list(range(floor(min_start_time),ceil(max_end_time+1))))
       
        for ti, tk in enumerate(track):
            if tk is None:
                continue
            for jb in tk:
                y0 = (ti+1)*self.unit_y
                y1 = y0 + self.job_height_scale*self.unit_y
                x0 = (jb[0] - min_start_time + 1)*self.unit_x
                x1 = (jb[1] - min_start_time + 1)*self.unit_x
                self.draw.rectangle([x0,y0,x1,y1], fill=jb[2])
    
    def add_title(self, title):
        assert self.draw is not None
        font, _ = ft.adjust_font_size(self.unit_x*0.2)
        dx, dy = font.getsize(title)
        self.draw.text([0,0], title, fill='black', font=font)
    
    def save(self):
        if self.img is None:
            printf('img has not been drawn yet')
            exit()
        else:
            self.img.save(self.op_path, 'PNG')
        
