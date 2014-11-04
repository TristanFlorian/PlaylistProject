# -*- coding: utf-8 -*-

import logging
import argparse
import sys

''' Renseigne où se situe le fichier de log, est à quel niveau on y inscrit des données '''
def initLoggingConfig():
    logging.basicConfig(filename='le_fichier_de.log',level=logging.DEBUG)
    #logging.basicConfig(level=logging.DEBUG)

''' Classe hérité de la classe action de argparse '''
class appendTypeQuantite(argparse.Action):
    ''' Constructeur '''
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs == 2:
            super(appendTypeQuantite, self).__init__(option_strings, dest, nargs=nargs, **kwargs)
        else:
            logging.error("Option %s must have 2 arguments in its definition" % option_strings)
    
    ''' Ensemble d'instructions lors de l'appel à cette classe '''
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
                            action=appendTypeQuantite)
        ''' Paramètre permettant de renseigner le pourcentage d'un genre dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
        self.parser.add_argument("-g",
                            "--genre",
                            nargs = 2,
                            metavar=('GENRE','QUANTITE'),
                            help = "Indique qu'on spécifie le pourcentage d'un genre dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", 
                            action=appendTypeQuantite)
        ''' Paramètre permettant de renseigner le pourcentage d'un sous-genre dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
        self.parser.add_argument("-sg",
                            "--sousgenre", 
                            nargs = 2, 
                            metavar=('SOUSGENRE','QUANTITE'),
                            help = "Indique qu'on spécifie le pourcentage d'un sous-genre dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", 
                            action=appendTypeQuantite)
        ''' Paramètre permettant de renseigner le pourcentage d'un artiste dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
        self.parser.add_argument("-art",
                            "--artiste", 
                            nargs = 2, 
                            metavar=('ARTISTE','QUANTITE'),
                            help = "Indique qu'on spécifie le pourcentage d'un artiste dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", 
                            action=appendTypeQuantite)
        ''' Paramètre permettant de renseigner le pourcentage d'un album dans la playliste [entier naturel] (Ex: "60" -> 60%) '''
        self.parser.add_argument("-alb",
                            "--album", 
                            nargs = 2, 
                            metavar=('ALBUM','QUANTITE'),
                            help = "Indique qu'on spécifie le pourcentage d'un album dans la playliste. [entier naturel] (Ex: 30 -> 30%%)", 
                            action=appendTypeQuantite)
    
            