import json, random

# Ouverture des fichiers en lecture
fichier = open('liste.de.mots.francais.frgut.txt', 'r', encoding='utf-8')

# Création des variables de stockage
mot = {}
probabilite = {}

# Lecture du fichier
listeMot = fichier.read().split()

# Fonction pour créer le dictionnaire qui contient les occurences
def creationDictionnaire(dico, symbole1, symbole2, symbole3, symbole4):
    lettre1 = symbole1
    lettre2 = symbole2
    lettre3 = symbole3
    lettre4 = symbole4
    
    if lettre1 not in dico:
        dico[lettre1] = {}

    if lettre2 not in dico[lettre1]:
        dico[lettre1][lettre2] = {}

    if lettre3 not in dico[lettre1][lettre2]:
        dico[lettre1][lettre2][lettre3]= {} 

    if lettre4 not in dico[lettre1][lettre2][lettre3]:
        dico[lettre1][lettre2][lettre3][lettre4]= 0

    dico[lettre1][lettre2][lettre3][lettre4] += 1

# Fonction pour créer le dictionnaire qui contient les probabilities
def creationProba(proba, dico, symbole1, symbole2, symbole3, symbole4):
    lettre1 = symbole1
    lettre2 = symbole2
    lettre3 = symbole3
    lettre4 = symbole4

    if lettre1 not in proba:
        proba[lettre1] = {}

    if lettre2 not in proba[lettre1]:
        proba[lettre1][lettre2] = {}
    
    if lettre3 not in proba[lettre1][lettre2]:
        proba[lettre1][lettre2][lettre3]= {}
    if lettre4 not in proba[lettre1][lettre2][lettre3]:
        calcul = ((dico[lettre1][lettre2][lettre3][lettre4] * 100) / len(listeMot))
        proba[lettre1][lettre2][lettre3][lettre4] = calcul

# Déclaration des symboles de début et de fin
symboleDebut = "###"
symboleFin = "$"

# Boucle pour créer le dictionnaire d'occurence
for ligne in listeMot:
    ligne = symboleDebut + ligne + symboleFin # Pour ajouter le symbole de début et de fin
    for i in range(1, len(ligne)):
        creationDictionnaire(mot, ligne[i-3], ligne[i-2], ligne[i-1], ligne[i])

# Boucle pour créer le dictionnaire de probabilité
for ligne in listeMot:
    ligne = symboleDebut + ligne + symboleFin # Pour ajouter le symbole de début et de fin
    for i in range(1, len(ligne)):
        creationProba(probabilite, mot, ligne[i-3], ligne[i-2], ligne[i-1], ligne[i])

# Création d'un fichier json pour stocker nos probabilite
json_file = json.dumps(probabilite, ensure_ascii=False, indent=4)
with open('probabilite.json', 'w', encoding='utf-8') as f:
    f.write(json_file)

# Fonction pour générer un mot aléatoire
def generer_mot(probabilite, symboleDebut, symboleFin):
    # Variable qui sera retourner
    mot_genere = ""

    # Initialisation des variables qui pourront chercher les probabilités
    symbole1 = symboleDebut
    symbole2 = random.choice(list(probabilite[symbole1].keys()))
    symbole3 = random.choice(list(probabilite[symbole1][symbole2].keys()))
    symbole4 = ""

    # Boucle pour générer le mot
    while symbole4 != symboleFin:
        symboles_suivants = probabilite[symbole1][symbole2][symbole3]
        symbole4 = random.choices(list(symboles_suivants.keys()), weights=symboles_suivants.values())[0]

        if symbole4 != symboleFin:
            mot_genere += symbole4

            symbole1 = symbole2
            symbole2 = symbole3
            symbole3 = symbole4

    return mot_genere

# Pour voir si la fonction marche
mot_genere = generer_mot(probabilite, "#", symboleFin)
print("Mot généré:", mot_genere)