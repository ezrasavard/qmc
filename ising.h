#ifndef ISING
#define ISING

#define MAX_SPINS 2000
#define COUPLING_PRECISION 1e4

typedef struct AdjacencyList {
    int *nidx; // array of index for neighbours
    int len; // length of neighbours array
} AdjacencyList;

/*
  Storage for Ising spin glass problem info
*/
typedef struct IsingProblem {
    long int *h;
    long int **J;
    double exact; // reference solution
    int *spins;
    int *original_spins; // problem can be reset
    AdjacencyList *adj;
    int N; // size of spins array
    char *name;
    double gs; // solution
    int *s1;
    int *s2;
    long int *couplings;
    int datalines;
    double avg_coupling;
}IsingProblem;

IsingProblem *init_IsingProblem(char *fname);

void delete_IsingProblem(IsingProblem *p);

void reset_IsingProblem(IsingProblem *p);

long int get_dE_local(const int i, int const *spins, IsingProblem const *p);

long int get_E_local(int const *spins, IsingProblem const *p);

void spins_as_hex(int N, int *spins, char *hex);

void hex_to_spins(int N, char *hex, int *spins);
#endif
