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
	chi=m2_mean_arr-m_mean_arr**2
	plt.plot(-(T_arr-2.27)*L,m_mean_arr*L**.125,label=f'L={L}')
	plt.xlabel(r"$(T_c-T)L^{\frac{1}{\nu}}$",size='xx-large')
	plt.ylabel(r"$mL^{\frac{\beta}{\nu}}$",size='xx-large')
	
	
	#plt.plot(-(T_arr-2.27)*L,chi*L**(-1.72+2),label=f'L={L}')
	#plt.xlabel(r"$(T_c-T)L^{\frac{1}{\nu}}$",size='xx-large')
	#plt.ylabel(r"$\chi L^{\frac{-\gamma}{\nu}}$",size='xx-large')
	
plt.title(r"$\beta=0.125$, $\nu=1$",size='xx-large')	
plt.grid()
plt.legend()
plt.show()

