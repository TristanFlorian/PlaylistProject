#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from GestionDesArguments import Arguments

''' Traitement du programme principal '''
# Création de la liste des arguments
listeArgumentsCLI = Arguments.initListeArguments()
# On spécifie la configuration du fichier de log
Arguments.initLoggingConfig()

Arguments.checkListeDesArguments(listeArgumentsCLI)

# Ecriture d'une ligne d'étoiles dans le fichier de log, pour séparrer les infos en fonction de chaque exécution
logging.debug(' *****************************************')
logging.shutdown()
# la commande exit(0) permet de quitter le programme en indiquant qu'il n'y a pas eu d'erreurs
exit(0)