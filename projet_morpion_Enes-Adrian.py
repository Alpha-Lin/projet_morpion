# Enes Adrian
from sys import stdout, stdin
import os
import random
import keyboard
import time

tailleCase = 1
nbEnter = 0

class Player():
    def __init__(self):
        self.points = 0
        self.priorite = False

    def getPoints(self):
        return self.points
    
    def getPriorite(self):
        return self.priorite

    def incremantePoints(self):
        self.points += 1

    def changePriorite(self):
        self.priorite = not self.priorite

def creation_grille(taille):
    return [['.'] * taille for i in range(taille)]

def affichage(grille, tailleLigne, i1 = -1, i2 = -1):
    if (i1 > -1):
        tmp_sign = grille[i1][i2]
        grille[i1][i2] = 'N'           # Sélecteur
    for ligne in range(tailleLigne):
        for _ in range(tailleLigne):
            stdout.write('+-' + '-' * 2 * (tailleCase - 1))
        stdout.write('+\n')

        for _ in range(tailleCase // 2):  # Intervient pour le zoom
            for _ in range(tailleLigne):
                stdout.write("|" + " " * (tailleCase * 2 - 1))
            stdout.write("|\n")

        for symbole in grille[ligne]:
            stdout.write('|' + ' ' * (tailleCase - 1) + symbole + ' ' * (tailleCase - 1))
        
        for _ in range(tailleCase // 2): # Intervient pour le zoom
            stdout.write("|\n")
            for _ in range(tailleLigne):
                stdout.write("|" + " " * (tailleCase * 2 - 1))

        stdout.write("|\n")
    for _ in range(tailleLigne):
        stdout.write('+-' + '-' * 2 * (tailleCase - 1))
    stdout.write('+\n\n')

    if (i1 > -1): grille[i1][i2] = tmp_sign

def affichage2(grille, i1 = -1, i2 = -1):
    tailleLigne = len(grille[0])

    if (i1 > -1):
        tmp_sign = grille[i1][i2]
        grille[i1][i2] = 'N'

    stdout.write("  ")
    for i in range(tailleLigne): stdout.write(str(i))
    stdout.write("\n")
    for ligne in range(tailleLigne):
        stdout.write(str(ligne) + " ")
        for symbole in grille[ligne]: stdout.write(symbole)
        stdout.write("\n\n")

    if (i1 > -1): grille[i1][i2] = tmp_sign

def libre(emplacement_check, grille, taille):
    if not (-1 < emplacement_check[0] < taille) or not (-1 < emplacement_check[1] < taille) or grille[emplacement_check[0]][emplacement_check[1]] != ".":
        return False
    return True

def verif_win(win_or_not, first_letter, player, J1, J2):
    if not win_or_not or first_letter == ".":
        return False

    J1.changePriorite()
    if player:
        stdout.write("Bravo joueur 2 vous avez gagnez.\n")
        J2.incremantePoints()
    else:
        stdout.write("Bravo joueur 1 vous avez gagnez.\n")
        J1.incremantePoints()
    return True

def is_win(grille, player, J1, J2, taille):
    for y in range(taille):                          #lignes
        if grille[y][0] != '.':
            win = True
            first_letter = grille[y][0]
            for i in range(taille - 1):
                if grille[y][1 + i] != first_letter:
                    win = False
                    break
            if verif_win(win, first_letter, player, J1, J2): return True

    for y in range(taille):                          #colonnes
        if grille[0][y] != '.':
            win = True
            first_letter = grille[0][y]
            for i in range(taille - 1):
                if grille[1 + i][y] != first_letter:
                    win = False
                    break
            if verif_win(win, first_letter, player, J1, J2): return True

    if grille[0][0] != '.':
        win = True
        first_letter = grille[0][0]
        for i in range(taille - 1):                          #diagonale gauche
            if grille[i + 1][i + 1] != first_letter:
                win = False
                break
        if verif_win(win, first_letter, player, J1, J2): return True

    if grille[0][taille - 1] != '.':
        win = True
        first_letter = grille[0][taille - 1]
        for i in range(taille - 1):                          #diagonale droite
            if grille[i + 1][1 - i] != first_letter:
                win = False
                break
        if verif_win(win, first_letter, player, J1, J2): return True

def IA_Game(grille, taille, caracter, ennemi):
    for ligne in range(taille): # vérif lignes
        if grille[ligne].count(ennemi) == 0 and grille[ligne].count(caracter) >= taille // 3 and grille[ligne].count(".") > 0: # Intervient si caracter >= 1/3 de la ligne et ligne vide
            return (ligne, grille[ligne].index("."))
    for colonne in range(taille): # Intervient si caracter >= 1/3 de la colonne et colonne vide
        nbCaracters = 0
        nbPoints = [0, 0]
        for ligne in range(taille):
            if grille[ligne][colonne] == caracter: nbCaracters += 1
            elif grille[ligne][colonne] == ".":
                nbPoints[0] += 1 # nb_Points
                nbPoints[1] = ligne # Ligne du point
            elif grille[ligne][colonne] == ennemi: break
            if nbCaracters >= taille // 3 and nbPoints[0] > 0:
                return (nbPoints[1], colonne)
            
    nbCaracters = 0    
    points = [0, None] # nbPoints et position point
    for i in range(taille):                          #diagonale gauche
        if grille[i][i] == ".":
            points[0] += 1
            points[1] = i
        elif grille[i][i] == caracter:
            nbCaracters += 1
        elif grille[i][i] == ennemi: break
        if points[0] > 0 and nbCaracters >= taille // 3:
            return (points[1], points[1])

    nbCaracters = 0    
    points = [0, None, None] # nbPoints et position point
    for i in range(taille):                          #diagonale gauche
        if grille[i][taille - 1 - i] == ".":
            points[0] += 1
            points[1] = i
            points[2] = taille - 1 - i
        elif grille[i][taille - 1 - i] == caracter:
            nbCaracters += 1
        elif grille[i][taille - 1 - i] == ennemi: break
        if points[0] > 0 and nbCaracters >= taille // 3:
            return (points[1], points[2])


def IA_GameUltim(grille, taille, caracter):
    for ligne in range(taille):
        if grille[ligne].count(".") == 1 and grille[ligne].count(caracter) == taille - 1:
            return (ligne, grille[ligne].index("."))
    for colonne in range(taille):
        points = [0, None]
        nbCaracters = 0
        for ligne in range(taille):
            if grille[ligne][colonne] == ".":
                points[0] += 1
                points[1] = ligne
            elif grille[ligne][colonne] == caracter:
                nbCaracters += 1
        if points[0] == 1 and nbCaracters == taille - 1: # renvoie les coordonnées si il reste une place de libre
            return (points[1], colonne)
    nbCaracters = 0    
    points = [0, None, None]
    for i in range(taille):                          #diagonale gauche
        if grille[i][i] == ".":
            points[0] += 1
            points[1] = i
        elif grille[i][i] == caracter:
            nbCaracters += 1
    if points[0] == 1 and nbCaracters == taille - 1:
            return (points[1], points[1])

    nbCaracters = 0    
    points = [0, None, None]
    for i in range(taille):                          #diagonale droite
        if grille[i][taille - 1 - i] == ".":
            points[0] += 1
            points[1] = i
            points[2] = taille - 1 - i
        elif grille[i][taille - 1 - i] == caracter:
            nbCaracters += 1
    if points[0] == 1 and nbCaracters == taille - 1:
            return (points[1], points[2])

def clearEtAffiche(grille, taille, emplacement):
    os.system("cls" if os.name == "nt" else "clear")
    affichage(grille, taille, emplacement[0], emplacement[1])

def keyboard_gameplay(grille, emplacement, player, taille):
    time.sleep(.3)
    key = keyboard.read_key()
    global tailleCase
    while not key == "enter":
        if key == "droite":
            if emplacement[1] + 1 <= taille - 1:
                stdout.write("Joueur " + str(("2" if player else "1")) + "\n")
                emplacement[1] += 1 
                clearEtAffiche(grille, taille, emplacement)
        elif key == "gauche":
            if emplacement[1] - 1 >= 0:
                stdout.write("Joueur " + str(("2" if player else "1")) + "\n")
                emplacement[1] -= 1 
                clearEtAffiche(grille, taille, emplacement)
        elif key == "haut":
            if emplacement[0] - 1 >= 0:
                stdout.write("Joueur " + str(("2" if player else "1")) + "\n")
                emplacement[0] -= 1 
                clearEtAffiche(grille, taille, emplacement)
        elif key == "bas":
            if emplacement[0] + 1 <= taille - 1:
                stdout.write("Joueur " + str(("2" if player else "1")) + "\n")
                emplacement[0] += 1 
                clearEtAffiche(grille, taille, emplacement)
        elif key == "-":
            if tailleCase - 1 > 0:
                tailleCase -= 1
                clearEtAffiche(grille, taille, emplacement)
        elif key == "+":
            tailleCase += 1
            clearEtAffiche(grille, taille, emplacement)
        elif key == "esc": exit()
        time.sleep(0.3)
        key = keyboard.read_key()
    global nbEnter
    nbEnter += 1

    os.system("cls" if os.name == "nt" else "clear")   

def play_tour(player, grille, J1, J2, computer, taille, gameplay, robot):
    if (computer and player) or robot: #Si c'est à l'ordinateur de jouer
        caracter = "X" if player and robot else "O"
        ennemi = "O" if player and robot else "X"

        emplacement = IA_GameUltim(grille, taille, caracter) # s'il peut gagner
        if emplacement is None:
            emplacement = IA_GameUltim(grille, taille, ennemi) # s'il peut counter
            if emplacement is None:
                emplacement = IA_Game(grille, taille, caracter, ennemi) # s'il peut commencer une stratégie
                if emplacement is None:
                    emplacement = IA_Game(grille, taille, ennemi, caracter) # s'il peut contrer une stratégie
                    if emplacement is None:
                        emplacement = (random.randint(0, taille - 1), random.randint(0, taille - 1)) # au pif

            while not libre(emplacement, grille, taille):
                emplacement = (random.randint(0, taille - 1), random.randint(0, taille - 1))

        stdout.write(f"**********\nCoups de l'ordinateur : {emplacement[0]} {emplacement[1]}\n**********\n")
    else:
        if gameplay:
            emplacement = [0, 0]

            os.system("cls" if os.name == "nt" else "clear")

            stdout.write("Joueur " + str(("2" if player else "1")) + "\n")

            affichage(grille, taille, emplacement[0], emplacement[1])

            keyboard_gameplay(grille, emplacement, player, taille)

            while not libre(emplacement, grille, taille):
                keyboard_gameplay(grille, emplacement, player, taille)

        else:
            emplacement = input("Joueur " + str(("2" if player else "1")) + " choisissez un emplacement (ligne colonne): ").split()

            while not len(emplacement) == 2 or not (emplacement[0].isnumeric() and emplacement[1].isnumeric()) or not libre(list(map(int, emplacement)), grille, taille): #vérification du bon type, de la taille et de la place choisie
                emplacement = input("Choix Incorrect !\nJoueur " + str(("2" if player else "1")) + " choisissez un emplacement (ligne colonne): ").split()

            emplacement = list(map(int, emplacement))

    grille[emplacement[0]][emplacement[1]] = "X" if player == False else "O"

    affichage(grille, taille)

    return is_win(grille, player, J1, J2, taille)


def main():
    infos_J1 = Player()
    infos_J2 = Player()

    while True:
        global nbEnter
        nbEnter = 0

        robot = True if input("Robot vs Robot ? (O/N) : ") == "O" else False

        computer = True if not robot and input("Souhaitez-vous jouer avec un ordinateur (O/N) : ") == "O" else False
        keyboard_playing = True if not robot and input("Souhaitez-vous jouer avec les coordonnées ou avec le clavier ? (0/1) : ") == "1" else False

        taille_grille = input("Taille grille désirée (min 3) : ")

        while not taille_grille.isnumeric() or int(taille_grille) < 3:
            taille_grille = input("Choix incorrect ! Taille grille désirée (min 3) : ")

        taille_grille = int(taille_grille)

        grille = creation_grille(taille_grille)

        os.system("cls" if os.name == "nt" else "clear")

        affichage(grille, taille_grille)
        player = infos_J1.getPriorite()

        while not play_tour(player, grille, infos_J1, infos_J2, computer, taille_grille, keyboard_playing, robot):
            if not any("." in ligne for ligne in grille):
                stdout.write("Partie nulle\n")
                break

            player = not player
            if robot: time.sleep(.3)

        print(nbEnter)

        for _ in range(nbEnter): stdin.readline() # Clear le buffer d'entrée

        affichage(grille, taille_grille)
        
        if input(f"Partie terminée.\nPoints joueur 1 : {infos_J1.getPoints()}\nPoints joueur 2 : {infos_J2.getPoints()}\nVoulez-vous relancer ? (O/N) : ") == "N": break

        os.system("cls" if os.name == "nt" else "clear")

main()