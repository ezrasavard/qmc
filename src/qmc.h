#ifndef QMC
#define QMC

long int calc_jperp(int P, double T, double G, double Ep);

void qmc(double G0, double Gf, double Ep0, double Epf, int P, double T, \
         unsigned long int steps, IsingProblem* p, char* outfile, \
         bool log_accepts, long int dump_threshold);

#endif
