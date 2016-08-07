#ifndef QMC
#define QMC

#define DWAVE_SCHED_LEN 1001

double qmc_calc_cubic(double t, double a3, double a2, double a1, double a0);

long int calc_jperp(int P, double T, double G, double Ep);

void qmc(double G0, double Gf, double Ep0, double Epf, int P, double T, \
         unsigned long int steps, IsingProblem* p, char* outfile, \
         bool log_accepts, long int dump_threshold, double gsched[4], \
         double epsched[4]);

#endif
