import random
fightDuration = 23 # 21.33 GCDs 38s
generations=200
numParents = 5
numPopulation = 30
numAbilities = 12
noneAbilityInd = numAbilities

abilities = [ # 0 name, 1 skilltype, 2 adren, 3 damage, 4 cooldown, 5 duration, 6 hits
    ['Piercing Shot', 'basic', 9, 90, 3, 1.8, 2],
	['Binding Shot', 'basic', 9, 60, 15, 1.8, 1],
    ['Fragmentation Shot', 'basic', 9, 120.6, 15, 1.8, 5],
    ['Corruption Shot', 'basic', 9, 200, 15, 1.8, 5],
	['Needle Strike', 'basic', 9, 94.2, 5.4, 1.8, 1],
	['Snipe', 'basic', 9, 172, 10.2, 2.4, 1],
	['Greater Ricochet', 'basic', 9, 160, 10.2, 1.8, 7],
	['Rapid Fire', 'threshold', -15, 451.2, 20.4, 4.8, 8],
	['Snap Shot', 'threshold', -15, 265, 20.4, 1.8, 2],
	['Bombardment', 'threshold', -15, 131.4, 30, 1.8, 1],
	['Tight Bindings', 'threshold', -15, 120, 15, 1.8, 1],
    ["Crystal Rain", 'special', -27, 433.25, 30, 1.8, 2.44],
	["Death's Swiftness", 'ultimate', -65, 315, 120, 1.8, 1],
    ["None", 'ultimate', 0, 0, 0, 0, 0]
]
abilityWeights = [0 for _ in range(numAbilities)]
population = [[0 for _ in range(fightDuration)] for _ in range(numPopulation)] # [i][0] # reserved for total dps, [i][1-fightDuration] reserved for abilities
parents = [[0 for _ in range(fightDuration)] for _ in range(numParents)]
parents[0] = [7272.642000000001, 10, 3, 4, 2, 6, 2, 4, 8, 0, 5, 2, 7, 4, 2, 9, 6, 5, 4, 6, 6, 6, 7]
best = [-1 for _ in range(fightDuration)]

def rankPopulation():
    calculateDps()

def sortRank(child):
    return -child[0] # rank input array by total dps

def resetPopulation(pop):
    pop[:] = [[0 for _ in range(fightDuration)] for _ in range(numPopulation)]

def assignParents():
    population.sort(key=sortRank)
    parents[:] = population[:len(parents)]
    if (parents[0][0] > best[0]):
        print('new best ' + str(parents[0][0]))
        best[:] = parents[0]

def generatePopulation(_parents):
    resetPopulation(population)
    population[0] = best
    for i in range(1, numPopulation):
        parent = _parents[int(i/int(numPopulation/numParents))] # distributes weights from parents to children at a rate of numParents:numPopulation
        adrenaline = 100
        cooldowns = [-1 for _ in abilities]
        time = 0
        abil = noneAbilityInd
        for j in range(1, fightDuration):
            if time > 38:
                population[i][j] = noneAbilityInd
                continue
            staticOrderweight = 6 # increases static order weight of parent's traits by weight/numAbilities
            #if i > 0:
            #   relativeOrderWeight = 5 
            attempts = 35
            for _ in range(0,attempts):
                abil = random.random() * (numAbilities + staticOrderweight * (1-(parent[j] == noneAbilityInd)))
                if abil >= numAbilities:
                    abil = parent[j]
                else:
                    abil = int(abil)
                if not haveAdrenFor(abil, adrenaline):
                    continue
                elif time > cooldowns[abil]:
                    adrenaline = min(adrenaline + abilities[abil][2], 100)
                    population[i][j] = abil
                    #print('  abil selected ' + str(abil) + ' ' + str(abilities[abil][0]))
                    cooldowns[abil] = time + abilities[abil][4]
                    time += abilities[abil][5]
                    break
            #print('  cds-' + str(cooldowns))
            #print('  ind#' + str(j) + ' ' + str(population[i]))
        #print(' pop#' + str(i))


def haveAdrenFor(abilityInd, adren):
    abilityType = abilities[abilityInd][1]
    if (abilityType == 'basic') or (abilityType == 'threshold' and adren >= 50) or (abilityType == 'ultimate' and adren >= 100):
        return True
    elif (abilityType == 'special' and adren >= abilities[abilityInd][2]):
        return True
    return False



def calculateDps():
    for i in population:
        if i in parents and i[0] <= 0:
            continue
        calculateDamageWithModifiers(i)

def sumDamages(damageArray):
    sum = 0
    for num in range(1,fightDuration):
        sum += damageArray[num]
    return sum

def calculateDamageWithModifiers(rotation):
    inSwiftness = False # increase damage of abils preceded by deaths switfness within past 38.4s
    bound = False # increase piercing shot damage by 30% if binding shot is within past 9.6s
    unBoundTime = -1 # increase ability-damage of abils preceded by needle strike by 7%
    currentTime = 0
    damageByAbilityIndex = [0 for _ in rotation]
    for j in range(1, len(rotation)):
        baseDamage = damage = abilities[rotation[j]][3]
        if inSwiftness:
            damage *= 1.5
        elif abilities[rotation[j]][0] == "Death's Swiftness":
            inSwiftness=True
        if (abilities[rotation[j]][0] == 'Binding Shot') or (abilities[rotation[j]][0] == 'Tight Bindings'):
            bound = True
            unBoundTime = currentTime + 9.6
        elif abilities[rotation[j]][0] == 'Piercing Shot':
            if bound and currentTime < unBoundTime:
                damage *= 1.3
            else:
                bound = False
        if j > 1 and abilities[rotation[j-1]][int(0)] == 'Needle Strike':
            damage += baseDamage * 0.07
        damageByAbilityIndex[j] = damage
        currentTime += abilities[rotation[j]][5]
    rotation[0] = sumDamages(damageByAbilityIndex)
    return damageByAbilityIndex

#child1 = [0 for _ in range(0,fightDuration)]
#print(calculateDamageWithModifiers(child1))

#child1 =[0, 4, 5, 2, 4, 9, 2, 10, 3, 4, 2, 7, 2, 1, 1, 3, 7, 6, 8, 8, 2, 0, 4]

def translatePrintToNames(child):
    output = child.copy()
    for i in range(0,len(child)):
        if i == 0:
            continue
        output[i] = abilities[int(child[i])][0]
    print(output)

for gen in range(0, generations):
    print('generation ' + str(gen))
    generatePopulation(parents)

    rankPopulation()

    assignParents()

    #for parent in parents:
        #translatePrintToNames(parents[0])
print(best)
translatePrintToNames(best)

# for 
# 	for j
# 		print(parents[i][j] + ', ')
# 	println('')

