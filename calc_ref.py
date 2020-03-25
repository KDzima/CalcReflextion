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
from PyQt5.QtCore import QObject

def moving_average(a, n=20) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

if __name__ == "__main__":

    tl=2.74e-8
    tm=2.628e-8
    t0=2.518e-8
    z1=1800
    z2=2250 #2260
         
    SignalArray=np.loadtxt('TDArray.txt')
    TimeArray=np.loadtxt('TimesArray.txt')
    TimeArraySub=TimeArray-2.45e-8
    Positions=np.loadtxt('TD_Positions.txt')
    Positions_in_mkm=np.zeros(len(Positions[:,1]))
    
    for i in range(len(Positions[:,1])):
        Positions_in_mkm[i]=(Positions[i,1]-Positions[-1,1])*2.5
        
    i0=np.argmin(abs(TimeArray-t0))
    im=np.argmin(abs(TimeArray-tm))
    il=np.argmin(abs(TimeArray-tl))
    #j1,j2=0,360
    plt.figure(1)
    plt.plot(TimeArray,SignalArray[:,15])
    
    plt.figure(2)
    plt.contourf(Positions_in_mkm,TimeArraySub,SignalArray,200,cmap='RdBu_r')
    plt.colorbar().set_label('Intensity, arb.u.')
    plt.xlabel('Distance, um')
    plt.ylabel('Time,s')
    
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
    IR=np.zeros(len(TD1[0,:]))
    V=np.zeros(len(TD1[0,:]))
    for k in range(len(TD1[0,:])):
        TD1sumT[k]=np.sum(TD1[:,k])
        TD2sumT[k]=np.sum(TD2[:,k])
    TD1meanTZ=moving_average(TD1sumT,20)
    TD2meanTZ=moving_average(TD2sumT,20)
    for k in range(len(TD1meanTZ)):
        noise=np.mean(TD3[:,k])
        if (np.max(TD1meanTZ[k])/noise>10) and ((TD2meanTZ[k])/noise>10):
            IR[k]=TD1meanTZ[k]/TD2meanTZ[k]
            
            #R[k]=np.max(TD1[:,k])/np.max(TD2[:,k])
            #t1=np.argmax(TD1[:,k])
            #t2=np.argmax(TD2[:,k])
            #V[k]=2*(Z[k]-Positions[-1,1]*2.5e-6)/(T1[t1]-T2[t2])
    #print('ref mean ', np.mean(R),' std ', np.std(R))
    print('integral ref mean ', np.mean(IR),' std ', np.std(IR))
    #print('Velocity mean ', np.mean(V),' std ', np.std(V))
    #np.savetxt('ref.txt',R)
    #np.savetxt('V.txt',V)
    np.savetxt('Iref.txt',IR)   