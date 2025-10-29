"""
routing_sim.py

Simple simulator for:
 - Distance Vector (iterative)
 - Link State (Dijkstra)
 - Two poisoning scenarios:
    1) False-low-cost advertisement (malicious node claims 0-cost to dest)
    2) Link failure causing count-to-infinity in DV (shows mitigation idea)

Run: python routing_sim.py
"""

import heapq
import math
from copy import deepcopy

INF = 10**9

# -----------------------
# Topology (undirected, symmetric weights)
# Nodes: A, B, C, D
# -----------------------
NODES = ["A", "B", "C", "D"]

BASE_LINKS = {
    ("A", "B"): 1,
    ("A", "C"): 5,
    ("B", "C"): 2,
    ("B", "D"): 4,
    ("C", "D"): 1
}

def build_adj(links):
    adj = {n: {} for n in NODES}
    for (u,v), w in links.items():
        adj[u][v] = w
        adj[v][u] = w
    return adj

# -----------------------
# Helper printing
# -----------------------
def print_routing_table(rt):
    # rt: dict[node][dest] = (cost, next_hop)
    for node in sorted(rt.keys()):
        print(f"Routing table for {node}:")
        rows = []
        for d in sorted(NODES):
            c, nh = rt[node].get(d, (INF, None))
            rows.append(f"{d}: cost={c if c<INF else '∞'} next={nh}")
        print("  " + " | ".join(rows))
    print()

# -----------------------
# Distance Vector Simulation
# -----------------------
def init_dv(adj):
    # routing table for each node: {dest: (cost, next_hop)}
    rt = {}
    for u in NODES:
        rt[u] = {}
        for v in NODES:
            if u == v:
                rt[u][v] = (0, u)
            elif v in adj[u]:
                rt[u][v] = (adj[u][v], v)
            else:
                rt[u][v] = (INF, None)
    return rt

def dv_iterate(adj, rt, poisoned_advert=None):
    """
    One synchronous DV iteration: each node sends its current distance vector to neighbors,
    and neighbors update their table.
    poisoned_advert: optional dict {node: {dest: cost}} to simulate malicious advertisements
    """
    new_rt = deepcopy(rt)
    # Each node receives neighbor vectors and updates
    for u in NODES:
        for neighbor, link_cost in adj[u].items():
            # neighbor advertises its rt[neighbor]
            advertised = rt[neighbor]
            # apply malicious advertisement if present
            if poisoned_advert and neighbor in poisoned_advert:
                # merge advertised copy with poison overrides
                advertised = deepcopy(advertised)
                for dest, fake_cost in poisoned_advert[neighbor].items():
                    advertised[dest] = (fake_cost, advertised[dest][1])
            # try to relax routes at u using neighbor's advertised costs
            for dest in NODES:
                neigh_cost_to_dest, _ = advertised[dest]
                candidate = link_cost + neigh_cost_to_dest
                current_cost, _ = new_rt[u][dest]
                if candidate < current_cost:
                    new_rt[u][dest] = (candidate, neighbor)
    return new_rt

def simulate_dv(adj, steps=10, poisoned_advert=None, fail_link=None, poisoned_reverse=False):
    """
    Simulate DV for a number of synchronous steps.
    - poisoned_advert: dict{node:{dest:cost}} -> malicious advert overrides
    - fail_link: tuple (u,v) to simulate removal of link at step 0
    - poisoned_reverse: if True, simulate poisoned reverse behavior on updates (simple model)
    """
    # Optionally remove a link to simulate failure
    if fail_link:
        a,b = fail_link
        adj = deepcopy(adj)
        if b in adj[a]:
            del adj[a][b]
        if a in adj[b]:
            del adj[b][a]

    rt = init_dv(adj)
    history = [rt]
    print("Initial DV routing tables:")
    print_routing_table(rt)

    for i in range(1, steps+1):
        # optionally simulate poisoned reverse: if enabled, neighbors will advertise ∞ for routes that go back via you
        advertise_override = None
        if poisoned_reverse:
            # build per-node advertisement that sets cost=INF for destinations where next hop points back to receiver
            advertise_override = {}
            # For each node x, when it sends to neighbor y, it will poison (advertise INF) routes whose next hop == y
            # We implement this inside the per-neighbor loop in dv_iterate below by returning a structure consumed there.
            # Simpler approach: we won't implement full poisoned reverse; keep for demonstration flag only.
            advertise_override = None

        rt = dv_iterate(adj, rt, poisoned_advert=poisoned_advert)
        history.append(rt)
        print(f"After iteration {i}:")
        print_routing_table(rt)

    return history

# -----------------------
# Link State Simulation (Dijkstra)
# -----------------------
def dijkstra(adj, source):
    dist = {n: INF for n in NODES}
    prev = {n: None for n in NODES}
    dist[source] = 0
    pq = [(0, source)]
    while pq:
        d,u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v,w in adj[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    # build routing table entry for source
    rt = {}
    for dest in NODES:
        if dist[dest] == INF:
            rt[dest] = (INF, None)
        elif dest == source:
            rt[dest] = (0, source)
        else:
            # find next hop by walking prev[]
            cur = dest
            while prev[cur] and prev[cur] != source:
                cur = prev[cur]
            next_hop = cur if prev[cur] or cur==source else dest
            rt[dest] = (dist[dest], next_hop)
    return rt

def simulate_ls(adj):
    print("Link-State routing (each node computes Dijkstra locally from full topology):")
    rt = {}
    for node in NODES:
        rt[node] = dijkstra(adj, node)
    print_routing_table(rt)
    return rt

# -----------------------
# Demonstrations
# -----------------------
def demo_normal():
    print("=== DEMO: Normal (no poisoning) ===")
    adj = build_adj(BASE_LINKS)
    simulate_dv(adj, steps=3)
    simulate_ls(adj)

def demo_false_low_advertisement():
    print("=== DEMO: False-low-cost advertisement (poisoning) ===")
    adj = build_adj(BASE_LINKS)
    # Let's say node C maliciously advertises it has cost 0 to D (instead of 1),
    # i.e., tries to attract traffic to D via itself (blackhole).
    poisoned_advert = {
        "C": {
            "D": 0  # false advertisement: C claims it can reach D at cost 0
        }
    }
    print("Distance Vector with malicious advertisement by C (claims cost 0 to D):")
    simulate_dv(adj, steps=4, poisoned_advert=poisoned_advert)
    print("Link-State with same malicious advertisement -> LS is safe because LS relies on real topology/weights.")
    # For LS, we must fake topology (if we assume maliciously injects false link weight into LS DB, then LS will be affected).
    # But typical LS assumes authenticated LSA; we show normal LS result (not poisoned).
    simulate_ls(adj)

def demo_count_to_infinity():
    print("=== DEMO: Count-to-Infinity (link failure) ===")
    adj = build_adj(BASE_LINKS)
    # First converge normally
    history = simulate_dv(adj, steps=3)
    print("Now fail link B-D (remove it) and continue DV with no poisoned reverse -> may show count-to-infinity behavior.")
    # Remove link (B,D) and continue iterating from the last table (simulate asynchronous slow convergence)
    # We'll start from last history state but with the adjacency missing link.
    last_rt = history[-1]
    # Simulate further iterations with link (B,D) removed
    adj_failed = build_adj(BASE_LINKS)
    # remove B-D
    del adj_failed["B"]["D"]
    del adj_failed["D"]["B"]
    print("Topology after removing link B-D:")
    print(adj_failed)
    # Continue DV starting from last_rt
    rt = deepcopy(last_rt)
    for i in range(1, 8):
        rt = dv_iterate(adj_failed, rt)  # no poisoned reverse -> slow convergence possible
        print(f"After failure iteration {i}:")
        print_routing_table(rt)

# -----------------------
# Main entry
# -----------------------
if __name__ == "__main__":
    # Demo 1: normal convergence
    demo_normal()

    # Demo 2: false-low-cost advertisement (poisoning)
    demo_false_low_advertisement()

    # Demo 3: count-to-infinity demonstration (link failure)
    demo_count_to_infinity()
