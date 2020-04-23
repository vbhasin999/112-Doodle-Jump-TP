import math

def getDistance(x1, y1, x2, y2):
    a = (x2-x1)**2
    b = (y2-y1)**2
    d = math.sqrt(a+b)
    return d

platWidth = 100
def getClosestPlatDist(c, LoP):
    closestPlat = 10000
    smallestDistToPlat = 10000
    charX = c[0] 
    charY = c[1]
    for plat in LoP:
        platX = plat[0] + platWidth/2  #using midpoint of platform
        platY = plat[1]
        dist = getDistance(charX, charY, plat[0], plat[1])

        if platY <= charY:
            continue
        
        elif dist < smallestDistToPlat:
            smallestDistToPlat = dist
            closestPlat = plat
    return closestPlat

'''
getClosestPlatDist((0, 1),[[195, 351.0], [171, 158.0], [244, 539.0], [255, 224.0], 
                        [358, 642.0], [142, 411.0], [305, 789.0]])
'''

def depthFirstSearch(charPos, getClosestPlat):
    pass
