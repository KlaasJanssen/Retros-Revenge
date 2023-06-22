import pygame
import os

def import_folder(path):
    surfaces = []
    for file in os.listdir(path):
        surf = pygame.image.load(path + "/" + file).convert_alpha()
        surfaces.append(surf)

    return surfaces
