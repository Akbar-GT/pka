from flask import Flask, render_template, request, send_from_directory
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import os

app = Flask(__name__)

graph = {
    'Malioboro': {
        'Keraton Yogyakarta': 2,
        'Taman Sari': 4,
        'Bukit Bintang': 12,
        'Alun-Alun Kidul': 3
    },
    'Keraton Yogyakarta': {
        'Malioboro': 2,
        'Taman Sari': 2,
        'Alun-Alun Kidul': 2,
        'Tebing Breksi': 14
    },
    'Taman Sari': {
        'Malioboro': 4,
        'Keraton Yogyakarta': 2,
        'Pantai Parangtritis': 24,
        'Alun-Alun Kidul': 1
    },
    'Candi Prambanan': {
        'Bukit Bintang': 15,
        'Tebing Breksi': 7,
        'Gunung Merapi Lava Tour': 20
    },
    'Candi Borobudur': {
        'Gunung Merapi Lava Tour': 28,
        'Malioboro': 30,
        'Bukit Bintang': 25
    },
    'Bukit Bintang': {
        'Malioboro': 12,
        'Candi Prambanan': 15,
        'Tebing Breksi': 5,
        'Candi Borobudur': 25
    },
    'Tebing Breksi': {
        'Candi Prambanan': 7,
        'Bukit Bintang': 5,
        'Gunung Merapi Lava Tour': 14,
        'Keraton Yogyakarta': 14
    },
    'Pantai Parangtritis': {
        'Taman Sari': 24,
        'Alun-Alun Kidul': 21,
        'Gunung Merapi Lava Tour': 40
    },
    'Gunung Merapi Lava Tour': {
        'Candi Borobudur': 28,
        'Tebing Breksi': 14,
        'Candi Prambanan': 20,
        'Pantai Parangtritis': 40
    },
    'Alun-Alun Kidul': {
        'Keraton Yogyakarta': 2,
        'Pantai Parangtritis': 21,
        'Taman Sari': 1,
        'Malioboro': 3
    }
}

def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        visited.add(node)
        if node == end:
            return (cost, path)
        for neighbor in graph[node]:
            if neighbor not in visited:
                heapq.heappush(queue, (cost + graph[node][neighbor], neighbor, path))
    return (float("inf"), [])

def draw_graph(path, cost):
    import networkx as nx
    import matplotlib.pyplot as plt
    import os

    G = nx.Graph()
    for node in graph:
        for neighbor in graph[node]:
            G.add_edge(node, neighbor, weight=graph[node][neighbor])

    # Gunakan layout yang lebih teratur
    pos = nx.kamada_kawai_layout(G)

    # Gambar node dan edge dasar
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='#add8e6')
    nx.draw_networkx_edges(G, pos, width=2, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # Tampilkan bobot/label jarak
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=9,
                                 bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

    # Jika ada path terpendek, sorot
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color='red')
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='#ffa07a')

    plt.title(f"Rute Terpendek: {' → '.join(path)} (Jarak: {cost} km)", fontsize=14)
    plt.axis('off')
    os.makedirs('static', exist_ok=True)
    plt.tight_layout()
    plt.savefig("static/route.png")
    plt.close()

@app.route("/", methods=["GET", "POST"])
def index():
    route = []
    cost = 0
    start = end = None

    if request.method == "POST":
        start = request.form["start"]
        end = request.form["end"]
        cost, route = dijkstra(graph, start, end)
        draw_graph(route, cost)

    return render_template("index.html", nodes=list(graph.keys()), route=route, cost=cost, start=start, end=end)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(debug=True)
