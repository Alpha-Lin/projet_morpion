"""
Jeu du morpion :

Le but de ce jeu est d'aligner une rangée entière de son caractère pour gagner.
Vous pouvez jouer à deux, seul ou regarder des robots s'affronter

par Enes et Adrian
"""
from sys import stdout, stdin
import os
import random
import time
import keyboard

class Player():
    """
    Initialise une instance Player() correspondant à un joueur
    """

    def __init__(self):
        """
        attributs :
        - points : points du joueur
        - priorité : définit s'il joue en premier
        """
        self.points = 0
        self.priorite = False

    def getPoints(self):
        """
        Getter de l'attribut points : renvoie le nombre de points du joueur
        """
        return self.points
    
    def getPriorite(self):
        """
        Getter de l'attribut priorite : renvoie si le joueur est prioritaire
        """
        return self.priorite

    def incremantePoints(self):
        """
        Setter de l'attribut points : incrémente de 1 le nombre de points du joueur
        """
        self.points += 1

    def changePriorite(self):
        """
        Setter de l'attribut priorite : inverser la priorité
        """
        self.priorite = not self.priorite

class Grille():
    """
    Initialise une instance Grille() correspondant à la grille utilisée lors d'une manche 
    """

    def __init__(self, taille):
        """
        attributs : 
        - grille = contenu de la grille
        - taille = taille de la grille
        - tailleCase = taille de chaque case de la grille
        - nbEnter = nombre de fois où la touche "entrée" est pressée
        """
        self.grille = [['.'] * taille for i in range(taille)]
        self.taille = taille
        self.tailleCase = 1
        self.nbEnter = 0

    def getGrille(self):
        """
        "Getter de grille : renvoie la grille"
        """
        return self.grille

    def getNbEnter(self):
        """
        Getter de nbEnter : renvoie le nombre d'entrée fait depuis le début de la manche
        """
        return self.nbEnter

    def affichage(self, i1 = -1, i2 = -1):
        """
        Affiche la grille selon un modèle +-+
        
        paramètres :
        - i1 = ligne du sélecteur
        - i2 = colonne du sélecteur
        """
        if i1 > -1:
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
                stdout.write('|' + ' ' * (self.tailleCase - 1) + symbole + \
                ' ' * (self.tailleCase - 1))

            for _ in range(self.tailleCase // 2): # Intervient pour le zoom
                stdout.write("|\n")
                for _ in range(self.taille):
                    stdout.write("|" + " " * (self.tailleCase * 2 - 1))
            
            stdout.write("|\n")
        for _ in range(self.taille):
            stdout.write('+-' + '-' * 2 * (self.tailleCase - 1))
        stdout.write('+\n\n')

        if i1 > -1:
            self.grille[i1][i2] = tmp_sign


    def affichage2(self, i1 = -1, i2 = -1):
        """
        Affiche la grille selon un modèle neutre

        paramètres :
        - i1 = ligne du sélecteur
        - i2 = colonne du sélecteur
        """
        if i1 > -1:
            tmp_sign = self.grille[i1][i2]
            self.grille[i1][i2] = 'N'

        stdout.write("  ")

        for i in range(self.taille):
            stdout.write(str(i))

        stdout.write("\n")
        for ligne in range(self.taille):
            stdout.write(str(ligne) + " ")
            for symbole in self.grille[ligne]:
                stdout.write(symbole)
            stdout.write("\n\n")

        if i1 > -1:
            self.grille[i1][i2] = tmp_sign

    def libre(self, emplacement_check):
        """
        Vérifie si l'emplacement passé en paramètre correspondant à celui dans la grille est libre
        """
        if not (-1 < emplacement_check[0] < self.taille) or \
        not (-1 < emplacement_check[1] < self.taille) or \
        self.grille[emplacement_check[0]][emplacement_check[1]] != ".":
            return False
        return True

    def is_win(self, player, J1, J2):
        """
        Vérifie si le joueur en question a gagné.
        
        paramètres :
        - player = joueur prioritaire
        - J1 = joueur 1
        - J2 = joueur 2

        La vérification se passe en 4 étapes :
        1) vérifie si une des lignes est remplie
        2) vérifie si une des colonnes est remplie
        3) vérifie si la diagonale gauche est remplie
        4) vérifie si la diagonale droite est remplie
        """
        for y in range(self.taille):                          #lignes
            if self.grille[y][0] != '.':
                win = True
                first_letter = self.grille[y][0]
                for i in range(self.taille - 1):
                    if self.grille[y][1 + i] != first_letter:
                        win = False
                        break
                if self.verif_win(win, first_letter, player, J1, J2):
                    return True

        for y in range(self.taille):                          #colonnes
            if self.grille[0][y] != '.':
                win = True
                first_letter = self.grille[0][y]
                for i in range(self.taille - 1):
                    if self.grille[1 + i][y] != first_letter:
                        win = False
                        break
                if self.verif_win(win, first_letter, player, J1, J2):
                    return True

        if self.grille[0][0] != '.':
            win = True
            first_letter = self.grille[0][0]
            for i in range(self.taille - 1):                          #diagonale gauche
                if self.grille[i + 1][i + 1] != first_letter:
                    win = False
                    break
            if self.verif_win(win, first_letter, player, J1, J2):
                return True

        if self.grille[0][self.taille - 1] != '.':
            win = True
            first_letter = self.grille[0][self.taille - 1]
            for i in range(self.taille - 1):                          #diagonale droite
                if self.grille[i + 1][1 - i] != first_letter:
                    win = False
                    break
            if self.verif_win(win, first_letter, player, J1, J2):
                return True

    @staticmethod
    def verif_win(win_or_not, first_letter, player, J1, J2):
        """
        Est appelé lorsque is_win a trouvé une rangée pleine du même signe.
        La méthode va se charger de vérifier que cette rangée n'est pas constituée que de ".".
        
        S'il s'avère que c'est une victoire :
        - elle change la priorité en fonction du vainqueur
        - affiche un message de victoire
        - incrémente de 1 les points du vainqueur
        """
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
        """
        Méthode permetant à l'IA de contrer toute offensive (horizontalement, verticalement et en diagonale)
        Elle intervient quand elle voit que 1/3 de la rangée est remplie d'uniquement un signe du joueur et de "."

        Paramètres :
        - carater : définit le caractère du joueur
        - ennemi : définit le caractère de l'adversaire du joueur
        """
        nbCaracters = 0    
        points = [0, None] # nbPoints et position point
        for i in range(self.taille):                          #diagonale gauche
            if self.grille[i][i] == ".":
                points[0] += 1
                points[1] = i
            elif self.grille[i][i] == caracter:
                nbCaracters += 1
            elif self.grille[i][i] == ennemi:
                break
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
            elif self.grille[i][self.taille - 1 - i] == ennemi:
                break
            if points[0] > 0 and nbCaracters >= self.taille // 3:
                return (points[1], points[2])

        for ligne in range(self.taille): # vérif lignes
            if self.grille[ligne].count(ennemi) == 0 and self.grille[ligne].count(caracter) >= self.taille // 3 \
            and self.grille[ligne].count(".") > 0:                                  # Intervient si caracter >= 1/3 de la ligne et ligne vide
                return (ligne, self.grille[ligne].index("."))
        for colonne in range(self.taille):                                          # Intervient si caracter >= 1/3 de la colonne et colonne vide
            nbCaracters = 0
            nbPoints = [0, 0]
            for ligne in range(self.taille):
                if self.grille[ligne][colonne] == caracter:
                    nbCaracters += 1
                elif self.grille[ligne][colonne] == ".":
                    nbPoints[0] += 1 # nb_Points
                    nbPoints[1] = ligne # Ligne du point
                elif self.grille[ligne][colonne] == ennemi:
                    break
                if nbCaracters >= self.taille // 3 and nbPoints[0] > 0:
                    return (nbPoints[1], colonne)
                
    def IA_GameUltim(self, caracter):
        """
        Analyse chaque rangée afin de voir si l'une d'entre elle est quasiment pleine (remplie du même signe et d'un ".") 

        Le paramètre caracter définit sur quel caractère se baser
        """
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
        """
        Nettoye la console et affiche à quel joueur est-ce au tour de jouer.
        """
        os.system("cls" if os.name == "nt" else "clear")
        stdout.write("Joueur " + str(("2" if player else "1")) + "\n")
        self.affichage(emplacement[0], emplacement[1])

    def keyboard_gameplay(self, emplacement, player):
        """
        définit les déplacements du joueur en fonction des touches pressées
        grace au module "keyboard"  
        """
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
        """
        adrian
        """
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
                            coins = [coin for coin in [(0, 0), (0, self.taille - 1), (self.taille - 1, 0), (self.taille - 1, self.taille - 1)] \
                             if self.libre(coin)]  # les coins
                            if coins:
                                emplacement = random.choice(coins)
                            else:
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

                while not len(emplacement) == 2 or not (emplacement[0].isnumeric() and emplacement[1].isnumeric())\
                 or not self.libre(list(map(int, emplacement))): #vérification du bon type, de la taille et de la place choisie
                    emplacement = input("Choix Incorrect !\nJoueur " + str(("2" if player else "1"))\
                     + " choisissez un emplacement (ligne colonne): ").split()

                emplacement = list(map(int, emplacement))

        self.grille[emplacement[0]][emplacement[1]] = "X" if not player else "O"

        self.affichage()

        return self.is_win(player, J1, J2)
    
    def full(self):
        """
        Renvoie True si la grille ne contient plus aucun "."
        """
        return not any("." in ligne for ligne in self.grille)

def main():
    """
    fonction appelant d'entrée de jeu toutes les méthodes liées aux paramètres:
    - robot vs robot 
    - taille de la grille 
    - jouer contre un IA 

    elle a aussi pour but de rendre plus propre le terminal grace à des clears
    """
    j1 = Player()
    j2 = Player()

    while True:
        robot = input("Robot vs Robot ? (O/N) : ") == "O"

        computer = not robot and input("Souhaitez-vous jouer avec un ordinateur (O/N) : ") == "O"
        keyboard_playing = not robot and input("Souhaitez-vous jouer avec les coordonnées ou avec le clavier ? (0/1) : ") == "1"

        taille_grille = input("Taille grille désirée (min 3) : ")

        while not taille_grille.isnumeric() or int(taille_grille) < 3:
            taille_grille = input("Choix incorrect ! Taille grille désirée (min 3) : ")

        grille = Grille(int(taille_grille))

        os.system("cls" if os.name == "nt" else "clear")

        grille.affichage()
        player = j1.getPriorite()

        while not grille.play_tour(player, j1, j2, computer, keyboard_playing, robot):
            if grille.full():
                stdout.write("Partie nulle\n")
                break

            player = not player
            if robot: time.sleep(.3)

        for _ in range(grille.getNbEnter()): stdin.readline() # Clear le buffer d'entrée

        grille.affichage()
        
        if input(f"Partie terminée.\nPoints joueur 1 : {j1.getPoints()}\nPoints joueur 2 :\
         {j2.getPoints()}\nVoulez-vous relancer ? (O/N) : ") == "N": break

        os.system("cls" if os.name == "nt" else "clear")      

main()
