import numpy as np
from ase.io import read
import os
import re
from matplotlib import pyplot as plt

# filename1 = str(input('enter the DE_xyz file to read : '))
filename1='DE_train.xyz'
a = read(filename1 ,index = ':')
# filename2 = str(input('enter the quip_xyz file to read: '))
filename2='quip_train.xyz'
b = read(filename2 ,index = ':')
# filename3 = str(input('enter the wm_xyz file to read : '))
filename3='wm_train.xyz'
c = read(filename3 ,index = ':')
# # filename4 = str(input('enter the coeff. file to read : '))
# filename4='co_2_train.xyz'
# d = read(filename4 ,index = ':')


DE_eV=[]
for i in a:
    DE_eV.append(i.get_total_energy())

with open( filename2 , 'r') as f:
    lines = f.readlines()
    input_string = str(lines[:])
    energy_data = re.findall(r'energy=([\d.E+-]+)', input_string)
    quip_eV = [float(energy) for energy in energy_data]
ML_err = []
for i in range(len(DE_eV)):
    ML_err.append(DE_eV[i] - quip_eV[i])
abs_ML_err = []
for i in range(len(DE_eV)):
    abs_ML_err.append(abs(DE_eV[i] - quip_eV[i]))

# print(quip_eV[0])
# print(quip_eV[1])
# print(quip_eV[2])


                  
wm_eV=[]
for i in c:
    wm_eV.append(i.get_total_energy())

# co = []
# for i in d:
#     co.append(i.get_total_energy())


# plt.subplot(2,2,1)
# plt.plot(co, wm_eV, '.r' )
# plt.xlabel('coeff.')
# plt.ylabel('H2O_energy_eV')

# plt.subplot(2,2,2)
# plt.plot(co, ML_err, '.r' )
# plt.axhline(y=0, )
# plt.xlabel('coeff.')
# plt.ylabel('ML_err_eV')

# plt.subplot(2,2,3)
plt.plot(wm_eV, abs_ML_err, '.r' )
plt.axhline(y=0, color = 'black')
plt.xlabel('H2O_energy_eV')
plt.ylabel('abs_ML_err')
plt.show()

# plt.subplot(2,2,4)
# plt.plot(co, DE_eV, '.r' )
# plt.xlabel('coeff.')
# plt.ylabel('DE(har.-anhar.)_eV')


# plt.legend(['q_1', 'q_2' , 'q_3'], loc=2)

plt.plot(wm_eV, DE_eV, '.r' )
plt.xlabel('wm_eV')
plt.ylabel('DE_eV')
plt.show()