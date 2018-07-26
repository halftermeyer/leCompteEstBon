
# coding: utf-8

# # Le compte est bon

# On cherche une solution optimale à un tirage du *compte est bon*.

# Ce tirage à la forme d'une liste d'entier représentant les cartes tirées, et d'un entier-objectif.
# Par exemple :
# ```
# cartes = [100, 75, 150, 75, 5, 7]
# objectif = 952
# ```

# ## Une stratégie récursive

# On va considérer tour à tour toutes les bipartitions du multi-ensemble `cartes`. On supposera que pour une bipartition donnée, par exemple $(D, G) = ([100, 75, 5, 7], [75, 150])$, on connait les deux ensembles de nombres calculables $C(D)$ et $C(G)$. On construira à partir de ces deux ensembles et des quatre opérations arithmétiques un nouvel ensemble. 

# In[1]:


# Définition des opérations

def montreCalcul(op, x, y, res, cx, cy):
    return "".join(cx + cy + str(x)+op+str(y)+'='+str(res)+'\n')

# Les opérations sont appliquées à des couples [val, 'calcul']
# On met à jour la façon dont le calcul est effectué avec montreCalcul
def add(x,y):
    return (x[0]+y[0] ,montreCalcul('+',x[0],y[0],x[0]+y[0],x[1],y[1]))
def mult(x,y):
    return (x[0]*y[0], montreCalcul('*',x[0],y[0],x[0]*y[0],x[1],y[1]))
def diff(x,y):
    return (x[0]-y[0], montreCalcul('-',x[0],y[0],x[0]-y[0],x[1],y[1])) if x[0]-y[0] >= 0 else None
def div(x,y):
    return (x[0]//y[0], montreCalcul('/',x[0],y[0],x[0]//y[0],x[1],y[1])) if y[0] != 0 and x[0]%y[0] == 0 else None


operations = [add, mult, diff, div]


# In[2]:


def listeSousListeEtComplement(liste):
    """
    génère toute les bipartitions de la liste sauf les 2 triviales où l'une est vide
    afin que la taille de la liste soit strictement décroissante d'un appel récursif à l'autre
    """
    for i in range (2**len(liste))[1:-1]:
        preums = []
        deuz = []
        ## int -> bin str -> list ex ['0', '1', '0', ...] -> [False, True, False, ...]
        mask = [True if x == '1' else False for x in list(("{0:0"+str(len(liste))+"b}").format(i))]
        for pick_index in range(len(mask)):
            (preums if mask[pick_index] else deuz).append(liste[pick_index])
        yield((preums, deuz))


# In[3]:


def cartesPlusJoli(cartes):
    "transforme la liste d'entier en une liste de [12, 'je prends la carte 12\n']"
    plusjoli = []
    for elem in cartes:
        #plusjoli.append((elem, '[' + str(elem)+ ']\n'))
        plusjoli.append((elem, ''))
    return plusjoli


# In[4]:


def memoize_param_to_string_key(f):
    "mémoïzation d'une fonction prenant en entrée une liste"
    memo = {}
    def helper(x):
        if str(x) not in memo: # on convertit la liste en str car non hashable        
            memo[str(x)] = f(x)
        return memo[str(x)]
    return helper


# In[5]:


@memoize_param_to_string_key
def calculeCalculables(liste):
    """
    calcule récursivement tous les nombres calculables en conservant une manière de le calculer
    si la liste est réduite à une carte, la manière de le calculer est triviale,
    sinon, on calcule les bipartitions, leurs ensembles calculables récursivements,
    et on combine les deux dans une double boucle for pour toutes les opérations + - -' * / /'
    """
    
    if len(liste) < 2:
        return {x[0]: x[1] for x in liste}
    
    possibles = {}
    
    for sousListes in [(calculeCalculables(x[0]), calculeCalculables(x[1]))
                       for x in listeSousListeEtComplement(liste)]:
        possibles.update(sousListes[0])
        possibles.update(sousListes[1])
        for k0,v0 in sousListes[0].items(): #k,v
            for k1,v1 in sousListes[1].items():
                for op in operations:
                    tmp = op([k0,v0],[k1,v1])
                    if tmp is not None:
                        possibles[tmp[0]] = tmp[1]  
    
    return possibles


# In[6]:


from math import fabs

def meilleur (objectif, calculables):
    """
    propose une solution optimale
    retourne la valeur, un calcul et le delta à l'objectif
    """
    best = None
    deltaBest = objectif +1
    for k in calculables:
        delta = fabs(objectif - k)
        if delta <  deltaBest:
            best = k
            deltaBest = delta
    return (best, calculables[best], int(deltaBest))
            


# In[7]:


import time
def resoudrePartie(cartes, objectif):
    debut = time.time()
    joliesCartes = cartesPlusJoli(cartes)
    calculables = calculeCalculables(joliesCartes)
    solution = meilleur (objectif, calculables)
    fin = time.time()
    return solution, fin-debut


# In[8]:


### partie
cartes = [100, 4, 25, 7, 8, 1, 8]
objectif = 652

### calcul
solution, duree = resoudrePartie(cartes, objectif)


### réponse

print('La meilleure solution trouvée en',
       "%.2f" % (duree*1000),
      'ms est',
      solution[0],
      'à ±',
      solution[2],
      "de l'objectif",
      objectif,
      ".")
print('Elle peut être obtenue ainsi :',
      solution[1], sep = "\n")
    

