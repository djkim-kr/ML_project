import numpy as np
from ase.io import read
import os
from matplotlib import pyplot as plt

filename1 = str(input('enter the 1_xyz file to read : '))
a = read(filename1 ,index = ':')
filename2 = str(input('enter the coefficient info : '))
b = read(filename2 ,index = ':')

filename3 = str(input('enter the 2_xyz file to read : '))
c = read(filename3 ,index = ':')

filename4 = str(input('enter the 3_xyz file to read : '))
d = read(filename4 ,index = ':')


E_eV_1=[]
for i in a:
    E_eV_1.append(i.get_total_energy())
E_eV_2=[]
for i in c:
    E_eV_2.append(i.get_total_energy())
E_eV_3=[]
for i in d:
    E_eV_3.append(i.get_total_energy())



x = []
for i in b:
    x.append(i.get_total_energy())

plt.plot(x, E_eV_1, '.r' )
plt.plot(x, E_eV_2, '.b' )
plt.plot(x, E_eV_3, '.g' )
plt.xlabel('coeff.')
plt.ylabel('E_eV')
plt.legend(['q_1', 'q_2' , 'q_3'], loc=2)
# plt.title("")
# plt.title()
plt.show()