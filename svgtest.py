import svgwrite
import math

dwg = svgwrite.Drawing('test.svg', size=(500, 500), profile='tiny')
for i in range(1,25):
    for j in range(1,25):
        dwg.add(dwg.line((i*20,j*20),(250,250),stroke_width=0.5,stroke='black',stroke_opacity=1.0))
dwg.saveas("linetest1_2.svg")



def fractalTree(startCoords, angle, magnitude, remainingSteps):
    dwg = svgwrite.Drawing('test.svg', size=(500, 500), profile='tiny')
    endCoords = (magnitude * math.sin(angle),magnitude * math.cos(angle))
    dwg.add(dwg.line(startCoords, endCoords,stroke_width=0.5,stroke='black',stroke_opacity=1.0))

    newCoords = (magnitude/2 * math.sin(angle),magnitude/2 * math.cos(angle))
    newAngle = angle + 0.1
    newMagnitude = magnitude * 0.8
    newSteps = remainingSteps - 1

    if remainingSteps > 0:
        fractalTree(newCoords, newAngle, newMagnitude, newSteps)
