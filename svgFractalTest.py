import svgwrite
import math

dwg = svgwrite.Drawing('test.svg', size=(500, 500), profile='tiny')

def fractalTree(startCoords, angle, magnitude, remainingSteps):
    print(startCoords)
    print(angle)
    print(magnitude)
    print(remainingSteps)

    endCoords = (startCoords[0]+magnitude * math.sin(angle),startCoords[1]+magnitude * math.cos(angle))
    dwg.add(dwg.line(startCoords, endCoords,stroke_width=0.5,stroke='black',stroke_opacity=1.0))

    # newCoords = (magnitude * math.sin(angle)/2,magnitude * math.cos(angle)/2)
    newCoords = (startCoords[0] + magnitude * 0.5 * math.sin(angle),startCoords[1] + magnitude * 0.5 * math.cos(angle))
    newAngle = angle + 0.1
    newMagnitude = magnitude * 0.9
    newSteps = remainingSteps - 1

    #Alternate branch

    if remainingSteps > 0:
        fractalTree(newCoords, newAngle, newMagnitude, newSteps)

fractalTree((250.00,250.00),0,100,500)

dwg.saveas("fractalTest2_2.svg")
