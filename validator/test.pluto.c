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
    int i, j, k, l, m, n, t, k;

    int i1, i2;

    int X[10];

    int T = 10;

    double t_start, t_end;

    init_array();

#ifdef PERFCTR
    PERF_INIT; 
#endif

    IF_TIME(t_start = rtclock());

  int t1, t2, t3;
 register int lbv, ubv;
if (T >= 1) {
  for (t2=1;t2<=T-1;t2++) {
    for (t3=0;t3<=t2-1;t3++) {
      X[t2][t2+1] = 1;;
    }
  }
  for (t2=0;t2<=T-1;t2++) {
    X[t2][t2-1] = 1;;
  }
}

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
