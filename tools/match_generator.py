from random import randint, shuffle

n_obstacles = randint(0, 3)
n_bumps = randint(0, 3)

passengers = [
    "Criança verde",
    "Adulto verde",
    "Criança azul",
    "Adulto azul",
    "Criança marrom",
    "Adulto marrom",
    "Adulto vermelho",
]

shuffle(passengers)
print("Ordem passageiros: ", passengers)


positions = list("ABCDEFGHIJ")
print("Nro. de obstáculos: ", n_obstacles)
if n_obstacles > 0:
    shuffle(positions)
    print("Posições obstaculos: ", positions[:n_obstacles])


print("Nro. lombadas: ", n_bumps)
if n_bumps > 0:
    bump_positions = list(range(1, 21))
    shuffle(bump_positions)
    print("Posições lombadas: ", bump_positions[:n_bumps])


shuffle(positions)
print("Posição inicial: ", positions[0])
print("Orientação: ", "NSLO"[randint(0, 3)])
