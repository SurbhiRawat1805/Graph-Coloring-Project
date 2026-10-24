import tkinter as tk
import subprocess
import math

SELECT_COLOR = "#4da6ff"
DEFAULT_COLOR = "lightgray"

class GraphUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Coloring")
        self.root.geometry("650x500")

        self.nodes = []
        self.edges = []
        self.node_positions = {}
        self.node_labels = {}

        self.selected_node = None
        self.edge_mode = False
        self.edge_selected = []

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(pady=10)

        control = tk.Frame(root)
        control.pack()

        tk.Button(control, text="Add Node", command=self.add_node).grid(row=0, column=0, padx=5)
        tk.Button(control, text="Add Edge", command=self.enable_edge_mode).grid(row=0, column=1, padx=5)

        tk.Label(control, text="Colors:").grid(row=0, column=2)
        self.color_entry = tk.Entry(control, width=5)
        self.color_entry.grid(row=0, column=3)

        tk.Button(control, text="Solve", command=self.solve).grid(row=0, column=4, padx=5)

        self.canvas.bind("<Button-1>", self.handle_click)
        self.root.bind("<Key>", self.key_input)

        self.root.focus_set()  # 🔥 important

    # Add node
    def add_node(self):
        n = len(self.nodes)
        angle = 2 * math.pi * n / max(1, (n+1))
        x = 300 + 180 * math.cos(angle)
        y = 200 + 180 * math.sin(angle)

        self.nodes.append(n)
        self.node_positions[n] = (x, y)
        self.node_labels[n] = ""

        self.draw()

    # Handle click (node select OR edge select)
    def handle_click(self, event):
        self.root.focus_set()  # 🔥 ensures typing works

        for node, (x, y) in self.node_positions.items():
            if (event.x - x)**2 + (event.y - y)**2 < 400:

                if self.edge_mode:
                    self.edge_selected.append(node)

                    if len(self.edge_selected) == 2:
                        u, v = self.edge_selected
                        if u != v:
                            self.edges.append((u, v))

                        self.edge_selected = []
                        self.edge_mode = False
                        self.draw()
                else:
                    self.selected_node = node
                    self.draw()

                return

    # Enable edge selection mode
    def enable_edge_mode(self):
        self.edge_mode = True
        self.edge_selected = []

    # Direct typing into node
    def key_input(self, event):
        if self.selected_node is None:
            return

        if event.keysym == "BackSpace":
            self.node_labels[self.selected_node] = ""
        elif event.char and event.char.isprintable():
            self.node_labels[self.selected_node] = event.char

        self.draw()

    # Build adjacency matrix
    def build_matrix(self):
        n = len(self.nodes)
        matrix = [[0]*n for _ in range(n)]

        for u, v in self.edges:
            matrix[u][v] = 1
            matrix[v][u] = 1

        return matrix

    # Solve using C++
    def solve(self):
        try:
            m = int(self.color_entry.get())
        except:
            return

        n = len(self.nodes)
        matrix = self.build_matrix()

        input_data = f"{n} {m}\n"
        for row in matrix:
            input_data += " ".join(map(str, row)) + "\n"

        try:
            result = subprocess.run(
                ["./coloring"],   # Windows: coloring.exe
                input=input_data,
                text=True,
                capture_output=True
            )

            output = result.stdout.strip()

            if output == "NO":
                return

            colors = list(map(int, output.split()))
            self.color_graph(colors)

        except Exception as e:
            print("Error:", e)

    # Display colored graph
    def color_graph(self, colors):
        palette = ["red", "blue", "green", "yellow", "orange", "purple"]

        self.canvas.delete("all")

        for u, v in self.edges:
            x1, y1 = self.node_positions[u]
            x2, y2 = self.node_positions[v]
            self.canvas.create_line(x1, y1, x2, y2, width=2)

        for node in self.nodes:
            x, y = self.node_positions[node]
            color = palette[(colors[node]-1) % len(palette)]

            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color)

            label = self.node_labels.get(node, "")
            text = label if label else str(node)

            self.canvas.create_text(x, y, text=text, fill="white", font=("Arial", 12, "bold"))

    # Draw default graph
    def draw(self):
        self.canvas.delete("all")

        for u, v in self.edges:
            x1, y1 = self.node_positions[u]
            x2, y2 = self.node_positions[v]
            self.canvas.create_line(x1, y1, x2, y2)

        for node in self.nodes:
            x, y = self.node_positions[node]

            color = SELECT_COLOR if node == self.selected_node else DEFAULT_COLOR

            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color)

            label = self.node_labels.get(node, "")
            text = label if label else str(node)

            self.canvas.create_text(x, y, text=text, font=("Arial", 12, "bold"))


# Run
root = tk.Tk()
GraphUI(root)
root.mainloop()