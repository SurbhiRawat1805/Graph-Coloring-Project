# Graph Coloring

A small graph-coloring tool: a Python window where you draw a graph, and a C++ program that colors it.

Adjacent nodes never share a color. You choose how many colors are allowed. If that many colors are not enough, the solver reports that no coloring exists.

## Project layout

| File | Role |
| --- | --- |
| `Python_file.py` | Window for adding nodes and edges, then coloring the graph |
| `coloring.cpp` | Backtracking solver. Reads the graph and prints a coloring |

`.vscode` is editor settings for this machine. It is not required to build or run the project.

## Requirements

- A C++ compiler such as g++ (MinGW on Windows)
- Python 3 with Tkinter (included with the standard Windows installer)

## Build and run

From this folder:

```bash
g++ coloring.cpp -o coloring
python Python_file.py
```

On Windows, `g++` writes `coloring.exe`. The window starts that program as `./coloring` from this same folder, so compile here before you press **Solve**.

## Using the window

1. **Add Node** places the next node. Nodes are laid out in a circle.
2. **Add Edge**, then click two nodes, draws an undirected edge between them.
3. Click a node and type digits to give it a label. **Backspace** deletes the last digit. An unlabeled node shows its index.
4. Type the number of colors in **Colors**, then press **Solve**.

Each color is drawn from a fixed palette (red, blue, green, yellow, purple, orange). If you allow more than six colors, later colors reuse those shades. If no valid coloring exists, the console prints `No solution` and the drawing stays unchanged.

## Solver input and output

`coloring.cpp` reads from standard input:

```text
n m
row 0 of the adjacency matrix
row 1
...
row n-1
```

`n` is the number of nodes. `m` is the number of colors. Each matrix entry is `0` or `1`. The matrix is symmetric because edges are undirected.

Example (a triangle, 3 colors):

```text
3 3
0 1 1
1 0 1
1 1 0
```

Possible output:

```text
1 2 3
```

Colors are numbered from 1. If the graph cannot be colored with `m` colors, the program prints:

```text
NO
```

You can run the solver on its own:

```bash
g++ coloring.cpp -o coloring
./coloring
```

Then type the matrix and press Enter. On Windows, run `coloring.exe` the same way.
