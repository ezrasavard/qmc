#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <assert.h>
#include <stdbool.h>
#include <string.h>
#include "ising.h"
#include "mcmc.h"
#include "qmc.h"

long int calc_jperp(int P, double T, double G, double Ep) {

    double Jp = -0.5*P*T*log(tanh(G/(Ep*P*T)));

    return((long int)(COUPLING_PRECISION)*Jp);
}

// adding clock zones will require each spin to have its own schedule
void qmc(double G0, double Gf, double Ep0, double Epf, int P, double T, \
         unsigned long int steps, IsingProblem* p, char* outfile,
         bool log_accepts, long int dump_threshold) {

    char buff[256];
    FILE *fp;
    if (dump_threshold != 0) {
        fp = fopen(outfile, "w+");
        if(fp == NULL) {
            perror("Error opening outfile");
            return;
        }
        sprintf(buff, "G0: %3lf, Gf: %6lf, Ep0: %3lf, Epf: %3lf, \
                P: %d, T: %6lf, steps: %lu\n", G0, Gf, Ep0, Epf, P, T, steps);
        fputs(buff, fp);
    }
    FILE *fp_accepts;
    if (log_accepts == true) {
        sprintf(buff,"%s_%s", outfile, "accepts");
        fp_accepts = fopen(buff, "w+");
        if(fp_accepts == NULL) {
            perror("Error opening accepts outfile");
            return;
        }
    }
    // Create schedules
    double* G_sched = malloc(sizeof(double)*steps);
    double* Ep_sched = malloc(sizeof(double)*steps);
    long int* Jp = malloc(sizeof(long int)*steps);
    double B = 1/(P*T);

    double dG = (G0 - Gf)/steps;
    double dEp = (Epf - Ep0)/steps; // can be zero
    assert(dG > 0);
    double G = G0;
    double Ep = Ep0;

    for(int i = 0; i < steps; i++, G -= dG) {
        Jp[i] = calc_jperp(P, T, G, Ep);
        G_sched[i] = G;
        Ep_sched[i] = Ep;
        Ep += dEp;
    }

    //Calculate initial energy
    long int E = get_E_local(p->spins, p);

    //Build slice array
    int** slices = malloc(sizeof(int*)*P);
    for(int i = 0; i < P; i++)
        slices[i] = malloc(sizeof(int)*(p->N));
    int* boundary_slices = malloc(sizeof(int)*(P+2));
    for(int i = 0; i < (P+2); i++) {
        boundary_slices[i] = i-1;
    }
    boundary_slices[0] = P-1;
    boundary_slices[P+1] = 0;

    long int* slice_energies = malloc(sizeof(long int)*P);

    for(int i = 0; i < (p->N); i++) {
        for(int k = 0; k < P; k++) {
            slices[k][i] = p->spins[i];
        }
    }

    for(int i = 0; i < P; i++) {
        slice_energies[i] = E;
    }

    //Anneal
    double dE = 0;
    long int dE_local = 0;
    long int dE_inter = 0;
    int left;
    int right;
    int i;
    long int* tmp_E = malloc(sizeof(long int)*P);
    for(long unsigned int tau = 0; tau < steps; tau++) {
        //local moves
        //each slice, random spin
        //check dE slice, dE interslice
        for(int k = 0; k < P; k++) {
            //random spin
            i = rand()/((RAND_MAX/(p->N)) + 1);
            assert(0 <= i < (p->N));
            dE_local = get_dE_local(i, slices[k], p);
            //interslice
            left = boundary_slices[k];
            right = boundary_slices[k+2];
            assert(0 <= left < (p->N));
            assert(0 <= right < (p->N));
            dE_inter = Jp[tau]*slices[k][i]*(slices[left][i] + slices[right][i]);
            dE = Ep_sched[tau]*(dE_local + dE_inter);
            if (MCStepAccepted(B, dE)) {
                if (log_accepts == true) {
                    sprintf(buff, "%lu\n", tau);
                    fputs(buff, fp_accepts);
                }
                slices[k][i] *= -1;
                assert((slices[k][i] == 1) || (slices[k][i] == -1));
                slice_energies[k] += dE_local;
            }
            if (dump_threshold != 0) {
                if ((slice_energies[k]) < dump_threshold) {
                    sprintf(buff, "%lu %lf\n", tau, (slice_energies[k]/COUPLING_PRECISION));
                    fputs(buff, fp);
                }
            }
        }
        //global move
        //all slices, same spin
        //check dE slices and add them up
        i = rand()/((RAND_MAX/(p->N)) + 1);
        dE = 0;
        for(int k = 0; k < P; k++) {
            tmp_E[k] = get_dE_local(i, slices[k], p);
            dE += tmp_E[k];
            if (dump_threshold != 0) {
                if ((slice_energies[k]) < dump_threshold) {
                    sprintf(buff, "%lu %lf\n", tau, (slice_energies[k]/COUPLING_PRECISION));
                    fputs(buff, fp);
                }
            }
        }
        dE *= Ep_sched[tau];
        if (MCStepAccepted(B, dE)) {
            if (log_accepts == true) {
                sprintf(buff, "%lu\n", tau);
                fputs(buff, fp_accepts);
            }
            for(int k = 0; k < P; k++) {
                slices[k][i] *= -1;
                slice_energies[k] += tmp_E[k];
            }
        }
    }

    if (log_accepts == true)
        fclose(fp_accepts);
    if (dump_threshold != 0)
        fclose(fp);
    //Return minimum from array
    double min = 0; // values are negative
    int kmin = 0;
    for (int k = 0; k < P; k++) {
        if (slice_energies[k] < min) {
            min = slice_energies[k];
            kmin = k;
        }
    }
    p->gs = min/COUPLING_PRECISION;

    for(int i = 0; i < (p->N); i++)
        p->spins[i] = slices[kmin][i];

    //Free everything
    free(G_sched);
    free(Ep_sched);
    free(Jp);
    free(tmp_E);
    for(int i = 0; i < P; i++) {
        int* ptr = slices[i];
        free(ptr);
    }
    free(slices);
    free(slice_energies);
}
