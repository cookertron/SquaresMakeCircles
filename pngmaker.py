import sys, time
from random import randint, uniform
import pygame
from pygame.locals import *
from pygame import Rect as R
from pygame import Vector2 as V

# Créez une classe carrée afin que nous puissions avoir plusieurs carrés qui s'affichent en même temps.
class _square:
    def __init__(self, radius): # Chaque objet carré a son propre rayon.
        # L'angle de départ est aléatoire. Cela sépare les carrés afin qu'ils ne soient pas agglutinés ensemble.
        self.start_angle = randint(0, 360)
        self.radius = radius # Enregistrez la valeur du rayon.
        # Rotationnez l'image du carré pour qu'elle corresponde à l'angle à partir duquel le cercle commence à être tracé.
        self.square_image = pygame.transform.rotate(SQUARE_IMAGE, self.start_angle)

    def update(self, angle_offset): # Dessinez, déplacez et faites pivoter le carré.
        #Parce que nous avons fait pivoter l'image carrée pour qu'elle corresponde au point de départ du cercle,
        # et que nous avons créé une copie, nous n'avons besoin de faire pivoter que celle-ci.
        # Si nous faisions pivoter l'image tournée à chaque fois, l'image serait déformée.
        rotated_square_image = pygame.transform.rotate(self.square_image, 360 - angle_offset)
        
        # image_offset est le point 2D au centre du nouveau carré pivoté. Il est stocké sous
        # forme de vecteur pygame pour permettre une arithmétique vectorielle.
        image_offset = V(rotated_square_image.get_rect().center)

        # Vector(1, 0) a un angle de 0 degrés, Vector(0, 1) a un angle de 45 degrés.
        # Ici, nous faisons pivoter le vecteur (1, 0) vers l'angle choisi et le multiplions par le rayon pour calculer
        # la position du carré à partir du centre de l'image.
        # Vous pouvez obtenir le même effet en utilisant cos / sin comme suit:
        # x = centerx + math.cos(r) * radius
        # y = centery + math.sin(r) * radius
        pos = CENTER + V(1, 0).rotate(self.start_angle + angle_offset) * self.radius

        # Dessinez le carré pivoté sur l'image en le plaçant à POS, moins les valeurs du centre,
        # de façon à ce que le carré soit dessiné centré sur POS.
        PDS.blit(rotated_square_image, pos - image_offset)

# Initialiser pygame
pygame.init()

# Résolution de l'image
PDR = R(0, 0, 1080, 1080)

# Mettez le mode d'affichage, mais gardez l'affichage caché. Nous n'avons pas besoin de voir ce qui se passe.
PDS = pygame.display.set_mode(PDR.size, HIDDEN)

# PDS est notre toile, alors peignons-la en blanc.
PDS.fill((255, 255, 255))

# Les vecteurs (V) sont une façon facile de gérer les points dans un espace 2D dans pygame.
# CENTRE est un point au centre de notre image.
CENTER = V(PDR.center)

# Chargez l'image à partir du stockage sur disque
SQUARE_IMAGE = pygame.image.load("rect870.png").convert_alpha()

# Définissez le rayon de départ sur 800 pour remplir l'image.
radius = 800
squares = [] # Créez une liste vide pour stocker les carrés.
while radius > 200: # Diminuer le rayon à chaque tour jusqu'à ce qu'il soit inférieur à 200.
    squares.append(_square(radius)) # Créez un nouvel objet carré pour chaque rayon.
    radius -= randint(25, 125) # Réduisez le rayon d'une quantité aléatoire à chaque tour.

# Faire un cycle à travers les objets carrés, en les dessinant, en mettant à jour leur position et en les faisant tourner.

for angle in range(360): # Chaque carré doit tourner 360 degrés pour compléter le parcours circulaire.
    for square in squares:
        square.update(angle)

# Sauvegardez l'image sur le disque dur en utilisant l'heure comme nom de fichier.
pygame.image.save(PDS, "{}.png".format(time.perf_counter()))