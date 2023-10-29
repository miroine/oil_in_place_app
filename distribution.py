import pandas as pd 
import base64
import statistics
import scipy.stats as stats
import numpy as np


def normal_distribution(mean_value=0, std_value=1, size=10000, truncated_limites =None, seed=100): 
    """
    return a numpy array based on normal distribution
    """
    if truncated_limites:
        return stats.truncnorm((truncated_limites[0] - mean_value) / std_value, (truncated_limites[1] - mean_value) / std_value, loc=mean_value, scale=std_value).rvs(size = size, random_state=seed) 
    else:
        return stats.norm.rvs(size=size, loc=mean_value, scale=std_value)

def triangular_distribution(ml_value=10, min_value=0, max_value= 20, size=10000, seed=100):
    """
    return a triangular distribution
    """
    return stats.triang.rvs((ml_value-min_value)/(max_value-min_value), loc=min_value, scale=max_value-min_value, size=size, random_state = seed)


def uniform_distribution(min_value=0, max_value=1, size=10000, random_state=100):
    """
    return a uniform distribution
    """
    return stats.uniform.rvs(loc = min_value, scale=max_value-min_value, size=size, random_state = random_state)

def beta_distribution(a=1, b=1, size=10000):
    """
    """
    return stats.beta.rvs(a=a,b=b, size=size)

