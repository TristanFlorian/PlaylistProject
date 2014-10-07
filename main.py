#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import logging

''' Fonction de vérification des sous arguments '''
def checkSousArgs(unArgument, nomDeLArgument):
    try:
        # Conversion en entier
        unArgument[1] = int(unArgument[1])
        # Si nb n'est pas un entier naturel et qu'il est supérieur ou égal à 100, on lève une exception, et on met dans nb, la valeur absolue qu'il contenait
        # Si le 2ème ss-arg est inférieur à zéro, on ne garde que sa valeur absolue et on lève et écrit une exception dans le fichier de logs
        if (checkIntNatural(unArgument[1]) == False):
            raise Exception('" doit être positive !')
            unArgument[1] = abs(unArgument[1])
        # Si le 2ème ss-arg est supérieur à 100, on ne garde pas sa valeur, on la remplace par 0
        if (checkIntInfCent(unArgument[1]) == False):
            raise Exception('" doit être inférieure à "100" !')
            unArgument[1] = 0
        # Ensuite, on indique qu'on utilise la variable globale args, et on modifie les ss-arg avec la transformation précédament effectuée
        global args
        setattr(args, nomDeLArgument, [unArgument[0], unArgument[1]])
    except ValueError:
        logging.error(' --' + nomDeLArgument + ', impossible de convertir "' + unArgument[1] + '" en nombre entier !')
    except Exception as er:
        logging.warning(' --' + nomDeLArgument + ', la valeur "' + unArgument[1] + er.args[1])

''' Vérifie qu'un nombre est un entier naturel '''
def checkIntNatural(nb):
    return nb > 0
    
''' Vérifie qu'un nombre est inférieur à 100 '''
def checkIntInfCent(nb):
    return nb < 100

''' Traitement du programme principal '''
parser = argparse.ArgumentParser()          # Création d'un objet de classe ArgumentParser
logging.basicConfig(filename='errors.log', level=logging.DEBUG)   # Les erreurs seront redirigées dans le fichier de log nommé 'errors.log'

# Gestion des arguments positionnels
''' Le 1er paramètre correspond au nom que l'on veut attribuer à la playliste [chaine] (Ex: "maPlayliste") '''
parser.add_argument("nom_playlist", help = "Le nom du fichier contenant la playlist.")
''' Le 2ème paramètre correspond à la durée désirée pour la playliste [entier naturel] '''
parser.add_argument("temps_playlist", type=int,  help = "Spécifie la durée de la playlist, en minutes. [entier naturel] (Ex : 60)")

# Gestion des arguments optionnels
    # Gestion Format
''' Paramètre permettant de renseigner le format de playliste désiré selon la liste {m3u,xspf,pls} '''
parser.add_argument("--format", nargs = 1, choices=['m3u','xspf','pls'], help = "Donne le format de sortie de la playliste (m3u | xspf | pls)")
    # Gestion Titre
''' Paramètre permettant de renseigner le pourcentage d'un titre dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
parser.add_argument("--titre", nargs = 2, help = "Indique qu'on spécifie le pourcentage d'un titre dans la playliste. [entier naturel] (Ex: 30 -> 30%%)")
    # Gestion du genre
''' Paramètre permettant de renseigner le pourcentage d'un genre dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
parser.add_argument("--genre", nargs = 2, help = "Indique qu'on spécifie le pourcentage d'un genre dans la playliste. [entier naturel] (Ex: 30 -> 30%%)")
    # Gestion du sous-genre
''' Paramètre permettant de renseigner le pourcentage d'un sous-genre dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
parser.add_argument("--sousgenre", nargs = 2, help = "Indique qu'on spécifie le pourcentage d'un sous-genre dans la playliste. [entier naturel] (Ex: 30 -> 30%%)")
    # Gestion de l'artiste
''' Paramètre permettant de renseigner le pourcentage d'un artiste dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
parser.add_argument("--artiste", nargs = 2, help = "Indique qu'on spécifie le pourcentage d'un artiste dans la playliste. [entier naturel] (Ex: 30 -> 30%%)")
    # Gestion de l'album
''' Paramètre permettant de renseigner le pourcentage d'un album dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
parser.add_argument("--album", nargs = 2, help = "Indique qu'on spécifie le pourcentage d'un album dans la playliste. [entier naturel] (Ex: 30 -> 30%%)")

args = parser.parse_args()

#''' Boucle pour tester l'ensemble des paramètres optionnels, et réalise le test uniquement si l'argument est renseigné '''
# for ARG in ['titre','genre','sousgenre','artiste','album']:
#     if getattr(args, ARG) is not None:
#         checkSousArgs(getattr(args, ARG), ARG)

# Gestion de l'argument genre et ses sous-arguments
# Pour chaque argument qui est dans le dictionnaire dans le for,
for PremierArg in ['titre','genre','sousgenre','artiste','album']:
    # Si l'argument est renseigné
    if getattr(args, PremierArg) is not None:
        # On écrit la valeur de ses ss-arg dans le fichier de logs
        logging.info(' Argument --' + PremierArg + ' :\t' + getattr(args, PremierArg)[0] + ' ; ' + getattr(args, PremierArg)[1])
        # Puis on vérifie que le 2eme ss-arg de l'argument est correct et on le remplace par la nouvelle valeure créée lors de la vérification
        checkSousArgs(getattr(args, PremierArg), PremierArg)
# Ecriture d'une ligne d'étoiles dans le fichier de log, pour séparrer les infos en fonction de chaque exécution
logging.debug(' *****************************************')
logging.shutdown()
# la commande exit(0) permet de quitter le programme en indiquant qu'il n'y a pas eu d'erreurs
exit(0)