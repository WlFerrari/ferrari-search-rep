from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        pilha = [(initial, 0)]
        menor_profundidade = {initial.tiles: 0}
        expandidos = 0
        gerados = 1
        maior_fronteira = 1

        if not initial.is_solvable:
            return SearchResult(None, expandidos, gerados, maior_fronteira)

        while pilha:
            atual, profundidade = pilha.pop()
            if profundidade > menor_profundidade.get(atual.tiles, self.depth_limit + 1):
                continue
            if atual.is_goal:
                return SearchResult(
                    atual,
                    expandidos,
                    gerados,
                    maior_fronteira,
                    profundidade,
                )
            if profundidade >= self.depth_limit:
                continue

            expandidos += 1
            filhos = atual.neighbors()
            gerados += len(filhos)
            for vizinho in reversed(filhos):
                proxima_profundidade = profundidade + 1
                profundidade_anterior = menor_profundidade.get(vizinho.tiles)
                if profundidade_anterior is not None and profundidade_anterior <= proxima_profundidade:
                    continue
                menor_profundidade[vizinho.tiles] = proxima_profundidade
                pilha.append((vizinho, proxima_profundidade))

            maior_fronteira = max(maior_fronteira, len(pilha))

        return SearchResult(None, expandidos, gerados, maior_fronteira)
