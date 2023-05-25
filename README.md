# dps-rotation-gen

Evolutionary Selection Algorithm to generate and rank dps rotations by dps
mu - number of parents each iter
lambda - size of population
lambda/mu - children per parent

create valid population
score population against fitness fn
rank population
select parents
*mutate parents for children*
replace population with children (inclusive?)

issues:
add logic to guarantee a valid ability is selected within n random tries
implement preserving relative order to promote comboing needle strike with strong abilities

ideas on training mutation algorithm to promote good rotations
if parents ability in same order in rotation precedes abilities with high inflated base damage add a stronger weight to this ability
track combos of any size
small rotations of 2-20 abilities in order which gravitate together with a higher weight the higher the inflated dps is

goal of a good rotation is to take each ability and use them in an order which maximizes the special effects of each ability to inflate base damage as high as possible

ensure long duration buffs benefit high damaging abilities with percentage damage buffs (early deaths swiftness)
increases flat damage of multihitting abilities (ecb before sgb bleeds grico)

weigh ratio of proximity to damage increase relationship of each ability and store them in a matrix that updates slightly with each generation based on top 5 parents?

drive 9