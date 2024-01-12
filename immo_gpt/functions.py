import enchant

d = enchant.Dict("fr_FR")
d.check("Salut")
d.check("Salu")
d.suggest("chanbre")