import itertools
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_FILE = PROJECT_ROOT / "main.py"


class MinimumForestTests(unittest.TestCase):
    def run_program(self, input_text):
        result = subprocess.run(
            [sys.executable, str(MAIN_FILE)],
            input=input_text,
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout.strip()

    def test_single_isolated_vertex(self):
        self.assertEqual(
            self.run_program("1 0\n"),
            "COMPONENTS 1\nPRIM 0 0\nKRUSKAL 0 0\nAGREEMENT YES",
        )

    def test_disconnected_graph_cycle_and_isolate(self):
        self.assertEqual(
            self.run_program("5 4\n0 1 4\n1 2 2\n0 2 3\n3 4 1\n"),
            "COMPONENTS 2\n"
            "PRIM 6 3\n3 4 1\n1 2 2\n0 2 3\n"
            "KRUSKAL 6 3\n3 4 1\n1 2 2\n0 2 3\n"
            "AGREEMENT YES",
        )

    def test_equal_weights_and_reversed_endpoints(self):
        self.assertEqual(
            self.run_program("3 3\n2 0 1\n2 1 1\n1 0 1\n"),
            "COMPONENTS 1\n"
            "PRIM 2 2\n0 1 1\n0 2 1\n"
            "KRUSKAL 2 2\n0 1 1\n0 2 1\n"
            "AGREEMENT YES",
        )

    def test_two_disconnected_tied_cycles(self):
        self.assertEqual(
            self.run_program(
                "6 6\n0 1 2\n1 2 2\n0 2 2\n3 4 5\n4 5 5\n3 5 5\n"
            ),
            "COMPONENTS 2\n"
            "PRIM 14 4\n0 1 2\n0 2 2\n3 4 5\n3 5 5\n"
            "KRUSKAL 14 4\n0 1 2\n0 2 2\n3 4 5\n3 5 5\n"
            "AGREEMENT YES",
        )

    def test_maximum_size_complete_graph(self):
        vertex_count = 100
        edges = list(itertools.combinations(range(vertex_count), 2))
        input_lines = [f"{vertex_count} {len(edges)}"]
        input_lines.extend(f"{first} {second} 1" for first, second in edges)
        output = self.run_program("\n".join(input_lines) + "\n")

        lines = output.splitlines()
        self.assertEqual(lines[0], "COMPONENTS 1")
        self.assertEqual(lines[1], "PRIM 99 99")
        kruskal_header = 2 + 99
        self.assertEqual(lines[kruskal_header], "KRUSKAL 99 99")
        self.assertEqual(lines[-1], "AGREEMENT YES")
        self.assertEqual(len(lines), 1 + 100 + 100 + 1)


if __name__ == "__main__":
    unittest.main()
