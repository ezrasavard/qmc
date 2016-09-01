#ifndef MCMC
#define MCMC

#define ZERO_TEMP 1e-6
#define SA_QUEUE_LEN 1000

// Revolving Queue for SA data storage
typedef struct Queue {
    int capacity;
    long int* data;
    long int* head;
    long int* end;
}Queue;

Queue* init_Queue();

void delete_Queue(Queue* Q);

void Queue_push(Queue* Q, double value);

bool MCStepAccepted(double B, long int dE);

void SimAnneal(double T0, double Tf, unsigned long int steps, IsingProblem* problem, char* outfile, bool log_accepts, long int dump_threshold);

#endif
