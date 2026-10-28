import heapq
import sys


class DisjointSetUnion:
    def __init__(self, size):
        self.parent = list(range(size))
        self.size = [1] * size
        self.component_count = size

    def find(self, vertex):
        while self.parent[vertex] != vertex:
            self.parent[vertex] = self.parent[self.parent[vertex]]
            vertex = self.parent[vertex]
        return vertex

    def union(self, first, second):
        first_root = self.find(first)
        second_root = self.find(second)
        if first_root == second_root:
            return False

        if self.size[first_root] < self.size[second_root]:
            first_root, second_root = second_root, first_root

        self.parent[second_root] = first_root
        self.size[first_root] += self.size[second_root]
        self.component_count -= 1
        return True


def prim_forest(vertex_count, adjacency):
    selected = [False] * vertex_count
    forest_edges = []
    total_cost = 0

    for start in range(vertex_count):
        if selected[start]:
            continue

        selected[start] = True
        candidates = []
        for neighbor, weight in adjacency[start]:
            first, second = sorted((start, neighbor))
            heapq.heappush(candidates, (weight, first, second))

        while candidates:
            weight, first, second = heapq.heappop(candidates)
            if selected[first] and selected[second]:
                continue

            next_vertex = second if selected[first] else first
            selected[next_vertex] = True
            forest_edges.append((weight, first, second))
            total_cost += weight

            for neighbor, next_weight in adjacency[next_vertex]:
                if not selected[neighbor]:
                    edge_first, edge_second = sorted((next_vertex, neighbor))
                    heapq.heappush(
                        candidates, (next_weight, edge_first, edge_second)
                    )

    forest_edges.sort()
    return total_cost, forest_edges


def kruskal_forest(vertex_count, edges):
    dsu = DisjointSetUnion(vertex_count)
    forest_edges = []
    total_cost = 0

    for weight, first, second in sorted(edges):
        if dsu.union(first, second):
            forest_edges.append((weight, first, second))
            total_cost += weight

    forest_edges.sort()
    return total_cost, forest_edges, dsu.component_count


def format_forest(name, total_cost, forest_edges):
    lines = [f"{name} {total_cost} {len(forest_edges)}"]
    lines.extend(
        f"{first} {second} {weight}" for weight, first, second in forest_edges
    )
    return lines


def solve(data):
    values = iter(map(int, data.split()))
    try:
        vertex_count = next(values)
    except StopIteration:
        return ""
    edge_count = next(values)

    adjacency = [[] for _ in range(vertex_count)]
    edges = []
    for _ in range(edge_count):
        first, second, weight = next(values), next(values), next(values)
        if first > second:
            first, second = second, first
        adjacency[first].append((second, weight))
        adjacency[second].append((first, weight))
        edges.append((weight, first, second))

    prim_cost, prim_edges = prim_forest(vertex_count, adjacency)
    kruskal_cost, kruskal_edges, component_count = kruskal_forest(
        vertex_count, edges
    )

    output = [f"COMPONENTS {component_count}"]
    output.extend(format_forest("PRIM", prim_cost, prim_edges))
    output.extend(format_forest("KRUSKAL", kruskal_cost, kruskal_edges))
    agrees = prim_cost == kruskal_cost and len(prim_edges) == len(kruskal_edges)
    output.append(f"AGREEMENT {'YES' if agrees else 'NO'}")
    return "\n".join(output)


if __name__ == "__main__":
    print(solve(sys.stdin.read()))
