import tkinter as tk
import subprocess
import math

BG_COLOR = "#d6ecff"
SELECT_COLOR = "#4da6ff"
DEFAULT_COLOR = "#ecf0f1"
EDGE_SELECT_COLOR = "#ffd966"

BTN_COLOR = "#3498db"
BTN_HOVER = "#2980b9"
BTN_TEXT = "white"
FONT = ("Segoe UI", 11, "bold")

class GraphUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Coloring")
        self.root.geometry("700x550")
        self.root.configure(bg=BG_COLOR)

        self.nodes = []
        self.edges = []
        self.node_positions = {}
        self.node_labels = {}

        self.selected_node = None
        self.edge_mode = False
        self.edge_selected = []

        self.canvas = tk.Canvas(root, width=620, height=420, bg="white", highlightthickness=0)
        self.canvas.pack(pady=15)

        control = tk.Frame(root, bg=BG_COLOR)
        control.pack()

        self.styled_button(control, "Add Node", self.add_node).grid(row=0, column=0, padx=8)
        self.styled_button(control, "Add Edge", self.enable_edge_mode).grid(row=0, column=1, padx=8)

        tk.Label(control, text="Colors:", bg=BG_COLOR, font=("Segoe UI", 10)).grid(row=0, column=2)

        self.color_entry = tk.Entry(control, width=5, font=("Segoe UI", 10))
        self.color_entry.grid(row=0, column=3, padx=5)

        self.styled_button(control, "Solve", self.solve).grid(row=0, column=4, padx=8)

        self.canvas.bind("<Button-1>", self.handle_click)
        self.root.bind("<Key>", self.key_input)

        self.root.focus_set()

    def styled_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            bg=BTN_COLOR,
            fg=BTN_TEXT,
            font=FONT,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            command=command
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=BTN_COLOR))
        return btn

    def add_node(self):
        n = len(self.nodes)

        self.nodes.append(n)
        self.node_labels[n] = ""

        self.update_positions()
        self.draw()
        
    def update_positions(self):
        n = len(self.nodes)

        if n == 0:
            return

        center_x, center_y = 310, 210

        # Increase radius based on node count
        radius = max(120, min(220, 30 * n))

        for i, node in enumerate(self.nodes):
            angle = 2 * math.pi * i / n
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)

            self.node_positions[node] = (x, y)

    def enable_edge_mode(self):
        self.edge_mode = True
        self.edge_selected = []
        self.selected_node = None
        self.draw()

    def handle_click(self, event):
        self.root.focus_set()

        clicked_node = None

        for node, (x, y) in self.node_positions.items():
            if (event.x - x)**2 + (event.y - y)**2 < 400:
                clicked_node = node
                break

        if clicked_node is None:
            return

        if self.edge_mode:
            if clicked_node not in self.edge_selected:
                self.edge_selected.append(clicked_node)

            if len(self.edge_selected) == 2:
                u, v = self.edge_selected

                if u != v and (u, v) not in self.edges and (v, u) not in self.edges:
                    self.edges.append((u, v))

                self.edge_selected = []
                self.edge_mode = False

            self.draw()
            return

        self.selected_node = clicked_node
        self.draw()

    def key_input(self, event):
        if self.selected_node is None:
            return

        current = self.node_labels.get(self.selected_node, "")

        if event.keysym == "BackSpace":
            self.node_labels[self.selected_node] = current[:-1]

        elif event.char.isdigit():
            if len(current) < 5:  # limit length (optional)
                self.node_labels[self.selected_node] = current + event.char

        self.draw()

    def build_matrix(self):
        n = len(self.nodes)
        matrix = [[0]*n for _ in range(n)]

        for u, v in self.edges:
            matrix[u][v] = 1
            matrix[v][u] = 1

        return matrix

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
                ["./coloring"],
                input=input_data,
                text=True,
                capture_output=True
            )

            output = result.stdout.strip()

            if output == "NO":
                print("No solution")
                return

            colors = list(map(int, output.split()))
            self.color_graph(colors)

        except Exception as e:
            print("Error:", e)

    def color_graph(self, colors):
        palette = ["#e74c3c", "#3498db", "#2ecc71", "#f1c40f", "#9b59b6", "#e67e22"]

        self.canvas.delete("all")

        for u, v in self.edges:
            x1, y1 = self.node_positions[u]
            x2, y2 = self.node_positions[v]
            self.canvas.create_line(x1, y1, x2, y2, width=2)

        for node in self.nodes:
            x, y = self.node_positions[node]
            color = palette[(colors[node]-1) % len(palette)]

            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline="")

            label = self.node_labels.get(node, "")
            text = label if label else str(node)

            self.canvas.create_text(x, y, text=text, fill="white", font=("Segoe UI", 11, "bold"))

    def draw(self):
        self.canvas.delete("all")

        for u, v in self.edges:
            x1, y1 = self.node_positions[u]
            x2, y2 = self.node_positions[v]
            self.canvas.create_line(x1, y1, x2, y2, width=2)

        for node in self.nodes:
            x, y = self.node_positions[node]

            if node in self.edge_selected:
                color = EDGE_SELECT_COLOR
            elif node == self.selected_node:
                color = SELECT_COLOR
            else:
                color = DEFAULT_COLOR

            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline="")

            label = self.node_labels.get(node, "")
            text = label if label else str(node)

            self.canvas.create_text(x, y, text=text, font=("Segoe UI", 11, "bold"))


# RUN
root = tk.Tk()
GraphUI(root)
root.mainloop()