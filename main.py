#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from GestionDesArguments import Arguments
import generatePlaylist
from GestionDesArguments.Arguments import ligneCommande

''' Traitement du programme principal '''
# On spécifie la configuration du fichier de log
Arguments.initLoggingConfig()
# Création de la liste des arguments
listeArgumentsCLI = Arguments.ligneCommande()
listeArgumentsCLI.initListeArguments()

dictionnaire = listeArgumentsCLI.getDictionnary()
arguments = listeArgumentsCLI.getListeArguments()
listeDeValeurs = Arguments.getListArgumentsValues(dictionnaire, arguments)
print(listeDeValeurs)
# On effectue le controle des pourcentages
#liste = generatePlaylist.checkTotal(listeArgumentsCLI.getListeArguments())


# Ecriture d'une ligne d'étoiles dans le fichier de log, pour séparrer les infos en fonction de chaque exécution
logging.debug(listeArgumentsCLI)
logging.debug(' *****************************************')
logging.shutdown()
# la commande exit(0) permet de quitter le programme en indiquant qu'il n'y a pas eu d'erreurs
exit(0)