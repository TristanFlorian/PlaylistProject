
def checkTotal(listeDeValeurs):
    # Si la liste contient des valeurs Nulles, on initialise ces valeurs avec (1 ÷ nbDeValeurs * 100)
    if (contientDesNone(listeDeValeurs)):
        listeDeValeurs = refactorisationDesValeursNulles(listeDeValeurs)
    # Si elle est inférieure à 100, on remet toutes les valeurs de la liste sur une base 100
    if (getSumFromList(listeDeValeurs) < 100 or getSumFromList(listeDeValeurs) > 100):
        listeDeValeurs = miseEnBaseCent(listeDeValeurs)
        
    
''' Retourne la somme des valeurs de la liste passée en paramètres '''
def getSumFromList(listeDeValeurs):
    sommeDesValeurs = 0
    # On additionne chaque valeur de la liste à la sommeDesValeurs
    for i in listeDeValeurs:
        sommeDesValeurs += listeDeValeurs[i]
        i += 1
    return sommeDesValeurs

''' Parcours la liste passée en paramètre et retourne True si une des valeurs est None '''
def contientDesNone(listeDeValeurs):
    trouve = False
    for i in listeDeValeurs:
        if (listeDeValeurs[i] is None):
            trouve = True
        i += 1
    return trouve

''' Pour chaque valeur Nulle dans la liste, on lui attribue la valeur : 1 ÷ nbDeValeurs * 100 ; Puis on retourne la liste modifiée '''
def refactorisationDesValeursNulles(listeDeValeurs):
    for i in listeDeValeurs:
        if (listeDeValeurs[i] is None):
            listeDeValeurs[i] = 1 / len(listeDeValeurs) * 100
        i += 1
    return listeDeValeurs

''' Rebase les valeurs sur 100 '''
def miseEnBaseCent(listeDeValeurs):
    for i in listeDeValeurs:
        listeDeValeurs[i] = listeDeValeurs / (100 / len(listeDeValeurs))
        i += 1
    return listeDeValeurs