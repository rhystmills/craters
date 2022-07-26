import svgwrite
import math

dwg = svgwrite.Drawing('test.svg', size=(500, 500), profile='tiny')

def fractalTree(startCoords, angle, magnitude, remainingSteps):
    print(startCoords)
    print(angle)
    print(magnitude)
    print(remainingSteps)

    endCoords = (startCoords[0]+magnitude * math.sin(angle),startCoords[1]+magnitude * math.cos(angle))
    hexcode = '#' + format(15-remainingSteps, 'x') + format(15-remainingSteps, 'x') + format(15-remainingSteps, 'x')
    dwg.add(dwg.line(startCoords, endCoords,stroke_width=remainingSteps*0.5,stroke=hexcode,stroke_opacity=1.0))

    # newCoords = (magnitude * math.sin(angle)/2,magnitude * math.cos(angle)/2)
    newCoords = (startCoords[0] + magnitude * 1 * math.sin(angle),startCoords[1] + magnitude * 1 * math.cos(angle))
    newAngle = angle + 0.5
    newMagnitude = magnitude * 0.8
    newSteps = remainingSteps - 1

    #Alternate branch
    altMagnitude = magnitude * 0.8
    altAngle = angle - 0.5

    if remainingSteps > 0:
        fractalTree(newCoords, newAngle, newMagnitude, newSteps)
        fractalTree(endCoords, altAngle, altMagnitude, newSteps)

fractalTree((250.00,250.00),0,100,12)

dwg.saveas("fractalTest3_3.svg")
