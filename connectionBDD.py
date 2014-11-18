#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlalchemy
import DonneesConnexion

''' On établi la connexion à la base '''
def initConnection():
    return sqlalchemy.create_engine("postgresql://"+ DonneesConnexion.getLogin() +":"+ DonneesConnexion.getMdp() +"@" + DonneesConnexion.getAddress() + "/radio_libre")
    
''' Retourne un objet de classe sqlalchemy.Table qui contient la table morceaux de la BDD '''
def getTableMorceaux():
    metadata = sqlalchemy.MetaData()
    tableMorceaux = sqlalchemy.Table('morceaux', metadata,
                                     sqlalchemy.Column('titre', sqlalchemy.String),
                                     sqlalchemy.Column('album', sqlalchemy.String),
                                     sqlalchemy.Column('artiste', sqlalchemy.String),
                                     sqlalchemy.Column('genre', sqlalchemy.String),
                                     sqlalchemy.Column('sousgenre', sqlalchemy.String),
                                     sqlalchemy.Column('duree', sqlalchemy.Integer),
                                     sqlalchemy.Column('format', sqlalchemy.String),
                                     sqlalchemy.Column('polyphonie', sqlalchemy.Integer),
                                     sqlalchemy.Column('chemin', sqlalchemy.String))
    return tableMorceaux