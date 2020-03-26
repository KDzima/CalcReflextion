# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:25:52 2020

@author: Dima
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import interpolate


Params=np.genfromtxt('Parameters.txt',skip_header=1)
FolderList=os.listdir('Data\\')

def moving_average(a, n=20) :
    ret = np.nancumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

for i,wave in enumerate(Params[:,0]):
    FolderPath='Data\\'+str(wave)+'\\'
    SignalArray=np.loadtxt(FolderPath+'TDArray.txt')
    TimeArray=np.loadtxt(FolderPath+'TimesArray.txt')
    Positions=np.loadtxt(FolderPath+'TD_Positions.txt')  
    
    
    tl=Params[i,3]*1e-8
    tm=Params[i,2]*1e-8
    t0=Params[i,1]*1e-8
    
    z1=Params[i,4]
    z2=Params[i,5]
              
    i0=np.argmin(abs(TimeArray-t0))
    im=np.argmin(abs(TimeArray-tm))
    il=np.argmin(abs(TimeArray-tl))
    
    j1=np.argmin(abs(Positions[:,1]-z1))
    j2=np.argmin(abs(Positions[:,1]-z2))
    
    TD1=SignalArray[im:il,j1:j2]
    TD2=SignalArray[i0:im,j1:j2]
    TD3=SignalArray[il:-1,j1:j2]
    T1=TimeArray[im:il]
    T2=TimeArray[i0:im]
    Z_buf=Positions[j1:j2,1]
    
    Z=np.zeros(len(Z_buf))
    for i in range(len(Z_buf)):
        Z[i]=(Z_buf[-1]-Z_buf[i])*2.5e-6
    R=np.zeros(len(TD1[0,:]))
    TD1sumT=np.zeros(len(TD1[0,:]))
    TD2sumT=np.zeros(len(TD1[0,:]))
    #IR=np.zeros(len(TD1[0,:]))
    #IR=np.nan
    V=np.zeros(len(TD1[0,:]))
    for k in range(len(TD1[0,:])):
        TD1sumT[k]=np.sum(TD1[:,k])
        TD2sumT[k]=np.sum(TD2[:,k])
    TD1meanTZ=moving_average(TD1sumT,20)
    TD2meanTZ=moving_average(TD2sumT,20)
    IR=np.zeros(len(TD1meanTZ))
    for k in range(len(TD1meanTZ)):
        noise=np.mean(TD3[:,k])
        if (np.max(TD1meanTZ[k])/noise>10) and ((TD2meanTZ[k])/noise>10):
            IR[k]=TD1meanTZ[k]/TD2meanTZ[k]
            
    IR=IR[np.argwhere(IR)]
            

    print('Wavelength', wave,' integral ref mean ', np.mean(IR),' std ', np.std(IR))
    
    np.savetxt(FolderPath+'Reflection_by_integral.txt',IR)
    