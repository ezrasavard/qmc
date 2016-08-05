#include <assert.h>
#include <jansson.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "ising.h"
#include "mcmc.h"
#include "qmc.h"

void print_help() {

    printf("*** MCMC Solver ***\n");
    printf("Program is designed primarily for research using quantum monte carlo\n");
    printf("\nPositional Arguments:\
            \n\n\tproblem data file name\
            \n\toutput file name\
            \n\tsolver name ('qmc' or 'sa')\
            \n\t(DEPRECATED) number of monte carlo steps\
            \n\t(DEPRECATED) number of trials\
            \n\nKeyworded Arguments:\
            \n\n\t--steps <int>:        number of steps to use\
            \n\n\t--trials <int>:       number of trials\
            \n\n\t--log_accepts:        turn on logging of move acceptances\
            \n\n\t--log_thresh <float>: threshold for logging slice energies\
            \n\n\t--T <int>:            annealing temp\
            \n\n\t--P <int>:            (QMC) number of trotter slices\
            \n\n\t--PTxJ <double>:      overrides T choice and sets PT as multipler" 
            "\n\t                      of the average coupling strength in the problem\
            \n\n\t--MCSxS <int>:        sets the number of monte carlo steps as a "
            "\n\t                      multiple of the number of spins in the problem\
            \n\n\t--automagic:          (experimental!) automatically choose PTxJ and MCSxS "
            "\n\t                      to simulate the DWave output distribution\
            \n\nSee \"examples\" for examples of usage\n\n");

}

int main(int argc, char* argv[]) {

    srand(time(NULL));

//*******************************************
//************** Begin ArgParsing ***********
//*******************************************

    // validate arguments
    char* problem;
    char* outfile;
    char* solver;

    // not yet implemented
    // want a real argparser for these
    unsigned long int steps = 1e5; // number of Monte Carlo steps
    double T_start = 3; // override annealing start temp
    double T_low = ZERO_TEMP; // override annealing end temp
    double T = 0.015; // (QMC) annealing temp
    int P = 60; // (QMC) number of Trotter slices for QMC
    double G0 = 10; // (QMC) override initial tranverse field
    double Gf = 1e-4; // (QMC) override final tranverse field
    double Ep0 = 0.1; // (QMC) override initial longitudinal field 
    double Epf = 1; // (QMC) override final longitudinal field
    int trials = 5; // number of trials to run
    bool log_accepts = false;
    double log_thresh = 0;

    if(argc > 1)
        problem = argv[1];
    else {
        print_help();
        return 1;
    }

    if(strcmp(argv[1], "--help") == 0) {
        print_help();
        return 1;
    }

    if(argc > 2)
        outfile = argv[2];
    else {
        printf("missing output file name\n");
        print_help();
        return 1;
    }

    if(strcmp(argv[3], "qmc") == 0 || (strcmp(argv[3], "sa")) == 0)
        solver = argv[3];
    else {
        printf("invalid solver: %s\n",argv[3]);
        print_help();
        return 1;
    }

    // keeping for backwards compatibility with old tests
    steps = atol(argv[4]);
    trials = atoi(argv[5]);
    bool automagic = false;

    for (int i = 4; i < argc; i++) {
        if (strcmp(argv[i], "--P") == 0) {
            i++;
            P = atoi(argv[i]);
        }
        if (strcmp(argv[i], "--T") == 0) {
            i++;
            T = atof(argv[i]);
        }
        if (strcmp(argv[i], "--trials") == 0) {
            i++;
            trials = atoi(argv[i]);
        }
        if (strcmp(argv[i], "--steps") == 0) {
            i++;
            steps = atol(argv[i]);
        }
        if (strcmp(argv[i], "--log_accepts") == 0) {
            log_accepts = true;
        }
        if (strcmp(argv[i], "--log_thresh") == 0) {
            i++;
            log_thresh = atof(argv[i])*COUPLING_PRECISION;
        }
        if (strcmp(argv[i], "--automagic") == 0) {
            automagic = true;
        }
    }

    double PTxJ = 0;
    int MCSxS = 0;
    for (int i = 6; i < argc; i++) {
        if (strcmp(argv[i], "--PTxJ") == 0) {
            i++;
            PTxJ = atof(argv[i]);
        }
        if (strcmp(argv[i], "--MCSxS") == 0) {
            i++;
            MCSxS = atoi(argv[i]);
        }
    }


//*******************************************
//************** End ArgParsing *************
//*******************************************

    // initialize problem
    IsingProblem* p = init_IsingProblem(argv[1]);
    if(p == NULL) {
        printf("unable to initialize ising problem: %s\n", problem);
        return 1;
    }

    // prepare storage for solutions
    char* s = NULL;
    char param_string[256];
    /*
       Magic Numbers
       9:
           3 digits for " 0x"
           6 digits for representing the ground state
       4:
           1 hex character for 4 bits (spins)
     */
    int hex_len = (4 + MAX_SPINS)/4;
    int buff_len = 9 + hex_len;
    char soln_hex[hex_len];
    char soln_buff[buff_len];

    json_t *root = json_object();
    json_t *solutions = json_array(); //array of (gs_energy hex_spins) strings
    json_t *problem_descrip = json_array(); //array of (i j h/J) value strings

    json_object_set_new(root, "solver", json_string(solver) );
    json_object_set_new(root, "problem", problem_descrip);
    json_object_set_new(root, "data", solutions);

    // put problem data in JSON output
    for(int i = 0; i < (p->datalines); i++) {
        sprintf(soln_buff, "%d %d %ld", p->s1[i], p->s2[i], p->couplings[i]);
        json_array_append(problem_descrip, json_string(soln_buff));
    }

    // prepare parameters

    // automagic has been developed using P = 60 and adjusting T
    // automagic is the result of my undergraduate research
    // automagic has been tested on QCA circuits only and ranging from
    //  N = 14 to N = 215
    if (automagic == true) {
        double NlnN = (p->N)*log(p->N);
        double f = 6.5;
        double g = 0.5*powf((f-3.3),1.5) + 6.5;
        P = 60;
        PTxJ = f*powf(NlnN,0.33);
        MCSxS = g*powf(NlnN,0.66);
    }

    if (PTxJ != 0)
        T = PTxJ*(p->avg_coupling)/P;
    if (MCSxS != 0)
        steps = MCSxS*(p->N);

    printf("Average coupling: %6lf\n"
           "PT Value: %6lf\n",(p->avg_coupling),T*P);

    // run the solver
    char dumpfile[256];
    for(int i = 0; i < trials; i++) {
        sprintf(dumpfile, "%s_trial-%03d_dump.txt", outfile, i);
        if(strcmp(solver,"sa") == 0) {
            SimAnneal(T_start, T_low, steps, p, dumpfile, log_accepts,\
                      log_thresh);
            sprintf(param_string, "{\"T_start\": %6lf, \"T_low\": %6lf, \"steps\": %lu}",\
                    T_start, T_low, steps);
        }
        else {
            sprintf(param_string, "{\"G0\": %3lf, \"Gf\": %6lf, \"Ep0\": %3lf,"
                   " \"Epf\": %3lf, \"P\": %d, \"T\": %6lf, \"steps\": %lu,"
                   " \"PTxJ\": %3lf, \"MCSxS\": %d, \"N\": %d}",\
                   G0, Gf, Ep0, Epf, P, T, steps, PTxJ, MCSxS, p->N);
            assert(T > 0);
            qmc(G0, Gf, Ep0, Epf, P, T, steps, p, dumpfile, log_accepts,\
                log_thresh);
        }

        spins_as_hex((p->N), (p->spins), soln_hex);
        sprintf(soln_buff, "%6lf 0x%s", p->gs, soln_hex);
        json_array_append(solutions, json_string(soln_buff));
        reset_IsingProblem(p);
    }

    json_object_set_new(root, "test_params", json_string(param_string));

    s = json_dumps(root, JSON_INDENT(1));
    json_decref(root);

    // write output data to file
    FILE *fp = fopen(outfile, "w+");
    if(fp == NULL) {
        perror("Error opening file");
        return 1;
    }

    for(int i = 1; i < argc; i++) {
        printf("arg: %d - %s\n", i, argv[i]);
    }
    fputs(s, fp);
    fclose(fp);

    // clean up
    delete_IsingProblem(p);

}
