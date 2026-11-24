import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distancia = 0
        for posicao, peca in enumerate(state.tiles):
            if peca == 0:
                continue
            destino = peca - 1
            linha, coluna = divmod(posicao, 3)
            linha_final, coluna_final = divmod(destino, 3)
            distancia += abs(linha - linha_final) + abs(coluna - coluna_final)
        return distancia

    def search(self, initial: State) -> SearchResult:
        abertos = [(self.heuristic(initial), initial)]
        menor_custo = {initial.tiles: initial.cost}
        expandidos = 0
        gerados = 1
        maior_fronteira = 1

        if not initial.is_solvable:
            return SearchResult(None, expandidos, gerados, maior_fronteira)

        while abertos:
            _, atual = heapq.heappop(abertos)
            if atual.cost != menor_custo.get(atual.tiles):
                continue
            if atual.is_goal:
                return SearchResult(
                    atual,
                    expandidos,
                    gerados,
                    maior_fronteira,
                    len(atual.path()) - 1,
                )

            expandidos += 1
            for vizinho in atual.neighbors():
                gerados += 1
                if vizinho.cost >= menor_custo.get(vizinho.tiles, float("inf")):
                    continue
                menor_custo[vizinho.tiles] = vizinho.cost
                prioridade = vizinho.cost + self.heuristic(vizinho)
                heapq.heappush(abertos, (prioridade, vizinho))

            maior_fronteira = max(maior_fronteira, len(abertos))

        return SearchResult(None, expandidos, gerados, maior_fronteira)
