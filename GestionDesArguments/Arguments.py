# -*- coding: utf-8 -*-

import logging
import argparse
import sys
import controlePourcentageTotal

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
            values[1] = quantity if 100 >= quantity else None
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
        self.formats = ['m3u','xspf','pls']
        self.arguments = argparse.Namespace()
        self.parser = argparse.ArgumentParser()
        self.ajoutArguments()
        self.format = None
        self.checkFormat()
        self.argumentsRenseignes = list()
        
    
    ''' Initialise l'argument parser '''
    def initListeArguments(self):
        self.arguments = self.parser.parse_args()
    
    ''' Retourne le dictionnaire '''
    def getDictionnary(self):
        return self.nameList
    
    ''' Retourne l'ensemble des arguments ainsi que les valeurs qui y sont associées '''
    def getListeArguments(self):
        return self.parser.parse_args()
        
    def getNomPlaylist(self):
        return (getattr(self.getListeArguments(), 'nom_playlist'))
    
    def getFormat(self):
        return self.format
    
    def getDureePlaylist(self):
        return (getattr(self.getListeArguments(), 'temps_playlist'))
        
    def getArgumentsRenseignes(self):
        return self.argumentsRenseignes
    
    def checkFormat(self):
        if (getattr(self.parser.parse_args(), 'format')) is None:
            self.format = 'm3u'
        else:
            self.format = getattr(self.parser.parse_args(), 'format')[0]
                
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
                            choices=self.formats, 
                            help = "Donne le format de sortie de la playliste " + str(self.formats))
        #Ajout des arguments optionnels en fonction du dictionnaire de la ligneCommande
        for nomArgument in self.nameList:
            # Si l'argument à ajouter est différent de album et artiste,
            # on créer un argument réduit composé de l'initiale uniquement,
            # sinon on créer un argument réduit composé des trois premières lettres de l'argument
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

    ''' Génère une liste de liste de listes de couples de valeurs '''
    def makeValuesList(self):
        # Pour chaque argument du parser
        i = 0
        values = []
        for nomArgument in self.getDictionnary():
            # Si l'argument est renseigné
            if getattr(self.getListeArguments(), nomArgument) is not None:
                # On initialise un compteur à 0
                j = 0
                # Puis on indique qu'il s'agit d'une liste de listes
                values.append(list())
                # Comme chaque argument est une liste de liste, car si on renseigne deux fois --genre,
                # on le stock
                # Ex : Cli : ... --genre Rock 50 --genre Metal 40
                #    -> on a [ ['Rock', 50], ['Metal',40] ]
                while j < len(getattr(self.getListeArguments(), nomArgument)):
                    if getattr(self.getListeArguments(), nomArgument)[j] is not None:
                        # On recréer une nouvelle liste dans la liste de liste au cas où il resterait des valeurs au prochain passage
                        # dans la boucle
                        values[i].append(list())
                        # On range les valeurs dans une nouvelle liste de la liste de l'argument
                        values[i][j].append(getattr(self.getListeArguments(), nomArgument)[j][0])   # Rangement de la chaine
                        values[i][j].append(getattr(self.getListeArguments(), nomArgument)[j][1])   # Rangement du pourcentage
                        j = j + 1
                # On insère le nom de l'argument dans le tableau "argumentsRenseignes" afin de savoir que la première liste de listes de couples
                # de valeurs correspond à l'argument renseigné
                self.argumentsRenseignes.append(nomArgument)
                i = i + 1
        # Puis on retourne le tout
        return values
        
''' Classe permettant de travailler plus facilement avec les valeurs saisies dans la CLI, en associant un dictionnaire à la liste de listes de couples de valeurs '''
class valeursCLI():
    ''' Constructeur de la classe, prenant la liste des valeurs de la CLI et la liste des arguments renseignés, dans leur ordre '''
    def __init__(self, listeArguments, listeDeValeurs):
        self.listeArguments = listeArguments
        self.listeDeValeurs = listeDeValeurs
        self.sumPourcentages = controlePourcentageTotal.getSumFromList(listeDeValeurs)
        
    ''' Accesseur de l'attribut listeArguments '''
    def getListeArguments(self):
        return self.listeArguments
    
    ''' Accesseur de l'attribut listeDeValeurs '''
    def getListeDeValeurs(self):
        return self.listeDeValeurs
    
    ''' Accesseur de l'attribut sumPourcentages '''
    def getSumPourcentages(self):
        return self.getSumPourcentages()
    
    ''' Modificateur de l'attribut listeDeValeurs à partir d'une nouvelle liste de valeurs '''
    def setListeDeValeurs(self,listeDeValeurs):
        self.listeDeValeurs = listeDeValeurs