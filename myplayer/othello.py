from jogadas_disponiveis import *
import numpy as np
from copy import deepcopy
import sys

class Othello:

    def __init__(self, tabuleiro, jogador):
        self.tabuleiro = self.get_tabuleiro(tabuleiro) if isinstance(tabuleiro, str) else tabuleiro
        self.jogador = jogador
        self.oponente = "W" if jogador == "B" else "B"
        self.folhas = []
        self.PValues = np.array([
            [120,-20,20,5,5,20,-20,120],
            [-20,-40,-5,-5,-5,-5,-40,-20],
            [20,-5,15,3,3,15,-5,20],
            [5,-5,3,3,3,3,-5,5],
            [5,-5,3,3,3,3,-5,5],
            [20,-5,15,3,3,15,-5,20],
            [-20,-40,-5,-5,-5,-5,-40,-20],
            [120,-20,20,5,5,20,-20,120]
        ], dtype="int")

    def get_tabuleiro(self, tabuleiro_nome):
        with open(tabuleiro_nome) as file:
            tabuleiro = [[char for char in file.readline()[:-1]] for _ in range(8)]
            tabuleiro = np.array(tabuleiro).reshape(8, 8)
            return tabuleiro

    def get_melhor_jogada(self, profundidade_maxima=1):
        alfa = -9999999999999999999
        beta = 9999999999999999999
        _, melhor_jogada = self.max(self.tabuleiro, None, self.jogador, 0, profundidade_maxima, alfa, beta)
        return "{},{}".format(*melhor_jogada)

    def max(self, tabuleiro_inicial, jogada, jogador, profundidade_atual, profundidade_maxima, alfa, beta):
        if profundidade_atual == profundidade_maxima:
            return self.get_heuristica(jogada), jogada
        else:
            jogadas_disponiveis = get_jogadas_disponiveis(tabuleiro_inicial, jogador)
            #print(jogadas_disponiveis)
            melhor_jogada = None
            for jogada, posicoes_capturadas in jogadas_disponiveis:
                tabuleiro = deepcopy(tabuleiro_inicial)
                for peca in posicoes_capturadas:
                    tabuleiro[peca[0], peca[1]] = jogador
                oponente = "W" if jogador == "B" else "B"
                utilidade, _ = self.min(tabuleiro, oponente, profundidade_atual, profundidade_maxima, alfa, beta)
                if utilidade > alfa:
                    alfa = utilidade
                    melhor_jogada = jogada
                if beta < alfa:
                    if not melhor_jogada:
                        melhor_jogada = jogada
                    return alfa, melhor_jogada
            if not melhor_jogada:
                melhor_jogada = jogada
            return alfa, melhor_jogada

    def min(self, tabuleiro_inicial, jogador, profundidade_atual, profundidade_maxima, alfa, beta):
        jogadas_disponiveis = get_jogadas_disponiveis(tabuleiro_inicial, jogador)
        pior_jogada = None
        for jogada, posicoes_capturadas in jogadas_disponiveis:
            tabuleiro = deepcopy(tabuleiro_inicial)
            for peca in posicoes_capturadas:
                tabuleiro[peca[0], peca[1]] = jogador
            oponente = "W" if jogador == "B" else "B"
            utilidade, _ = self.max(tabuleiro, jogada, oponente, profundidade_atual+1, profundidade_maxima, alfa, beta)
            if utilidade < beta:
                beta = utilidade
                pior_jogada = jogada
            if alfa > beta:
                return beta, pior_jogada
        return beta, pior_jogada

    def play(self, tab, linha, coluna, jogador):
        novo_tabuleiro = deepcopy(tab)
        novo_tabuleiro[linha, coluna] = jogador
        return novo_tabuleiro

    def get_heuristica(self, jogada):
         return self.PValues[jogada[0], jogada[1]]
         

if __name__ == "__main__":
    arquivo_estado = sys.argv[1]
    jogador_string = sys.argv[2]
    # arquivo_estado = "state.txt"
    # jogador_string = "black"
    if jogador_string == "black":
        jogador = "B"
    else:
        jogador = "W"
    jogo = Othello(f"{arquivo_estado}", jogador)
    melhor_jogada = jogo.get_melhor_jogada(profundidade_maxima=1)
    print(melhor_jogada[::-1])
    # print("*******************")
    # print(jogador, jogador_string, melhor_jogada)
    # print("*******************")
    # with open("move.txt", "w") as file:
    #     file.write(melhor_jogada[::-1])


