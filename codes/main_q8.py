import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import girvan_newman
from networkx.algorithms.community.quality import modularity

# =========================================================
# 1) Veri okuma ve ağ küçültme
# =========================================================
G = nx.read_edgelist("ca-GrQc.txt.gz", nodetype=int)

# Largest connected component
G = G.subgraph(max(nx.connected_components(G), key=len)).copy()

# Degree filtresi
min_degree = 7
nodes = [n for n in G.nodes() if G.degree(n) >= min_degree]
G = G.subgraph(nodes).copy()

# Tekrar largest connected component
G = G.subgraph(max(nx.connected_components(G), key=len)).copy()

print("Analizde kullanılan çekirdek alt-ağ:")
print("Düğüm sayısı:", G.number_of_nodes())
print("Kenar sayısı:", G.number_of_edges())

# =========================================================
# 2) Girvan-Newman community analizi
# =========================================================
res = []
comp = girvan_newman(G)

for step in range(8):   # daha fazlası yine yavaş olabilir
    comms = [set(c) for c in next(comp)]
    q = modularity(G, comms)
    res.append((step + 1, comms, q))

best_step, best_part, best_mod = max(res, key=lambda x: x[2])
sizes = sorted([len(c) for c in best_part], reverse=True)

print("\nEn iyi adım:", best_step)
print("En iyi modularity:", round(best_mod, 4))
print("Topluluk sayısı:", len(best_part))
print("Küme boyutları:", sizes)
print("Overlapping yok: Girvan-Newman disjoint community üretir.")

# =========================================================
# 3) Modularity grafiği
# =========================================================
plt.figure(figsize=(6, 4))
plt.plot([r[0] for r in res], [r[2] for r in res], marker="o")
plt.xlabel("Adım")
plt.ylabel("Modularity")
plt.title("Girvan-Newman Modularity")
plt.tight_layout()
plt.savefig("girvan_newman_modularity.png", dpi=200)
plt.close()

# =========================================================
# 4) Küme boyut dağılımı
# =========================================================
plt.figure(figsize=(6, 4))
plt.bar(range(1, len(sizes) + 1), sizes)
plt.xlabel("Topluluk")
plt.ylabel("Boyut")
plt.title("Küme Boyut Dağılımı")
plt.tight_layout()
plt.savefig("girvan_newman_sizes.png", dpi=200)
plt.close()

# =========================================================
# 5) Dendrogram Ağa.
# =========================================================
T = nx.DiGraph()
root = "L0_0"
T.add_node(root, size=G.number_of_nodes(), level=0)

prev = [(root, set(G.nodes()))]

for level, comms, _ in res:
    curr = []
    for j, c in enumerate(comms):
        nid = f"L{level}_{j}"
        T.add_node(nid, size=len(c), level=level)
        curr.append((nid, c))

    for pid, pset in prev:
        childs = [(nid, c) for nid, c in curr if c.issubset(pset)]
        for nid, _ in childs:
            T.add_edge(pid, nid)

    prev = curr

def pos(tree, node, x=0.5, y=0, dx=1.0, out=None):
    if out is None:
        out = {}
    out[node] = (x, y)
    ch = list(tree.successors(node))
    if ch:
        step = dx / len(ch)
        start = x - dx / 2 + step / 2
        for i, c in enumerate(ch):
            pos(tree, c, start + i * step, y - 1, step, out)
    return out

plt.figure(figsize=(12, 6))
P = pos(T, root)
labels = {n: T.nodes[n]["size"] for n in T.nodes}
nx.draw(T, P, labels=labels, with_labels=True, node_size=700, font_size=8, arrows=False)
plt.title("Girvan-Newman Dendrogram")
plt.tight_layout()
plt.savefig("girvan_newman_dendrogram.png", dpi=200)
plt.close()