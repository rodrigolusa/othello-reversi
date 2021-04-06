from old.jogadas_disponiveis import *
import numpy as np
from copy import deepcopy

class Otelo:

    def __init__(self, tabuleiro, jogador):
        self.tabuleiro = self.get_tabuleiro(tabuleiro) if isinstance(tabuleiro, str) else tabuleiro
        self.jogador = jogador
        self.oponente = "W" if jogador == "B" else "B"
        self.folhas = []

    def get_tabuleiro(self, tabuleiro_nome):
        with open(tabuleiro_nome) as file:
            tabuleiro = [[char for char in file.readline()[:-1]] for _ in range(8)]
            tabuleiro = np.array(tabuleiro).reshape(8, 8)
            return tabuleiro

    def get_melhor_jogada(self, profundidade_maxima=2):
        alfa = -9999999999999999999
        beta = 9999999999999999999
        _, melhor_jogada = self.max(self.tabuleiro, None, self.jogador, 2, profundidade_maxima, alfa, beta)
        return melhor_jogada

    def max(self, tabuleiro_inicial, jogada, jogador, profundidade, profundidade_maxima, alfa, beta):
        if profundidade > profundidade_maxima:
            return self.get_heuristica(tabuleiro_inicial), jogada
        else:
            jogadas_disponiveis = get_jogadas_disponiveis2(tabuleiro_inicial, jogador)
            print(jogadas_disponiveis)
            melhor_jogada = None
            for jogada, posicoes_capturadas, in jogadas_disponiveis:
                tabuleiro = deepcopy(tabuleiro_inicial)
                for peca in posicoes_capturadas:
                    tabuleiro[peca[0], peca[1]] = jogador
                oponente = "W" if jogador == "B" else "B"
                utilidade = self.min(tabuleiro, oponente, profundidade, profundidade_maxima, alfa, beta)
                if utilidade > alfa:
                    alfa = utilidade
                    melhor_jogada = jogada
                if beta < alfa:
                    return alfa, melhor_jogada

            return alfa, melhor_jogada

    def min(self, tabuleiro_inicial, jogador, profundidade, profundidade_maxima, alfa, beta):
        jogadas_disponiveis = get_jogadas_disponiveis(tabuleiro_inicial, jogador)
        for jogada, posicoes_capturadas in jogadas_disponiveis:
            tabuleiro = deepcopy(tabuleiro_inicial)
            for peca in posicoes_capturadas:
                tabuleiro[peca[0], peca[1]] = jogador
            oponente = "W" if jogador == "B" else "B"
            utilidade, _ = self.max(tabuleiro, jogada, oponente, profundidade+1, profundidade_maxima, alfa, beta)
            if utilidade < beta:
                beta = utilidade
            if alfa > beta:
                return beta
        return beta

    def get_heuristica(self, tabuleiro):
        heuristica = 0
        posicoes_capturadas = get_localizacao_pecas(tabuleiro, self.jogador)
        for posicao_x, posicao_y in posicoes_capturadas:
            if posicao_x in [0, 7] or posicao_y in [0, 7]:
                heuristica += 10
            else:
                heuristica += 1
        return heuristica






jogo = Otelo("arquivo_estado_tabuleiro", "B")
print(jogo.get_melhor_jogada())


