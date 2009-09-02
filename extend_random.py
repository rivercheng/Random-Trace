import random
import scipy.stats

def nextInt(upperbound):
    return random.randint(0, upperbound-1)

def nextDouble():
    return random.random()

def lognormal(miu, sigma):
    return scipy.stats.lognorm.rvs(miu, sigma)[0]

def genextreme(a, b, c):
    return scipy.stats.genextreme.rvs(a, b, c)[0]

def weibull(a, loc, scale):
    return scipy.stats.weibull_min.rvs(a, loc, scale)[0]




