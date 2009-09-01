%module gsl
%{
#include "gsl/gsl_randist.h"
#include "gsl/gsl_rng.h"
#include "gsl/gsl_types.h"
#include "gsl/gsl_errno.h"
%}

#define GSL_VAR extern

#include <stdio.h>
#include <errno.h>

enum { 
  GSL_SUCCESS  = 0, 
  GSL_FAILURE  = -1,
  GSL_CONTINUE = -2,  /* iteration has not converged */
  GSL_EDOM     = 1,   /* input domain error, e.g sqrt(-1) */
  GSL_ERANGE   = 2,   /* output range error, e.g. exp(1e100) */
  GSL_EFAULT   = 3,   /* invalid pointer */
  GSL_EINVAL   = 4,   /* invalid argument supplied by user */
  GSL_EFAILED  = 5,   /* generic failure */
  GSL_EFACTOR  = 6,   /* factorization failed */
  GSL_ESANITY  = 7,   /* sanity check failed - shouldn't happen */
  GSL_ENOMEM   = 8,   /* malloc failed */
  GSL_EBADFUNC = 9,   /* problem with user-supplied function */
  GSL_ERUNAWAY = 10,  /* iterative process is out of control */
  GSL_EMAXITER = 11,  /* exceeded max number of iterations */
  GSL_EZERODIV = 12,  /* tried to divide by zero */
  GSL_EBADTOL  = 13,  /* user specified an invalid tolerance */
  GSL_ETOL     = 14,  /* failed to reach the specified tolerance */
  GSL_EUNDRFLW = 15,  /* underflow */
  GSL_EOVRFLW  = 16,  /* overflow  */
  GSL_ELOSS    = 17,  /* loss of accuracy */
  GSL_EROUND   = 18,  /* failed because of roundoff error */
  GSL_EBADLEN  = 19,  /* matrix, vector lengths are not conformant */
  GSL_ENOTSQR  = 20,  /* matrix not square */
  GSL_ESING    = 21,  /* apparent singularity detected */
  GSL_EDIVERGE = 22,  /* integral or series is divergent */
  GSL_EUNSUP   = 23,  /* requested feature is not supported by the hardware */
  GSL_EUNIMPL  = 24,  /* requested feature not (yet) implemented */
  GSL_ECACHE   = 25,  /* cache limit exceeded */
  GSL_ETABLE   = 26,  /* table limit exceeded */
  GSL_ENOPROG  = 27,  /* iteration is not making progress towards solution */
  GSL_ENOPROGJ = 28,  /* jacobian evaluations are not improving the solution */
  GSL_ETOLF    = 29,  /* cannot reach the specified tolerance in F */
  GSL_ETOLX    = 30,  /* cannot reach the specified tolerance in X */
  GSL_ETOLG    = 31,  /* cannot reach the specified tolerance in gradient */
  GSL_EOF      = 32   /* end of file */
} ;

void gsl_error (const char * reason, const char * file, int line,
                int gsl_errno);

void gsl_stream_printf (const char *label, const char *file,
                        int line, const char *reason);

const char * gsl_strerror (const int gsl_errno);

typedef void gsl_error_handler_t (const char * reason, const char * file,
                                  int line, int gsl_errno);

typedef void gsl_stream_handler_t (const char * label, const char * file,
                                   int line, const char * reason);

gsl_error_handler_t * 
gsl_set_error_handler (gsl_error_handler_t * new_handler);

gsl_error_handler_t *
gsl_set_error_handler_off (void);

gsl_stream_handler_t * 
gsl_set_stream_handler (gsl_stream_handler_t * new_handler);

FILE * gsl_set_stream (FILE * new_stream);

/* GSL_ERROR: call the error handler, and return the error code */

#define GSL_ERROR(reason, gsl_errno) \
       do { \
       gsl_error (reason, __FILE__, __LINE__, gsl_errno) ; \
       return gsl_errno ; \
       } while (0)

/* GSL_ERROR_VAL: call the error handler, and return the given value */

#define GSL_ERROR_VAL(reason, gsl_errno, value) \
       do { \
       gsl_error (reason, __FILE__, __LINE__, gsl_errno) ; \
       return value ; \
       } while (0)

/* GSL_ERROR_VOID: call the error handler, and then return
   (for void functions which still need to generate an error) */

#define GSL_ERROR_VOID(reason, gsl_errno) \
       do { \
       gsl_error (reason, __FILE__, __LINE__, gsl_errno) ; \
       return ; \
       } while (0)

/* GSL_ERROR_NULL suitable for out-of-memory conditions */

#define GSL_ERROR_NULL(reason, gsl_errno) GSL_ERROR_VAL(reason, gsl_errno, 0)

/* Sometimes you have several status results returned from
 * function calls and you want to combine them in some sensible
 * way. You cannot produce a "total" status condition, but you can
 * pick one from a set of conditions based on an implied hierarchy.
 *
 * In other words:
 *    you have: status_a, status_b, ...
 *    you want: status = (status_a if it is bad, or status_b if it is bad,...)
 *
 * In this example you consider status_a to be more important and
 * it is checked first, followed by the others in the order specified.
 *
 * Here are some dumb macros to do this.
 */
#define GSL_ERROR_SELECT_2(a,b)       ((a) != GSL_SUCCESS ? (a) : ((b) != GSL_SUCCESS ? (b) : GSL_SUCCESS))
#define GSL_ERROR_SELECT_3(a,b,c)     ((a) != GSL_SUCCESS ? (a) : GSL_ERROR_SELECT_2(b,c))
#define GSL_ERROR_SELECT_4(a,b,c,d)   ((a) != GSL_SUCCESS ? (a) : GSL_ERROR_SELECT_3(b,c,d))
#define GSL_ERROR_SELECT_5(a,b,c,d,e) ((a) != GSL_SUCCESS ? (a) : GSL_ERROR_SELECT_4(b,c,d,e))

#define GSL_STATUS_UPDATE(sp, s) do { if ((s) != GSL_SUCCESS) *(sp) = (s);} while(0)



typedef struct
  {
    const char *name;
    unsigned long int max;
    unsigned long int min;
    size_t size;
    void (*set) (void *state, unsigned long int seed);
    unsigned long int (*get) (void *state);
    double (*get_double) (void *state);
  }
gsl_rng_type;

typedef struct
  {
    const gsl_rng_type * type;
    void *state;
  }
gsl_rng;


/* These structs also need to appear in default.c so you can select
   them via the environment variable GSL_RNG_TYPE */

GSL_VAR const gsl_rng_type *gsl_rng_borosh13;
GSL_VAR const gsl_rng_type *gsl_rng_coveyou;
GSL_VAR const gsl_rng_type *gsl_rng_cmrg;
GSL_VAR const gsl_rng_type *gsl_rng_fishman18;
GSL_VAR const gsl_rng_type *gsl_rng_fishman20;
GSL_VAR const gsl_rng_type *gsl_rng_fishman2x;
GSL_VAR const gsl_rng_type *gsl_rng_gfsr4;
GSL_VAR const gsl_rng_type *gsl_rng_knuthran;
GSL_VAR const gsl_rng_type *gsl_rng_knuthran2;
GSL_VAR const gsl_rng_type *gsl_rng_knuthran2002;
GSL_VAR const gsl_rng_type *gsl_rng_lecuyer21;
GSL_VAR const gsl_rng_type *gsl_rng_minstd;
GSL_VAR const gsl_rng_type *gsl_rng_mrg;
GSL_VAR const gsl_rng_type *gsl_rng_mt19937;
GSL_VAR const gsl_rng_type *gsl_rng_mt19937_1999;
GSL_VAR const gsl_rng_type *gsl_rng_mt19937_1998;
GSL_VAR const gsl_rng_type *gsl_rng_r250;
GSL_VAR const gsl_rng_type *gsl_rng_ran0;
GSL_VAR const gsl_rng_type *gsl_rng_ran1;
GSL_VAR const gsl_rng_type *gsl_rng_ran2;
GSL_VAR const gsl_rng_type *gsl_rng_ran3;
GSL_VAR const gsl_rng_type *gsl_rng_rand;
GSL_VAR const gsl_rng_type *gsl_rng_rand48;
GSL_VAR const gsl_rng_type *gsl_rng_random128_bsd;
GSL_VAR const gsl_rng_type *gsl_rng_random128_glibc2;
GSL_VAR const gsl_rng_type *gsl_rng_random128_libc5;
GSL_VAR const gsl_rng_type *gsl_rng_random256_bsd;
GSL_VAR const gsl_rng_type *gsl_rng_random256_glibc2;
GSL_VAR const gsl_rng_type *gsl_rng_random256_libc5;
GSL_VAR const gsl_rng_type *gsl_rng_random32_bsd;
GSL_VAR const gsl_rng_type *gsl_rng_random32_glibc2;
GSL_VAR const gsl_rng_type *gsl_rng_random32_libc5;
GSL_VAR const gsl_rng_type *gsl_rng_random64_bsd;
GSL_VAR const gsl_rng_type *gsl_rng_random64_glibc2;
GSL_VAR const gsl_rng_type *gsl_rng_random64_libc5;
GSL_VAR const gsl_rng_type *gsl_rng_random8_bsd;
GSL_VAR const gsl_rng_type *gsl_rng_random8_glibc2;
GSL_VAR const gsl_rng_type *gsl_rng_random8_libc5;
GSL_VAR const gsl_rng_type *gsl_rng_random_bsd;
GSL_VAR const gsl_rng_type *gsl_rng_random_glibc2;
GSL_VAR const gsl_rng_type *gsl_rng_random_libc5;
GSL_VAR const gsl_rng_type *gsl_rng_randu;
GSL_VAR const gsl_rng_type *gsl_rng_ranf;
GSL_VAR const gsl_rng_type *gsl_rng_ranlux;
GSL_VAR const gsl_rng_type *gsl_rng_ranlux389;
GSL_VAR const gsl_rng_type *gsl_rng_ranlxd1;
GSL_VAR const gsl_rng_type *gsl_rng_ranlxd2;
GSL_VAR const gsl_rng_type *gsl_rng_ranlxs0;
GSL_VAR const gsl_rng_type *gsl_rng_ranlxs1;
GSL_VAR const gsl_rng_type *gsl_rng_ranlxs2;
GSL_VAR const gsl_rng_type *gsl_rng_ranmar;
GSL_VAR const gsl_rng_type *gsl_rng_slatec;
GSL_VAR const gsl_rng_type *gsl_rng_taus;
GSL_VAR const gsl_rng_type *gsl_rng_taus2;
GSL_VAR const gsl_rng_type *gsl_rng_taus113;
GSL_VAR const gsl_rng_type *gsl_rng_transputer;
GSL_VAR const gsl_rng_type *gsl_rng_tt800;
GSL_VAR const gsl_rng_type *gsl_rng_uni;
GSL_VAR const gsl_rng_type *gsl_rng_uni32;
GSL_VAR const gsl_rng_type *gsl_rng_vax;
GSL_VAR const gsl_rng_type *gsl_rng_waterman14;
GSL_VAR const gsl_rng_type *gsl_rng_zuf;

const gsl_rng_type ** gsl_rng_types_setup(void);

GSL_VAR const gsl_rng_type *gsl_rng_default;
GSL_VAR unsigned long int gsl_rng_default_seed;

gsl_rng *gsl_rng_alloc (const gsl_rng_type * T);
int gsl_rng_memcpy (gsl_rng * dest, const gsl_rng * src);
gsl_rng *gsl_rng_clone (const gsl_rng * r);

void gsl_rng_free (gsl_rng * r);

void gsl_rng_set (const gsl_rng * r, unsigned long int seed);
unsigned long int gsl_rng_max (const gsl_rng * r);
unsigned long int gsl_rng_min (const gsl_rng * r);
const char *gsl_rng_name (const gsl_rng * r);

int gsl_rng_fread (FILE * stream, gsl_rng * r);
int gsl_rng_fwrite (FILE * stream, const gsl_rng * r);

size_t gsl_rng_size (const gsl_rng * r);
void * gsl_rng_state (const gsl_rng * r);

void gsl_rng_print_state (const gsl_rng * r);

const gsl_rng_type * gsl_rng_env_setup (void);

unsigned long int gsl_rng_get (const gsl_rng * r);
double gsl_rng_uniform (const gsl_rng * r);
double gsl_rng_uniform_pos (const gsl_rng * r);
unsigned long int gsl_rng_uniform_int (const gsl_rng * r, unsigned long int n);


#ifdef HAVE_INLINE
extern inline unsigned long int gsl_rng_get (const gsl_rng * r);

extern inline unsigned long int
gsl_rng_get (const gsl_rng * r)
{
  return (r->type->get) (r->state);
}

extern inline double gsl_rng_uniform (const gsl_rng * r);

extern inline double
gsl_rng_uniform (const gsl_rng * r)
{
  return (r->type->get_double) (r->state);
}

extern inline double gsl_rng_uniform_pos (const gsl_rng * r);

extern inline double
gsl_rng_uniform_pos (const gsl_rng * r)
{
  double x ;
  do
    {
      x = (r->type->get_double) (r->state) ;
    }
  while (x == 0) ;

  return x ;
}

extern inline unsigned long int gsl_rng_uniform_int (const gsl_rng * r, unsigned long int n);

extern inline unsigned long int
gsl_rng_uniform_int (const gsl_rng * r, unsigned long int n)
{
  unsigned long int offset = r->type->min;
  unsigned long int range = r->type->max - offset;
  unsigned long int scale;
  unsigned long int k;

  if (n > range || n == 0) 
    {
      GSL_ERROR_VAL ("invalid n, either 0 or exceeds maximum value of generator",
                     GSL_EINVAL, 0) ;
    }

  scale = range / n;

  do
    {
      k = (((r->type->get) (r->state)) - offset) / scale;
    }
  while (k >= n);

  return k;
}
#endif HAVE_INLINE

unsigned int gsl_ran_bernoulli (const gsl_rng * r, double p);
double gsl_ran_bernoulli_pdf (const unsigned int k, double p);

double gsl_ran_beta (const gsl_rng * r, const double a, const double b);
double gsl_ran_beta_pdf (const double x, const double a, const double b);

unsigned int gsl_ran_binomial (const gsl_rng * r, double p, unsigned int n);
unsigned int gsl_ran_binomial_knuth (const gsl_rng * r, double p, unsigned int n);
unsigned int gsl_ran_binomial_tpe (const gsl_rng * r, double p, unsigned int n);
double gsl_ran_binomial_pdf (const unsigned int k, const double p, const unsigned int n);

double gsl_ran_exponential (const gsl_rng * r, const double mu);
double gsl_ran_exponential_pdf (const double x, const double mu);

double gsl_ran_exppow (const gsl_rng * r, const double a, const double b);
double gsl_ran_exppow_pdf (const double x, const double a, const double b);

double gsl_ran_cauchy (const gsl_rng * r, const double a);
double gsl_ran_cauchy_pdf (const double x, const double a);

double gsl_ran_chisq (const gsl_rng * r, const double nu);
double gsl_ran_chisq_pdf (const double x, const double nu);

void gsl_ran_dirichlet (const gsl_rng * r, const size_t K, const double alpha[], double theta[]);
double gsl_ran_dirichlet_pdf (const size_t K, const double alpha[], const double theta[]);
double gsl_ran_dirichlet_lnpdf (const size_t K, const double alpha[], const double theta[]);

double gsl_ran_erlang (const gsl_rng * r, const double a, const double n);
double gsl_ran_erlang_pdf (const double x, const double a, const double n);

double gsl_ran_fdist (const gsl_rng * r, const double nu1, const double nu2);
double gsl_ran_fdist_pdf (const double x, const double nu1, const double nu2);

double gsl_ran_flat (const gsl_rng * r, const double a, const double b);
double gsl_ran_flat_pdf (double x, const double a, const double b);

double gsl_ran_gamma (const gsl_rng * r, const double a, const double b);
double gsl_ran_gamma_int (const gsl_rng * r, const unsigned int a);
double gsl_ran_gamma_pdf (const double x, const double a, const double b);
double gsl_ran_gamma_mt (const gsl_rng * r, const double a, const double b);
double gsl_ran_gamma_knuth (const gsl_rng * r, const double a, const double b);

double gsl_ran_gaussian (const gsl_rng * r, const double sigma);
double gsl_ran_gaussian_ratio_method (const gsl_rng * r, const double sigma);
double gsl_ran_gaussian_ziggurat (const gsl_rng * r, const double sigma);
double gsl_ran_gaussian_pdf (const double x, const double sigma);

double gsl_ran_ugaussian (const gsl_rng * r);
double gsl_ran_ugaussian_ratio_method (const gsl_rng * r);
double gsl_ran_ugaussian_pdf (const double x);

double gsl_ran_gaussian_tail (const gsl_rng * r, const double a, const double sigma);
double gsl_ran_gaussian_tail_pdf (const double x, const double a, const double sigma);

double gsl_ran_ugaussian_tail (const gsl_rng * r, const double a);
double gsl_ran_ugaussian_tail_pdf (const double x, const double a);

void gsl_ran_bivariate_gaussian (const gsl_rng * r, double sigma_x, double sigma_y, double rho, double *x, double *y);
double gsl_ran_bivariate_gaussian_pdf (const double x, const double y, const double sigma_x, const double sigma_y, const double rho);

double gsl_ran_landau (const gsl_rng * r);
double gsl_ran_landau_pdf (const double x);

unsigned int gsl_ran_geometric (const gsl_rng * r, const double p);
double gsl_ran_geometric_pdf (const unsigned int k, const double p);

unsigned int gsl_ran_hypergeometric (const gsl_rng * r, unsigned int n1, unsigned int n2, unsigned int t);
double gsl_ran_hypergeometric_pdf (const unsigned int k, const unsigned int n1, const unsigned int n2, unsigned int t);

double gsl_ran_gumbel1 (const gsl_rng * r, const double a, const double b);
double gsl_ran_gumbel1_pdf (const double x, const double a, const double b);

double gsl_ran_gumbel2 (const gsl_rng * r, const double a, const double b);
double gsl_ran_gumbel2_pdf (const double x, const double a, const double b);

double gsl_ran_logistic (const gsl_rng * r, const double a);
double gsl_ran_logistic_pdf (const double x, const double a);

double gsl_ran_lognormal (const gsl_rng * r, const double zeta, const double sigma);
double gsl_ran_lognormal_pdf (const double x, const double zeta, const double sigma);

unsigned int gsl_ran_logarithmic (const gsl_rng * r, const double p);
double gsl_ran_logarithmic_pdf (const unsigned int k, const double p);

void gsl_ran_multinomial (const gsl_rng * r, const size_t K,
                          const unsigned int N, const double p[],
                          unsigned int n[] );
double gsl_ran_multinomial_pdf (const size_t K,
                                const double p[], const unsigned int n[] );
double gsl_ran_multinomial_lnpdf (const size_t K,
                           const double p[], const unsigned int n[] );


unsigned int gsl_ran_negative_binomial (const gsl_rng * r, double p, double n);
double gsl_ran_negative_binomial_pdf (const unsigned int k, const double p, double n);

unsigned int gsl_ran_pascal (const gsl_rng * r, double p, unsigned int n);
double gsl_ran_pascal_pdf (const unsigned int k, const double p, unsigned int n);

double gsl_ran_pareto (const gsl_rng * r, double a, const double b);
double gsl_ran_pareto_pdf (const double x, const double a, const double b);

unsigned int gsl_ran_poisson (const gsl_rng * r, double mu);
void gsl_ran_poisson_array (const gsl_rng * r, size_t n, unsigned int array[],
                            double mu);
double gsl_ran_poisson_pdf (const unsigned int k, const double mu);

double gsl_ran_rayleigh (const gsl_rng * r, const double sigma);
double gsl_ran_rayleigh_pdf (const double x, const double sigma);

double gsl_ran_rayleigh_tail (const gsl_rng * r, const double a, const double sigma);
double gsl_ran_rayleigh_tail_pdf (const double x, const double a, const double sigma);

double gsl_ran_tdist (const gsl_rng * r, const double nu);
double gsl_ran_tdist_pdf (const double x, const double nu);

double gsl_ran_laplace (const gsl_rng * r, const double a);
double gsl_ran_laplace_pdf (const double x, const double a);

double gsl_ran_levy (const gsl_rng * r, const double c, const double alpha);
double gsl_ran_levy_skew (const gsl_rng * r, const double c, const double alpha, const double beta);

double gsl_ran_weibull (const gsl_rng * r, const double a, const double b);
double gsl_ran_weibull_pdf (const double x, const double a, const double b);

void gsl_ran_dir_2d (const gsl_rng * r, double * x, double * y);
void gsl_ran_dir_2d_trig_method (const gsl_rng * r, double * x, double * y);
void gsl_ran_dir_3d (const gsl_rng * r, double * x, double * y, double * z);
void gsl_ran_dir_nd (const gsl_rng * r, size_t n, double * x);

void gsl_ran_shuffle (const gsl_rng * r, void * base, size_t nmembm, size_t size);
int gsl_ran_choose (const gsl_rng * r, void * dest, size_t k, void * src, size_t n, size_t size) ;
void gsl_ran_sample (const gsl_rng * r, void * dest, size_t k, void * src, size_t n, size_t size) ;


typedef struct {                /* struct for Walker algorithm */
    size_t K;
    size_t *A;
    double *F;
} gsl_ran_discrete_t;

/*%include <typemaps.i>
%apply (long, double *IN) {(long K, double *P)};*/
%include <carrays.i>
%array_functions(double, doubleArray)
gsl_ran_discrete_t * gsl_ran_discrete_preproc (size_t K, const double *P); 

void gsl_ran_discrete_free(gsl_ran_discrete_t *g);
size_t gsl_ran_discrete (const gsl_rng *r, const gsl_ran_discrete_t *g);
double gsl_ran_discrete_pdf (size_t k, const gsl_ran_discrete_t *g);

