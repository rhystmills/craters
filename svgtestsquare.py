import svgwrite
import math
import random

dwg = svgwrite.Drawing('test.svg', size=(500, 500), profile='tiny')
for i in range(0,30):
    for j in range (0,30):
        dwg.add(dwg.rect((10*i,10*j), (10, 10), transform="rotate({} {} {})".format((random.random()-0.5)*i*j/5,10*i,10*j), fill="none",stroke_width=0.5,stroke='black'))
dwg.saveas("squaretest3_4.svg")



# def fractalTree(startCoords, angle, magnitude, remainingSteps):
#     dwg = svgwrite.Drawing('test.svg', size=(500, 500), profile='tiny')
#     endCoords = (magnitude * math.sin(angle),magnitude * math.cos(angle))
#     dwg.add(dwg.line(startCoords, endCoords,stroke_width=0.5,stroke='black',stroke_opacity=1.0))
#
#     newCoords = (magnitude/2 * math.sin(angle),magnitude/2 * math.cos(angle))
#     newAngle = angle + 0.1
#     newMagnitude = magnitude * 0.8
#     newSteps = remainingSteps - 1
#
#     if remainingSteps > 0:
#         fractalTree(newCoords, newAngle, newMagnitude, newSteps)
