#include <stdio.h>
#include <stdlib.h>

typedef long long ll;

static ll p;

/* one step of T, on the packed index v = x*p + y */
static ll step(ll v) {
    ll x = v / p, y = v % p;
    ll nx = ((x * x - 2 * y) % p + p) % p;
    ll ny = ((y * y - 2 * x) % p + p) % p;
    return nx * p + ny;
}

static int cmp_desc(const void *a, const void *b) {
    ll x = *(const ll *)a, y = *(const ll *)b;
    return (x < y) - (x > y);
}

int main(int argc, char **argv) {
    if (argc == 2) p = atoll(argv[1]);
    else { printf("p : "); if (scanf("%lld", &p) != 1) return 1; }
    if (p < 2) { fprintf(stderr, "p must be at least 2\n"); return 1; }

    ll N = p * p;
    int *mark = calloc((size_t)N, sizeof(int));   /* 0 = unvisited, else pass number */
    if (!mark) { fprintf(stderr, "out of memory\n"); return 1; }

    ll  cap = 64, ncyc = 0;
    ll *len = malloc(sizeof(ll) * cap);
    ll  pass = 0, total = 0;

    for (ll s = 0; s < N; s++) {
        if (mark[s]) continue;
        pass++;
        ll v = s;
        while (mark[v] == 0) { mark[v] = (int)pass; v = step(v); }
        if (mark[v] != (int)pass) continue;       /* ran into an older component */

        /* v lies on a brand-new cycle: measure it */
        ll L = 0, w = v;
        do { w = step(w); L++; } while (w != v);

        if (ncyc == cap) { cap *= 2; len = realloc(len, sizeof(ll) * cap); }
        len[ncyc++] = L;
        total += L;
    }
    free(mark);

    qsort(len, (size_t)ncyc, sizeof(ll), cmp_desc);

    printf("p = %lld\n", p);
    printf("loops (%lld total): ", ncyc);
    for (ll i = 0; i < ncyc; i++) printf("%lld%s", len[i], i + 1 < ncyc ? ", " : "\n");
    printf("points on loops: %lld  out of %lld\n\n", total, N);

    printf("size | count\n");
    for (ll i = 0; i < ncyc; ) {
        ll j = i;
        while (j < ncyc && len[j] == len[i]) j++;
        printf("%8lld | %lld\n", len[i], j - i);
        i = j;
    }

    free(len);
    return 0;
}