# -*- coding: utf-8 -*-

'''Ecriture du fichier de playlist au format M3U'''
def writeM3U(ligneCLI, playlist):
    playlistFileName = ligneCLI.getNomPlaylist() +"."+ ligneCLI.getFormat()
    playlistFile = open(playlistFileName, 'w')
    playlistFile.write("#EXTM3U\n\n")
    dureeTotale = 0
    for musique in playlist:
        playlistFile.write("#EXTINF:" + str(musique[5]) + 
                           ", " + musique[2] + 
                           " - " + musique[0] + "\n")
        playlistFile.write(musique[8] + "\n\n")
        dureeTotale += musique[5]
    #print("Durée de la playlist : " + str(dureeTotale) + " secondes")
    playlistFile.close()

'''Ecriture du fichier de playlist au format XSPF'''
def writeXSPF(listeArgumentsCLI, playlist):
    # Ouverture du fichier maPlayliste.monFormat, ou création de celui-ci s'il n'existe pas
    playlistFileName = listeArgumentsCLI.getNomPlaylist() +"."+ listeArgumentsCLI.getFormat()
    playlistFile = open(playlistFileName, 'w')
    # On écrit l'entête du fichier xml de la playliste
    playlistFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"+
                       "<playlist version=\"1\" xmlns=\"http://xspf.org/ns/0/\">\n"+
                       "\t<title>"+ playlistFileName +"</title>\n"+
                       "\t<trackList>\n")
    # Pour chaque musique dans la playliste,
    for musique in playlist:
        # On renseigne le chemin, le titre, l'artiste, l'album et la durée (en millisecondes) du morceau,
        playlistFile.write("\n\t\t<track>\n\t\t\t<location>file://"+ musique[8] +"</location>\n"+
                           "\t\t\t<title>"+ musique[0] +"</title>\n"+
                           "\t\t\t<creator>"+ musique[2] +"</creator>\n"+
                           "\t\t\t<album>"+ musique[1] +"</album>\n"+
                           "\t\t\t<duration>"+ str(musique[5]*1000) +"</duration>\n"+
                           "\t\t</track>\n")
        playlistFile.write("\t</trackList>\n</playlist>")
    playlistFile.close()

'''Ecriture du fichier de playlist au format PLS'''
def writePLS(listeArgumentsCLI, playlist):
    i=1
    # Ouverture du fichier maPlayliste.monFormat, ou création de celui-ci s'il n'existe pas
    playlistFileName = listeArgumentsCLI.getNomPlaylist() +"."+ listeArgumentsCLI.getFormat()
    playlistFile = open(playlistFileName, 'w')
    # Écriture de la playliste en fonction de la playliste générée avec la base de données
    playlistFile.write("[playlist]\n\nNumberOfEntries=" + str(len(playlist)) + "\n\n")
    # Pour chaque musique dans la playliste,
    for musique in playlist:
        # On renseigne le nom du morceau,
        playlistFile.write("File"+ str(i) +"="+ musique[4] +"\n")
        # son titre,
        playlistFile.write("Title"+ str(i) +"="+ musique[0] + "\n")
        # et sa durée en millisecondes
        playlistFile.write("Length"+ str(i) +"="+ str(musique[3]) + "\n\n")
        i += 1
    playlistFile.write("\nVersion=2")
    playlistFile.close()
