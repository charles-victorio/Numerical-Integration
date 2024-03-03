"""Examples of analyzing different algorithms.

This graph shows examples of ways we can analyze the performance of different algorithms.
"""

from algorithms import *

from math import exp, sin, cos, sqrt, pi

import numpy as np
import matplotlib.pyplot as plt

# https://math.stackexchange.com/questions/3427744/solve-this-integral-for-free-wifi
I2 = Integral(lambda x: (x * x * x * cos(0.5 * x) + 0.5) * sqrt(4 - x * x), -2, 2)
exact_answer = pi
solver = Integrator(I2)

def measure_parameters_vs_abs_error(integral: Integral, strategy: Strategy, params: list, exact_answer: float):
    # params: parameters of strategy for each trial
    solver = Integrator(integral)
    abs_error = []
    for p in params:
        solver.set_strategy(strategy(p)) # doesnt work when more than 1 parameter can be configured
        abs_error_for_this_trial = abs(solver.integrate().output - exact_answer)
        abs_error.append(abs_error_for_this_trial)
    return abs_error

# Monte Carlo
mc_n_samples_for_each_trial = [1000, 10_000, 100_000, 1_000_000]
mc_abs_error_for_each_trial = measure_parameters_vs_abs_error(I2, MonteCarlo, mc_n_samples_for_each_trial, pi)

# Romberg
r_M_for_each_trial = [5, 10, 15]
r_abs_error_for_each_trial = measure_parameters_vs_abs_error(I2, Romberg, r_M_for_each_trial, pi)

# Make graphs
fig, axes = plt.subplots(1, 2)
axes[0].plot(mc_n_samples_for_each_trial, mc_abs_error_for_each_trial)
axes[1].plot(r_M_for_each_trial, r_abs_error_for_each_trial)

axes[0].set_title("Monte Carlo")
axes[0].set_xlabel("Number of samples")
axes[0].set_ylabel("Absolute Error")
axes[1].set_title("Romberg")
axes[1].set_xlabel("Number of iterations of Romberg integration (M)")
axes[1].set_ylabel("Absolute Error")

plt.show()