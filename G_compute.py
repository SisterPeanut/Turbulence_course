# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 15:34:37 2025

@author: shipe822
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


path = "C:/Users/shipe822/Desktop/"


data_sheet1 = np.loadtxt(path+"FALL2_1.txt")
data_sheet2 = np.loadtxt(path+"FALL2_2.txt")


time = np.arange(np.datetime64('1994-06-14T00'), np.datetime64('1994-06-15T00'), np.timedelta64(10, 'm'))

G = data_sheet1[:,9]
U = data_sheet2[:,4:10]
Theta = data_sheet2[:,10:16]
Tg = data_sheet2[:,17:22]

# Height = np.array([0.84,1.95,4.78,10.1,17.2,29.0])
# log_height = np.log(Height)

depth = np.array([0.02,0.05,0.10,0.30,0.63])
log_depth = np.log(depth)


aT_az_array = np.full(len(time),np.nan)


def model(x, a, b, c):
    return a + b*x + c*x**2


for time_i in range(len(time)):
    u_vertical_i = Tg[time_i,:]
    params, covariance = curve_fit(model, log_depth,u_vertical_i)
    a_fit, b_fit, c_fit = params

    aT_az = (b_fit+2*c_fit*np.log(0.02))/0.02

    aT_az_array[time_i] = aT_az




lamda = 0.35   # optimal value
G_compute = -lamda*aT_az_array



fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(time, G, label="obs")
ax.plot(time, G_compute, label="compute")

ax.axhline(y=0.98,linestyle="--",color="black")
# ax.set_ylim(0.6,1.02)
ax.set_xlim(8930,8931)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Correlation coefficients $R^2$")
ax.legend()
ax.grid(linestyle="--")


np.savetxt("Ground heat flux.txt", G_compute)



