''' Si la liste de valeurs contient des valeurs nulles, elles sont remplacées ; si la somme des valeurs
est différente de 100, on rebase le tout sur 100 '''
def checkTotal(listeDeValeurs):
    i = 0
    j = 0
    # Si la liste contient des valeurs Nulles, on initialise ces valeurs avec (1 ÷ nbDeValeurs * 100)
    if (contientDesNone(listeDeValeurs)):
        listeDeValeurs = refactorisationDesValeursNulles(listeDeValeurs)
    # Si elle est inférieure à 100, on remet toutes les valeurs de la liste sur une base 100
    if (105 < getSumFromList(listeDeValeurs) < 95):
        listeDeValeurs[i][j] = miseEnBaseCent(listeDeValeurs[i][j])
    # On génère la liste de morceaux en fonction de la liste de pourcentages
    return listeDeValeurs
    
''' Retourne la somme des valeurs de la liste passée en paramètres '''
def getSumFromList(listeDeValeurs):
    sommeDesValeurs = 0
    # On additionne chaque valeur de la liste à la sommeDesValeurs
    for i in range(len(listeDeValeurs)):
        for j in range(len(listeDeValeurs[i])):
            sommeDesValeurs += listeDeValeurs[i][j][1]
            j += 1
        i += 1
    return sommeDesValeurs

''' Parcours la liste passée en paramètre et retourne True si une des valeurs est None '''
def contientDesNone(listeDeValeurs):
    trouve = False
    for i in range(len(listeDeValeurs)):
        for j in range(len(listeDeValeurs[i])):
            if (listeDeValeurs[i][j][1] is None):
                trouve = True
            j += 1
        i += 1
    return trouve

''' Pour chaque valeur Nulle dans la liste, on lui attribue la valeur : 1 ÷ nbDeValeurs * 100 ; Puis on retourne la liste modifiée '''
def refactorisationDesValeursNulles(listeDeValeurs):
    for i in range(len(listeDeValeurs)):
        for j in range(len(listeDeValeurs[i])):
            if (listeDeValeurs[i][j][1] is None):
                listeDeValeurs[i][j][1] = round((1 / getLenListeDeValeurs(listeDeValeurs) * 100),1)
            j+= 1
        i += 1
    return listeDeValeurs

''' Retourne le nombre de paramètres renseignés '''
# Ex : -g xxx xx -art xxx xx -t xxx xx
#  -> On va retourner la valeur 3
#
def getLenListeDeValeurs(listeDeValeurs):
    for i in range(len(listeDeValeurs)):
        for j in range(len(listeDeValeurs[i])):
            j+=1
        i+=1
    return j

''' Rebase les valeurs sur 100 '''
def miseEnBaseCent(listeDeValeurs):
    for i in range(len(listeDeValeurs)):
        for j in range(len(listeDeValeurs[i])):
            listeDeValeurs[i][j][1] = round((listeDeValeurs[i][j][1] / (100 / getLenListeDeValeurs(listeDeValeurs))),1)
        i += 1
    return listeDeValeurs

''' Methode permettant de générer la playliste '''
def genererLaListeDeMorceaux(listeDeValeurs):
    pass
    #for i in 
    
    
def genererLaPlayListe(listeDeMorceaux, leFormat):
    if leFormat == 'm3u':
        pass