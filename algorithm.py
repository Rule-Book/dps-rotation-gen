import random
fightDuration = 22
generations=10
numParents = 5
numPopulation = 30
numAbilities = 11
numAbilityAttributes = 7 # 0 name, 1 skilltype, 2 adren, 3 damage, 4 cooldown, 5 duration, 6 hits
abilities = [
	['Piercing Shot', 'basic', 9, 90, 3, 1.8, 2],
	['Binding Shot', 'basic', 9, 60, 15, 1.8, 1],
	['Needle Strike', 'basic', 9, 94.2, 5.4, 1.8, 1],
	['Fragmentation Shot', 'basic', 9, 120.6, 15, 1.8, 5],
	['Snipe', 'basic', 9, 172, 10.2, 2.4, 1],
	['Greater Ricochet', 'basic', 9, 160, 10.2, 1.8, 7],
	['Rapid Fire', 'threshold', -15, 451.2, 20.4, 4.8, 8],
	['Snap Shot', 'threshold', -15, 265, 20.4, 1.8, 2],
	['Bombardment', 'threshold', -15, 131.4, 30, 1.8, 1],
	['Tight Bindings', 'threshold', -15, 120, 15, 1.8, 1],
	["Death's Swiftness", 'ultimate', 65, 1.8, 315]
]
abilityWeights = [0 for q in range(numAbilities)]
population = [[0 for q in range(fightDuration+1)] for r in range(numPopulation)] # [i][0] # reserved for total dps, [i][1-fightDuration] reserved for abilities
parents = [[0 for _ in range(fightDuration+1)] for _ in range(numParents)]

#set total dps to -1 to make debugging easier
for z in population:
	z[0] = -1

for z in parents:
	z[0] = -1

def rankPopulation():
    calculateDps()

def sortRank(child):
    return child[0] # total dps

def assignParents():
    population.sort(key=sortRank)
    for i in range(0,numParents):
        parents[i] = population[i]

def generatePopulation(_parents):
    for i in range(0, numPopulation):
        parent = _parents[int(i/int(numPopulation/numParents))] # distributes weights from parents to children at a rate of numParents:numPopulation
        adrenaline = 100
        for j in range(1, fightDuration+1):
            staticOrderweight = 4 # increases static order weight of parent's traits by weight/numAbilities
            #if i > 0:
            #   relativeOrderWeight = 5 
            attempts = 20
            for k in range(0,attempts):
                print('attempt ' +str(k))
                abil = random.random() * numAbilities + staticOrderweight
                if abil > numAbilities:
                    abil = parent[j]
                else:
                    abil = int(abil)
                if not haveAdrenFor(abil, adrenaline):
                    continue
                else:
                    print('set ij to ' +str(abil))
                    population[i][j] = abil
                    break

def haveAdrenFor(abilityInd, adren):
    abilityType = abilities[abilityInd][2]
    if (abilityType == 'threshold' and adren >= 50) or (abilityType == 'ultimate' and adren >= 100):
        return True
    print('no adren')
    return False

def calculateDps():
    for i in population:
        if i in parents and i[0] <= 0:
            continue
        calculateDamageWithModifiers(i)
        children[i][0] = sumDamages()

def sumDamages(damageArray):
    sum = 0
    for num in range(0,fightDuration):
        #print('base damage of abilities[' + str(num) + '] is ' + str(abilities[damageArray[num]][3]))
        print('damage of ind ' + str(num) + ' = ' + str(damageArray[num+1]))
        sum += damageArray[num+1]
    print('sum = ' + str(sum))
    return sum

def calculateDamageWithModifiers(rotation):
    inSwiftness = False # increase damage of abils preceded by deaths switfness within past 38.4s
    bound = False # increase piercing shot damage by 30% if binding shot is within past 9.6s
    unBoundTime = -1 # increase ability-damage of abils preceded by needle strike by 7%
    currentTime = 0
    damageByAbilityIndex = [0 for _ in rotation]
    for j in range(0, len(rotation)):
        if j == 0:
            continue
        print('j is ' + str(j))
        #print('base damage of abilities[' + str(j) + '] is ' + str(abilities[rotation[j]][3]))
        baseDamage = damage = abilities[rotation[j]][3]
        if inSwiftness:
            damage *= 1.5
        elif abilities[rotation[j]][0] == "Death's Swiftness":
            inSwiftness=True
        if abilities[rotation[j]][0] == 'Binding Shot' or 'Tight Bindings':
            bound = True
        elif abilities[rotation[j]][0] == 'Piercing Shot':
            if bound and currentTime < unBoundTime:
                damage *= 1.3
            else:
                bound = False
        if abilities[rotation[j]-1][0] == 'Needle Strike':
            damage += baseDamage * 0.07
        damageByAbilityIndex[j] = damage
        currentTime += abilities[rotation[j]][5]
    rotation[0] = sumDamages(damageByAbilityIndex)
    return damageByAbilityIndex

#child1 = [0 for _ in range(0,fightDuration+1)]
#print(calculateDamageWithModifiers(child1))

#child1 =[0, 4, 5, 2, 4, 9, 2, 10, 3, 4, 2, 7, 2, 1, 1, 3, 7, 6, 8, 8, 2, 0, 4]

for gen in range(0, 1):
    print('generation ' + str(gen))
    generatePopulation(parents)

    rankPopulation()

    assignParents()
    for parent in population:
        print(parent)

# for 
# 	for j
# 		print(parents[i][j] + ', ')
# 	println('')

