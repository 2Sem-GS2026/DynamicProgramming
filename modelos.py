from dataclasses import dataclass

@dataclass
class Trecho:
    id: int
    origem: str
    destino: str
    distancia: float
    inclinacao: float
    piso: str
    possui_rampa: bool
    bloqueado: bool = False
    lado_esquerdo_bloqueado: bool = False
    lado_direito_bloqueado: bool = False


@dataclass
class Problema:
    id: int
    trecho_id: int
    lado: str
    inicio: float
    fim: float
    tipo: str
    gravidade: int
    descricao: str
