import random
import scipy.stats

def nextInt(upperbound):
    return random.randint(0, upperbound-1)

def nextDouble():
    return random.random()

def lognormal(sigma, scale):
    return scipy.stats.lognorm.rvs(sigma, scale = scale)[0]

def genextreme(a, b, c):
    return scipy.stats.genextreme.rvs(a, b, c)[0]

def weibull(a, loc, scale):
    return scipy.stats.weibull_min.rvs(a, loc, scale)[0]




