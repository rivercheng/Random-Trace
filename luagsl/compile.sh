#!/bin/sh
swig -lua gsl.i
gcc -I/usr/include/lua5.1 -c gsl_wrap.c
gcc -shared -I/usr/include/lua5.1 -L/usr/lib -lgsl -lgslcblas gsl_wrap.o -o gsl.so
