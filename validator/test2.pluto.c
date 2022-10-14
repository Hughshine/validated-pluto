#include <omp.h>
#include <math.h>
#define ceild(n,d)  (((n)<0) ? -((-(n))/(d)) : ((n)+(d)-1)/(d))
#define floord(n,d) (((n)<0) ? -((-(n)+(d)-1)/(d)) : (n)/(d))
#define max(x,y)    ((x) > (y)? (x) : (y))
#define min(x,y)    ((x) < (y)? (x) : (y))

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>


#ifdef PERFCTR
#include <papi.h>
#include "papi_defs.h"
#endif

#include "decls.h"

#include "util.h"

int main()
{
    int i, j, k, l, m, n, t;

    int i1, i2;

    double t_start, t_end;

    init_array();

#ifdef PERFCTR
    PERF_INIT; 
#endif

    IF_TIME(t_start = rtclock());

  int t1, t2;
 int lb, ub, lbp, ubp, lb2, ub2;
 register int lbv, ubv;
if (T >= 1) {
  lbp=0;
  ubp=floord(T-1,32);
#pragma omp parallel for private(lbv,ubv,t2)
  for (t1=lbp;t1<=ubp;t1++) {
    lbv=32*t1;
    ubv=min(T-1,32*t1+31);
#pragma ivdep
#pragma vector always
    for (t2=lbv;t2<=ubv;t2++) {
      X[t2][t2-1] = 1;;
      X[t2][t2+1] = 1;;
    }
  }
}

#pragma scop
    for (t = 0; t < T; t++) {
        X[t][t+1] = 2;
        X[t][t-1] = 1;
    }
#pragma endscop

    IF_TIME(t_end = rtclock());
    IF_TIME(fprintf(stderr, "%0.6lfs\n", t_end - t_start));

#ifdef PERFCTR
    PERF_EXIT; 
#endif

    if (fopen(".test", "r")) {
        print_array();
    }
    return 0;
}
