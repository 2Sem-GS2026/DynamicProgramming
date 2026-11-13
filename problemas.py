"""Cadastro e persistência de problemas nas calçadas."""

import json
from pathlib import Path

from cidade import criar_trechos
from modelos import Problema


ARQUIVO_PROBLEMAS = Path(__file__).with_name("problemas.json")

TIPOS_PROBLEMA = [
    "Em construção",
    "Piso irregular",
    "Calçada quebrada",
    "Obstáculo",
    "Ausência de rampa",
]


def carregar_problemas(caminho=ARQUIVO_PROBLEMAS):
    """Carrega os problemas do arquivo JSON."""

    if not caminho.exists():
        return []

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        return [Problema(**item) for item in dados]

    except (json.JSONDecodeError, TypeError, KeyError) as erro:
        raise ValueError(
            f"Não foi possível carregar os problemas: {erro}"
        ) from erro


def salvar_problemas(problemas, caminho=ARQUIVO_PROBLEMAS):
    """Salva os problemas no arquivo JSON."""

    dados = [
        {
            "id": problema.id,
            "trecho_id": problema.trecho_id,
            "lado": problema.lado,
            "inicio": problema.inicio,
            "fim": problema.fim,
            "tipo": problema.tipo,
            "gravidade": problema.gravidade,
            "descricao": problema.descricao,
        }
        for problema in problemas
    ]

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False,
        )


def cadastrar_problema(
    problemas,
    trecho_id,
    lado,
    inicio,
    fim,
    tipo,
    gravidade,
    descricao,
    trechos=None,
):
    """Registra um problema em um lado e intervalo do trecho."""

    if trechos is None:
        trechos = criar_trechos()

    trecho = next(
        (item for item in trechos if item.id == trecho_id),
        None,
    )

    if trecho is None:
        raise ValueError("Trecho não encontrado.")

    if lado not in ("esquerdo", "direito", "ambos"):
        raise ValueError("Lado inválido.")

    if not 0 <= inicio < fim <= trecho.distancia:
        raise ValueError(
            f"O intervalo deve estar entre 0 e {trecho.distancia} metros."
        )

    if tipo not in TIPOS_PROBLEMA:
        raise ValueError("Tipo de problema inválido.")

    if gravidade not in (1, 2, 3):
        raise ValueError("A gravidade deve ser 1, 2 ou 3.")

    if not descricao.strip():
        raise ValueError("A descrição não pode ficar vazia.")

    identificador = max(
        (problema.id for problema in problemas),
        default=0,
    ) + 1

    problema = Problema(
        id=identificador,
        trecho_id=trecho_id,
        lado=lado,
        inicio=round(inicio, 2),
        fim=round(fim, 2),
        tipo=tipo,
        gravidade=gravidade,
        descricao=descricao.strip(),
    )

    problemas.append(problema)

    return problema




def aplicar_problemas(trechos, problemas):

    originais = {
        trecho.id: trecho
        for trecho in criar_trechos()
    }

    intervalos = {
        trecho.id: {
            "esquerdo": [],
            "direito": [],
        }
        for trecho in trechos
    }

    # Tipos que representam impedimento físico de circulação.
    tipos_bloqueio = (
        "Em construção",
        "Obstáculo",
    )

    for trecho in trechos:
        original = originais[trecho.id]

        trecho.piso = original.piso
        trecho.possui_rampa = original.possui_rampa

        trecho.lado_esquerdo_bloqueado = False
        trecho.lado_direito_bloqueado = False
        trecho.bloqueado = False

    for problema in problemas:
        trecho = next(
            (
                item
                for item in trechos
                if item.id == problema.trecho_id
            ),
            None,
        )

        if trecho is None:
            continue

        # Problemas que afetam a condição do piso.
        if problema.tipo == "Piso irregular":
            trecho.piso = "irregular"

        elif problema.tipo == "Calçada quebrada":
            trecho.piso = "ruim"

        elif problema.tipo == "Ausência de rampa":
            trecho.possui_rampa = False

        # Somente problemas que impedem a circulação
        # entram na verificação de bloqueio.
        if problema.tipo not in tipos_bloqueio:
            continue

        if problema.lado in ("esquerdo", "ambos"):
            intervalos[trecho.id]["esquerdo"].append(
                (problema.inicio, problema.fim)
            )

        if problema.lado in ("direito", "ambos"):
            intervalos[trecho.id]["direito"].append(
                (problema.inicio, problema.fim)
            )

    for trecho in trechos:
        intervalos_esquerdo = intervalos[trecho.id]["esquerdo"]
        intervalos_direito = intervalos[trecho.id]["direito"]

        trecho.lado_esquerdo_bloqueado = bool(intervalos_esquerdo)
        trecho.lado_direito_bloqueado = bool(intervalos_direito)

        # Bloqueia a conexão somente quando os dois lados
        # possuem uma interdição no mesmo intervalo.
        for inicio_esquerdo, fim_esquerdo in intervalos_esquerdo:
            for inicio_direito, fim_direito in intervalos_direito:

                inicio_sobreposto = max(
                    inicio_esquerdo,
                    inicio_direito,
                )

                fim_sobreposto = min(
                    fim_esquerdo,
                    fim_direito,
                )

                if inicio_sobreposto < fim_sobreposto:
                    trecho.bloqueado = True
                    break

            if trecho.bloqueado:
                break
