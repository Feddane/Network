from random import randint

#Liste des options
jeu  = ["pierre", "papier", "ciseaux"]

#Attribuer une option aléatoire à l'ordinateur
ordinateur = jeu[randint(0,2)]

#Gardez le compte des points
Pointsjoueur = 0
Pointsordinateur = 0

continuer = True

#La boucle continue jusqu'à ce que la variable continuer est fausse
while(continuer):
    #Demander le choix de l'ordinateur<br>
    joueur = input("pierre, papier, ciseaux? ou tapez Fin pour arrêter le jeu!\n")

    #Vérification des scenarios
    if(joueur == 'Fin'):
        continuer = False
    elif(joueur == ordinateur):
        print("Egalité!")
    elif(joueur == "pierre"):
        if(ordinateur == "papier"):
            print("Perdu!", ordinateur, "recouvre", joueur)
            Pointsordinateur = Pointsordinateur + 1 
        else:
            print("Gagné!", joueur, "écrase", ordinateur)
            Pointsjoueur = Pointsjoueur + 1
    elif(joueur == "papier"):
        if(ordinateur == "ciseaux"):
            print("Perdu!", ordinateur, "cut", joueur)
            Pointsordinateur = Pointsordinateur + 1
        else:
            print("You win!", joueur, "recouvre", ordinateur)
            Pointsjoueur = Pointsjoueur + 1
    elif(joueur == "ciseaux"):
        if(ordinateur == "Rock"):
            print("Perdu...", ordinateur, "écrase", joueur)
            Pointsordinateur = Pointsordinateur + 1
        else:
            print("Gagné!", joueur, "cut", ordinateur)
            Pointsjoueur = Pointsjoueur + 1
    else:
        print("Votre choix n'est pas correct, vérifiez l'orthographe!")
    #Attribuer une option aléatoire à l'ordinateur
    ordinateur = jeu[randint(0,2)]
    print('********Tour suivant********')

#Impression des points
print("********Points********")
print("joueur: ", Pointsjoueur)
print("ordinateur: ", Pointsordinateur)