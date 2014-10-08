#!/usr/bin/python3
# -*- coding: utf-8 -*-

import motDePasse
import sqlalchemy

# Déclaration et connexion au moteur sql utilisé
engine = sqlalchemy.create_engine('postgresql://f.thierry:' + motDePasse.getMdp() + '@172.16.99.2:5432/radio_libre')
# Connexion à la base
conn = engine.connect()
# Déclaration et initialisation des metadata
metadata = sqlalchemy.MetaData()
# Création de la sqlalchemy.Stringucture de la bdd
morceaux = sqlalchemy.Table('morceaux', metadata, 
                            sqlalchemy.Column('titre', sqlalchemy.String, primary_key = True), 
                            sqlalchemy.Column('album', sqlalchemy.String), sqlalchemy.Column('artiste', sqlalchemy.String), 
                            sqlalchemy.Column('genre', sqlalchemy.String), sqlalchemy.Column('sousgenre', sqlalchemy.String), 
                            sqlalchemy.Column('duree', sqlalchemy.Integer), sqlalchemy.Column('format',sqlalchemy.String), 
                            sqlalchemy.Column('polyphonie',sqlalchemy.Integer), sqlalchemy.Column('chemin',sqlalchemy.String))
# Affichage du contenu de la table morceaux
s = sqlalchemy.select([morceaux]).where(morceaux.c.titre == 'Toxic')
result = conn.execute(s)

for row in result:
    print(row)