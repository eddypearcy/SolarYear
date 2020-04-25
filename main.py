# -*- coding: utf-8 -*-

import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt


# Importing the production data into an array of floats
# Dates are not needed since the data is already sorted
production = np.genfromtxt("./daily_production.csv", delimiter=",", skip_header=1, usecols=[1])

# Removing the NaN values
production = production[np.bitwise_not(np.isnan(production))]

# Creating a day-based indexing array
days = np.arange(0, production.size)


# Creating the parametric function that the data will be fitted to
# A sinewave seems appropriate since to analyze the periodic behaviour of the data
def fit_func(x, a, b, c, d):
    return a * np.sin(2 * np.pi * x / b + c) + d


# Fitting the sinewave to the data
# For this fit to work, the optimizer needs an initial guess: "there are somewhere around 300 days in a year"
[opt_a, opt_b, opt_c, opt_d], pcov = opt.curve_fit(fit_func, days, production, p0=(1e04, 300, 0, 1e04))

# Let's compare the fit to the original data
fig, ax = plt.subplots(1, 1)
ax.scatter(days, production / 1000, s=1, c="r", label="Data points")
ax.plot(days, fit_func(days, opt_a, opt_b, opt_c, opt_d) / 1000, "k-", label="Fitted sinewave")
ax.set_xlabel("Index of the day")
ax.set_ylabel("Daily production [kWh]")
ax.grid()
ax.legend()

# 'opt_b' contains the fitted value for the parameter 'b' of 'fit_func'
print("There are approximately {:3.0f} days in a year!".format(opt_b))

# Display the plot
plt.show()
