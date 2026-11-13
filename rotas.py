import heapq
from cidade import LOCAIS, TRECHOS

PERFIL_PADRAO = "padrao"
PERFIL_CADEIRANTE = "cadeirante"
INCLINACAO_MAXIMA = 8.33

cache_rotas = {}


def limpar_cache_rotas():
    cache_rotas.clear()


def trecho_permitido(trecho, perfil):
    if trecho.bloqueado:
        return False
    if perfil == PERFIL_PADRAO:
        return True
    if perfil == PERFIL_CADEIRANTE:
        if trecho.inclinacao > INCLINACAO_MAXIMA:
            return False
        if not trecho.possui_rampa:
            return False
        if trecho.piso != "bom":
            return False
        return True
    raise ValueError(f"Perfil desconhecido: {perfil}")

def dijkstra(origem, destino, perfil, trechos):
    grafo = {local: [] for local in LOCAIS}
    for trecho in trechos:
        if not trecho_permitido(trecho, perfil):
            continue

        grafo[trecho.origem].append((trecho.destino, trecho.distancia))
        grafo[trecho.destino].append((trecho.origem, trecho.distancia))

    distancias = {
        local: float("inf")
        for local in LOCAIS
    }

    anteriores = {
        local: None
        for local in LOCAIS
    }

    distancias[origem] = 0
    fila = [(0, origem)]

    while fila:
        distancia_atual, atual = heapq.heappop(fila)
        if distancia_atual > distancias[atual]:
            continue
        if atual == destino:
            break
        for vizinho, peso in grafo[atual]:
            nova_distancia = distancia_atual + peso
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                anteriores[vizinho] = atual
                heapq.heappush(fila, (nova_distancia, vizinho))
    if distancias[destino] == float("inf"):
        return None
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]
    caminho.reverse()

    return caminho, round(distancias[destino], 2)


def calcular_rota(origem, destino, perfil=PERFIL_PADRAO, trechos=None):
    if origem not in LOCAIS or destino not in LOCAIS:
        raise ValueError("Origem ou destino não existem no mapa.")
    if perfil not in (PERFIL_PADRAO, PERFIL_CADEIRANTE):
        raise ValueError(f"Perfil desconhecido: {perfil}")
    if origem == destino:
        return [origem], 0
    if trechos is not None:
        return dijkstra(origem, destino, perfil, trechos)

    chave = (origem, destino, perfil)
    if chave not in cache_rotas:
        cache_rotas[chave] = dijkstra(origem, destino, perfil, TRECHOS)
    resultado = cache_rotas[chave]
    if resultado is None:
        return None
    caminho, distancia = resultado
    return list(caminho), distancia