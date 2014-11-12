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
    ''' Constructeur de la classe '''
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs == 2:
            super(appendTypeQuantite, self).__init__(option_strings, dest, nargs=nargs, **kwargs)
        else:
            logging.error("Option %s nécéssite deux arguments" % option_strings)
    ''' L'appel de la classe '''       
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            quantity = abs(int(values[1]))
            values[1] = quantity if 100 >= quantity > 0 else None
        except ValueError:
            logging.error("La qantité saisie n'est pas un nombre (NaN): '" + values[1] + "'")
            sys.exit(1)
        current_dest_value = getattr(namespace, self.dest)
        if type(current_dest_value) is list:
            logging.debug(current_dest_value)
            logging.debug(values)
            current_dest_value.append(values)
            setattr(namespace, self.dest, current_dest_value)
        else:
            logging.debug(values)
            setattr(namespace, self.dest, [values])
            
''' Classe représentant une ligne de commande, avec ses arguments (positionnels et optionnels) '''
class ligneCommande(object):
    ''' Constructeur de la classe '''
    def __init__(self):
        # Dictionnaire, permettant de générer les différents arguments
        self.nameList = ['titre', 'genre', 'sousgenre', 'artiste', 'album']
        self.arguments = argparse.Namespace()
        self.parser = argparse.ArgumentParser()
        self.ajoutArguments()
    
    def initListeArguments(self):
        self.arguments = self.parser.parse_args()
    
    def getDictionnary(self):
        return self.nameList
    
    def getListeArguments(self):
        return self.parser
    
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
        for nomArgument in self.nameList:
            argument = '-' + nomArgument[0] if (nomArgument[0] != 'a') else '-' + nomArgument[0-3]
            if nomArgument[0] != 'a':
                argument = '-' + nomArgument[0]
            else:
                argument =  '-' + nomArgument[0:4]
            self.parser.add_argument(argument,
                                     '--' + nomArgument,
                                     nargs = 2,
                                     dest = nomArgument,
                                     metavar=(str.upper(nomArgument), 'QUANTITÉ'),
                                     help = "Indique qu'on spécifie le pourcentage d'un " + nomArgument + " dans la playliste. [entier naturel] (Ex: 30 -> 30%%)",
                                     action=appendTypeQuantite)

    ''' Génère une liste de liste de valeurs '''
    def makeValuesList(self):
        # On créer une liste de liste (avec des )
        liste = [[0,0]]
        # Pour chaque argument de la CLI
        for nomArgument in self.nameList:
            # Si l'argument est renseigné
            if getattr(self.parser.parse_args(), nomArgument) is not None:
                # On initialise les compteurs à 0
                i = j = 0
                # Comme chaque argument est une liste de liste, car si on renseigne deux fois --genre,
                # on le stock
                # Ex : Cli : ... --genre Rock 50 --genre Metal 40
                #    -> on a [ ['Rock', 50], ['Metal',40] ]
                # Donc pour chaque liste de l'argument
                while i < len(getattr(self.parser.parse_args(), nomArgument)):
                    while j < len(getattr(self.parser.parse_args(), nomArgument)[i]):
                        # On va mettre les valeurs dans la liste
                        liste[i][j] = [[getattr(self.parser.parse_args(), nomArgument)[i][0], getattr(self.parser.parse_args(), nomArgument)[i][1]]]
                        j = j + 1
                    j = 0
                    i = i + 1
        return liste

def getListArgumentsValues(dictionnary, oneParser):
    values = [[[0,0]]]
    args = oneParser.parse_args()
    # Pour chaque argument dans le parser
    for nomArgument in dictionnary:
        # On initialise les compteurs à 0
        i = j = l = 0
        # Si l'argument est renseigné
        if getattr(args, nomArgument) is not None:
            # Comme chaque argument est une liste de liste, car si on renseigne deux fois --genre,
            # on le stock
            # Ex : Cli : ... --genre Rock 50 --genre Metal 40
            #    -> on a [ ['Rock', 50], ['Metal',40] ]
            # Donc pour chaque liste de l'argument
            while j < len(getattr(args, nomArgument)):
                while l < len(getattr(args, nomArgument)[i]):
                    # On va mettre les valeurs dans la liste
                    values[i][j][l] = [[[getattr(args, nomArgument)[i][0], getattr(args, nomArgument)[i][1]]]]
                    l = l + 1
                l = 0
                j = j + 1
        i = i + 1
            