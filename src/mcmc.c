#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <assert.h>
#include <stdbool.h>
#include <string.h>
#include "ising.h"
#include "mcmc.h"
 
//*******************************************
//************** Begin Queue ****************
//*******************************************
/*
  Revolving Queue for SA data storage
  init_Queue: allocates memory
  delete_Queue: frees memory
  Queue_push: adds elements to the Queue and removes the oldest element
*/
Queue* init_Queue() {

    Queue* Q = malloc(sizeof(Queue));
    Q->capacity = SA_QUEUE_LEN;
    Q->data = calloc(SA_QUEUE_LEN, sizeof(long int));
    Q->head = Q->data;
    Q->end = Q->data + SA_QUEUE_LEN;

    return Q;
}

void delete_Queue(Queue* Q) {

    free(Q->data);
    free(Q);
}

void Queue_push(Queue* Q, double value) {
    //write value to head
    //increment head

    *(Q->head) = value;
    if (Q->head == Q->end) {
        Q->head = Q->data;
    }
    else
        Q->head++;
}

//*******************************************
//*************** End Queue *****************
//*******************************************

/*Metropolis-Hastings Acceptance Function
  param B:  inverse effective temperature "Beta"
  param dE: delta E for evaluation
*/
bool MCStepAccepted(double B, long int dE) {

    double r = (double)rand()/RAND_MAX;
    return ((long int)(dE <= 0) || (exp(-B*dE/COUPLING_PRECISION) > r));
}

/*
  Simple Simulated Annealing for Ising spin glass problems
  param T0:    initial annealing temperature
  param Tf:   final annealing temperature
  param steps:      number of Monte Carlo steps
  param problem:    ising problem structure pointer
*/
void SimAnneal(double T0, double Tf, unsigned long int steps, IsingProblem* problem, char* outfile, bool log_accepts, long int dump_threshold) {

    //Generate B schedule
    double* B = malloc(sizeof(double)*steps);
    double dT = (T0 - Tf)/steps;
    assert(dT > 0);
    double T = T0;
    for(int i = 0; i < steps; i++, T -= dT) {
        B[i] = 1/T;
    }
    char buff[256];
    FILE *fp;
    if (dump_threshold != 0) {
        fp = fopen(outfile, "w+");
        if(fp == NULL) {
            perror("Error opening file");
            return;
        }
        sprintf(buff, "T0: %6lf, Tf: %6lf, steps: %lu\n", T0, Tf, steps);
        fputs(buff, fp);
    }
    FILE *fp_accepts;
    if (log_accepts == true) {
        sprintf(buff,"%s_%s", outfile, "accepts");
        fp_accepts = fopen(buff, "w+");
        if(fp == NULL) {
            perror("Error opening accepts outfile");
            return;
        }
    }
    
    //Calculate initial energy
    long int E = get_E_local(problem->spins, problem);

    //Initialize a queue
    Queue* energies = init_Queue();

    //Anneal
    int r = 0;
    long int dE = 0;
    for (long unsigned int i = 0; i < steps; i++) {
        //random spin
        r = rand()/((RAND_MAX/(problem->N)) + 1);
        dE = get_dE_local(r, problem->spins, problem);
        if (MCStepAccepted(B[i], dE)) {
            if (log_accepts == true) {
                sprintf(buff, "%lu\n", i);
                fputs(buff, fp_accepts);
            }
            problem->spins[r] *= -1;
            E += dE;
        }
        if (dump_threshold != 0) {
            if (E < dump_threshold) {
                sprintf(buff, "%lu %ld\n", i, E);
                fputs(buff, fp);
            }
        }
        Queue_push(energies, E);
    }

    //Return minimum from queue
    long int min = 0; // values are negative
    for (int i = 0; i < energies->capacity; i++) {
        if (energies->data[i] < min)
            min = energies->data[i];
    }

    if (dump_threshold != 0)
        fclose(fp);
    free(B);
    delete_Queue(energies);

    problem->gs = min/COUPLING_PRECISION;
}
