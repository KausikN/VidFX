'''
TerrainGen Image Effects Library
'''

# Imports
import cv2
import noise
import numpy as np

# Main Functions
# Util Functions
def GeneratePerlinNoise_2D(WorldSize, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0):
    world = np.zeros((WorldSize[0], WorldSize[1]))
    for i in (range(WorldSize[0])):
        for j in range(WorldSize[1]):
            world[i][j] = noise.pnoise2(i/scale, j/scale,
            octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=repeatx, repeaty=repeaty, base=base)
    
    return world

def ColoriseTerrain2D_ValueThresholdColorMapped(terrain, thresholdColors=[[]], defaultColor=[65, 105, 225]):
    color_world = np.ones((terrain.shape[0], terrain.shape[1], 3), np.uint8) * defaultColor
    for i in (range(terrain.shape[0])):
        for j in range(terrain.shape[1]):
            for th in thresholdColors:
                if terrain[i, j] >= th[0] and terrain[i, j] < th[1]:
                    color_world[i, j] = th[2]
    return color_world

def ColoriseTerrain2D_ArchipelagoSimple(terrain, thresholds=[0.25, 0.6, 0.85, 0.95]):
    blue = [65, 105, 225]
    beach = [238, 214, 175]
    green = [34, 139, 34]
    mountain = [139, 137, 137]
    snow = [255, 250, 250]
    color_world = ColoriseTerrain2D_ValueThresholdColorMapped(terrain,
        thresholdColors=[
            [thresholds[0], thresholds[1], beach],
            [thresholds[1], thresholds[2], green],
            [thresholds[2], thresholds[3], mountain],
            [thresholds[3], 1.0, snow]
        ], 
        defaultColor=blue)
    return color_world

# Effect Functions
def ImageEffect_TerrainGen(I, random_seed=False, seed=0, thresholds=[0.25, 0.4, 0.85, 0.95], scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024):
    if random_seed:
        seed = np.random.randint(0, 1000)
    # Generate and normalise perlin noise
    I_Noise = GeneratePerlinNoise_2D(I.shape[:2], scale=scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=repeatx, repeaty=repeaty, base=seed)
    I_Noise = (I_Noise - np.min(I_Noise)) / (np.max(I_Noise) - np.min(I_Noise))
    # Mask with input image binarised
    I_mask = np.mean(I, axis=2) > 127
    I_masked = I_Noise * I_mask
    # Colorise
    I_colourised = ColoriseTerrain2D_ArchipelagoSimple(I_masked, thresholds=thresholds)
    output = I_colourised

    return output

def ImageEffect_Archipelago(I, thresholds=[0.25, 0.4, 0.85, 0.95]):
    # GreyScale Input image
    I_grey = np.mean(I, axis=2)
    I_greynorm = (I_grey - np.min(I_grey)) / (np.max(I_grey) - np.min(I_grey))
    # Colorise
    I_colourised = ColoriseTerrain2D_ArchipelagoSimple(I_greynorm, thresholds=thresholds)
    output = I_colourised

    return output