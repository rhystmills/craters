import svgwrite
import math
import random

dwg = svgwrite.Drawing('test.svg', size=(500, 500), profile='tiny')
for i in range(0,10):
    for j in range (0,30):
        x_size_nudge = (random.random() - 0.5) * i * j / 8
        y_size_nudge = (random.random() - 0.5) * i * j / 8
        x_nudge = (random.random() - 0.5) * j * j / 100
        y_nudge = (random.random() - 0.5) * j * j / 100
        dwg.add(dwg.rect((10*i+y_nudge,10*j+y_nudge), (10, 10), transform="rotate({} {} {})".format((random.random()-0.5)*j*j/10,10*i,10*j), fill="none",stroke_width=0.5,stroke='black'))
dwg.saveas("squaretest4_3.svg")