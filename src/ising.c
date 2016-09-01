#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <assert.h>
#include <stdbool.h>
#include <string.h>
#include "ising.h"
 

IsingProblem* init_IsingProblem(char* fname) {

    // read the file
    FILE *fp = fopen(fname, "r");
    if(fp == NULL) {
        perror("Error opening file");
        fclose(fp);
        return(NULL);
    }

    // count the number of lines in the file
    char ch;
    int lines = 0;
    while(!feof(fp)) {
        ch = fgetc(fp);
        if(ch == '\n')
            lines++;
    }
    lines -= 1;
    if(lines < 1){
        perror("File has no data");
        return(NULL);
    }
    rewind(fp);

    // read first line, get exact solution
    char buff[256];
    fgets(buff, 32, fp);
    double exact;
    sscanf(buff, "%lf", &exact);

    // read data
    int c1; int c2; double coupling;
    long int* couplings = malloc(sizeof(long int)*lines);
    int* spins1 = malloc(sizeof(int)*lines);
    int* spins2 = malloc(sizeof(int)*lines);
    for(int i = 0; i < lines; i++) {
        fgets(buff, 32, fp);
        sscanf(buff, "%d %d %lf", &c1, &c2, &coupling);
        spins1[i] = c1;
        spins2[i] = c2;
        couplings[i] = (long int)(COUPLING_PRECISION*coupling);
    }
    fclose(fp);

    // the largest spin index should always be in the bottom row of
    // the two spin index columns
    int max_spin_ind = ((spins1[lines-1] > spins2[lines-1]) ? spins1[lines-1] : spins2[lines-1]);
    // count the number of unique spins without changing the ordering
    // map the cell numbers to a 1 indexed array
    int* spin_map = calloc(max_spin_ind+1, sizeof(int));
    int N = 0;
    for(int i = 0; i < lines; i++) {
        if(spin_map[spins1[i]] == 0){
            N++;
            spin_map[spins1[i]] = N;
        }
        if(spin_map[spins2[i]] == 0){
            N++;
            spin_map[spins2[i]] = N;
        }
    }

    printf("N: %d\n", N);
    printf("Max spin index: %d\n", max_spin_ind);

    // calculate average coupling strength
    double avg = 0;
    for (int i = 0; i < lines; i++)
        avg += (double)(abs(couplings[i]));
    avg /= (N*N - 1); // accounts for sparsity
    avg /= COUPLING_PRECISION;

    // allocate arrays
    IsingProblem* p = malloc(sizeof(IsingProblem));
    char* name = strdup(fname);

    long int* h = calloc(N, sizeof(long int));
    long int** J = calloc(N, sizeof(long int*));
    for (int i = 0; i < N; i++)
        J[i] = calloc(N, sizeof(long int));

    // produce h, J matrices from data
    int i; int j;
    for(int k = 0; k < lines; k++) {
        i = spin_map[spins1[k]]-1;
        j = spin_map[spins2[k]]-1;

        if(i == j)
            h[i] = couplings[k];
        else {
            J[i][j] = couplings[k];
            J[j][i] = couplings[k];
        }
    }

    // adjacency list
    AdjacencyList* adj = malloc(sizeof(AdjacencyList)*N);
    int count;
    for(int i = 0; i < N; i++) {
        count = 0;
        for(int j = 0; j < N; j++) {
            if(i == j)
                continue;
            if(J[i][j] != 0) {
                count++;
            }
        }
        adj[i].len = count;
        if(count == 0)
            adj[i].nidx = NULL;
        else
            adj[i].nidx = calloc(count, sizeof(int));
    }

    for(int i = 0; i < N; i++) {
        count = 0;
        if(adj[i].len == 0)
            continue;
        for(int j = 0; j < N; j++) {
            if(i == j)
                continue;
            if(J[i][j] != 0) {
                adj[i].nidx[count] = j;
                count++;
            }
        }
    }

    free(spin_map);

    // randomize spins
    int* original_spins = malloc(sizeof(int)*N);
    int* spins = malloc(sizeof(int)*N);

    for(int i = 0; i < N; i++) {
        int r = rand();
        if(r % 2 == 0) {
            original_spins[i] = 1;
            spins[i] = 1;
        }
        else {
            original_spins[i] = -1;
            spins[i] = -1;
        }
    }


    p->h = h;
    p->J = J;
    p->adj = adj;
    p->exact = exact;
    p->spins = spins;
    p->original_spins = original_spins;
    p->N = N;
    p->name = name;
    p->gs = 0;
    p->datalines = lines;
    p->s1 = spins1;
    p->s2 = spins2;
    p->couplings = couplings;
    p->avg_coupling = avg;

    return p;
}

void delete_IsingProblem(IsingProblem* p) {

    free(p->name);
    free(p->h);
    for (int i = 0; i < (p->N); i++) {
        long int* ptr = p->J[i];
        free(ptr);
    }
    free(p->J);
    free(p->adj);
    free(p->spins);
    free(p->original_spins);
    free(p->s1);
    free(p->s2);
    free(p->couplings);
    free(p);
}

void reset_IsingProblem(IsingProblem* p) {

    for(int i = 0; i < p->N; i++)
        p->spins[i] = p->original_spins[i];
    p->gs = 0;
}

/*Calculate delta E for flipping spin i
  param i:  spin index
  param p:  ising problem struct
*/
long int get_dE_local(const int i, int const *spins, IsingProblem const *p) {

    long int dE = p->h[i];
    int len = p->adj[i].len;

    int j;
    for(int k = 0; k < len; k++) {
        j = p->adj[i].nidx[k];
        dE += (spins[j])*(p->J[i][j]);
    }

    return -2*(spins[i])*dE;
}

long int get_E_local(int const *spins, IsingProblem const *p) {

    long int E = 0;
    long int E_i;

    int i; int j; int k; int len;
    for (i = 0; i < (p->N); i++) {
        E_i = p->h[i];
        k = 0;
        len = p->adj[i].len;
        while(k < len) {
            j = p->adj[i].nidx[k];
            E_i += .5*(spins[j])*(p->J[i][j]);
            k++;
        }
        E += E_i*(spins[i]);
    }
    return E;
}

/*Convert a spins vector in {+1, -1} to a hex representation
  spins[0] is MSB
  N:        length of the spin vector
  spins:    vector in {+1, -1}
  hex:      char buffer for writing to
            (length of hex) >= (length of spins + 4)/4
*/
void spins_as_hex(int N, int* spins, char* hex) {

    unsigned hex_digit = 0;
    int i = 0;
    char* j = hex;
    int stop = 0; //end of first digit, if less than 4
    if(N > 4)
        stop = N % 4;

    while(true) {
        if(spins[i] == 1) {
            hex_digit |= 1;
        }
        i++;
        if(i == N) {
            sprintf(j, "%x", hex_digit);
            break;
        }
        else if(i == stop) {
            sprintf(j, "%x", hex_digit);
            j++;
            hex_digit = 0;
        }
        else if((i > stop) && (((i-stop) % 4) == 0)) {
            sprintf(j, "%x", hex_digit);
            j++;
            hex_digit = 0;
        }
        else
            hex_digit <<= 1;
    }
}

/*write to spins
  spins[0] is MSB
  hex:      string of hex digits
  N:        length of the spins buffer
  spins:    write out to vector in {+1, -1}
*/
void hex_to_spins(int N, char* hex, int* spins) {

    // read the leftmost digit
    // check how many spins it needs to represent
    // write it to spins
    // proceed in groups of 4 going forward
    int stop = N;
    unsigned digit = 0;
    char *k = hex;
    int i = 0;
    char tmp[2];
    tmp[1] = '\0';
    if(N >= 4)
        stop = N % 4;

    while(k != NULL) {

        tmp[0] = *k;
        sscanf(tmp, "%x", &digit);
        k++;
        while(true) {

            if(stop == 0)
                break;

            stop--;
            if((digit >> stop) & 1)
                spins[i] = 1;
            else
                spins[i] = -1;

            i++;
            if(i == N) {
                assert(k != NULL);
                return;
            }
        }
        stop = 4;
    }
}
