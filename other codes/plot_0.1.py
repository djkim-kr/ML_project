import numpy as np
from ase.io import read
import os
from matplotlib import pyplot as plt

E = 27.211386
# filename = str(input('enter the xyz file to read : '))
filename = './wm_3_0.1.xyz' 
a = read(filename ,index = ':')


E_abs_eV=[]
for i in a:
    E_abs_eV.append(i.get_total_energy()*E)

E_eV = []
for i in range(len(E_abs_eV)):
    E_eV.append(E_abs_eV[i] - E_abs_eV[5])

x = [-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]

plt.plot(x, E_eV, '.r' )
plt.xlabel('coeff.')
plt.ylabel('E_eV')
# plt.title()
plt.show()