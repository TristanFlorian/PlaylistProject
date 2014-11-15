# -*- coding: utf-8 -*-

import writePlaylist
import controlePourcentageTotal
import connectionBDD
import sqlalchemy
import random

''' Methode permettant de générer la playliste '''
def genererLaListeDeMorceaux(valeursCLI):
    global connect
    playlist = list()
    # Connexion à la base
    connect = connectionBDD.initConnection()
    # Récupération d'un objet de classe sqlalchemy.table qui représente le contenu de la base mais en objet pythonique
    tableMorceaux = connectionBDD.getTableMorceaux()
    
    # Pour chaque argument
    for i in range(len(valeursCLI.getListeArguments())):
        # On ajoute une musique de la bdd à la playliste,
        # et on vérifie que la somme de la durée est ~= au pourcentage de l'argument renseigné
        addedSum = 0
        while (controlePourcentageTotal.getSumOfOneArgument(valeursCLI.getListeDeValeurs()[i])-5) < addedSum < (controlePourcentageTotal.getSumOfOneArgument(valeursCLI.getListeDeValeurs()[i])+5):
            playlist[i].append(list())
            # En fonction de l'argument qu'on traite, on va changer le critère de selection de la requête
            if valeursCLI.getListeArguments()[i] == 'titre':
                # Faire une requete pour ajouter une musique correspondant à l'argument renseigné
                playlist[i] = sqlalchemy.select([tableMorceaux]).where(tableMorceaux.c.titre == valeursCLI.getListeDeValeurs()[i][0][0])
            elif valeursCLI.getListeArguments()[i] == 'genre':
                playlist[i] = sqlalchemy.select([tableMorceaux]).where(tableMorceaux.c.genre == valeursCLI.getListeDeValeurs()[i][0][0])
            elif valeursCLI.getListeArguments()[i] == 'sousgenre':
                playlist[i] = sqlalchemy.select([tableMorceaux]).where(tableMorceaux.c.sousgenre == valeursCLI.getListeDeValeurs()[i][0][0])
            elif valeursCLI.getListeArguments()[i] == 'artiste':
                playlist[i] = sqlalchemy.select([tableMorceaux]).where(tableMorceaux.c.artiste == valeursCLI.getListeDeValeurs()[i][0][0])
            elif valeursCLI.getListeArguments()[i] == 'album':
                playlist[i] = sqlalchemy.select([tableMorceaux]).where(tableMorceaux.c.album == valeursCLI.getListeDeValeurs()[i][0][0])
            else:
                print("PROBLEME !!!")
            
            # On ajoute à la somme, la durée du morceau ajouté
            addedSum += playlist[i][5]
            print("sum : " + str(addedSum))
        i += 1
    random.shuffle(playlist)
    return playlist   
        
def writeThePlaylistFile(ligneCLI, playlist):
    if ligneCLI.getFormat() == 'm3u':
        writePlaylist.writeM3U(ligneCLI, playlist)
    elif ligneCLI.getFormat() == 'xspf':
        writePlaylist.writeXSPF(ligneCLI, playlist)
    elif ligneCLI.getFormat() == 'pls':
        writePlaylist.writePLS(ligneCLI, playlist)