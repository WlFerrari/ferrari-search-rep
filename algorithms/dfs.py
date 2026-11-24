from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [(initial, 0)]
        best_depth = {initial.tiles: 0}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        if not initial.is_solvable:
            return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size)

        while frontier:
            current, depth = frontier.pop()
            if depth > best_depth.get(current.tiles, self.depth_limit + 1):
                continue
            if current.is_goal:
                return SearchResult(
                    current,
                    nodes_expanded,
                    nodes_generated,
                    max_frontier_size,
                    depth,
                )
            if depth >= self.depth_limit:
                continue

            nodes_expanded += 1
            children = current.neighbors()
            nodes_generated += len(children)
            for neighbor in reversed(children):
                next_depth = depth + 1
                previous_depth = best_depth.get(neighbor.tiles)
                if previous_depth is not None and previous_depth <= next_depth:
                    continue
                best_depth[neighbor.tiles] = next_depth
                frontier.append((neighbor, next_depth))

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size)
