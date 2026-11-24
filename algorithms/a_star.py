import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal_index = tile - 1
            row, column = divmod(index, 3)
            goal_row, goal_column = divmod(goal_index, 3)
            distance += abs(row - goal_row) + abs(column - goal_column)
        return distance

    def search(self, initial: State) -> SearchResult:
        sequence = count()
        frontier = [(self.heuristic(initial), next(sequence), initial)]
        best_cost = {initial.tiles: initial.cost}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        if not initial.is_solvable:
            return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size)

        while frontier:
            _, _, current = heapq.heappop(frontier)
            if current.cost != best_cost.get(current.tiles):
                continue
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
                if neighbor.cost >= best_cost.get(neighbor.tiles, float("inf")):
                    continue
                best_cost[neighbor.tiles] = neighbor.cost
                priority = neighbor.cost + self.heuristic(neighbor)
                heapq.heappush(frontier, (priority, next(sequence), neighbor))

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size)
