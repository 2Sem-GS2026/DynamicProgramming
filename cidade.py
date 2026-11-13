import math
from modelos import Trecho

# Coordenadas dos cruzamentos.
# Formato: (x, y).
LOCAIS = {
    "A": (0, 0),
    "B": (10, 0),
    "C": (20, 0),
    "D": (30, 0),
    "E": (40, 0),

    "F": (0, 10),
    "G": (10, 10),
    "H": (20, 10),
    "I": (30, 10),
    "J": (40, 10),

    "K": (0, 20),
    "L": (10, 20),
    "M": (20, 20),
    "N": (30, 20),
    "O": (40, 20),

    "P": (0, 30),
    "Q": (10, 30),
    "R": (20, 30),
    "S": (30, 30),
    "T": (40, 30),
}


# Conexões entre cruzamentos.
# Formato: (origem, destino, inclinação, piso, possui_rampa).
LIGACOES = [
    ("A", "B", 2, "bom", True),
    ("B", "C", 3, "bom", True),
    ("C", "D", 2, "bom", True),
    ("D", "E", 3, "bom", True),

    ("F", "G", 2, "bom", True),
    ("G", "H", 3, "bom", True),
    ("H", "I", 2, "bom", True),
    ("I", "J", 3, "bom", True),

    ("K", "L", 2, "bom", True),
    ("L", "M", 3, "bom", True),
    ("M", "N", 2, "bom", True),
    ("N", "O", 3, "bom", True),

    ("P", "Q", 2, "bom", True),
    ("Q", "R", 3, "bom", True),
    ("R", "S", 2, "bom", True),
    ("S", "T", 3, "bom", True),

    ("A", "F", 2, "bom", True),
    ("F", "K", 3, "bom", True),
    ("K", "P", 2, "bom", True),

    ("B", "G", 2, "bom", True),
    ("G", "L", 3, "bom", True),
    ("L", "Q", 2, "bom", True),

    ("C", "H", 2, "bom", True),
    ("H", "M", 3, "bom", True),
    ("M", "R", 2, "bom", True),

    ("D", "I", 2, "bom", True),
    ("I", "N", 3, "bom", True),
    ("N", "S", 2, "bom", True),

    ("E", "J", 2, "bom", True),
    ("J", "O", 3, "bom", True),
    ("O", "T", 2, "bom", True),

    # Conexões diagonais 
    ("Q", "K", 5, "irregular", True),
    ("I", "O", 2, "bom", True),
    ("G", "M", 2, "bom", True),
    ("G", "C", 5, "irregular", True),
    ("C", "I", 6, "irregular", True),
]


def criar_trechos():
    trechos = []
    for identificador, ligacao in enumerate(LIGACOES, start=1):
        origem, destino, inclinacao, piso, possui_rampa = ligacao
        distancia = math.dist(LOCAIS[origem], LOCAIS[destino])
        trecho = Trecho(id=identificador, origem=origem, destino=destino,
                        distancia=round(distancia, 2), inclinacao=inclinacao, 
                        piso=piso, possui_rampa=possui_rampa)
        trechos.append(trecho)
    return trechos

TRECHOS = criar_trechos()