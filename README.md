# DynamicProgramming

# CalçadaLivre

## Ficha da CitizenTech

| Campo | Preenchimento |
|---|---|
| Nome da CitizenTech | CalçadaLivre |
| Cidade e bairro | São Paulo, Bela Vista |
| Cidadão beneficiado | Pessoas com mobilidade reduzida (cadeirantes, idosos, pessoas com carrinho de bebê) que circulam a pé pelo trecho. Perfil entrevistado: adulto de 35 a 45 anos, usuário de cadeira de rodas manual, que se desloca diariamente do metrô Trianon-MASP até o trabalho, na região da Av. Paulista. Hoje evita calçadas com degraus, buracos e obstruções por tentativa e erro, sem informação prévia sobre o estado do trecho. |
| Problema, em uma frase | Pessoas com mobilidade reduzida não sabem quais calçadas estão livres ou obstruídas antes de sair de casa e acabam encontrando barreiras no meio do caminho. |
| Como funciona | Moradores registram obstáculos nas calçadas (buraco, degrau, obstrução, falta de rampa). O sistema guarda os registros, marca cada um como verificado ou não, sugere rotas acessíveis e ajuda a priorizar o que deve ser consertado. |
| O que cada parte faz | **Agile:** documenta o design da solução. **Database:** estrutura e guarda trechos, ocorrências e usuários no Oracle. **DDD-Java:** API REST sobre o banco. **Dynamic Programming:** calcula a melhor rota acessível em grafo. **AR-VR:** vídeo 3D que simula a rota. **Network:** rede da base comunitária que hospeda o servidor. |
| Link do repositório | https://github.com/2Sem-GS2026 |
| Indicador de impacto | (1) % de trechos com acessibilidade verificada, calculado a partir de `status_verificacao`; (2) tempo médio entre o registro e a resolução de uma ocorrência, calculado a partir de `data_registro` e `data_resolucao`. Os três campos existem no modelo do banco e na API. |
| ODS conectados | **ODS 11 (metas 11.2 e 11.7):** rotas acessíveis facilitam o deslocamento seguro e o acesso a pontos de transporte, e o mapeamento das calçadas busca tornar o espaço público acessível, com atenção a pessoas com deficiência e idosos. **ODS 10 (meta 10.2):** promove a inclusão social e econômica de pessoas com mobilidade reduzida, independentemente de idade ou deficiência. **ODS 9 (meta 9.1):** usa dados colaborativos e tecnologia para apoiar a manutenção da infraestrutura urbana de calçadas, com foco em acesso equitativo. |

## Integrantes

| Nome completo | RM |
|---|---|
| Enrico Bagli Borges | 562541 |
| Henrique Infanti Coratolo | 561865  |
| João Gabriel Boaventura Marques e Silva | 569298 |
