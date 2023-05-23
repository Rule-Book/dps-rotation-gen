mu - number of parents each iter
lambda - size of population
lambda/mu - children per parent

create valid population
score population against fitness fn
rank population
select parents
*mutate parents for children*
replace population with children (inclusive?)

constants
fightDuration = 23
mu = 5
lam = 30
baseAbilArray[10][7] # parsed from ability calcs.txt
weightAbilArray[baseAbilArray.len]
population[lam][fightDuration] # [i][0] # reserved for total dps, [i][1-fightDuration] reserved for abilities
parents[mu][fightDuration]
generations=10

for generations
	parents = [0,0,0,0,0,...]

	generateChildren(parents)
	calculateDps(children) # stored in [i][0]

	rankPopulation

	selectParents(population)

for i
	for j
		print(parents[i][j] + ', ')
	println('')


generateChildren(parents)
	for i < lam
		for j < fightDuration
			choose parent array as parents[i/mu] associates weights from each parent equally across children
			create weight array for j based on static location and relative location of abils in parent array
			for adrenReq=0; k < 20 && adren < adrenReq; k++
				select weighted random ability
			children[i][j] = selected ability

calculateDps(children)
	for i < lam
		if children[i][0] != 0
			calculateModifiers(children[i])
			children[i][0] = sumDamages()
		

damages[population.len]
translateToDamages(child[]) # translate abilityNo to damage for each index in damage
	for i
		damages[i] = baseAbilArray[child[i]]

sumDamages()
	for j < fightDuration
			sum=0
			for j
				sum=damages[j]+sum
			return sum

calculateModifiers(child[])
	translateToDamages(children[i])
	increase ability-damage of abils preceded by needle strike by 7%
	increase piercing shot damage by 30% if binding shot is within past 9.6s
	increase damage of abils preceded by deaths switfness within past 38.4s

	swift=false
	bound=false
	currentTime=0
	unBoundTime=-1
	for i
		if swift
			damages[i] *= 1.5
		elif i == deaths swiftness
			swift=true
		elif i == binding shot || tight bindings
			bound = true
		elif i == piercing shot 
			if bound && currentTime < unBoundTime
				damages[i] *= 1.3
			else
				bound = false
		elif i == needle && i+1 < child.len
			damages[i+1] *= 1.07
		currentTime += i.duration
