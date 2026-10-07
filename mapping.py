def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def T(point, p):
    x, y = point
    return (
        (x * x - 2 * y) % p,
        (y * y - 2 * x) % p
    )


p = int(input())

if not is_prime(p):
    print("ERROR: p must be prime.")
    raise SystemExit


info = {}
cycles = []

for x in range(p):
    for y in range(p):
        start = (x, y)

        if start in info:
            continue

        path = []
        position = {}
        cur = start

        while cur not in info and cur not in position:
            position[cur] = len(path)
            path.append(cur)
            cur = T(cur, p)

        if cur in position:
            j = position[cur]
            cycle = path[j:]
            cid = len(cycles)
            cycles.append(cycle)

            for q in cycle:
                info[q] = (cid, 0)

            d = 1
            k = j - 1

            while k >= 0:
                info[path[k]] = (cid, d)
                d += 1
                k -= 1

        else:
            cid = info[cur][0]
            d = info[cur][1] + 1
            k = len(path) - 1

            while k >= 0:
                info[path[k]] = (cid, d)
                d += 1
                k -= 1


order = sorted(
    range(len(cycles)),
    key=lambda i: len(cycles[i])
)

new_cycles = [cycles[i] for i in order]

new_id = {}

for new_cid, old_cid in enumerate(order):
    new_id[old_cid] = new_cid

for point in info:
    old_cid, depth = info[point]
    info[point] = (new_id[old_cid], depth)

cycles = new_cycles


cycle_names = []

for cid, cycle in enumerate(cycles):
    cycle_names.append(
        f"cycle{cid + 1}_length{len(cycle)}"
    )


periodic_points = 0
max_cycle = 0
max_tail = 0

cycle_length_count = {}
tail_depth_count = {}

for cycle in cycles:
    L = len(cycle)
    periodic_points += L
    max_cycle = max(max_cycle, L)
    cycle_length_count[L] = cycle_length_count.get(L, 0) + 1

for point in info:
    d = info[point][1]
    max_tail = max(max_tail, d)
    tail_depth_count[d] = tail_depth_count.get(d, 0) + 1


print()
print("=" * 70)
print(f" A2 CHEBYSHEV MAP MOD {p}")
print("=" * 70)
print(f"T(x, y) = (x² - 2y, y² - 2x) mod {p}")
print()

print("[ BASIC STATISTICS ]")
print(f"{'Total points':<25}: {p * p}")
print(f"{'Number of cycles':<25}: {len(cycles)}")
print(f"{'Periodic points':<25}: {periodic_points}")
print(f"{'Nonperiodic points':<25}: {p * p - periodic_points}")
print(f"{'Max cycle length':<25}: {max_cycle}")
print(f"{'Max tail length':<25}: {max_tail}")

print()
print("[ CYCLE LENGTH DISTRIBUTION ]")
print(f"{'Length':>10} {'Cycles':>10}")
print("-" * 25)

for L in sorted(cycle_length_count):
    print(f"{L:>10} {cycle_length_count[L]:>10}")

print()
print("[ TAIL DEPTH DISTRIBUTION ]")
print(f"{'Depth':>10} {'Points':>10}")
print("-" * 25)

for d in sorted(tail_depth_count):
    print(f"{d:>10} {tail_depth_count[d]:>10}")


print()
print("=" * 70)
print(" CYCLES")
print("=" * 70)

for cid, cycle in enumerate(cycles):
    name = cycle_names[cid]

    print()
    print(f"{name}")

    path = "  →  ".join(str(q) for q in cycle)
    path += f"  →  {cycle[0]}"

    print("    " + path)


print()
print("=" * 70)
print(" TAILS")
print("=" * 70)

for cid, cycle in enumerate(cycles):
    name = cycle_names[cid]

    tails = []

    for point in info:
        if info[point][0] == cid and info[point][1] > 0:
            tails.append(point)

    tails.sort(
        key=lambda q: (
            -info[q][1],
            q[0],
            q[1]
        )
    )

    print()
    print(f"{name}  |  tails = {len(tails)}")

    if not tails:
        print("    (no tails)")
        continue

    for point in tails:
        depth = info[point][1]

        path = []
        cur = point

        while info[cur][1] > 0:
            path.append(cur)
            cur = T(cur, p)

        path.append(cur)

        print(
            f"    depth {depth:>2} : "
            + "  →  ".join(str(q) for q in path)
            + f"  →  {name}"
        )


print()
print("=" * 70)
print(" SUMMARY")
print("=" * 70)

print(
    f"Points: {p * p}  |  "
    f"Cycles: {len(cycles)}  |  "
    f"Periodic: {periodic_points}  |  "
    f"Nonperiodic: {p * p - periodic_points}"
)

print("=" * 70)