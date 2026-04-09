import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import Counter

# =========================================================
# Dosya Okuma ve Temel İstatistikler 
# =========================================================
G = nx.read_edgelist("ca-GrQc.txt.gz", nodetype=int)

print("Düğüm sayisi:", G.number_of_nodes())
print("Kenar sayisi:", G.number_of_edges())
print("Yönlü mü:", G.is_directed())

# =========================================================
# 2.4 Soru - İstatistikler
# =========================================================
N = G.number_of_nodes()
m = G.number_of_edges()
degrees = [d for n, d in G.degree()]
avg_degree = sum(degrees) / N

components = list(nx.connected_components(G))
num_components = len(components)
largest_cc = max(components, key=len)
largest_cc_size = len(largest_cc)
largest_cc_ratio = largest_cc_size / N

print("Ortalama derece =", avg_degree)
print("Bağli bileşen sayisi =", num_components)
print("En büyük bileşen boyutu =", largest_cc_size)
print("En büyük bileşen orani =", largest_cc_ratio)

# =========================================================
# 4.1 Soru Derece Dağılımı
# =========================================================
print("##########################")
print("Question 4.1 - Degree Distribution")
degrees = [d for n, d in G.degree()]
degree_count = Counter(degrees)
N = len(degrees)
k_vals = sorted(degree_count.keys())
p_k = [degree_count[k] / N for k in k_vals]

print("k_vals:", k_vals[:])
print("p_k:", p_k[:])

# =========================================================
# 4.2 Soru - Görselleştirme
# =========================================================
plt.plot(k_vals, p_k, "o")
plt.xlabel("k")
plt.ylabel("P(k)")
plt.title("Degree Distribution")
plt.savefig("degree_distribution_linear.png")


plt.loglog(k_vals, p_k, "o")
plt.xlabel("k")
plt.ylabel("P(k)")
plt.title("Degree Distribution (log-log)")
plt.savefig("degree_distribution_loglog.png")

# =========================================================
# 4.3 Soru - Rastgele Ağ ile Karşılaştırma
# =========================================================
print("##########################")
print("Question 4.3 - Random Graph Comparison")
N = G.number_of_nodes()
m = G.number_of_edges()

p = (2 * m) / (N * (N - 1))
Gr = nx.gnp_random_graph(N, p, seed=42)

print("Rastgele ağ düğüm sayısı:", Gr.number_of_nodes())
print("Rastgele ağ kenar sayısı:", Gr.number_of_edges())

deg_real = [d for _, d in G.degree()]
deg_rand = [d for _, d in Gr.degree()]

count_real = Counter(deg_real)
count_rand = Counter(deg_rand)

k_real = sorted(count_real.keys())
pk_real = [count_real[k] / len(deg_real) for k in k_real]

k_rand = sorted(count_rand.keys())
pk_rand = [count_rand[k] / len(deg_rand) for k in k_rand]

plt.figure(figsize=(6,4))
plt.loglog(k_real, pk_real, "o", label="Gerçek Ağ")
plt.loglog(k_rand, pk_rand, "s", label="Rastgele Ağ")
plt.xlabel("Derece (k)")
plt.ylabel("P(k)")
plt.title("Gerçek Ağ vs Rastgele Ağ")
plt.legend()
plt.grid(True)
plt.savefig("real_vs_random_degree_distribution.png")

# =========================================================
# 4.4 Soru - Degree Exponent Tahmini
# =========================================================
print("##########################")
print("Question 4.4 - Degree Exponent Estimation")
degrees = np.array([d for _, d in G.degree()])
degrees = degrees[degrees > 0]

count = Counter(degrees)
k_vals = np.array(sorted(count.keys()))
p_k = np.array([count[k] / len(degrees) for k in k_vals])

# çok küçük olasılıkları at
mask = p_k > 0
x = np.log10(k_vals[mask])
y = np.log10(p_k[mask])

coef = np.polyfit(x, y, 1)
slope = coef[0]
gamma = -slope

print("Yaklaşık slope =", slope)
print("Yaklaşık degree exponent (gamma) =", gamma)

# =========================================================
# 5. En Kısa Yol Hesabı
# =========================================================
print("##########################")
print("Question 5 - Shortest Path Calculation")
largest_cc_nodes = max(nx.connected_components(G), key=len)
Gcc = G.subgraph(largest_cc_nodes).copy()

print("Gcc düğüm sayisi:", Gcc.number_of_nodes())
print("Gcc kenar sayisi:", Gcc.number_of_edges())

avg_path = nx.average_shortest_path_length(Gcc)
diameter = nx.diameter(Gcc)

print("Ortalama yol uzunluğu:", avg_path)
print("Maksimum mesafe (diameter):", diameter)

lengths = []

for source in Gcc.nodes():
    sp = nx.single_source_shortest_path_length(Gcc, source)
    lengths.extend(sp.values())

# source->source olan 0 mesafeleri çıkar
lengths = [x for x in lengths if x > 0]

plt.figure(figsize=(6,4))
plt.hist(lengths, bins=30)
plt.xlabel("En kısa yol uzunluğu")
plt.ylabel("Frekans")
plt.title("Mesafe Dağılımı")
plt.grid(True)
plt.savefig("distance_distribution.png")

# =========================================================
# 5.3 Karşılaştırma
# =========================================================
print("##########################")
print("Question 5.3 - Comparison with Random Graph")
# gerçek ağ
C_real = nx.average_clustering(Gcc)
L_real = nx.average_shortest_path_length(Gcc)

# rastgele ağın en büyük bağlı bileşeni
largest_cc_rand = max(nx.connected_components(Gr), key=len)
Grcc = Gr.subgraph(largest_cc_rand).copy()

C_rand = nx.average_clustering(Grcc)
L_rand = nx.average_shortest_path_length(Grcc)

print("Gerçek ağ clustering:", C_real)
print("Rastgele ağ clustering:", C_rand)
print("Gerçek ağ ortalama yol:", L_real)
print("Rastgele ağ ortalama yol:", L_rand)


lengths = []

for source in Grcc.nodes():
    sp = nx.single_source_shortest_path_length(Grcc, source)
    lengths.extend(sp.values())

# source->source olan 0 mesafeleri çıkar
lengths = [x for x in lengths if x > 0]

plt.figure(figsize=(6,4))
plt.hist(lengths, bins=30)
plt.xlabel("En kısa yol uzunluğu")
plt.ylabel("Frekans")
plt.title("Mesafe Dağılımı")
plt.grid(True)
plt.savefig("distance_distribution_random.png")


# =========================================================
# 6. Derece Korelasyonu
# =========================================================
print("##########################")
print("Question 6 - Degree Correlation")
# r değeri hesaplama ve assortative mi disassortative mı olduğunu yorumlama
r = nx.degree_assortativity_coefficient(G)
print("Assortativity coefficient r =", r)
#  eij hesaplama
from collections import defaultdict

eij = defaultdict(int)

for u, v in G.edges():
    du = G.degree(u)
    dv = G.degree(v)
    a, b = sorted((du, dv))
    eij[(a, b)] += 1

# ilk birkaç değer
for key, val in list(eij.items())[:10]:
    print(key, val)

# knn(k) hesaplama
knn_dict = nx.average_degree_connectivity(G)

k_vals = sorted(knn_dict.keys())
knn_vals = [knn_dict[k] for k in k_vals]

# knn(k) görselleştirme
plt.figure(figsize=(6,4))
plt.plot(k_vals, knn_vals, "o-")
plt.xlabel("k")
plt.ylabel("knn(k)")
plt.title("Nearest Neighbor Degree Function")
plt.grid(True)
plt.savefig("knn_k_linear.png")

plt.figure(figsize=(6,4))
plt.loglog(k_vals, knn_vals, "o")
plt.xlabel("k")
plt.ylabel("knn(k)")
plt.title("knn(k) - loglog")
plt.grid(True)
plt.savefig("knn_k_loglog.png")


# =========================================================
# 6.4 Xulvi-Brunet & Sokolov
# =========================================================
print("##########################")
print("Question 6.4 - Xulvi-Brunet")


def xulvi(G, assortative=True, n_iter=20000, seed=42):
    H, rng = G.copy(), random.Random(seed)
    for _ in range(n_iter):
        e = list(H.edges())
        (a, b), (c, d) = rng.sample(e, 2)
        if len({a, b, c, d}) < 4:
            continue

        s = sorted([a, b, c, d], key=H.degree)
        new_edges = [(s[0], s[1]), (s[2], s[3])] if assortative else [(s[0], s[3]), (s[1], s[2])]

        if any(u == v or H.has_edge(u, v) for u, v in new_edges):
            continue

        H.remove_edges_from([(a, b), (c, d)])
        H.add_edges_from(new_edges)
    return H

def knn_xy(H):
    d = nx.average_degree_connectivity(H)
    x = sorted(d)
    return x, [d[k] for k in x]

def plot_adj(H, title, fname, max_nodes=200):
    nodes = sorted(H.nodes(), key=H.degree)
    if len(nodes) > max_nodes:
        idx = np.linspace(0, len(nodes)-1, max_nodes, dtype=int)
        nodes = [nodes[i] for i in idx]
    A = nx.to_numpy_array(H, nodelist=nodes)
    plt.figure(figsize=(5,5))
    plt.imshow(A, cmap="binary")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(fname)

G_assort = xulvi(G, assortative=True)
G_disassort = xulvi(G, assortative=False)

r0 = nx.degree_assortativity_coefficient(G)
r1 = nx.degree_assortativity_coefficient(G_assort)
r2 = nx.degree_assortativity_coefficient(G_disassort)

print("Original r =", r0)
print("Assortative r =", r1)
print("Disassortative r =", r2)

x0, y0 = knn_xy(G)
x1, y1 = knn_xy(G_assort)
x2, y2 = knn_xy(G_disassort)

plt.figure(figsize=(7,5))
plt.loglog(x0, y0, "o", label="Original")
plt.loglog(x1, y1, "s", label="Assortative")
plt.loglog(x2, y2, "^", label="Disassortative")
plt.xlabel("k")
plt.ylabel("knn(k)")
plt.title("Xulvi-Brunet Comparison")
plt.legend()
plt.grid(True)
plt.savefig("xulvi_real_knn.png")

plot_adj(G_assort, "Assortative Aij", "xulvi_assort_adj.png")
plot_adj(G_disassort, "Disassortative Aij", "xulvi_disassort_adj.png")

# =========================================================
# 7. Robustness Analysis
# =========================================================
# Gcc'nin rastgele node silmeye karşı dayanıklılığını inceleyelim
print("##########################")
print("Question 7 - Robustness Analysis")

import networkx as nx
import matplotlib.pyplot as plt
import random

def gcc_ratio_original(graph, original_n):
    if graph.number_of_nodes() == 0:
        return 0
    gcc = max(nx.connected_components(graph), key=len)
    return len(gcc) / original_n

def critical_threshold(fractions, gcc_ratios, threshold=0.01):
    for f, g in zip(fractions, gcc_ratios):
        if g <= threshold:
            return f
    return None

original_n = G.number_of_nodes()
step = max(1, original_n // 50)

# -------------------------
# 1) Rastgele düğüm silme
# -------------------------
num_trials = 10
fractions_random = None
all_random_curves = []

for _ in range(num_trials):
    G_random = G.copy()
    nodes = list(G_random.nodes())
    random.shuffle(nodes)

    removed = 0
    fractions = [0]
    gcc_sizes = [gcc_ratio_original(G_random, original_n)]

    for i in range(0, len(nodes), step):
        to_remove = nodes[i:i+step]
        G_random.remove_nodes_from(to_remove)
        removed += len(to_remove)

        f = removed / original_n
        g = gcc_ratio_original(G_random, original_n)

        fractions.append(f)
        gcc_sizes.append(g)

    if fractions_random is None:
        fractions_random = fractions

    all_random_curves.append(gcc_sizes)

# ortalama random eğrisi
avg_random_gcc = []
for i in range(len(fractions_random)):
    avg_random_gcc.append(sum(curve[i] for curve in all_random_curves) / num_trials)

# -------------------------
# 2) Hedefli saldırı
# -------------------------
G_target = G.copy()
removed = 0
fractions_target = [0]
gcc_sizes_target = [gcc_ratio_original(G_target, original_n)]

while G_target.number_of_nodes() > 0:
    deg_sorted = sorted(G_target.degree(), key=lambda x: x[1], reverse=True)
    to_remove = [node for node, deg in deg_sorted[:step]]

    G_target.remove_nodes_from(to_remove)
    removed += len(to_remove)

    f = removed / original_n
    g = gcc_ratio_original(G_target, original_n)

    fractions_target.append(f)
    gcc_sizes_target.append(g)

    if removed >= original_n:
        break

# -------------------------
# 3) Kritik eşikler
# -------------------------
critical_random = critical_threshold(fractions_random, avg_random_gcc, threshold=0.01)
critical_target = critical_threshold(fractions_target, gcc_sizes_target, threshold=0.01)

print("Random silmede %1 altına düşme noktası:", critical_random)
print("Hedefli saldırıda %1 altına düşme noktası:", critical_target)

# -------------------------
# 4) Grafik
# -------------------------
plt.figure(figsize=(7,5))
plt.plot(fractions_random, avg_random_gcc, "o-", label="Rastgele düğüm silme")
plt.plot(fractions_target, gcc_sizes_target, "s-", label="Hedefli saldırı")
plt.xlabel("Silinen düğüm oranı")
plt.ylabel("Dev bileşen oranı (|GCC| / N0)")
plt.title("Robustness Analysis")
plt.grid(True)
plt.legend()
plt.savefig("robustness_comparison.png")

# =========================================================
# 8. Topluluk Analizi
# =========================================================
print("##########################")
print("Question 8 - Community Analysis")
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community.quality import modularity

communities = list(greedy_modularity_communities(G))
mod_value = modularity(G, communities)

print("Topluluk sayısı:", len(communities))
print("Modularity:", mod_value)

sizes = [len(c) for c in communities]
print("İlk birkaç topluluk boyutu:", sizes[:10])

plt.figure(figsize=(6,4))
plt.hist(sizes, bins=20)
plt.xlabel("Topluluk boyutu")
plt.ylabel("Frekans")
plt.title("Community Size Distribution")
plt.grid(True)
plt.savefig("community_size_distribution.png")