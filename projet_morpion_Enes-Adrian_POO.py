# Enes Adrian
from sys import stdout, stdin
import os
import random
import keyboard
import time

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

class Grille():
    def __init__(self, taille):
        self.grille = [['.'] * taille for i in range(taille)]
        self.taille = taille
        self.tailleCase = 1
        self.nbEnter = 0

    def getGrille(self):
        return self.grille

    def getNbEnter(self):
        return self.nbEnter

    def affichage(self, i1 = -1, i2= -1):
        if (i1 > -1):
            tmp_sign = self.grille[i1][i2]
            self.grille[i1][i2] = 'N'           # Sélecteur
        for ligne in range(self.taille):
            for _ in range(self.taille):
                stdout.write('+-' + '-' * 2 * (self.tailleCase - 1))
            stdout.write('+\n')

            for _ in range(self.tailleCase // 2):  # Intervient pour le zoom
                for _ in range(self.taille):
                    stdout.write("|" + " " * (self.tailleCase * 2 - 1))
                stdout.write("|\n")

            for symbole in self.grille[ligne]:
                stdout.write('|' + ' ' * (self.tailleCase - 1) + symbole + ' ' * (self.tailleCase - 1))

            for _ in range(self.tailleCase // 2): # Intervient pour le zoom
                stdout.write("|\n")
                for _ in range(self.taille):
                    stdout.write("|" + " " * (self.tailleCase * 2 - 1))
            
            stdout.write("|\n")
        for _ in range(self.taille):
            stdout.write('+-' + '-' * 2 * (self.tailleCase - 1))
        stdout.write('+\n\n')

        if (i1 > -1): self.grille[i1][i2] = tmp_sign


    def affichage2(self, i1 = -1, i2 = -1):
        if (i1 > -1):
            tmp_sign = self.grille[i1][i2]
            self.grille[i1][i2] = 'N'

        stdout.write("  ")
        for i in range(self.taille): stdout.write(str(i))
        stdout.write("\n")
        for ligne in range(self.taille):
            stdout.write(str(ligne) + " ")
            for symbole in self.grille[ligne]: stdout.write(symbole)
            stdout.write("\n\n")

        if (i1 > -1): self.grille[i1][i2] = tmp_sign

    def libre(self, emplacement_check):
        if not (-1 < emplacement_check[0] < self.taille) or not (-1 < emplacement_check[1] < self.taille) or self.grille[emplacement_check[0]][emplacement_check[1]] != ".":
            return False
        return True

    def is_win(self, player, J1, J2):
        for y in range(self.taille):                          #lignes
            if self.grille[y][0] != '.':
                win = True
                first_letter = self.grille[y][0]
                for i in range(self.taille - 1):
                    if self.grille[y][1 + i] != first_letter:
                        win = False
                        break
                if self.verif_win(win, first_letter, player, J1, J2): return True

        for y in range(self.taille):                          #colonnes
            if self.grille[0][y] != '.':
                win = True
                first_letter = self.grille[0][y]
                for i in range(self.taille - 1):
                    if self.grille[1 + i][y] != first_letter:
                        win = False
                        break
                if self.verif_win(win, first_letter, player, J1, J2): return True

        if self.grille[0][0] != '.':
            win = True
            first_letter = self.grille[0][0]
            for i in range(self.taille - 1):                          #diagonale gauche
                if self.grille[i + 1][i + 1] != first_letter:
                    win = False
                    break
            if self.verif_win(win, first_letter, player, J1, J2): return True

        if self.grille[0][self.taille - 1] != '.':
            win = True
            first_letter = self.grille[0][self.taille - 1]
            for i in range(self.taille - 1):                          #diagonale droite
                if self.grille[i + 1][1 - i] != first_letter:
                    win = False
                    break
            if self.verif_win(win, first_letter, player, J1, J2): return True

    def verif_win(self, win_or_not, first_letter, player, J1, J2):
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

    def IA_Game(self, caracter, ennemi):
        for ligne in range(self.taille): # vérif lignes
            if self.grille[ligne].count(ennemi) == 0 and self.grille[ligne].count(caracter) >= self.taille // 3 and self.grille[ligne].count(".") > 0: # Intervient si caracter >= 1/3 de la ligne et ligne vide
                return (ligne, self.grille[ligne].index("."))
        for colonne in range(self.taille): # Intervient si caracter >= 1/3 de la colonne et colonne vide
            nbCaracters = 0
            nbPoints = [0, 0]
            for ligne in range(self.taille):
                if self.grille[ligne][colonne] == caracter: nbCaracters += 1
                elif self.grille[ligne][colonne] == ".":
                    nbPoints[0] += 1 # nb_Points
                    nbPoints[1] = ligne # Ligne du point
                elif self.grille[ligne][colonne] == ennemi: break
                if nbCaracters >= self.taille // 3 and nbPoints[0] > 0:
                    return (nbPoints[1], colonne)
                
        nbCaracters = 0    
        points = [0, None] # nbPoints et position point
        for i in range(self.taille):                          #diagonale gauche
            if self.grille[i][i] == ".":
                points[0] += 1
                points[1] = i
            elif self.grille[i][i] == caracter:
                nbCaracters += 1
            elif self.grille[i][i] == ennemi: break
            if points[0] > 0 and nbCaracters >= self.taille // 3:
                return (points[1], points[1])

        nbCaracters = 0    
        points = [0, None, None] # nbPoints et position point
        for i in range(self.taille):                          #diagonale gauche
            if self.grille[i][self.taille - 1 - i] == ".":
                points[0] += 1
                points[1] = i
                points[2] = self.taille - 1 - i
            elif self.grille[i][self.taille - 1 - i] == caracter:
                nbCaracters += 1
            elif self.grille[i][self.taille - 1 - i] == ennemi: break
            if points[0] > 0 and nbCaracters >= self.taille // 3:
                return (points[1], points[2])


    def IA_GameUltim(self, caracter):
        for ligne in range(self.taille):
            if self.grille[ligne].count(".") == 1 and self.grille[ligne].count(caracter) == self.taille - 1:
                return (ligne, self.grille[ligne].index("."))
        for colonne in range(self.taille):
            points = [0, None]
            nbCaracters = 0
            for ligne in range(self.taille):
                if self.grille[ligne][colonne] == ".":
                    points[0] += 1
                    points[1] = ligne
                elif self.grille[ligne][colonne] == caracter:
                    nbCaracters += 1
            if points[0] == 1 and nbCaracters == self.taille - 1: # renvoie les coordonnées si il reste une place de libre
                return (points[1], colonne)
        nbCaracters = 0    
        points = [0, None, None]
        for i in range(self.taille):                          #diagonale gauche
            if self.grille[i][i] == ".":
                points[0] += 1
                points[1] = i
            elif self.grille[i][i] == caracter:
                nbCaracters += 1
        if points[0] == 1 and nbCaracters == self.taille - 1:
                return (points[1], points[1])

        nbCaracters = 0    
        points = [0, None, None]
        for i in range(self.taille):                          #diagonale droite
            if self.grille[i][self.taille - 1 - i] == ".":
                points[0] += 1
                points[1] = i
                points[2] = self.taille - 1 - i
            elif self.grille[i][self.taille - 1 - i] == caracter:
                nbCaracters += 1
        if points[0] == 1 and nbCaracters == self.taille - 1:
                return (points[1], points[2])

    def clearEtAffiche(self, emplacement, player):
        os.system("cls" if os.name == "nt" else "clear")
        stdout.write("Joueur " + str(("2" if player else "1")) + "\n")
        self.affichage(emplacement[0], emplacement[1])

    def keyboard_gameplay(self, emplacement, player):
        time.sleep(.3)
        key = keyboard.read_key()
        while not key == "enter":
            if key == "droite":
                if emplacement[1] + 1 <= self.taille - 1:
                    stdout.write("Joueur " + str(("2" if player else "1")) + "\n")
                    emplacement[1] += 1
                    self.clearEtAffiche(emplacement, player)
            elif key == "gauche":
                if emplacement[1] - 1 >= 0:
                    stdout.write("Joueur " + str(("2" if player else "1")) + "\n")
                    emplacement[1] -= 1
                    self.clearEtAffiche(emplacement, player)
            elif key == "haut":
                if emplacement[0] - 1 >= 0:
                    stdout.write("Joueur " + str(("2" if player else "1")) + "\n")
                    emplacement[0] -= 1
                    self.clearEtAffiche(emplacement, player)
            elif key == "bas":
                if emplacement[0] + 1 <= self.taille - 1:
                    stdout.write("Joueur " + str(("2" if player else "1")) + "\n")
                    emplacement[0] += 1
                    self.clearEtAffiche(emplacement, player)
            elif key == "-":
                if self.tailleCase - 1 > 0: 
                    self.tailleCase -= 1
                    self.clearEtAffiche(emplacement, player)
            elif key == "+":
                self.tailleCase += 1
                self.clearEtAffiche(emplacement, player)
            elif key == "esc": exit()
            time.sleep(.3)
            key = keyboard.read_key()
        self.nbEnter += 1

    def play_tour(self, player, J1, J2, computer, gameplay, robot):
        if (computer and player) or robot: #Si c'est à l'ordinateur de jouer
            caracter = "X" if player and robot else "O"
            ennemi = "O" if player and robot else "X"

            emplacement = self.IA_GameUltim(caracter) # s'il peut gagner
            if emplacement is None:
                emplacement = self.IA_GameUltim(ennemi) # s'il peut counter
                if emplacement is None:
                    emplacement = self.IA_Game(caracter, ennemi) # s'il peut commencer une stratégie
                    if emplacement is None:
                        emplacement = self.IA_Game(ennemi, caracter) # s'il peut contrer une stratégie
                        if emplacement is None:
                            emplacement = (random.randint(0, self.taille - 1), random.randint(0, self.taille - 1)) # au pif

                while not self.libre(emplacement):
                    emplacement = (random.randint(0, self.taille - 1), random.randint(0, self.taille - 1))

            stdout.write(f"**********\nCoups de l'ordinateur : {emplacement[0]} {emplacement[1]}\n**********\n")
        else:
            if gameplay:
                emplacement = [0, 0]

                os.system("cls" if os.name == "nt" else "clear")

                stdout.write("Joueur " + str(("2" if player else "1")) + "\n")

                self.affichage(emplacement[0], emplacement[1])

                self.keyboard_gameplay(emplacement, player)

                while not self.libre(emplacement):
                    self.keyboard_gameplay(emplacement, player)

            else:
                emplacement = input("Joueur " + str(("2" if player else "1")) + " choisissez un emplacement (ligne colonne): ").split()

                while not len(emplacement) == 2 or not (emplacement[0].isnumeric() and emplacement[1].isnumeric()) or not self.libre(list(map(int, emplacement))): #vérification du bon type, de la taille et de la place choisie
                    emplacement = input("Choix Incorrect !\nJoueur " + str(("2" if player else "1")) + " choisissez un emplacement (ligne colonne): ").split()

                emplacement = list(map(int, emplacement))

        self.grille[emplacement[0]][emplacement[1]] = "X" if player == False else "O"

        self.affichage()

        return self.is_win(player, J1, J2)
    
    def full(self):
        return not any("." in ligne for ligne in self.grille)

def main():
    infos_J1 = Player()
    infos_J2 = Player()

    while True:
        robot = True if input("Robot vs Robot ? (O/N) : ") == "O" else False

        computer = True if not robot and input("Souhaitez-vous jouer avec un ordinateur (O/N) : ") == "O" else False
        keyboard_playing = True if not robot and input("Souhaitez-vous jouer avec les coordonnées ou avec le clavier ? (0/1) : ") == "1" else False

        taille_grille = input("Taille grille désirée (min 3) : ")

        while not taille_grille.isnumeric() or int(taille_grille) < 3:
            taille_grille = input("Choix incorrect ! Taille grille désirée (min 3) : ")

        grille = Grille(int(taille_grille))

        os.system("cls" if os.name == "nt" else "clear")

        grille.affichage()
        player = infos_J1.getPriorite()

        while not grille.play_tour(player, infos_J1, infos_J2, computer, keyboard_playing, robot):
            if grille.full():
                stdout.write("Partie nulle\n")
                break

            player = not player
            if robot: time.sleep(.3)

        for _ in range(grille.getNbEnter()): stdin.readline() # Clear le buffer d'entrée

        grille.affichage()
        
        if input(f"Partie terminée.\nPoints joueur 1 : {infos_J1.getPoints()}\nPoints joueur 2 : {infos_J2.getPoints()}\nVoulez-vous relancer ? (O/N) : ") == "N": break

        os.system("cls" if os.name == "nt" else "clear")      

main()