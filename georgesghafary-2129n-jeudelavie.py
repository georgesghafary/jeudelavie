# Le but de ce projet est de programmer le jeu de la vie qui est un automate cellulaire utiliser pour representer l'evolution d'une population
# initial avec des regles qui representent l'effet de la sur-population et de la sous-population
# les regles de ce jeu sont plutot simple est sont classees comme si-dessous:
# - si une cellule est vivante, et a 2 ou 3 cellules voisines vivanets, elle reste vivante. sinon elle meurt
# - si une cellule est morte et a exactement 3 cellules voisines vivantes, elle devient vivante. sinon elle reste morte
# toutes parties du programme si-dessous sont expliquees par commentaires

import math
import random
import pygame
import sys

NOIR = (0, 0, 0)
GRIS = (200, 200, 200)
BLANC = (255, 255, 255)
HAUTEUR_FRAME = 600
LARGEUR_FRAME = 600


class Cellule:
    def __init__(self, x, y, hauteur, largeur, etat):
        self.x = x
        self.y = y
        self.hauteur = hauteur
        self.largeur = largeur
        self.etat = etat
        self.voisin_gauche = True
        self.voisin_droite = True
        self.voisin_dessus = True
        self.voisin_dessous = True
        # somme voisins est la somme des voisins vivant de cette cellule
        self.somme_voisins = 0

    # afficher les cellules comme des rectangles et les colorier en noir si elles sont vivantes et en blanc si elles sont mortes
    def afficherCellule(self, surface):
        couleur = BLANC
        if(self.etat == 1):
            couleur = NOIR
        # enelver 2px de la largeur et la hauteur de chaque rectangle pour avoir l'effet d'une grille avec des bordures
        rect = pygame.Rect(self.x, self.y, self.largeur - 2, self.hauteur - 2)
        pygame.draw.rect(surface, couleur, rect)

    # initialiser les voisins pour savoir quelle voisins, d'apres sa position dans la grille, existes pour cette cellule
    # par example, si la cellule se trouve sur le bord gauche de la grille, elle n'aura pas de voisins a gauche etc...
    def initVoisins(self, i, j, colonnes, lignes):
        # verification si voisin dessus existe
        if i == 0:
            self.voisin_dessus = False
        # verification si voisin dessous existe
        if i == lignes - 1:
            self.voisin_dessous = False
        # verification si voisin gauche existe
        if j == 0:
            self.voisin_gauche = False
        # verification si voisin droite existe
        if j == colonnes - 1:
            self.voisin_droite = False

    # vu que l'etat des cellules changes d'apres l'etat de ses voisin, la plus simple technique qu'on peut utiliser est d'utiliser un entier
    # pour determiner l'etat de chaque cellule ( 0 si morte, 1 si vivante) et puis calculer la somme des voisins vivants en utilisant leurs etats
    # il faut bien sur, verifier si chacun des voisin existe avant d'ajouter la valuer de son etat a la somme des voisin de notre cellule
    def miseAJourSomme(self, grille, i, j):
        # verification voisin gauche meme ligne
        if self.voisin_gauche:
            self.somme_voisins += grille[i][j - 1].etat
        # verification voisin droite meme ligne
        if self.voisin_droite:
            self.somme_voisins += grille[i][j + 1].etat
        # verification ligne au dessus
        if self.voisin_dessus:
            # verification voisin dessus meme colonne
            self.somme_voisins += grille[i - 1][j].etat
            # verification voisin dessus colonne gauche
            if self.voisin_gauche:
                self.somme_voisins += grille[i - 1][j - 1].etat
            # verification voisin dessus colonne droite
            if self.voisin_droite:
                self.somme_voisins += grille[i - 1][j + 1].etat
        # verification voisin dessous meme colonne
        if self.voisin_dessous:
            self.somme_voisins += grille[i + 1][j].etat
            # verification voisin dessous colonne gauche
            if self.voisin_gauche:
                self.somme_voisins += grille[i + 1][j - 1].etat
            # verification voisin dessous colonne droite
            if self.voisin_droite:
                self.somme_voisins += grille[i + 1][j + 1].etat


def main():
    # initialization pygame
    pygame.init()
    FRAME = pygame.display.set_mode((LARGEUR_FRAME, HAUTEUR_FRAME))
    pygame.display.set_caption('Je de la vie')
    FRAME.fill(GRIS)

    grille_a_afficher = []
    grille_a_utiliser = []
    colonnes = 40
    lignes = 40
    hauteur_bloc = HAUTEUR_FRAME // lignes
    largeur_bloc = LARGEUR_FRAME // colonnes
    # la variable fps sera utiliser pour controller la vitesse de changement de l'etat de notre jeu pour qu'on puisse avoir une meilleur visualisation
    fps = 0

    # Les deux boucles suivants sont responsable de la creation de notre grille
    grille_a_afficher = [[] for i in range(lignes)]
    # C'est l'etat initial aleatoire
    for i in range(lignes):
        grille_a_afficher[i] = [Cellule(i * largeur_bloc, j * hauteur_bloc, hauteur_bloc, largeur_bloc,
                                        0) for j in range(colonnes)]
    # etat aleatoire - commenter l'etat actif et decommenter l'etat si dessous pour le visualiser
    aleatoire(grille_a_afficher)

    # etat blinker - commenter l'etat actif et decommenter l'etat si dessous pour le visualiser
    # blinker(grille_a_afficher)

    # etat beacon - commenter l'etat actif et decommenter l'etat si dessous pour le visualiser
    # beacon(grille_a_afficher)

    # etat glider - commenter l'etat actif et decommenter l'etat si dessous pour le visualiser
    # glider(grille_a_afficher)

    # etat gasper gliding gun - commenter l'etat actif et decommenter l'etat si dessous pour le visualiser
    # gasperGlidingGun(grille_a_afficher)

    # boucle infini pour que notre jeu s'execute continuellement
    while True:
        # chaque 300 iterations de boucle, on met a jour une nouvel generation pour avoir une visualization plus claire
        if fps >= 300:
            # iteration sur notre grille pour l'afficher, initializer les voisins de chaque cellule et mettre a jour la somme de ses voisins
            for i in range(len(grille_a_afficher)):
                for j in range(len(grille_a_afficher[i])):
                    grille_a_afficher[i][j].afficherCellule(FRAME)
                    grille_a_afficher[i][j].initVoisins(i, j, colonnes, lignes)
                    grille_a_afficher[i][j].miseAJourSomme(
                        grille_a_afficher, i, j)

            # la raison pour l'utilisation de deux grilles identiques est l'utilisation d'une pour mettre a jour la nouvelle sans affecter
            # l'etat actuelle de notre grille. Dans ce cas, on met a jour la grille a utiliser en utilisant l'etat de la grille a afficher
            # et apres avoir fini nos iterations, nous mettons a jour la grille a afficher en utilisant la nouvelle grille
            grille_a_utiliser = grille_a_afficher
            for i in range(len(grille_a_afficher)):
                for j in range(len(grille_a_afficher[i])):
                    if grille_a_afficher[i][j].etat == 0 and grille_a_afficher[i][j].somme_voisins == 3:
                        grille_a_utiliser[i][j].etat = 1
                        grille_a_utiliser[i][j].somme_voisins = 0
                    elif grille_a_afficher[i][j].etat == 1 and (grille_a_afficher[i][j].somme_voisins > 3 or grille_a_afficher[i][j].somme_voisins < 2):
                        grille_a_utiliser[i][j].etat = 0
                        grille_a_utiliser[i][j].somme_voisins = 0
                    else:
                        grille_a_utiliser[i][j].etat = grille_a_afficher[i][j].etat
                        grille_a_utiliser[i][j].somme_voisins = 0
            grille_a_afficher = grille_a_utiliser

            # nous reinitialisons la variable fps pour recommencer son incrementation
            fps = 0
        fps += 1

        # commandes specifique a pygame pour terminer le jeu en quittant la fenetre de jeu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def aleatoire(grille):
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            grille[i][j].etat = math.floor(random.randrange(0, 2))


def blinker(grille):
    grille[14][15].etat = 1
    grille[15][15].etat = 1
    grille[16][15].etat = 1


def beacon(grille):
    grille[8][10].etat = 1
    grille[9][10].etat = 1
    grille[8][11].etat = 1
    grille[9][11].etat = 1
    grille[10][12].etat = 1
    grille[11][12].etat = 1
    grille[10][13].etat = 1
    grille[11][13].etat = 1


def glider(grille):
    grille[5][5].etat = 1
    grille[6][6].etat = 1
    grille[7][6].etat = 1
    grille[7][5].etat = 1
    grille[7][4].etat = 1


def gasperGlidingGun(grille):
    grille[5][19].etat = 1
    grille[5][20].etat = 1
    grille[6][19].etat = 1
    grille[6][20].etat = 1
    grille[15][19].etat = 1
    grille[15][20].etat = 1
    grille[15][21].etat = 1
    grille[16][18].etat = 1
    grille[16][22].etat = 1
    grille[17][17].etat = 1
    grille[17][23].etat = 1
    grille[18][17].etat = 1
    grille[18][23].etat = 1
    grille[19][20].etat = 1
    grille[20][18].etat = 1
    grille[20][22].etat = 1
    grille[21][19].etat = 1
    grille[21][20].etat = 1
    grille[21][21].etat = 1
    grille[22][20].etat = 1
    grille[25][17].etat = 1
    grille[25][18].etat = 1
    grille[25][19].etat = 1
    grille[26][17].etat = 1
    grille[26][18].etat = 1
    grille[26][19].etat = 1
    grille[27][16].etat = 1
    grille[27][20].etat = 1
    grille[28][15].etat = 1
    grille[28][26].etat = 1
    grille[28][20].etat = 1
    grille[28][21].etat = 1
    grille[38][17].etat = 1
    grille[38][18].etat = 1
    grille[39][17].etat = 1
    grille[39][18].etat = 1


main()
