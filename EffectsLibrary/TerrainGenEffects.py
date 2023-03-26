'''
TerrainGen Image Effects Library
'''

# Imports
from .EffectUtils import *

import noise

# Main Functions
# Util Functions
def GeneratePerlinNoise_2D(WorldSize, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0, **params):
    world = np.zeros((WorldSize[0], WorldSize[1]))
    for i in (range(WorldSize[0])):
        for j in range(WorldSize[1]):
            world[i][j] = noise.pnoise2(i/scale, j/scale,
            octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=repeatx, repeaty=repeaty, base=base)
    
    return world

def ColoriseTerrain2D_ValueThresholdColorMapped(terrain, thresholdColors=[[]], defaultColor=[65/255.0, 105/255.0, 225/255.0], **params):
    color_world = np.ones((terrain.shape[0], terrain.shape[1], 3), float) * defaultColor
    for i in (range(terrain.shape[0])):
        for j in range(terrain.shape[1]):
            for th in thresholdColors:
                if terrain[i, j] >= th[0] and terrain[i, j] < th[1]:
                    color_world[i, j] = th[2]
    return color_world

def ColoriseTerrain2D_ArchipelagoSimple(terrain, thresholds=[0.25, 0.6, 0.85, 0.95], **params):
    blue = [65/255.0, 105/255.0, 225/255.0]
    beach = [238/255.0, 214/255.0, 175/255.0]
    green = [34/255.0, 139/255.0, 34/255.0]
    mountain = [139/255.0, 137/255.0, 137/255.0]
    snow = [255/255.0, 250/255.0, 250/255.0]
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
def ImageEffect_TerrainGen(I, random_seed=False, seed=0, thresholds=[0.25, 0.4, 0.85, 0.95], scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, **params):
    if random_seed:
        seed = np.random.randint(0, 1000)
    # Generate and normalise perlin noise
    I_Noise = GeneratePerlinNoise_2D(I.shape[:2], scale=scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=repeatx, repeaty=repeaty, base=seed)
    I_Noise = (I_Noise - np.min(I_Noise)) / (np.max(I_Noise) - np.min(I_Noise))
    # Mask with input image binarised
    I_mask = np.mean(I[:, :, :3], axis=2) > 0.5
    I_masked = I_Noise * I_mask
    # Colorise
    I_colourised = ColoriseTerrain2D_ArchipelagoSimple(I_masked, thresholds=thresholds)

    I_effect = np.clip(I_colourised, 0.0, 1.0, dtype=float)
    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

def ImageEffect_Archipelago(I, thresholds=[0.25, 0.4, 0.85, 0.95], **params):
    # GreyScale Input image
    I_grey = np.mean(I[:, :, :3], axis=2)
    I_greynorm = (I_grey - np.min(I_grey)) / (np.max(I_grey) - np.min(I_grey))
    # Colorise
    I_colourised = ColoriseTerrain2D_ArchipelagoSimple(I_greynorm, thresholds=thresholds)
    
    I_effect = np.clip(I_colourised, 0.0, 1.0, dtype=float)
    I_effect = np.dstack((I_effect[:, :, 0], I_effect[:, :, 1], I_effect[:, :, 2], I[:, :, 3]))
    return I_effect

# Main Vars
EFFECTFUNCS_TERRAINGEN = {
    "TerrainGen": {
        "name": "TerrainGen",
        "code": "TerrainGen(random_seed=False, seed=0, thresholds=[0.25, 0.4, 0.85, 0.95], scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024)",
        "func": ImageEffect_TerrainGen,
        "params": {
            "random_seed": False,
            "seed": 0,
            "thresholds": [0.25, 0.4, 0.85, 0.95],
            "scale": 100.0,
            "octaves": 6,
            "persistence": 0.5,
            "lacunarity": 2.0,
            "repeatx": 1024,
            "repeaty": 1024
        }
    },
    "Archipelago": {
        "name": "Archipelago",
        "code": "Archipelago(thresholds=[0.25, 0.4, 0.85, 0.95])",
        "func": ImageEffect_Archipelago,
        "params": {
            "thresholds": [0.25, 0.4, 0.85, 0.95]
        }
    },
}