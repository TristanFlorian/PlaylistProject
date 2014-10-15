# -*- coding: utf-8 -*-

import logging
import argparse
import sys

class MonAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(MonAction, self).__init__(option_strings, dest, nargs=nargs, **kwargs)
        logging.debug(option_strings)
    
    def __call__(self, parser, namespace, values, option_string=None):
        values[1] = int(values[1])
        setattr(namespace, option_string, values)
        logging.debug(values)

parser = argparse.ArgumentParser()
listeNomArguments = ['titre','genre','sousgenre','artiste','album']

''' Renseigne où se situe le fichier de log, est à quel niveau on y inscrit des données '''
def initLoggingConfig():
    logging.basicConfig(filename='le_fichier_de.log',level=logging.DEBUG)
    #logging.basicConfig(level=logging.DEBUG)





''' vérifie qu'un argument donné en paramètre est bien un nombre entier, et qu'il ne dépasse pas 100 '''
def checkSousArgs(unArgument, nomDeLArgument, indice):
    try:
        # Conversion en entier
        print(unArgument)
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
        return unArgument[1]
    except ValueError:
        logging.error(' --' + nomDeLArgument + ', impossible de convertir "' + unArgument[1] + '" en nombre entier !')
#    except Exception as er:
#        logging.warning(' --' + nomDeLArgument + ', la valeur "' + str(unArgument[1]) + er.args[0])

''' Vérifie qu'un nombre est un entier naturel (> 0) '''
def checkIntNatural(nb):
    return nb > 0

''' Retourne la valeur absolue du nombre passé en paramètre s'il est inférieur à 0, sinon, il le retourne sans l'avoir modifié '''
def controlIntNatural(nb):
    '''
    >>> nb = controlIntNatural(2)
    >>> print(str(nb))
    2
    >>> nb = controlIntNatural(-2)
    >>> print(str(nb))
    2
    '''
    if(checkIntNatural(nb) == True):
        return nb
    else:
        return abs(nb)

''' Vérifie qu'un nombre est inférieur à 100 '''
def checkIntInfCent(nb):
    return nb < 100

''' Vérifie la valeur du 2ème sous argument de chaque argument dans la liste d'arguments '''
def checkListeDesArguments(listeDArguments, listeParamDansLog):
    for nomArgument in listeNomArguments:
        # Si l'argument est renseigné
        if getattr(listeDArguments, nomArgument) is not None:
            i = 0
            while i < len(getattr(listeDArguments, nomArgument)):
                # Comme on a spécifié que les arguments avaient la propriété "append", l'argument args.genre devient non plus une liste (avec un str et un int)
                # mais une liste de liste avec un str et un int
                # Donc pour chaque argument 
                # On écrit la valeur de ses ss-arg dans le fichier de logs
                if (listeParamDansLog == 0):
                    logging.info(' Argument --' + nomArgument + ' :\t' + getattr(listeDArguments, nomArgument)[i][0] + ' ; ' + getattr(listeDArguments, nomArgument)[i][1])
                # Puis on vérifie que le 2eme ss-arg de l'argument est correct et on le remplace par la nouvelle valeure créée lors de la vérification
                else:
                    azerty = checkSousArgs(getattr(listeDArguments, nomArgument)[i], nomArgument, i)
                    setattr(listeDArguments, nomArgument, [getattr(listeDArguments, nomArgument)[0], azerty])
                #print(checkSousArgs(getattr(listeDArguments, nomArgument)[i], nomArgument, i))
                #print(' Argument --' + nomArgument + ' :\t' + str(getattr(listeDArguments, nomArgument)[i][0]) + ' ; ' + str(getattr(listeDArguments, nomArgument)[i][1]) + ' ;; ' + str(type(getattr(listeDArguments, nomArgument)[i][1])))
                i = i + 1




class appendTypeQuantity(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs == 2:
            super(appendTypeQuantity, self).__init__(option_strings, dest, nargs=nargs, **kwargs)
        else:
            logging.error("Option %s must have 2 arguments in its definition" % option_strings)
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            quantity = abs(int(values[1]))
            values[1] = quantity if 100 >= quantity > 0 else None
        except ValueError:
            logging.error("Quantity Input value is Not A Number (NaN): '" + values[1] + "'")
            sys.exit(1)
        current_dest_value = getattr(namespace, self.dest)
        if type(current_dest_value) is list:
            current_dest_value.append(values)
            setattr(namespace, self.dest, current_dest_value)
        else:
            logging.debug(values)
            setattr(namespace, self.dest, [values])



''' Classe représentant une ligne de commande, avec ses arguments (positionnels et optionnels) '''
class ligneCommande(object):
    ''' Constructeur de la classe '''
    def __init__(self):
        self.arguments = argparse.Namespace()
        self.parser = argparse.ArgumentParser()
        self.ajoutArguments()
    
    def initListeArguments(self):
        self.arguments = self.parser.parse_args()
    
    ''' Ajoute la liste des arguments positionnels et optionnels '''
    def ajoutArguments(self):
        # Les arguments positionnels
        ''' Le 1er paramètre correspond au nom que l'on veut attribuer à la playliste [chaine] (Ex: "maPlayliste") '''
        self.parser.add_argument("nom_playlist", help = "Le nom du fichier contenant la playlist.")
        ''' Le 2ème paramètre correspond à la durée désirée pour la playliste [entier naturel] '''
        self.parser.add_argument("temps_playlist", type=int,  help = "Spécifie la durée de la playlist, en minutes. [entier naturel] (Ex : 60)")
        # Les arguments optionnels
        ''' Paramètre permettant de renseigner le format de playliste désiré selon la liste {m3u,xspf,pls} '''
        self.parser.add_argument("-f",
                            "--format", 
                            nargs = 1, 
                            choices=['m3u','xspf','pls'], 
                            help = "Donne le format de sortie de la playliste (m3u | xspf | pls)")
        ''' Paramètre permettant de renseigner le pourcentage d'un titre dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
        self.parser.add_argument("-t",
                            "--titre", 
                            nargs = 2, 
                            metavar=('TITRE','QUANTITE'),
                            help = "Indique qu'on spécifie le pourcentage d'un titre dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", 
                            action="append")
        ''' Paramètre permettant de renseigner le pourcentage d'un genre dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
        self.parser.add_argument("-g",
                            "--genre",
                            nargs = 2,
                            metavar=('GENRE','QUANTITE'),
                            help = "Indique qu'on spécifie le pourcentage d'un genre dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", 
                            action=MonAction)
        ''' Paramètre permettant de renseigner le pourcentage d'un sous-genre dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
        self.parser.add_argument("-sg",
                            "--sousgenre", 
                            nargs = 2, 
                            metavar=('SOUSGENRE','QUANTITE'),
                            help = "Indique qu'on spécifie le pourcentage d'un sous-genre dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", 
                            action="append")
        ''' Paramètre permettant de renseigner le pourcentage d'un artiste dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
        self.parser.add_argument("-art",
                            "--artiste", 
                            nargs = 2, 
                            metavar=('ARTISTE','QUANTITE'),
                            help = "Indique qu'on spécifie le pourcentage d'un artiste dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", 
                            action="append")
        ''' Paramètre permettant de renseigner le pourcentage d'un album dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
        self.parser.add_argument("-alb",
                            "--album", 
                            nargs = 2, 
                            metavar=('ALBUM','QUANTITE'),
                            help = "Indique qu'on spécifie le pourcentage d'un album dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", 
                            action="append")
    
            