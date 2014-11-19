# -*- coding: utf-8 -*-

import writePlaylist
import controlePourcentageTotal
import connectionBDD
import sqlalchemy
import random
import GestionDesArguments

quantiteEscomptee = 0


''' Methode permettant de générer la playliste '''
def genererLaListeDeMorceaux(ligneCLI):

    ''' Methode permettant de générer un morceau de la playliste en fonction d'un paramètre de la CLI '''
    def filtrerListe(listeFinale, listeAFiltrer, dureePlayliste):
        global quantiteEscomptee
        # Si la qté escomptée est supérieure à 0, on va ajouter un morceau à la listeFinale de morceaux
        if quantiteEscomptee > 0:
            random.shuffle(listeAFiltrer)
            # Si en enlevant la durée du morceau selectionné on est toujours dans la marge, on va ajouter le morceau à la playliste
            if(quantiteEscomptee - listeAFiltrer[0][5]) >= (dureePlayliste * 0.05 * -1):
                morceauChoisi = listeAFiltrer[0]
                listeFinale.append(morceauChoisi)
                quantiteEscomptee -= morceauChoisi.duree
                filtrerListe(listeFinale, listeAFiltrer, dureePlayliste)
                # Si la quantiteEscomptée est < 0, c'est qu'on a prit le bon nombre de morceaux
            else :
                return listeFinale
        else:
            return listeFinale


    ''' Permet d'ajouter des morceaux, ayant une durée inférieure ou égale à la durée restante à combler, à la playliste générée précédament '''
    def filtrerListeDureeFaible(listeFinale, listeAFiltrer, dureePlayliste):
        global quantiteEscomptee
        # On mélange la liste
        random.shuffle(listeAFiltrer)
        if listeAFiltrer is not None:
            morceauChoisi = listeAFiltrer.pop()
            # On regarde si (dureeRestante - morceau.duree) >= ((ligneCLI.getDureePlaylist() * 0.05) * -1)
            if (dureePlayliste * 0.05) >= (quantiteEscomptee - morceauChoisi.duree) >= (dureePlayliste * 0.05 * -1):
                listeFinale.append(morceauChoisi)
                quantiteEscomptee -= morceauChoisi.duree
            filtrerListeDureeFaible(listeFinale, listeAFiltrer, dureePlayliste)
        elif (dureePlayliste * 0.05) >= quantiteEscomptee >= (dureePlayliste * 0.05 * -1):
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

                # Quelques variables pour plus de lisibilité
                dureeTotaleDeLaPlayliste = ligneCLI.getDureePlaylist() * 60
                pourcentageDesire = valeurs.getListeDeValeurs()[i][j][1]                        # ex: 20 %
                quantiteDesire = pourcentageDesire * dureeTotaleDeLaPlayliste / 100 * 60        # -> 20*dureeTotale /100
                margeSuperieure = (quantiteDesire * 60 * 0.05)                                  # équivaut à +5% donc 105% total
                margeInferieure = ((quantiteDesire * 60) * 0.05) * -1                           # équivaut à -5% donc 95% total
                
                global quantiteEscomptee
                quantiteEscomptee = pourcentageDesire * dureeTotaleDeLaPlayliste / 100
                # En fonction de l'argument qu'on traite, on va filtrer les morceaux en fonction de la quantité
                playListFinale = filtrerListe(collectionListesFiltrees,
                                                             playList,
                                                             dureeTotaleDeLaPlayliste)
                # Si la dureeRestante n'est pas comprise dans les marges, on va récupérer tous les morceaux (correspondant au critère de selection
                # dont la durée est inférieure à la dureeRestante pour essayer d'en selectionner une dedans
                if (margeSuperieure < quantiteEscomptee or quantiteEscomptee < margeInferieure):
                    # On récupère tous les morceaux dont la durée est inférieure ou égale à la duréeRestante
                    playList = list(connect.execute(sqlalchemy.select([tableMorceaux]).where(tableMorceaux.c.genre == valeurs.getListeDeValeurs()[i][j][0])))
                    # On essaye de selectionner un ou plusieurs morceaux
                    playListFinale, dureeRestante = filtrerListeDureeFaible(playListFinale, playList, quantiteDesire)
                    
                    # Si la duree restante n'est pas comprise dans la marge,
                    # on va tenter d'ajouter le morceau le plus court de la bdd à la playliste
                    if (dureeRestante < margeInferieure):
                        morceauLePlusCourt = list(connect.execute(sqlalchemy.func.min(tableMorceaux.duree)))[0]
                        if (margeSuperieure >= (dureeRestante - morceauLePlusCourt) < margeInferieure):
                            playListFinale.append(morceauLePlusCourt)
                    # Sinon, on affiche un message pour informer l'utilisateur de l'impossibilité d'atteindre la marge
                        else:
                            print("Attention : \nIl n'existe pas de morceau assez petit dans votre base de données permettant de fournir la quantité désiré pour l'argument : ")
                            print(valeurs.getListeDeValeurs()[i][j] + " : '" + valeurs.getListeDeValeurs()[i][j][1] + "'")
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
        quantiteEscomptee = ligneCLI.getDureePlaylist() * 60
        playListFinale = filtrerListe(collectionListesFiltrees,
                                      playList,
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
    # Récupération d'un objet de classe sqlalchemy.table qui représente le contenu de la base mais en objet pythonique
    tableMorceaux = connectionBDD.getTableMorceaux()
    
    if (getattr(ligneCLI.getListeArguments(), 'album') is None
        and getattr(ligneCLI.getListeArguments(), 'artiste') is None
        and getattr(ligneCLI.getListeArguments(), 'genre') is None
        and getattr(ligneCLI.getListeArguments(), 'sousgenre') is None
        and getattr(ligneCLI.getListeArguments(), 'titre') is None):
        thePlaylist = makeRandomPlaylist(ligneCLI)
    else:
        thePlaylist = makePlaylistWithArguments(ligneCLI, valeursCLI)
    
    random.shuffle(thePlaylist)
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