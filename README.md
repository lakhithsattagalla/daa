# Infrastructure Planning: Two Minimum-Cost Forests

This project currently finds a minimum spanning forest twice: once with Prim's
algorithm and once independently with Kruskal's algorithm. An original
connected component remains a separate tree; isolated vertices count as
components and contribute no edges. This implementation follows the detailed
behavior and constraints previously provided in chat, but the official problem
statement and sample are unavailable. Treat the solution as preliminary until
it can be checked against the official requirements. Cases in
`tests/test_cases.txt` are custom checks, not official samples.

## Input and output

Input is `n m`, followed by `m` undirected edges `u v w`. Vertices are numbered
from `0` to `n - 1`. The output reports the number of original connected
components, then each forest's total cost, edge count, and normalized edges,
then whether the two totals and edge counts agree. Forest edges are printed in
increasing `(weight, min_endpoint, max_endpoint)` order.

## Algorithm

- **Prim:** Start at the smallest not-yet-selected vertex. A min-heap stores
  edges crossing from its growing tree to unselected vertices. The heap key is
  `(weight, min_endpoint, max_endpoint)`. When the heap empties, restart from
  the smallest unselected vertex, which also handles isolated vertices.
- **Kruskal:** Sort all edges by that same key and accept an edge only when a
  disjoint-set union (DSU) says it connects two different components.
- The DSU component count after Kruskal processes the edges is the number of
  original connected components. Both spanning forests therefore have `n - c`
  edges. They are compared by total cost and edge count, not by edge identity.

Prim is `O((n + m) log(m + 1))` with the binary heap; Kruskal is
`O(m log(m + 1) + m α(n))`, where `α` is the inverse Ackermann function.
Storage is `O(n + m)`.

The constraints say weights are positive, there are no self-loops or duplicate
undirected edges, and `n <= 100`, `m <= 4950`. Disconnected graphs, isolated
vertices, and ties are handled. Zero/negative weights, self-loops, and parallel
edges are outside the stated input domain.

## Run in VS Code on Windows

1. In PowerShell, create and open the project:

   ```powershell
   New-Item -ItemType Directory -Force infrastructure-planning
   Set-Location infrastructure-planning
   code .
   ```

2. Check for Python 3:

   ```powershell
   py --version
   ```

   If `py` is not recognized, install Python 3 and select its interpreter in
   VS Code with **Python: Select Interpreter**.

3. Save the provided solution as `main.py`. The test vectors are in
   `tests\test_cases.txt`.
4. Run from the VS Code terminal:

   ```powershell
   py main.py
   ```

   Paste an input case, then press `Ctrl+Z` followed by `Enter` to signal
   end-of-file in Windows PowerShell. Alternatively, redirect a saved input:

   ```powershell
   Get-Content -Raw .\input.txt | py .\main.py
   ```

5. To run the automated tests from the project root:

   ```powershell
   py -m unittest discover -s tests -v
   ```

6. To debug, set a breakpoint in `main.py`, choose the selected Python
   interpreter, and press `F5`. Check the terminal input and traceback if a
   test fails.
7. Submit only `main.py` unless the platform explicitly accepts multiple files.
   Do not include explanatory text in judge input or output.

## Correctness

For each connected component, Prim repeatedly chooses a minimum-key edge
crossing the cut between the vertices already in its current tree and the
remaining vertices. By the cut property, that edge is safe for a minimum
spanning tree. It stops only when the component has been exhausted, then starts
the next smallest unselected vertex. Thus Prim produces one minimum spanning
tree for each original component, including the zero-edge tree for an
isolate.

Kruskal examines edges in nondecreasing key order. DSU accepts an edge exactly
when it joins two previously separate sets, so accepted edges never form a
cycle. By the cut property, each accepted edge is safe for a minimum spanning
forest. Once every edge has been examined, each original connected component
has been joined into a tree. Therefore both algorithms produce minimum-cost
forests with `n - c` edges. Different valid edge sets are allowed; equal
minimum total costs and edge counts establish the requested agreement.
