import numpy as np
import matplotlib.pyplot as plt
from numba import jit
import pickle
from scipy.optimize import curve_fit as cf
import sys
#%matplotlib notebook
import time
 

kB=1
J=1
L=int(sys.argv[1])
e=int(sys.argv[2])
T1=float(sys.argv[3])
T2=float(sys.argv[4])
T_N=int(sys.argv[5])
N=L*L
N_steps=10**e

start = time.time()

def nbr2D(L):
    N=L*L
    nbrarr=np.zeros((N,4),dtype=int)
    
    for i in range(N):
        k1=i//L
        k2=i%L
        if 1<=k1<=L-2:
            nbrarr[i][2]=(k1-1)*L+k2 #up
            nbrarr[i][3]=(k1+1)*L+k2 #down
        else:
            a=(k1==0)
            nbrarr[i][2]=L*(L-2+a)+k2 #up
            nbrarr[i][3]=L*a+k2 #down
        if 1<=k2<=L-2:
            nbrarr[i][0]=i-1 #left
            nbrarr[i][1]=i+1 #right
        else:
            b=(k2==0)
            nbrarr[i][0]=(i-1+L*b)
            nbrarr[i][1]=(i+1-L*(1-b))
    return nbrarr
nbrarr=nbr2D(L)

'''
@jit(nopython=True)
def get_ensemble_avg(T,N_steps,N_ensemble,L):
    Sum_m=np.zeros(N_steps)
    Sum_E=np.zeros(N_steps)
    
    for i in range(N_ensemble):
        m_arr,E_arr=MC_update(T,N_steps,L)
        Sum_m=Sum_m+m_arr
        Sum_E=Sum_E+E_arr
    return Sum_m/N_ensemble,Sum_E/N_ensemble
'''

@jit(nopython=True)
def MC_update(state_arr,m,E,T): 
    beta=1/T

    #state_arr=np.ones(N)
    #beta=1/T #k_B=1
    i=np.random.randint(N) #flip position
    r=np.random.random()
    delE=0
    for k in range(4):
    	delE=delE+state_arr[nbrarr[i][k]]
    delE=2*J*state_arr[i]*delE
    
    if delE<0 or r<np.exp(-beta*delE):
    	m=m-2*state_arr[i]/N
    	E=E+delE
    	state_arr[i]=-state_arr[i]
    return m,E

'''    
@jit(nopython=True)
def eq_fit(t,tau):
    return np.exp(-t/tau)
'''


T_arr=np.linspace(T1,T2,T_N)

'''
tau_arr=np.zeros(T_N)
get_ensemble_avg(2,10,10,4)
N_range=np.arange(1,2501,1)
for i in range(T_N):
    m_arr,E_arr=get_ensemble_avg(T_arr[i],2500,1000,L)
    popt,pcov=cf(eq_fit,N_range,m_arr)
    tau_arr[i]=popt[0]
'''


'''
m_mean_arr=np.zeros(T_N)
m2_mean_arr=np.zeros(T_N)
m4_mean_arr=np.zeros(T_N)
for i in range(T_N):
	m_arr,E_arr=get_ensemble_avg(T_arr[i],int(tau_arr[i])*10+10**e,1,L)
	m_mean_arr[i]=np.mean(m_arr[-10**e:])
	m2_mean_arr[i]=np.mean(m_arr[-10**e:]**2)
	m4_mean_arr[i]=np.mean(m_arr[-10**e:]**4)
'''
@jit(nopython=True)
def get_data(T):
    state_arr=np.ones(N)
    Trlax=10000
    m=1
    E=-2*N
    m_mean=0
    m2_mean=0
    m4_mean=0
    
    for i in range(Trlax*N):
    	m,E=MC_update(state_arr,m,E,T)
    for i in range(N_steps*N):
        m,E=MC_update(state_arr,m,E,T)
        m_mean=m_mean+np.abs(m)
        m2_mean=m2_mean+m*m
        m4_mean=m4_mean+m*m*m*m
    return m_mean/(N_steps*N),m2_mean/(N_steps*N),m4_mean/(N_steps*N)
    	
m_mean_arr=np.zeros(T_N)
m2_mean_arr=np.zeros(T_N)
m4_mean_arr=np.zeros(T_N)

for i in range(T_N):
    m,m2,m4=get_data(T_arr[i])
    m_mean_arr[i]=m
    m2_mean_arr[i]=m2
    m4_mean_arr[i]=m4

path=open(f'L{L}T{T1}_{T2}','wb')
pickle.dump([m_mean_arr,m2_mean_arr,m4_mean_arr,T1,T2,T_N],path)
path.close()
end = time.time()

print(f'runtime = {end-start} sec')
