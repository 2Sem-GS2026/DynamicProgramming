# CalçadaLivre

Sistema de demonstração de acessibilidade urbana. Permite visualizar em uma cidade, registrar problemas nas calçadas e calcular rotas considerando diferentes perfis de circulação.

O objetivo principal é demonstrar que o menor caminho nem sempre é o caminho mais acessível.

## Integrantes

| Nome completo | RM |
|---|---|
| Enrico Bagli Borges | 562541 |
| Henrique Infanti Coratolo | 561865  |
| João Gabriel Boaventura Marques e Silva | 569298 |

Turma: 2ESR | Disciplina: Dynamic Programming | Global Solution 2026.2 - CitizenTech

## Funcionalidades

- Visualização gráfica da Cidade Modelo com Matplotlib.
- Cadastro de problemas nas calçadas, por lado e intervalo do trecho.
- Tipos de problema: em construção, piso irregular, calçada quebrada, obstáculo e ausência de rampa.
- Persistência dos problemas em JSON.
- Cálculo de rotas com o algoritmo de Dijkstra.
- Memoização do cálculo de rotas, com invalidação quando os problemas mudam.
- Perfil padrão e perfil cadeirante.
- Bloqueio de trechos interditados nos dois lados.

## Tecnologias

- Python 3
- Matplotlib
- JSON
- `heapq` (fila de prioridade do Dijkstra)

## Técnicas algorítmicas

### Grafos: Dijkstra

A cidade é modelada como um grafo não direcionado. Os cruzamentos são os vértices e os trechos de calçada são as arestas, com a distância em metros como peso.

Antes da busca, `rotas.py` filtra os trechos permitidos pelo perfil escolhido e monta a lista de adjacência apenas com eles. O Dijkstra então encontra o menor caminho entre origem e destino. Quando não existe caminho válido, o sistema informa que não há rota disponível.

Complexidade: O((V + E) log V), com V = 20 cruzamentos e E = 33 trechos.

### Programação Dinâmica: memoização

O cálculo de rota é registrado em um cache indexado pela tripla (origem, destino, perfil). Consultas repetidas com os mesmos parâmetros retornam o resultado armazenado, sem executar o Dijkstra novamente.

O cache depende do estado dos trechos. Por isso, ele é limpo sempre que um problema é cadastrado, porque o cadastro altera as interdições e as condições do piso.

Complexidade:
- Consulta inédita: O((V + E) log V), igual ao Dijkstra sem cache.
- Consulta repetida: O(1), com uma busca no dicionário.

A escolha se justifica porque o mapa muda apenas no cadastro de problemas, enquanto as consultas de rota são frequentes. Assim, o cache reaproveita resultados entre cadastros sem arriscar respostas desatualizadas.

## Estrutura

```text
calcadalivre-DynamicProgramming/
├── main.py          # Menu, interface de terminal e visualização
├── cidade.py        # Cruzamentos, coordenadas e conexões da cidade
├── modelos.py       # Estruturas de dados (Trecho e Problema)
├── rotas.py         # Dijkstra, memoização e regras dos perfis
├── problemas.py     # Cadastro, validação, persistência e aplicação de problemas
├── problemas.json   # Problemas cadastrados
├── requirements.txt # Dependências
└── README.md
```

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
python main.py
```

No menu principal:

```text
1 - Visualizar mapa
2 - Cadastrar problema
3 - Calcular rota
4 - Listar problemas
0 - Sair
```

### Cadastrar problema

1. Informe o cruzamento inicial e o cruzamento final (somente as letras).
2. Escolha o lado afetado: esquerdo, direito ou ambos. O lado é definido olhando do cruzamento de origem para o de destino.
3. Informe a distância inicial e final do problema, em metros, medidas a partir do cruzamento inicial.
4. Escolha o tipo e a gravidade (1 leve, 2 médio, 3 grave) e descreva o problema.

### Calcular rota

1. Informe a origem e o destino. Digite `sair` a qualquer momento para voltar ao menu.
2. Escolha o perfil:
   - Padrão: considera a distância e as interdições físicas.
   - Cadeirante: além disso, exige inclinação de até 8,33%, rampa existente e piso em boas condições.

## Regras de acessibilidade

| Tipo de problema | Efeito |
|------------------|--------|
| Em construção | Interdita o lado afetado. Interdição nos dois lados com sobreposição de intervalo bloqueia o trecho. |
| Obstáculo | Mesma regra de "Em construção". |
| Piso irregular | Piso passa a "irregular". Impede somente o perfil cadeirante. |
| Calçada quebrada | Piso passa a "ruim". Impede somente o perfil cadeirante. |
| Ausência de rampa | Remove a rampa do trecho. Impede somente o perfil cadeirante. |

## Limitações conhecidas

- Problemas de piso e rampa são aplicados ao trecho inteiro, mesmo quando cadastrados em apenas um lado.
- A interdição de um só lado não é considerada no cálculo de rotas: o trecho continua disponível pelos dois lados enquanto não houver bloqueio completo.
- A gravidade é armazenada, mas não influencia o cálculo.
- O cálculo trabalha com trechos inteiros, não com calçadas independentes por lado.
