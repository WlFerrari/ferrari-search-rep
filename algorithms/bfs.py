from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        fila = deque([initial])
        visitados = {initial.tiles}
        expandidos = 0
        gerados = 1
        maior_fronteira = 1

        if not initial.is_solvable:
            return SearchResult(None, expandidos, gerados, maior_fronteira)

        while fila:
            atual = fila.popleft()
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
                if vizinho.tiles in visitados:
                    continue
                visitados.add(vizinho.tiles)
                fila.append(vizinho)

            maior_fronteira = max(maior_fronteira, len(fila))

        return SearchResult(None, expandidos, gerados, maior_fronteira)
