import logging
import argparse

parser = argparse.ArgumentParser()

''' Renseigne où se situe le fichier de log, est à quel niveau on y inscrit des données '''
def initLoggingConfig():
    logging.basicConfig(filename='le_fichier_de.log',level=logging.DEBUG)

''' ajoute 2 arguments positionnels à l'objet parser '''
def initArgumentsPositionnels():
    # Gestion des arguments positionnels
    ''' Le 1er paramètre correspond au nom que l'on veut attribuer à la playliste [chaine] (Ex: "maPlayliste") '''
    parser.add_argument("nom_playlist", help = "Le nom du fichier contenant la playlist.")
    ''' Le 2ème paramètre correspond à la durée désirée pour la playliste [entier naturel] '''
    parser.add_argument("temps_playlist", type=int,  help = "Spécifie la durée de la playlist, en minutes. [entier naturel] (Ex : 60)")
    
''' ajoute 6 arguments optionnels à l'objet parser '''
def initArgumentsOptionnels():
    # Gestion Format
    ''' Paramètre permettant de renseigner le format de playliste désiré selon la liste {m3u,xspf,pls} '''
    parser.add_argument("--format", nargs = 1, choices=['m3u','xspf','pls'], help = "Donne le format de sortie de la playliste (m3u | xspf | pls)")
    # Gestion Titre
    ''' Paramètre permettant de renseigner le pourcentage d'un titre dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
    parser.add_argument("--titre", nargs = 2, help = "Indique qu'on spécifie le pourcentage d'un titre dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", action="append")
    # Gestion du genre
    ''' Paramètre permettant de renseigner le pourcentage d'un genre dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
    parser.add_argument("--genre", nargs = 2, help = "Indique qu'on spécifie le pourcentage d'un genre dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", action="append")
    # Gestion du sous-genre
    ''' Paramètre permettant de renseigner le pourcentage d'un sous-genre dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
    parser.add_argument("--sousgenre", nargs = 2, help = "Indique qu'on spécifie le pourcentage d'un sous-genre dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", action="append")
    # Gestion de l'artiste
    ''' Paramètre permettant de renseigner le pourcentage d'un artiste dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
    parser.add_argument("--artiste", nargs = 2, help = "Indique qu'on spécifie le pourcentage d'un artiste dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", action="append")
    # Gestion de l'album
    ''' Paramètre permettant de renseigner le pourcentage d'un album dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
    parser.add_argument("--album", nargs = 2, help = "Indique qu'on spécifie le pourcentage d'un album dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", action="append")

''' initialise l'objet listeArgumentsCLI en lui ajoutant une multitude d'arguments positionnels et d'arguments optionnels '''
def initListeArguments():
    initArgumentsPositionnels()
    initArgumentsOptionnels()
    return parser.parse_args()

''' vérifie qu'un argument donné en paramètre est bien un nombre entier, et qu'il ne dépasse pas 100 '''
def checkSousArgs(unArgument, nomDeLArgument, indice):
    try:
        # Conversion en entier
        unArgument[1] = int(unArgument[1])
        # Si nb n'est pas un entier naturel et qu'il est supérieur ou égal à 100, on lève une exception, et on met dans nb, la valeur absolue qu'il contenait
        # Si le 2ème ss-arg est inférieur à zéro, on ne garde que sa valeur absolue et on lève et écrit une exception dans le fichier de logs
        if (checkIntNatural(unArgument[1]) == False):
            raise Exception('" doit être positive !\n\t La valeur absolue de "' + str(unArgument[1]) + '" a été retenue à la place...')
        # Si le 2ème ss-arg est supérieur à 100, on ne garde pas sa valeur, on la remplace par 0
        if (checkIntInfCent(unArgument[1]) == False):
            raise Exception('" doit être inférieure à "100" !')
            unArgument[1] = 0
        # On ne garde que la valeur absolue du pourcentage saisi
        unArgument[1] = controlIntNatural(unArgument[1])
        # Ensuite, on indique qu'on utilise la variable globale args, et on modifie les ss-arg avec la transformation précédament effectuée
        global args
        setattr(args, nomDeLArgument[indice], [unArgument[0], unArgument[1]])
    except ValueError:
        logging.error(' --' + nomDeLArgument + ', impossible de convertir "' + unArgument[1] + '" en nombre entier !')
    except Exception as er:
        logging.warning(' --' + nomDeLArgument + ', la valeur "' + str(unArgument[1]) + er.args[0])
             
''' Vérifie qu'un nombre est un entier naturel (> 0) '''
def checkIntNatural(nb):
    return nb > 0
    
''' Retourne la valeur absolue du nombre passé en paramètre s'il est inférieur à 0, sinon, il le retourne sans l'avoir modifié '''
def controlIntNatural(nb):
    if(checkIntNatural(nb) == True):
        return nb
    else:
        return abs(nb)
    
''' Vérifie qu'un nombre est inférieur à 100 '''
def checkIntInfCent(nb):
    return nb < 100

''' Vérifie la valeur du 2ème sous argument de chaque argument dans la liste d'arguments '''
def checkListeDesArguments(listeDArguments):
    for nomArgument in ['titre','genre','sousgenre','artiste','album']:
        # Si l'argument est renseigné
        if getattr(listeDArguments, nomArgument) is not None:
            # Comme on a spécifié que les arguments avaient la propriété "append", l'argument args.genre devient non plus une liste (avec un str et un int) mais une
            # liste de liste avec un str et un int
            # Donc pour chaque argument 
            # On écrit la valeur de ses ss-arg dans le fichier de logs
            logging.info(' Argument --' + nomArgument + ' :\t' + getattr(listeDArguments, nomArgument)[0][0] + ' ; ' + getattr(listeDArguments, nomArgument)[0][1])
            # Puis on vérifie que le 2eme ss-arg de l'argument est correct et on le remplace par la nouvelle valeure créée lors de la vérification
            i = 0
            while i < len(getattr(listeDArguments, nomArgument)):
                checkSousArgs(getattr(listeDArguments, nomArgument)[i], nomArgument, i)
                i = i + 1