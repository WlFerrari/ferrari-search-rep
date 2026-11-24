from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        frontier = deque([initial])
        discovered = {initial.tiles}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        if not initial.is_solvable:
            return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size)

        while frontier:
            current = frontier.popleft()
            if current.is_goal:
                return SearchResult(
                    current,
                    nodes_expanded,
                    nodes_generated,
                    max_frontier_size,
                    len(current.path()) - 1,
                )

            nodes_expanded += 1
            for neighbor in current.neighbors():
                nodes_generated += 1
                if neighbor.tiles in discovered:
                    continue
                discovered.add(neighbor.tiles)
                frontier.append(neighbor)

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size)
