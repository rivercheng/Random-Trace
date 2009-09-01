require("gsl")
local gsl = gsl
module(...)

--initiate the number generator. 
--Mersenne Twister is used here.
local generator = gsl.gsl_rng_alloc(gsl.gsl_rng_mt19937)

--global variable
function min() 
    return gsl.gsl_rng_min(generator)
end

function max() 
    return gsl.gsl_rng_max(generator)
end

--if n is given return a int random value in [0, n-1]
--else return a random int value in [min, max]
function nextInt(n)
    if n then
        return gsl.gsl_rng_uniform_int(generator, n)
    else
        return gsl.gsl_rng_get(generator)
    end
end

function nextDouble(allow_zero)
    allow_zero = allow_zero or true
    if allow_zero then
        return gsl.gsl_rng_uniform(generator)
    else
        return gsl.gsl_rng_uniform_pos(generator)
    end
end

function lognormal(zeta, sigma)
    return gsl.gsl_ran_lognormal(generator, zeta, sigma)
end

function gamma(a, b)
    return gsl.gsl_ran_gamma(generator, a, b)
end

function gaussian(sigma)
    return gsl.gsl_ran_gaussian(generator, sigma)
end

function exponential(mu)
    return gsl.gsl_ran_exponential(generator, mu)
end

function pareto(a, b)
    return gsl.gsl_ran_pareto(generator, a, b)
end

function weibull(a, b)
    return gsl.gsl_ran_weibull(generator, a, b)
end

function logarithmic(p)
    return gsl.gsl_ran_logarithmic(generator, p)
end

function poisson(mu)
    return gsl.gsl_ran_poisson(generator, mu)
end

function initiate_general(size, t)
    local array = gsl.new_doubleArray(size)
    for i = 0, size-1 do
        gsl.doubleArray_setitem(array, i, t[i+1])
    end
    return gsl.gsl_ran_discrete_preproc(size, array)
end

function discrete(lookup)
    return gsl.gsl_ran_discrete(generator, lookup)
end

function free_general(lookup)
    gsl.gsl_ran_discrete_free(lookup)
end

function general_pdf(k, lookup)
    return gsl.gsl_ran_discrete_pdf(k, lookup)
end





