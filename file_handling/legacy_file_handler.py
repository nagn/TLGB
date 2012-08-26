#!/usr/bin/env python
from __future__ import division, print_function
import re
import Image, PngImagePlugin
import os, sys
"""
What could possibly go wrong?
"""
class NoData(Exception):
    pass
class NoEntities(Exception):
    pass
class NoMask(Exception):
    pass
GANG_GARRISON_LEVEL_DATA = "Gang Garrison 2 Level Data"
START_WALLMASK_TAG = "{WALKMASK}"
END_WALLMASK_TAG = "{END WALKMASK}"
START_ENTITY_TAG = "{ENTITIES}"
END_ENTITY_TAG = "{END ENTITIES}"
def decompressEntityData(filename):
    mapPNG = Image.open(str(filename))
    try :
        levelData = str(mapPNG.info['Gang Garrison 2 Level Data'])
    except KeyError:
        raise NoData("No Level Data Found in " + str(filename))
    del mapPNG
    if re.search(START_ENTITY_TAG+'\n(.*)\n'+END_ENTITY_TAG, levelData, re.DOTALL):
        #We include the newline tags to make sure that we get rid of them
        rawEntityData = re.search(START_ENTITY_TAG+'\n(.*)\n'+END_ENTITY_TAG, levelData, re.DOTALL).group(1)

        #The old entity format only specifies an entity every third line (the lack of real delimiters doesn't really help either)
        values = rawEntityData.splitlines(False)
        #return a list containing all the entities
        return(decodeEntityData(values))
    else:
        raise NoEntities("ENTITY DATA NOT FOUND IN " + str(filename))

def decodeEntityData(entityList):
    entities = []
    for i in range(0, len(entityList), 3):
        #Create a list of the corresponding arguments, and append it to the list
        entities.append([entityList[i],(int(entityList[i+1]),int(entityList[i+2]))])
    return (entities)
def getWallmaskData(filename):
    mapPNG = Image.open(str(filename))
    levelData = str(mapPNG.info['Gang Garrison 2 Level Data'])
    rawWallmaskData = re.search(START_WALLMASK_TAG+'\n(.*)\n'+END_WALLMASK_TAG, levelData, re.DOTALL).group(1)
    del mapPNG
    return(rawWallmaskData)
    
def decompressWallmaskData(filename, outputWallmaskName, transparentOutput):
    mapPNG = Image.open(str(filename))
    try :
        levelData = mapPNG.info['Gang Garrison 2 Level Data']
    except KeyError:
        raise NoData("No Level Data Found in " + str(filename))
    del mapPNG
    if re.search(START_WALLMASK_TAG+'\n(.*)\n'+END_WALLMASK_TAG, levelData, re.DOTALL):
        rawWallmaskData = re.search(START_WALLMASK_TAG+'\n(.*)\n'+END_WALLMASK_TAG, levelData, re.DOTALL).group(1)
        values = rawWallmaskData.splitlines(False)
        mapWidth = int(values[0])
        mapHeight = int(values[1])
        wallmaskData = values[2]
        

        
        if transparentOutput != True:
            img = Image.new('L', (mapWidth, mapHeight))
        else:
            img = Image.new('RGBA', (mapWidth, mapHeight))
        
        imagePixelData = []
        
        for char in wallmaskData:
            imagePixelData.extend(decodeChar(char, transparentOutput))
            decodeChar(char, transparentOutput)
        if len(imagePixelData) > mapWidth * mapHeight:
            #shave off the excess pixel data that are left over from a 6 bit chunk
            imagePixelData = imagePixelData[:-(len(imagePixelData) - mapWidth * mapHeight)]
        img.putdata(imagePixelData)
        #del(imagePixelData)
        if outputWallmaskName != None:
            if os.path.exists(outputWallmaskName):
                try:
                    os.remove(outputWallmaskName)
                except:
                    print ("Exception: ",str(sys.exc_info()))
            
            img.save(outputWallmaskName, 'png')
        return(img)
    else:
        raise NoMask("WALLMASK DATA NOT FOUND IN " + str(filename))
def memoize(f):
    cache= {}
    def memf(*x):
        if x not in cache:
            cache[x] = f(*x)
        return cache[x]
    return memf
@memoize
def decodeChar(char, transparentOutput):
    sixLeastSignificantBits = (ord(char) - 32) & 0b111111
    if transparentOutput == True:
        blackTuple = (0, 0, 0, 255)
        whiteTuple = (255, 255, 255 , 0)
    else:
        blackTuple = (0)
        whiteTuple = (255)
    result = []
    for i in range(0,6):
        if (sixLeastSignificantBits & (1<<(5-i))):
            #if it is solid
            result.append(blackTuple)
        else:
            result.append(whiteTuple)
    return(result)
def compressEntityData(entityList):
    #This function takes a list of entities (and their corresponding list of arguments) and converts them back into a string
    entityString = ""
    for entity in entityList:
        entityString += str(entity[0]) + chr(10) + str(entity[1][0]) + chr(10) + str(entity[1][1]) + chr(10)
    with open("Input.txt", "w") as text_file:
        text_file.write(entityString)    
    return(START_ENTITY_TAG + chr(10) + entityString + END_ENTITY_TAG)
def compressWallmaskData(wallmaskFilename):
    #this function takes a black and white PNG wallmask and compiles the corresponding character sequence from it
    wallmask = Image.open(str(wallmaskFilename))
    #convert to a black and white image
    bw = wallmask.convert('L')
    width, height = bw.size
    pixelList = list(bw.getdata())
    wallmaskString = ""
    for iteration in range(0, len(pixelList), 6):
        #take every six pixels, and and conver it to a char
        try:
            wallmaskString += convertPixels(pixelList[iteration:iteration+6])
        except IndexError:
            """This never gets executed because apparently python implicitly doesn't
            create an index in a slice for something it doesn't have/throw an error.
            However, be careful as directly accessing the index will.
            """
            #We over stepped at the end, so we need to fill in the rest with zeros
            print("hi")
            numRemainingPixels = len(pixelList) - iteration
            remainingPixels = pixelList[iteration:numRemainingPixels]
            numPixelsToFill = 6 - numRemainingPixels
            for pixelsLeft in range(numPixelsToFill):
                remainingPixels.append(0x00)
            wallmaskString += convertPixels(remainingPixels)
    return(START_WALLMASK_TAG + chr(10) + str(width) + chr(10) + str(height) + chr(10) + wallmaskString + chr(10) + END_WALLMASK_TAG)
def convertPixels(pixelSlice):
    char = 0x00
    #White is 255, and black is 0. We have to flip the pixels in order to make it so that solids are true, and transparents are false
    for i, pixel in enumerate(pixelSlice):
        char |= ((~pixel) & (0x01 << 5-i))
    return(chr(char + 32))

def embedLevelData(backgroundImage, entityList, wallmaskImage):
    mapPNG = Image.open(str(backgroundImage))
    mapPNG.info[GANG_GARRISON_LEVEL_DATA] = compressEntityData(entityList) + compressWallmaskData(wallmaskImage)
    pngsave(mapPNG, backgroundImage)
    
def extractLevelData(mapPNG, wallmaskOutput = None, transparentOutput = False):
    return(decompressEntityData(mapPNG), decompressWallmaskData(mapPNG, wallmaskOutput, transparentOutput))
def pngsave(im, file):
    # these can be automatically added to Image.info dict                                                                              
    # they are not user-added metadata
    reserved = ('interlace', 'gamma', 'dpi', 'transparency', 'aspect')

    # undocumented class
    meta = PngImagePlugin.PngInfo()

    # copy metadata into new object
    for k,v in im.info.iteritems():
        if k in reserved: continue
        meta.add_text(k, v, 0)
    # and save
    im.save(file, "PNG", pnginfo=meta)
