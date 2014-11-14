#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from GestionDesArguments import Arguments
import generatePlaylist

''' Traitement du programme principal '''
# On spécifie la configuration du fichier de log
Arguments.initLoggingConfig()
# Création de la liste des arguments
listeArgumentsCLI = Arguments.ligneCommande()
listeArgumentsCLI.initListeArguments()

# On effectue le controle des pourcentages
valeursDeLaCLI = Arguments.valeursCLI(generatePlaylist.checkTotal(listeArgumentsCLI.makeValuesList()), listeArgumentsCLI.argumentsRenseignes)
print(valeursDeLaCLI.getListeDeValeurs())
for i in range(len(valeursDeLaCLI.getListeArguments())):
    print("i = " + str(i) + "\tvaleur : " + str(valeursDeLaCLI.getListeArguments()[i]))
    print(valeursDeLaCLI.getListeDeValeurs()[i])


# Ecriture d'une ligne d'étoiles dans le fichier de log, pour séparrer les infos en fonction de chaque exécution
logging.debug(' *****************************************')
logging.shutdown()
# la commande exit(0) permet de quitter le programme en indiquant qu'il n'y a pas eu d'erreurs
exit(0)