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
