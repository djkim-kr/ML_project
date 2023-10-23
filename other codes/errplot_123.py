import numpy as np
from ase.io import read
import os
import re
from matplotlib import pyplot as plt

# filename1 = str(input('enter the DE_xyz file to read : '))
filename1_1='wm_1/DE_1_train.xyz'
a_1 = read(filename1_1 ,index = ':')
# filename2 = str(input('enter the quip_xyz file to read: '))
filename2_1='wm_1/quip_train.xyz'
# filename3 = str(input('enter the wm_xyz file to read : '))
filename3_1='wm_1/wm_1_train.xyz'
c_1 = read(filename3_1 ,index = ':')
# filename4 = str(input('enter the coeff. file to read : '))
filename4='wm_1/co_1_train.xyz'
d = read(filename4 ,index = ':')


DE_eV_1=[]
for i in a_1:
    DE_eV_1.append(i.get_total_energy())

with open( filename2_1 , 'r') as f:
    lines = f.readlines()
    input_string = str(lines[:])
    energy_data_1 = re.findall(r'energy=([\d.E+-]+)', input_string)
    quip_eV_1 = [float(energy) for energy in energy_data_1]
ML_err_1 = []
for i in range(len(DE_eV_1)):
    ML_err_1.append(DE_eV_1[i] - quip_eV_1[i])
abs_ML_err_1 = []
for i in range(len(DE_eV_1)):
    abs_ML_err_1.append(abs(DE_eV_1[i] - quip_eV_1[i]))

wm_eV_1=[]
for i in c_1:
    wm_eV_1.append(i.get_total_energy())
co = []
for i in d:
    co.append(i.get_total_energy())

filename1_2='wm_2/DE_2_train.xyz'
a_2 = read(filename1_2 ,index = ':')
# filename2 = str(input('enter the quip_xyz file to read: '))
filename2_2='wm_2/quip_train.xyz'
# filename3 = str(input('enter the wm_xyz file to read : '))
filename3_2='wm_2/wm_2_train.xyz'
c_2 = read(filename3_2 ,index = ':')
# filename4 = str(input('enter the coeff. file to read : '))


DE_eV_2=[]
for i in a_2:
    DE_eV_2.append(i.get_total_energy())

with open( filename2_2 , 'r') as f:
    lines = f.readlines()
    input_string = str(lines[:])
    energy_data_2 = re.findall(r'energy=([\d.E+-]+)', input_string)
    quip_eV_2 = [float(energy) for energy in energy_data_2]
ML_err_2 = []
for i in range(len(DE_eV_2)):
    ML_err_2.append(DE_eV_2[i] - quip_eV_2[i])
abs_ML_err_2 = []
for i in range(len(DE_eV_2)):
    abs_ML_err_2.append(abs(DE_eV_2[i] - quip_eV_2[i]))

wm_eV_2=[]
for i in c_2:
    wm_eV_2.append(i.get_total_energy())
co = []
for i in d:
    co.append(i.get_total_energy())

filename1_3='wm_3/DE_3_train.xyz'
a_3 = read(filename1_3 ,index = ':')
# filename2 = str(input('enter the quip_xyz file to read: '))
filename2_3='wm_3/quip_train.xyz'
# filename3 = str(input('enter the wm_xyz file to read : '))
filename3_3='wm_3/wm_3_train.xyz'
c_3 = read(filename3_3 ,index = ':')
# filename4 = str(input('enter the coeff. file to read : '))


DE_eV_3=[]
for i in a_3:
    DE_eV_3.append(i.get_total_energy())

with open( filename2_3 , 'r') as f:
    lines = f.readlines()
    input_string = str(lines[:])
    energy_data_3 = re.findall(r'energy=([\d.E+-]+)', input_string)
    quip_eV_3 = [float(energy) for energy in energy_data_3]
ML_err_3 = []
for i in range(len(DE_eV_3)):
    ML_err_3.append(DE_eV_3[i] - quip_eV_3[i])
abs_ML_err_3 = []
for i in range(len(DE_eV_3)):
    abs_ML_err_3.append(abs(DE_eV_3[i] - quip_eV_3[i]))

wm_eV_3=[]
for i in c_3:
    wm_eV_3.append(i.get_total_energy())
co = []
for i in d:
    co.append(i.get_total_energy())

plt.subplot(1,3,1)
plt.plot(co, wm_eV_1, '.r' )
plt.plot(co, wm_eV_2, '.b' )
plt.plot(co, wm_eV_3, '.g' )
plt.xlabel('coeff.')
plt.ylabel('H2O_energy_eV')
plt.legend(['q_1', 'q_2' , 'q_3'], loc=2)


plt.subplot(1,3,2)
plt.plot(co, ML_err_1, '.r' )
plt.plot(co, ML_err_2, '.b' )
plt.plot(co, ML_err_3, '.g' )
plt.axhline(y=0 )
plt.xlabel('coeff.')
plt.ylabel('ML_err_eV')
plt.legend(['q_1', 'q_2' , 'q_3'], loc=2)


plt.subplot(1,3,3)
plt.plot(co, DE_eV_1, '.r' )
plt.plot(co, DE_eV_2, '.b' )
plt.plot(co, DE_eV_3, '.g' )
plt.xlabel('coeff.')
plt.ylabel('DE(har.-anhar.)_eV')
plt.legend(['q_1', 'q_2' , 'q_3'], loc=2)



plt.show()
