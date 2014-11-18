#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from GestionDesArguments import Arguments
import generatePlaylist

''' Traitement du programme principal '''
# On spécifie la configuration du fichier de log
Arguments.initLoggingConfig()
print("Analyse de la ligne de commande...\n")

# Création de la liste des arguments
listeArgumentsCLI = Arguments.ligneCommande()
listeArgumentsCLI.initListeArguments()

print("Génération de la playliste...")
maPlayliste = generatePlaylist.genererLaListeDeMorceaux(listeArgumentsCLI)

# Ecriture d'une ligne d'étoiles dans le fichier de log, pour séparrer les infos en fonction de chaque exécution
logging.debug(' *****************************************')
logging.shutdown()
# la commande exit(0) permet de quitter le programme en indiquant qu'il n'y a pas eu d'erreurs
exit(0)