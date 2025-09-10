# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 09:36:01 2025

@author: shipe822
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import curve_fit


path = "C:/Users/shipe822/Desktop/"


data_sheet1 = np.loadtxt(path+"FALL2_1.txt")
data_sheet2 = np.loadtxt(path+"FALL2_2.txt")


time = np.arange(np.datetime64('1994-06-14T00'), np.datetime64('1994-06-15T00'), np.timedelta64(10, 'm'))


U = data_sheet2[:,4:10]
Theta = data_sheet2[:,10:16]
Tg = data_sheet2[:,17:22]

Height = np.array([0.84,1.95,4.78,10.1,17.2,29.0])
log_height = np.log(Height)

U_gradient_array = np.zeros(len(time))
theta_gradient_array = np.zeros(len(time))
theta_mean_array  = np.zeros(len(time))


def model(x, a, b, c):
    return a + b*x + c*x**2


for time_i in range(len(time)):
    u_vertical_i = U[time_i,:]
    params, covariance = curve_fit(model, log_height,u_vertical_i)
    a_fit, b_fit, c_fit = params

    U_gradient_array[time_i] = b_fit+2*c_fit*np.log(10)   # z=10



for time_i in range(len(time)):
    u_vertical_i = Theta[time_i,:]
    params, covariance = curve_fit(model, log_height,u_vertical_i)
    a_fit, b_fit, c_fit = params

    theta_gradient_array[time_i] = b_fit+2*c_fit*np.log(10)   # z=10
    theta_mean_array[time_i] = np.nanmean(u_vertical_i) + 273.15


def fai_m_compute(yita):
    if (yita<0):
        return (1-16*yita)**(-1/4)
    else:
        return 1+5*yita
    
def fai_h_compute(yita):
    if (yita<0):
        return (1-16*yita)**(-1/2)
    else:
        return 1+5*yita


#each time
def itervative(U_gradient,theta_gradient,theta_mean):  #au/alnz atheta/alnz
    change=100
    change_absolute=100
    flag=0
    alpha = 0.2
    
    u_star = 0.4*U_gradient
    theta_star = 0.4*theta_gradient
    L = u_star**2/(0.4*9.8*theta_star/theta_mean) 
    yita = 10/L
    fai_m = fai_m_compute(yita)
    fai_h = fai_h_compute(yita) 
    
    
    while(change>0.001 and change_absolute>0.001):
        
        u_star_old = u_star
        u_star_compute = 0.4*U_gradient/fai_m          
        u_star = (1-alpha)*u_star_old+alpha*u_star_compute        
        change = np.abs(u_star_old-u_star_compute)/u_star
        change_absolute = np.abs(u_star_old-u_star_compute)
        
        # print("u_star:",u_star)
        
        theta_star_old = theta_star
        theta_star_compute = 0.4*theta_gradient/fai_h
        theta_star = (1-alpha)*theta_star_old+alpha*theta_star_compute   

 
        L_old = L
        L_compute = u_star**2/(0.4*9.8*theta_star/theta_mean) 
        L = (1-alpha)*L_old+alpha*L_compute
        
        # yita = Height/L  
        yita = 10/L  
        # print("yita:",yita)
        
        fai_m = fai_m_compute(yita) 
        fai_h = fai_h_compute(yita) 
        flag+=1
    
    return u_star,theta_star,yita



u_star_array = np.zeros(len(time))
theta_star_array = np.zeros(len(time))
yita_array = np.zeros(len(time))


for time_i in range(len(time)):

    U_gradient=U_gradient_array[time_i]
    theta_gradient=theta_gradient_array[time_i]
    theta_mean = theta_mean_array[time_i]

    u_star,theta_star,yita = itervative(U_gradient,theta_gradient,theta_mean)
    
    u_star_array[time_i] = u_star
    theta_star_array[time_i] = theta_star
    yita_array[time_i] = yita



theta_w_flux_array = -1*u_star_array*theta_star_array


np.savetxt("u_star.txt", u_star_array)
np.savetxt("theta_w_flux.txt", theta_w_flux_array)
np.savetxt("stability z-L.txt", yita_array)
















