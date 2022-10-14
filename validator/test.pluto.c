#include <omp.h>

#define S1(zT1,t)	X[t][t-1] = 1;
#define S2(zT1,t)	X[t][t+1] = 1;

		int t1, t2;

	int lb, ub, lbp, ubp, lb2, ub2;
	register int lbv, ubv;

/* Start of CLooG code */
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
      S1(t1,t2);
      S2(t1,t2);
    }
  }
}
/* End of CLooG code */
