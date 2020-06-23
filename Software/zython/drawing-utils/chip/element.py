from logf.printf import printf
import numpy as np
from math import ceil

import PIL.Image as I
import PIL.ImageDraw as ID
import PIL.ImageFont as IF

import draw.font.font_util as ft

import pdb

def draw_rect_width(x1, y1, x2, y2, draw, width):
    fill='black'
    draw.line([x1,y1,x2,y1], width=width, fill=fill)
    draw.line([x1,y2,x2,y2], width=width, fill=fill)
    draw.line([x1,y1,x1,y2], width=width, fill=fill)
    draw.line([x2,y1,x2,y2], width=width, fill=fill)


class chip:
    def __init__(self, img_out, clb_wid, chan_wid, row, col, width=2):
        self.img_out = img_out
        self.clb_wid = clb_wid
        self.chan_wid = chan_wid
        self.row = row
        self.col = col
        self.W = col*(clb_wid+chan_wid) + chan_wid
        self.H = row*(clb_wid+chan_wid) + chan_wid
        self.img = I.new('RGB', (self.W, self.H), "white")
        self.draw = ID.Draw(self.img)
        for r in range(self.row):
            for c in range(self.col):
                x = self.chan_wid + c*(self.chan_wid + self.clb_wid)
                y = self.chan_wid + r*(self.chan_wid + self.clb_wid)
                # self.draw.rectangle([x,y,x+self.clb_wid,y+self.clb_wid],outline='black')
                draw_rect_width(x,y,x+self.clb_wid,y+self.clb_wid, self.draw, ceil(width))
        self.wire_pos = {}

    def add_track(self, track_fraction, wlen, is_x_dir, start_clb, width=1):
        """
        start_clb index starts from 0
        """
        width = ceil(width)
        if is_x_dir:
            for r in range(self.row-1):
                y = (r+1)*(self.chan_wid+self.clb_wid) + track_fraction*self.chan_wid
                for c in range(start_clb, self.col, wlen):
                    x0 = self.chan_wid + (self.chan_wid+self.clb_wid)*c
                    x1 = x0 + wlen*self.clb_wid + (wlen-1)*self.chan_wid
                    x1 = min(self.W-self.chan_wid, x1)
                    self.draw.line([x0,y,x1,y], fill="black", width=width)
                    self.wire_pos[(r+track_fraction, c)] = [x0,y,x1,y]
                if start_clb > 0:
                    x0 = self.chan_wid
                    x1 = x0 + start_clb*self.clb_wid + (start_clb-1)*self.chan_wid
                    self.draw.line([x0,y,x1,y], fill="black", width=width)
                    self.wire_pos[(r+track_fraction, 0)] = [x0,y,x1,y]
        else:
            for c in range(self.col-1):
                x = (c+1)*(self.chan_wid+self.clb_wid) + track_fraction*self.chan_wid
                for r in range(start_clb, self.row, wlen):
                    y0 = self.chan_wid + (self.chan_wid+self.clb_wid)*r
                    y1 = y0 + wlen*self.clb_wid + (wlen-1)*self.chan_wid
                    y1 = min(self.H-self.chan_wid, y1)
                    self.draw.line([x,y0,x,y1], fill='black', width=width)
                    self.wire_pos[(r,c+track_fraction)] = [x,y0,x,y1]
                if start_clb > 0:
                    y0 = self.chan_wid
                    y1 = y0 + start_clb*self.clb_wid + (start_clb-1)*self.chan_wid
                    self.draw.line([x,y0,x,y1], fill='black', width=width)
                    self.wire_pos[(0,c+track_fraction)] = [x,y0,x,y1]
                
    def sig_flow(self, r, c, fill='red', width=6):
        width = ceil(width)
        self.draw.line(self.wire_pos[(r,c)], fill=fill, width=width)

    def connect(self, r0, c0, r1, c1, fill='red', width=3):
        width = ceil(width)
        p0 = np.array(self.wire_pos[(r0,c0)][0:2])
        p1 = np.array(self.wire_pos[(r0,c0)][2:4])
        p2 = np.array(self.wire_pos[(r1,c1)][0:2])
        p3 = np.array(self.wire_pos[(r1,c1)][2:4])
        d = [None] * 4
        d[0] = np.linalg.norm(p0-p2)
        d[1] = np.linalg.norm(p0-p3)
        d[2] = np.linalg.norm(p1-p2)
        d[3] = np.linalg.norm(p1-p3)
        idx = list(d).index(min(*list(d)))
        s = (idx<=1) and list(p0) or list(p1)
        e = (idx%2==0) and list(p2) or list(p3)
        self.draw.line(s+e, fill=fill, width=width)
    
    def connect_pin(self, w_r,w_c, b_r,b_c, fill='red',width=3):
        """
        wire row / column & clb row / column
        """
        width = ceil(width)
        if w_r // 1 == w_r:     # wire in y direction
            cross_y = self.chan_wid + 0.5*self.clb_wid + b_r*(self.chan_wid+self.clb_wid)
            cross_x = self.wire_pos[(w_r,w_c)][0]
            pin_y = cross_y
            pin_x = (b_c+1)*(self.chan_wid+self.clb_wid) - (b_c-w_c//1)*self.clb_wid
        else:
            cross_x = self.chan_wid + 0.5*self.clb_wid + b_c*(self.chan_wid+self.clb_wid)
            cross_y = self.wire_pos[(w_r,w_c)][1]
            pin_x = cross_x
            pin_y = (b_r+1)*(self.chan_wid+self.clb_wid) - (b_r-w_r//1)*self.clb_wid
        
        self.draw.line([cross_x,cross_y,pin_x,pin_y], fill=fill,width=width)
        diag = 1/8*self.chan_wid
        self.draw.line([cross_x-diag,cross_y-diag,cross_x+diag,cross_y+diag], fill=fill, width=width)
        self.draw.line([cross_x-diag,cross_y+diag,cross_x+diag,cross_y-diag], fill=fill, width=width)

    def label_clb(self, r,c, txt, fill='black'):
        font, _ = ft.adjust_font_size(self.clb_wid*0.2)
        # some bug for getsize, when txt contains newline
        dx = 0
        dy = 0
        for s in txt.split('\n'):
            dx_, dy_ = font.getsize(s)
            dx = max(dx, dx_)
            dy += dy_
        x_ctr = self.chan_wid + 0.5*self.clb_wid + c*(self.chan_wid+self.clb_wid)
        y_ctr = self.chan_wid + 0.5*self.clb_wid + r*(self.chan_wid+self.clb_wid)
        self.draw.text([x_ctr-dx/2, y_ctr-dy/2], txt, fill=fill, font=font)
        
    def label_sig(self, r,c, txt, fill='black', k_size=0.15):
        font, _ = ft.adjust_font_size(self.chan_wid*k_size)
        dx, dy = font.getsize(txt)
        if r//1 == r:   # wire in y direction
            x_ctr = self.wire_pos[(r,c)][0]
            if r == 0:
                y_ctr = self.wire_pos[(r,c)][1]
                y = y_ctr-dy
            else:
                y_ctr = self.wire_pos[(r,c)][3]
                y = y_ctr
            x = x_ctr-dx/2
        else:
            y_ctr = self.wire_pos[(r,c)][1]
            if c == 0:
                x_ctr = self.wire_pos[(r,c)][0]
                x = x_ctr-dx
            else:
                x_ctr = self.wire_pos[(r,c)][2]
                x = x_ctr
            y = y_ctr-dy/2
        self.draw.text([x, y], txt, fill=fill, font=font)



    def save(self):
        self.img.save(self.img_out, "PNG")
