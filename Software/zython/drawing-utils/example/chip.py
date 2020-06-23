import draw.chip as chip
import PIL.Image as I
import PIL.ImageDraw as ID
import numpy as np


def example1():
    U = 120
    c = chip.element.chip("draw/example/chip1.png", 3*U, 5*U, 3, 4, U/20)
    c.add_track(1/4, 1, True, 0, width=U/20)
    c.add_track(2/4, 2, True, 0, width=U/20)
    c.add_track(3/4, 2, True, 1, width=U/20)
    c.add_track(1/4, 1, False, 0, width=U/20)
    c.add_track(2/4, 2, False, 0, width=U/20)
    c.add_track(3/4, 2, False, 1, width=U/20)
    
    c.label_clb(0,1,' MUL\n(0,1)')
    c.label_clb(1,2,' MUL\n(1,2)')
    c.label_clb(2,3,' MUL\n(2,3)')

    c.sig_flow(0.5,0, width=U/5)
    c.connect_pin(0.5,0,0,1, width=U/10)

    c.sig_flow(1.5,0, width=U/5)
    c.sig_flow(1.25,2, width=U/5)
    c.connect(1.5,0,1.25,2, width=U/10)
    c.connect_pin(1.25,2,1,2, width=U/10)

    c.sig_flow(1.75,0, width=U/5)
    c.sig_flow(1.75,1, width=U/5)
    c.sig_flow(1.75,3, width=U/5)
    c.connect(1.75,0,1.75,1, width=U/10)
    c.connect(1.75,1,1.75,3, width=U/10)
    c.connect_pin(1.75,3,2,3, width=U/10)

    c.label_sig(0.5,0,'A[0]',fill='red')
    c.label_sig(1.5,0,'A[1]',fill='red')
    c.label_sig(1.75,0,'A[2]',fill='red')
    
    c.sig_flow(0,0.75,fill='blue', width=U/5)
    c.connect_pin(0,0.75,0,1,fill='blue', width=U/10)
    c.sig_flow(0,1.5,fill='blue', width=U/5)
    c.connect_pin(0,1.5,1,2,fill='blue', width=U/10)
    c.sig_flow(0,2.5,fill='blue', width=U/5)
    c.sig_flow(2,2.5,fill='blue', width=U/5)
    c.connect(0,2.5,2,2.5,fill='blue', width=U/10)
    c.connect_pin(2,2.5,2,3,fill='blue', width=U/10)

    c.label_sig(0,0.75,'k',fill='blue')
    c.label_sig(0,1.5,'k',fill='blue')
    c.label_sig(0,2.5,'k',fill='blue')

    c.save()


def example2():
    U = 120
    c = chip.element.chip("draw/example/chip2.png", 3*U, 2*U, 3, 6, U/20)
    c.add_track(2/3,1,True,0, width=U/20)
    c.add_track(1/3,4,True,1, width=U/20)
    c.add_track(1/3,1,False,0, width=U/20)
    c.add_track(2/3,4,False,2, width=U/20)

    c.label_clb(0,4,'Sink')
    c.label_sig(1,1/3,'sig',k_size=0.3)
    c.sig_flow(1,1/3, width=U/5)
    c.sig_flow(2/3,1, width=U/5)
    c.sig_flow(2/3,2, width=U/5)
    c.sig_flow(2/3,3, width=U/5)
    c.sig_flow(2/3,4, width=U/5)
    c.sig_flow(1/3,1,fill='green', width=U/5)
    c.sig_flow(0,13/3,fill='red', width=U/5)
    c.sig_flow(4/3,1,fill='blue', width=U/5)
    c.sig_flow(0,14/3,fill='blue', width=U/5)

    c.connect(4/3,1,0,14/3,fill='blue', width=U/10)
    c.connect_pin(0,14/3,0,4,fill='blue', width=U/10)
    c.connect(2/3,1,2/3,2, width=U/10)
    c.connect(2/3,2,2/3,3, width=U/10)
    c.connect(2/3,3,2/3,4, width=U/10)
    c.connect(2/3,1,1,1/3, width=U/10)
    c.connect(1/3,1,1,1/3,fill='green', width=U/10)
    c.connect(2/3,4,0,13/3, width=U/10)
    c.connect(1/3,1,0,13/3,fill='green', width=U/10)
    c.connect_pin(0,13/3,0,4, width=U/10)

    c.save()


if __name__ == '__main__':
    example1()
    example2()
