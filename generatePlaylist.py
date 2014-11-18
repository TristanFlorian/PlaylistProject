# -*- coding: utf-8 -*-

import writePlaylist
import controlePourcentageTotal
import connectionBDD
import sqlalchemy
import random
import GestionDesArguments

''' Methode permettant de générer la playliste '''
def genererLaListeDeMorceaux(ligneCLI):
    ''' Methode permettant de générer un morceau de la playliste en fonction d'un paramètre de la CLI '''
    def filtrerListe(listeFinale, listeAFiltrer, quantiteEscomptee, dureePlayliste):
        # Tant que la quantiteEscomptée est > 0, on va retirer un morceau à la liste passée en paramètre pour le stocker ailleurs,
        # puis on réduit la quantiteEscomptée en fonction de la durée du morceau qu'on vient de selectionner,
        # puis on recommence la fonction
        if quantiteEscomptee > 0:
            random.shuffle(listeAFiltrer)
            if (dureePlayliste * 0.05) >= (quantiteEscomptee - listeAFiltrer[0][5]) >= (dureePlayliste * 0.05 * -1):
                morceauChoisi = listeAFiltrer[0]
                listeFinale.append(morceauChoisi)
                quantiteEscomptee -= morceauChoisi.duree
            filtrerListe(listeFinale, listeAFiltrer, quantiteEscomptee, dureePlayliste)
        # Si la quantiteEscomptée est < 0, c'est qu'on a prit le bon nombre de morceaux
        else:
            return listeFinale
    
    ''' Génère la playliste en fonction des arguments optionnels de selection '''
    def makePlaylistWithArguments(ligneCLI, valeurs):
        collectionListesFiltrees = list(list())
        # Pour chaque argument
        for i in range(len(valeurs.getListeDeValeurs())):
            for j in range(len(valeurs.getListeDeValeurs()[i])):
                # On ajoute une musique de la bdd à la playliste,
                # et on vérifie que la somme de la durée est ~= au pourcentage de l'argument renseigné
                if (valeurs.getListeArguments()[i] == 'genre'):
                    playList = list(connect.execute(sqlalchemy.select([tableMorceaux]).where(tableMorceaux.c.genre == valeurs.getListeDeValeurs()[i][j][0])))
                elif (valeurs.getListeArguments()[i] == 'artiste'):
                    playList = list(connect.execute(sqlalchemy.select([tableMorceaux]).where(tableMorceaux.c.artiste == valeurs.getListeDeValeurs()[i][j][0])))
                elif (valeurs.getListeArguments()[i] == 'album'):
                    playList = list(connect.execute(sqlalchemy.select([tableMorceaux]).where(tableMorceaux.c.album == valeurs.getListeDeValeurs()[i][j][0])))
                elif (valeurs.getListeArguments()[i] == 'titre'):
                    playList = list(connect.execute(sqlalchemy.select([tableMorceaux]).where(tableMorceaux.c.titre == valeurs.getListeDeValeurs()[i][j][0])))
                elif (valeurs.getListeArguments()[i] == 'sousgenre'):
                    playList = list(connect.execute(sqlalchemy.select([tableMorceaux]).where(tableMorceaux.c.sousgenre == valeurs.getListeDeValeurs()[i][j][0])))
                
                # En fonction de l'argument qu'on traite, on va filtrer les morceaux en fonction de la quantité
                playListFinale = filtrerListe(collectionListesFiltrees,
                                              playList,
                                              valeurs.getListeDeValeurs()[i][j][1] * ligneCLI.getDureePlaylist() / 100 * 60,
                                              ligneCLI.getDureePlaylist() * 60)
                # on passe en parametre la quantite à garder à l'interieur de la sous playlist
                if playListFinale is not None:
                    collectionListesFiltrees.append(playListFinale)
                j += 1
            i += 1
        return collectionListesFiltrees
            
    ''' Génère une playliste totalement aléatoire '''
    def makeRandomPlaylist(ligneCLI):
        collectionListesFiltrees = list(list())
        playList = list(connect.execute(sqlalchemy.select([tableMorceaux])))
        playListFinale = filtrerListe(collectionListesFiltrees,
                                      playList,
                                      ligneCLI.getDureePlaylist() * 60,
                                      ligneCLI.getDureePlaylist() * 60)
        if playListFinale is not None:
            collectionListesFiltrees.append(playListFinale)
        return collectionListesFiltrees
            
            
            
    #On va effectuer les controles de saisies sur le pourcentage total
    print("\tVérification du total de pourcentages saisis...")
    # On effectue le controle des pourcentages
    valeursCLI = GestionDesArguments.Arguments.valeursCLI(ligneCLI.getArgumentsRenseignes() ,controlePourcentageTotal.checkTotal(ligneCLI))
    print('Done !')
    
    global connect
    global tableMorceaux 
    
    # Connexion à la base
    connect = connectionBDD.initConnection()
    print('###################"')
    print(connect)
    # Récupération d'un objet de classe sqlalchemy.table qui représente le contenu de la base mais en objet pythonique
    tableMorceaux = connectionBDD.getTableMorceaux()
    print('###################"')
    print(tableMorceaux)
    print('###################"')
    
    
    print(ligneCLI.getListeArguments())
    if (getattr(ligneCLI.getListeArguments(), 'album') is None
        and getattr(ligneCLI.getListeArguments(), 'artiste') is None
        and getattr(ligneCLI.getListeArguments(), 'genre') is None
        and getattr(ligneCLI.getListeArguments(), 'sousgenre') is None
        and getattr(ligneCLI.getListeArguments(), 'titre') is None):
        thePlaylist = makeRandomPlaylist(ligneCLI)
    else:
        thePlaylist = makePlaylistWithArguments(ligneCLI, valeursCLI)
    
    print("Écriture de la playliste...")
    writeThePlaylistFile(ligneCLI, thePlaylist)
    print("Done !\n\nProfitez bien de votre playliste !")
    #collectionListesFiltrees  
        
        
        
        
def writeThePlaylistFile(ligneCLI, playlist):
    if ligneCLI.getFormat() == 'm3u':
        writePlaylist.writeM3U(ligneCLI, playlist)
    elif ligneCLI.getFormat() == 'xspf':
        writePlaylist.writeXSPF(ligneCLI, playlist)
    elif ligneCLI.getFormat() == 'pls':
        writePlaylist.writePLS(ligneCLI, playlist)