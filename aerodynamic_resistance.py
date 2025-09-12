# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 15:50:30 2025

@author: shipe822
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



path = "C:/Users/shipe822/Desktop/"


data_sheet1 = np.loadtxt(path+"FALL2_1.txt")
data_sheet2 = np.loadtxt(path+"FALL2_2.txt")
u_star_array = np.loadtxt(path+"u_star.txt")
theta_w_array = np.loadtxt(path+"theta_w_flux.txt")
yita_array = np.loadtxt(path+"stability z-L.txt")
theta_star_array = -theta_w_array/u_star_array


time = np.arange(np.datetime64('1994-06-14T00'), np.datetime64('1994-06-15T00'), np.timedelta64(10, 'm'))


U = data_sheet2[:,4:10]
Theta = data_sheet2[:,10:16]
Tg = data_sheet2[:,17:22]

Height = np.array([0.84,1.95,4.78,10.1,17.2,29.0])
log_height = np.log(Height)


def Fai_m_compute(yita):
    if (yita<0):
        x = (1-16*yita)**(1/4)
        Fai = 2*np.log((1+x)/2)+np.log((1+x**2)/2)-2*np.arctan(x)+np.pi/2
    else:
        Fai = -5*yita
    return Fai


def Fai_h_compute(yita):
    if (yita<0):
        x = (1-16*yita)**(1/4)
        Fai = 2*np.log((1+x**2)/2)
    else:
        Fai = -5*yita
    return Fai


z0m_prescrib = 1.46e-2
h = 10*z0m_prescrib
d = 0.65*h


z0m_compute_array = np.zeros(len(time))
z0h_compute_array = np.zeros(len(time))

for time_i in range(len(time)):
    z0m_compute_array[time_i] = (10-d)*np.exp((-0.4*U[time_i,3])/u_star_array[time_i]-Fai_m_compute(yita_array[time_i]))
    z0h_compute_array[time_i] = (10-d)*np.exp((-0.4*(Theta[time_i,3]-Tg[time_i,0]))/theta_star_array[time_i]-Fai_h_compute(yita_array[time_i]))



# z0h = z0m/20  #R=20

z0m = np.nanmedian(z0m_compute_array)  #0.0329
h = 10*z0m # 32.9 cm
d = 0.65*h
z0h = z0m/20 #  0.00177
z=10

Ra_array3 = np.zeros(len(time))

for time_i in range(len(time)):
    Ra_array3[time_i] = (np.log((z-d)/z0h)-Fai_h_compute(yita_array[time_i]))*(np.log((z-d)/z0m)-Fai_m_compute(yita_array[time_i]))/(0.4**2*U[time_i,3])


Ra_array3[Ra_array3>300] = np.nan

np.savetxt("aerodynamic resistance.txt", Ra_array3)


# 12cm
# 32.9 roughly 33
# 60cm



