import numpy as np
import matplotlib.pyplot as plt
import pickle

L_arr=[16,24,32,40]

for i in range(len(L_arr)):
	L=L_arr[i]
	m_mean_arr=[]
	m2_mean_arr=[]
	m4_mean_arr=[]
	T_arr=np.linspace(1.5,3,32)
	for j in range(1,5):
	    path=open(f'L{L}T{j}','rb')
	    m_arr,m2_arr,m4_arr,T1,T2,T_N=pickle.load(path)   
	    
	    m_mean_arr=m_mean_arr+list(m_arr)
	    m2_mean_arr=m2_mean_arr+list(m2_arr)
	    m4_mean_arr=m4_mean_arr+list(m4_arr)
	m_mean_arr=np.array(m_mean_arr)
	m2_mean_arr=np.array(m2_mean_arr)
	m4_mean_arr=np.array(m4_mean_arr)
	U=0.5*(3-m4_mean_arr/m2_mean_arr**2)
	plt.plot(T_arr,U,label=f'L={L}')
	#chi=m2_mean_arr-m_mean_arr**2
	
	#plt.plot((T_arr-2.27)*L,chi*L**(-1.72+2))
plt.xlabel('T',size='xx-large')
plt.ylabel('U',size='xx-large')
plt.grid()
plt.legend()
plt.show()
