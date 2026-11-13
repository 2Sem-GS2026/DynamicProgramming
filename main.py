import math
import cidade
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from rotas import (PERFIL_PADRAO, PERFIL_CADEIRANTE, calcular_rota, limpar_cache_rotas)
from problemas import (TIPOS_PROBLEMA,aplicar_problemas, carregar_problemas, cadastrar_problema, salvar_problemas)

COR_NORMAL = "green"
COR_PROBLEMA = "red"
COR_BLOQUEADO = "black"

figura_mapa = None

def obter_lados(trecho):
    x1, y1 = cidade.LOCAIS[trecho.origem]
    x2, y2 = cidade.LOCAIS[trecho.destino]
    dx = x2 - x1
    dy = y2 - y1
    distancia = math.hypot(dx, dy)
    deslocamento_x = -(dy / distancia) * 0.7
    deslocamento_y = (dx / distancia) * 0.7
    esquerdo = ((x1 + deslocamento_x, y1 + deslocamento_y),  (x2 + deslocamento_x, y2 + deslocamento_y))
    direito = ((x1 - deslocamento_x, y1 - deslocamento_y), (x2 - deslocamento_x, y2 - deslocamento_y))
    return esquerdo, direito


def desenhar_mapa(origem=None, destino=None, rota=None, destaque=None):
    global figura_mapa
    if figura_mapa is None or not plt.fignum_exists(figura_mapa.number):
        figura_mapa, ax = plt.subplots(figsize=(12, 9))
    else:
        figura_mapa.clear()
        ax = figura_mapa.add_subplot(111)
    fig = figura_mapa
    for trecho in cidade.TRECHOS:
        x1, y1 = cidade.LOCAIS[trecho.origem]
        x2, y2 = cidade.LOCAIS[trecho.destino]
        ax.plot([x1, x2], [y1, y2], color="#cfcfcf", linewidth=7, zorder=2)
        esquerdo, direito = obter_lados(trecho)

        for lado, coordenadas in (("esquerdo", esquerdo), ("direito", direito)):
            estilo = "-"
            if destaque == trecho.id:
                cor, largura = "#ff00ff", 5
            elif trecho.bloqueado:
                cor, largura = COR_BLOQUEADO, 4
            elif lado == "esquerdo" and trecho.lado_esquerdo_bloqueado:
                cor, largura = COR_BLOQUEADO, 4
            elif lado == "direito" and trecho.lado_direito_bloqueado:
                cor, largura = COR_BLOQUEADO, 4
            elif not trecho.possui_rampa:
                cor, largura, estilo = COR_PROBLEMA, 3, "--"
            elif trecho.piso == "ruim":
                cor, largura = "firebrick", 3
            elif trecho.piso == "irregular":
                cor, largura = "orange", 3
            else:
                cor, largura = COR_NORMAL, 3

            xs = [coordenadas[0][0], coordenadas[1][0]]
            ys = [coordenadas[0][1], coordenadas[1][1]]
            ax.plot(xs, ys, color=cor, linewidth=largura, linestyle=estilo, solid_capstyle="round", zorder=3)

        # Número do trecho.
        meio_x = (x1 + x2) / 2
        meio_y = (y1 + y2) / 2
        ax.annotate(str(trecho.id), (meio_x, meio_y), xytext=(0, 5), textcoords="offset points", fontsize=9, 
                    fontweight="bold", color="#ffffff", ha="center", va="center", 
                    bbox=dict(facecolor="#7c3aed", edgecolor="#ffffff", boxstyle="round,pad=0.3", linewidth=1),
                    zorder=8)
    if rota:
        coordenadas = [cidade.LOCAIS[local] for local in rota]
        ax.plot([p[0] for p in coordenadas], [p[1] for p in coordenadas], color="blue", linewidth=3, marker="o", label="Rota calculada", zorder=5)
    for nome, (x, y) in cidade.LOCAIS.items():
        cor = "#172554"
        if nome == origem:
            cor = "#2563eb"
        elif nome == destino:
            cor = "#dc2626"
        ax.scatter(x, y, color=cor, edgecolors="#00e5ff", linewidths=1.5, s=75, zorder=6)
        ax.annotate(nome, (x, y), xytext=(0, 10), textcoords="offset points", fontsize=11, fontweight="bold", color="#00e5ff", ha="center", va="center", bbox=dict(facecolor="#172554", edgecolor="#00e5ff", boxstyle="round,pad=0.3", linewidth=1.2), zorder=9)
    legenda = [
        Line2D([0], [0], color="green", linewidth=3, label="Calçada livre"),
        Line2D([0], [0], color="black", linewidth=4, label="Calçada obstruída"),
        Line2D([0], [0], color="orange", linewidth=3, label="Piso irregular"),
        Line2D([0], [0], color="firebrick", linewidth=3, label="Piso ruim"),
        Line2D([0], [0], color=COR_PROBLEMA, linewidth=3, linestyle="--", label="Sem rampa"),
        Line2D([0], [0], color="#ff00ff", linewidth=5, label="Trecho selecionado"),
        Line2D([0], [0], color="#cfcfcf", linewidth=7, label="Rua"),
    ]
    if rota:
        legenda.append(Line2D([0], [0], color="blue", linewidth=3, marker="o", label="Rota calculada"))
    ax.legend(handles=legenda, loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0, fontsize=9, frameon=True, title="Legenda")
    ax.set_title("CalçadaLivre - Cidade Modelo", fontsize=16, fontweight="bold")
    ax.set_xlabel("Distância (metros)")
    ax.set_ylabel("Distância (metros)")
    ax.set_aspect("equal")
    ax.set_xlim(-5, 45)
    ax.set_ylim(-5, 35)
    ax.grid(alpha=0.2)
    fig.subplots_adjust(left=0.08, right=0.78, top=0.92, bottom=0.08)
    fig.canvas.draw_idle()
    plt.show(block=False)
    plt.pause(0.1)

def encontrar_trecho(origem, destino):
    for trecho in cidade.TRECHOS:
        if (trecho.origem == origem and trecho.destino == destino) or (trecho.origem == destino and trecho.destino == origem):
            return trecho
    return None


def cadastrar_problema_interativo(problemas):
    try:
        executar_cadastro(problemas)
    finally:
        fechar_mapa()

def perguntar_tentar_novamente():
    while True:
        resposta = input("Tentar novamente? (s/n): ").strip().lower()
        if resposta in ("s", "n"):
            return resposta == "s"
        print("Responda com 's' ou 'n'.")


def executar_cadastro(problemas):
    desenhar_mapa()
    print("\nCRUZAMENTOS DISPONÍVEIS:")
    print(", ".join(cidade.LOCAIS.keys()))

    while True:
        origem = input("\nCruzamento inicial (ou 'sair' para voltar ao menu): ").strip().upper()
        if origem == "SAIR":
            print("\nRetornando ao menu.")
            return

        destino = input("Cruzamento final (ou 'sair' para voltar ao menu): ").strip().upper()
        if destino == "SAIR":
            print("\nRetornando ao menu.")
            return

        if origem not in cidade.LOCAIS or destino not in cidade.LOCAIS:
            print("Cruzamento inexistente. Escolha uma das letras listadas.")
            continue

        trecho = encontrar_trecho(origem, destino)
        if trecho is None:
            print(f"Não existe conexão direta entre {origem} e {destino}. Escolha outro par.")
            continue

        break

    print(f"\nTrecho selecionado: {trecho.origem} -> {trecho.destino}")
    print(f"Comprimento: {trecho.distancia} metros")
    desenhar_mapa(destaque=trecho.id)
    print("\nOs dois lados do trecho estão destacados no mapa.")
    print(f"Referência: olhando de {trecho.origem} para {trecho.destino}.")

    lados = {"1": "esquerdo", "2": "direito", "3": "ambos"}

    while True:
        print("\nQual lado apresenta o problema?")
        print("1 - Esquerdo")
        print("2 - Direito")
        print("3 - Ambos")
        opcao_lado = input("\nEscolha: ").strip()

        if opcao_lado in lados:
            lado = lados[opcao_lado]
            break

        print("\nOpção inválida.")
        if not perguntar_tentar_novamente():
            print("Cadastro cancelado.")
            return

    while True:
        try:
            inicio = float(input("\nDistância inicial do problema (metros): ").replace(",", "."))
            fim = float(input("Distância final do problema (metros): ").replace(",", "."))
        except ValueError:
            print("\nDistância inválida.")
            if not perguntar_tentar_novamente():
                print("Cadastro cancelado.")
                return
            continue

        if inicio < fim:
            break

        print("\nA distância inicial deve ser menor que a distância final.")
        if not perguntar_tentar_novamente():
            print("Cadastro cancelado.")
            return

    print("\nTIPO DO PROBLEMA")
    for indice, tipo in enumerate(TIPOS_PROBLEMA, start=1):
        print(f"{indice} - {tipo}")
    try:
        opcao_tipo = int(input("\nEscolha o tipo: "))
        if not 1 <= opcao_tipo <= len(TIPOS_PROBLEMA):
            print("\nTipo inválido. Cadastro cancelado.")
            return
        tipo = TIPOS_PROBLEMA[opcao_tipo - 1]
        gravidade = int(input("Quanto esse trecho está ruim? (1 leve, 2 médio, 3 grave): "))
        descricao = input("Descrição do problema: ")

        problema = cadastrar_problema(problemas=problemas, trecho_id=trecho.id,
            lado=lado, inicio=inicio, fim=fim, tipo=tipo, gravidade=gravidade,
            descricao=descricao, trechos=cidade.TRECHOS)

        salvar_problemas(problemas)
        aplicar_problemas(cidade.TRECHOS, problemas)
        limpar_cache_rotas()

        print(f"\nProblema #{problema.id} cadastrado.")
        print(f"Trecho: {trecho.origem} -> {trecho.destino}")
        print(f"Lado: {lado}")
        print(f"Intervalo: {inicio} a {fim} metros")

        esquerdo_obstruido = trecho.lado_esquerdo_bloqueado
        direito_obstruido = trecho.lado_direito_bloqueado
        if trecho.bloqueado:
            print("Os dois lados estão obstruídos. Trecho bloqueado.")
        elif esquerdo_obstruido and direito_obstruido:
            print("Os dois lados possuem obstruções em intervalos diferentes.")
        elif esquerdo_obstruido:
            print("Lado esquerdo obstruído. Lado direito livre.")
        elif direito_obstruido:
            print("Lado direito obstruído. Lado esquerdo livre.")
        else:
            print("Nenhuma obstrução física. Problema registrado como condição de piso ou rampa.")
    except ValueError as erro:
        print(f"\nNão foi possível cadastrar: {erro}")

def listar_problemas(problemas):
    if not problemas:
        print("\nNenhum problema cadastrado.")
        return
    print("\nPROBLEMAS CADASTRADOS")
    for problema in problemas:
        trecho = next((item for item in cidade.TRECHOS if item.id == problema.trecho_id), None)
        if trecho is None:
            continue
        print(f"\nProblema #{problema.id}")
        print(f"Trecho: {trecho.origem} -> {trecho.destino}")
        print(f"Lado: {problema.lado}")
        print(f"Intervalo: {problema.inicio} a {problema.fim} metros")
        print(f"Tipo: {problema.tipo}")
        print(f"Gravidade: {problema.gravidade}")
        print(f"Descrição: {problema.descricao}")


def calcular_e_exibir_rota():
    print("\nCRUZAMENTOS DISPONÍVEIS:")
    print(", ".join(cidade.LOCAIS.keys()))
    while True:
        origem = input("\nOrigem (ou 'sair' para voltar ao menu): ").strip().upper()
        if origem == "SAIR":
            print("\nRetornando ao menu.")
            return
        if origem in cidade.LOCAIS:
            break
        print("Cruzamento inexistente. Escolha uma das letras listadas.")
    while True:
        destino = input("Destino (ou 'sair' para voltar ao menu): ").strip().upper()
        if destino == "SAIR":
            print("\nRetornando ao menu.")
            return
        if destino in cidade.LOCAIS:
            break
        print("Cruzamento inexistente. Escolha uma das letras listadas.")
    while True:
        print("\n1 - Perfil padrão")
        print("2 - Perfil cadeirante")
        opcao = input("\nPerfil (ou 'sair' para voltar ao menu): ").strip().upper()
        if opcao == "SAIR":
            print("\nRetornando ao menu.")
            return
        if opcao == "1":
            perfil = PERFIL_PADRAO
            break
        if opcao == "2":
            perfil = PERFIL_CADEIRANTE
            break
        print("Perfil inválido. Escolha 1 ou 2.")
    try:
        resultado = calcular_rota(origem, destino, perfil)
        if resultado is None:
            print("\nNão existe rota disponível para esse perfil.")
            return
        caminho, distancia = resultado
        print("\nROTA ENCONTRADA")
        print(" -> ".join(caminho))
        print(f"Distância total: {distancia} metros")
        desenhar_mapa(origem=origem, destino=destino, rota=caminho)
    except ValueError as erro:
        print(f"\nErro: {erro}")

def iniciar():
    try:
        problemas = carregar_problemas()
    except ValueError as erro:
        print(erro)
        problemas = []
    aplicar_problemas(cidade.TRECHOS, problemas)
    while True:
        print("\n" + "=" * 40)
        print("             CALÇADALIVRE")
        print("             CIDADE MODELO")
        print("=" * 40)
        print("1 - Visualizar mapa")
        print("2 - Cadastrar problema")
        print("3 - Calcular rota")
        print("4 - Listar problemas")
        print("0 - Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        if opcao == "1":
            desenhar_mapa()
        elif opcao == "2":
            cadastrar_problema_interativo(problemas)
        elif opcao == "3":
            calcular_e_exibir_rota()
        elif opcao == "4":
            listar_problemas(problemas)
        elif opcao == "0":
            print("\nEncerrando o CalçadaLivre.")
            break
        else:
            print("\nOpção inválida.")


def fechar_mapa():
    global figura_mapa
    if figura_mapa is not None:
        plt.close(figura_mapa)
        figura_mapa = None

if __name__ == "__main__":
    iniciar()
