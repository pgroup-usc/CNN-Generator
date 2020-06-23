import draw.tree as tree
import PIL.Image as I
import PIL.ImageDraw as ID
import numpy as np

def graph1(unit):
    W = 10*unit
    H = 7*unit
    img = I.new("RGB", (W,H), "white")
    draw = ID.Draw(img)
    nodes = [[0.6*W, 0.15*H]]
    nodes+= [[0.55*W, 0.55*H]]
    nodes+= [[0.15*W, 0.8*H]]
    nodes+= [[0.85*W, 0.7*H]]
    idx = 0
    for n in nodes:
        tree.element.draw_node(draw, idx, n[0],n[1], unit)
        idx += 1 
    conns = [[(0,1), "1"]]
    conns+= [[(1,2), "3"]]
    conns+= [[(1,3), "100"]]
    conns+= [[(0,3), "2"]]
    conns+= [[(0,2), "101"]]
    for c in conns:
        tree.connect.connect_nodes(draw, c[0][0],c[0][1], unit, label=c[1])

    img.save("draw/example/graph1.png", "PNG")

def graph2(unit):
    W = 30*unit
    H = 23*unit
    img = I.new("RGB", (W,H), "white")
    draw = ID.Draw(img)
    nodes = [[(6*unit, unit), "W"]]
    nodes+= [[(10*unit, 5*unit), "Vp1"]]
    nodes+= [[(15*unit, 10*unit), "Vp2"]]
    nodes+= [[(20*unit, 13*unit), "Vp3"]]
    nodes+= [[(24*unit, 15*unit), "V"]]
    idx = 0
    for n in nodes:
        tree.element.draw_node(draw, idx, n[0][0],n[0][1], unit, label=n[1])
        idx += 1
    
    trees = [[(2*unit, 3*unit), ""]]
    trees+= [[(6*unit, 6*unit), ""]]
    trees+= [[(6*unit, 15*unit), ""]]
    trees+= [[(10*unit, 14.5*unit), ""]]
    trees+= [[(16*unit, 16*unit), ""]]
    trees+= [[(22*unit, 16.5*unit, ), ""]]
    trees+= [[(26.5*unit, 16.5*unit), ""]]
    for t in trees:
        tree.element.draw_subtree(draw, idx, t[0][0],t[0][1], unit, node_label=t[1])
        idx += 1
    
    conns = [[0,1]]
    conns+= [[1,2]]
    conns+= [[0,5]]
    conns+= [[1,6]]
    conns+= [[2,7]]
    conns+= [[2,8]]
    conns+= [[2,3, 3, "MAX"]]
    conns+= [[3,4]]
    conns+= [[3,9]]
    conns+= [[4,10]]
    conns+= [[4,11]]
    for c in conns:
        width=1
        label=""
        if len(c) == 4:
            width=c[2]
            label=c[3]
        tree.connect.connect_nodes(draw, c[0],c[1], unit, width=width, label=label)
    img.save("draw/example/graph2.png", "PNG")


if __name__ == "__main__":
    graph1(30)
    graph2(30)
