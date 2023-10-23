import numpy as np
from ase.io import read
import os
import re
from scipy import interpolate
from scipy.interpolate import interp1d 
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from matplotlib import pyplot as plt

#1 Hartree = 27.2114079527eV
#1 Bohr = 0.529177249 Angstrom
A = 0.529177249
O = 15.99491**(1/2)
H = 1.00782**(1/2)
E = 27.2114079527

def make_float(x):
    x_float = float(x[0,0])
    return x_float

def R_format(position):
    symbols = ['O', 'H', 'H']
    output_str = ''
    for i, (symbol, pos) in enumerate(zip(symbols, position)):
        output_str += "{:2s}   {:14.8f}   {:14.8f}   {:14.8f}".format(
            symbol, pos[0], pos[1], pos[2]
        )
        if i < len(symbols) -1:
            output_str += '\n'
    return output_str

def har_E(dis_vec, force_3Nx3N):
    cQT = np.array(dis_vec)
    cQ = np.transpose(cQT)
    pro1 = np.dot(force_3Nx3N, cQ)
    E_har_hartree = (1/2) * np.dot(cQT, pro1)
    E_har_eV = E_har_hartree * E
    A = make_float(E_har_eV)
    X = '{:.10f}'.format(A)
    return(str(X))

def modify_list1(lst, factor_O, factor_H):
    result = lst.copy()
    # Multiply factors for the components
    result[0] *= factor_O
    result[1] *= factor_O
    result[2] *= factor_O
    result[3] *= factor_H
    result[4] *= factor_H
    result[5] *= factor_H
    result[6] *= factor_H
    result[7] *= factor_H
    result[8] *= factor_H

    return result

# filename_1 = str(input('enter the xyz file to read : '))
# filename_2 = str(input('enter the quip file to read : '))
filename_1 = 'DE_train.xyz'
filename_2 = 'quip_train.xyz'

#extracting the energies from input file
IN = read(filename_1 ,index = ':')
E_input=[]
for i in IN:
    E_input.append(i.get_total_energy())
# print(E_input[0])

#extracting the position from input file, R_ang is in angstorm
tempx=[]
for i in IN:
    tempx.append(i.get_positions())
tempxx = [np.array(b) for b in tempx]
R_ang = [np.reshape(b, 9) for b in tempxx]

#extracting the energies from output file
with open( filename_2 , 'r') as f:
    lines = f.readlines()
    input_string = str(lines[:])
    energy_data = re.findall(r'energy=([\d.E+-]+)', input_string)
    E_output = [float(energy) for energy in energy_data]
# print(E_output[0])

#making a list which contains the Absolute difference between energies
Abs_diff = []
for i in range(len(E_input)):
    Abs_diff.append(abs(E_input[i] - E_output[i]))
# print(Abs_diff[0:3])

#finding top 20 largest difference in the list 
sorted_energies = sorted(Abs_diff, reverse=True)
top_20_energies = sorted_energies[:5000]
positions = [Abs_diff.index(energy) for energy in top_20_energies]

# #getting index, input energy, coordinates
# for i, energy in enumerate(top_20_energies):
#         position = positions[i]
#         print("Index:", position, "E_input:", E_input[position])
#         print('{}\n'.format(R_format(R_ang[position].reshape((3,3)))))

#writing the results in the log file in data directory in the right format for quippy
base_filename = os.path.basename(filename_1)
file_log = "data/OUT_{}".format(base_filename)
if not os.path.exists("data"):
    os.makedirs("data")
    
with open(file_log, 'w') as f:
    for i, energy in enumerate(top_20_energies):
        position = positions[i]
        f.write('3\n')
        f.write('Lattice="15.0 0.0 0.0 0.0 15.0 0.0 0.0 0.0 15.0" Properties=species:S:1:pos:R:3 energy={} pbc="T T T"\n'.format(E_input[position]))
        f.write('{}\n'.format(R_format(R_ang[position].reshape((3,3)))))
print('Results written to {}'.format(file_log))


#finding coefficients
with open( 'raw.c1.int.log' , 'r') as f:
    lines = f.readlines()

#get R_0 from the raw file and convert tot mass**(1/2) * bohr unit
    row3 = lines[2].split()
    row4 = lines[3].split()
    row5 = lines[4].split()
    O1 = [float(row3[2]), float(row3[3]), float(row3[4])]    
    H1 = [float(row4[2]), float(row4[3]), float(row4[4])]
    H2 = [float(row5[2]), float(row5[3]), float(row5[4])]
    init_coordinate = O1 + H1 + H2
    init_coordinate_bohr = np.array(init_coordinate)
    
    init_coordinate_amu = []
    for i in range(3):
        init_coordinate_amu.append(init_coordinate[i]*O)
    for i in range(3,9):
        init_coordinate_amu.append(init_coordinate[i]*H)
    R0_amu_vec= np.array(init_coordinate_amu)
    # print(R0_amu_vec)

    init_coordinate_ang = []
    for i in range(len(init_coordinate)):
        init_coordinate_ang.append(init_coordinate[i]*A)
    init_coordinate_ang_mat = np.array(init_coordinate_ang)

    for i in range(38,54):
        read_row = lines[i]
        numbers = re.findall(r'-?\d+\.\d+', read_row)
        
        new_list_name = f"temp_{i}"
        globals()[new_list_name] = []
        for m in range(len(numbers)): 
            globals()[new_list_name].append(float(numbers[m]))

    row1 = temp_38 + temp_44[0:3]
    row2 = temp_39 + temp_45[0:3]
    row3 = temp_40 + temp_46[0:3]
    row4 = temp_41 + temp_44[3:6]
    row5 = temp_42 + temp_45[3:6]
    row6 = temp_43 + temp_46[3:6]
    row7 = temp_44 + temp_51
    row8 = temp_45 + temp_52
    row9 = temp_46 + temp_53

    force_3Nx3N = np.mat([row1,row2,row3,row4,row5,row6,row7,row8,row9])

#get Q_i from the raw file and covert to mass*(1/2)*bohr unit
    Q_1_bohr = []
    Q_2_bohr = []
    Q_3_bohr = []
    Q_4_bohr = []
    Q_5_bohr = []
    Q_6_bohr = []
    Q_7_bohr = []
    Q_8_bohr = []
    Q_9_bohr = []
    
    for i in range(23,32):
        if len(lines[i].split()) > 6: 
            Q_1_bohr.append(float(float(lines[i].split()[4])))
            Q_2_bohr.append(float(float(lines[i].split()[5])))
            Q_3_bohr.append(float(float(lines[i].split()[6])))
            Q_9_bohr.append(float(float(lines[i].split()[3])))
        else:
            Q_1_bohr.append(float(float(lines[i].split()[2])))
            Q_2_bohr.append(float(float(lines[i].split()[3])))
            Q_3_bohr.append(float(float(lines[i].split()[4])))
            Q_9_bohr.append(float(float(lines[i].split()[1])))
    for i in range(9,18):
        if len(lines[i].split()) > 7:
            Q_4_bohr.append(float(float(lines[i].split()[3])))
            Q_5_bohr.append(float(float(lines[i].split()[4])))
            Q_6_bohr.append(float(float(lines[i].split()[5])))
            Q_7_bohr.append(float(float(lines[i].split()[6])))
            Q_8_bohr.append(float(float(lines[i].split()[7])))
        else:
            Q_4_bohr.append(float(float(lines[i].split()[1])))
            Q_5_bohr.append(float(float(lines[i].split()[2])))
            Q_6_bohr.append(float(float(lines[i].split()[3])))
            Q_7_bohr.append(float(float(lines[i].split()[4])))
            Q_8_bohr.append(float(float(lines[i].split()[5])))

    Q_1_bohr_vec = np.array(Q_1_bohr)
    Q_2_bohr_vec = np.array(Q_2_bohr)
    Q_3_bohr_vec = np.array(Q_3_bohr)
    Q_4_bohr_vec = np.array(Q_4_bohr)
    Q_5_bohr_vec = np.array(Q_5_bohr)
    Q_6_bohr_vec = np.array(Q_6_bohr)
    Q_7_bohr_vec = np.array(Q_7_bohr)
    Q_8_bohr_vec = np.array(Q_8_bohr)
    Q_9_bohr_vec = np.array(Q_9_bohr)

    Q_1_vec = np.array(modify_list1(Q_1_bohr, O, H))
    Q_2_vec = np.array(modify_list1(Q_2_bohr, O, H))
    Q_3_vec = np.array(modify_list1(Q_3_bohr, O, H))
    Q_4_vec = np.array(modify_list1(Q_4_bohr, O, H))
    Q_5_vec = np.array(modify_list1(Q_5_bohr, O, H))
    Q_6_vec = np.array(modify_list1(Q_6_bohr, O, H))
    Q_7_vec = np.array(modify_list1(Q_7_bohr, O, H))
    Q_8_vec = np.array(modify_list1(Q_8_bohr, O, H))
    Q_9_vec = np.array(modify_list1(Q_9_bohr, O, H))

#getting energies and coordinates from the file and convert it to the accoridng unit and form
OUT = read(file_log, index = ':')
energy = []
for i in OUT:
    energy.append(i.get_total_energy())
# print(energy)

tempx=[]
for i in OUT:
    tempx.append(i.get_positions())
tempxx = [np.array(d) for d in tempx]
tempxxx = [np.reshape(b, 9) for b in tempxx]
# print(R_ang[0])

R_ang_amu_vec=[]
for i in range(len(tempxxx)):
    temp_a = tempxxx[i][0:3]*(1/A)*O
    temp_b = tempxxx[i][3:9]*(1/A)*H
    R_ang_amu_vec.append(np.concatenate((temp_a,temp_b)))
# print(R_ang_amu_vec[0])

R_bohr_vec = []
for i in range(len(tempxxx)):
    temp_a = tempxxx[i][0:3]*(1/A)
    temp_b = tempxxx[i][3:9]*(1/A)
    R_bohr_vec.append(np.concatenate((temp_a,temp_b)))

#displacement vector, R-R_0
dis_vec=[]
for i in range(len(tempxxx)):
    dis_vec.append(R_ang_amu_vec[i]-R0_amu_vec)

dis_vec_nonmass = []
for i in range(len(tempxxx)):
    dis_vec_nonmass.append(R_bohr_vec[i]-init_coordinate_bohr)

c_1= []
c_2= []
c_3= []
c_4 = []
c_5 = []
c_6 = []
c_7 = []
c_8 = []
c_9 = []

energy_difference = []

#calculate coefficient by dot product and write the result
file_log2 = "data/OUT_co_{}".format(base_filename)
with open(file_log2, 'w') as f:
    f.write('v_1=1641.35, Bending \nv_2=3838.94, Symmetric stretching \nv_3=3942.89, Antisymmetric stretching\n')
    f.write('\nR_O in Angstrom\n')
    f.write('{}\n'.format(R_format(init_coordinate_ang_mat.reshape((3,3)))))
    f.write('\n')   
    for i in range(len(dis_vec)):
        C_1 = np.dot(dis_vec[i],Q_1_vec)
        C_2 = np.dot(dis_vec[i],Q_2_vec)
        C_3 = np.dot(dis_vec[i],Q_3_vec)
        C_4 = np.dot(dis_vec[i],Q_4_vec)
        C_5 = np.dot(dis_vec[i],Q_5_vec)
        C_6 = np.dot(dis_vec[i],Q_6_vec)
        C_7 = np.dot(dis_vec[i],Q_7_vec)
        C_8 = np.dot(dis_vec[i],Q_8_vec)
        C_9 = np.dot(dis_vec[i],Q_9_vec)

        f.write('C_1= {} C_2= {} C_3= {}\nC_4= {} C_5= {} C_6= {}\nC_7= {} C_8= {} C_9= {}\n'.format(C_1, C_2, C_3, C_4, C_5, C_5, C_7, C_8, C_9))
        f.write('energy={} Abs_diff={}\n'.format(energy[i], Abs_diff[positions[i]]))
        f.write('{}\n\n'.format(R_format(tempxxx[i].reshape((3,3)))))
        
        c_1.append(C_1)
        c_2.append(C_2)        
        c_3.append(C_3)
        c_4.append(C_4)
        c_5.append(C_5)
        c_6.append(C_6)
        c_7.append(C_7)
        c_8.append(C_8)
        c_9.append(C_9)
        energy_difference.append(Abs_diff[positions[i]])       
print('Results written to {}'.format(file_log2))

# trial
# print(har_E(np.reshape(c_1[0]*Q_1_bohr_vec, (1,9)), force_3Nx3N))
# print(har_E(np.reshape(c_2[0]*Q_2_bohr_vec, (1,9)), force_3Nx3N))
# print(har_E(np.reshape(c_3[0]*Q_3_bohr_vec, (1,9)), force_3Nx3N))
# print(har_E(np.reshape(dis_vec_nonmass[0], (1,9)), force_3Nx3N))
# print(har_E(np.reshape(c_1[0]*Q_1_bohr_vec +c_2[0]*Q_2_bohr_vec +c_3[0]*Q_3_bohr_vec, (1,9) ), force_3Nx3N))
# # print(har_E(np.reshape(c_1[0]*Q_1_bohr_vec +c_2[0]*Q_2_bohr_vec +c_3[0]*Q_3_bohr_vec+ c_4[0]*Q_4_bohr_vec, (1,9) ), force_3Nx3N))
# print(c_1[0])
# print(c_2[0])
# print(c_3[0])
# print(c_4[0])
# print(Q_1_bohr_vec[0])
# print(np.dot(c_1[0] , Q_1_bohr_vec) + np.dot(c_2[0],Q_2_bohr_vec) + np.dot(c_3[0],Q_3_bohr_vec))
# print(c_1[0]*Q_1_bohr_vec + c_2[0]*Q_2_bohr_vec + c_3[0]*Q_3_bohr_vec + c_4[0]*Q_4_bohr_vec)
# print(dis_vec[0])

e_1 = []
e_2 = []
e_3 = []
e_4 = []
e_5 = []
e_6 = []
e_7 = []
e_8 = []
e_9 = []

e_diff = []
e_123 = []
e_456789 = []
e_123456789 = []
e_har = []
e_portion = []
file_log3 = "data/OUT_E_{}".format(base_filename)
with open(file_log3,'w') as f:
    f.write('v_1=1641.37, Bending \nv_2=3839.46, Symmetric stretching \nv_3=3943.42, Antisymmetric stretching\n')
    f.write('\nR_O in Angstrom\n')
    f.write('{}\n'.format(R_format(init_coordinate_ang_mat.reshape((3,3)))))
    f.write('\n')   
    for i in range(len(c_1)):
        E_1 = har_E(np.reshape(c_1[i]*Q_1_bohr_vec, (1,9)), force_3Nx3N)
        E_2 = har_E(np.reshape(c_2[i]*Q_2_bohr_vec, (1,9)), force_3Nx3N)
        E_3 = har_E(np.reshape(c_3[i]*Q_3_bohr_vec, (1,9)), force_3Nx3N)
        E_4 = har_E(np.reshape(c_4[i]*Q_4_bohr_vec, (1,9)), force_3Nx3N)
        E_5 = har_E(np.reshape(c_5[i]*Q_5_bohr_vec, (1,9)), force_3Nx3N)
        E_6 = har_E(np.reshape(c_6[i]*Q_6_bohr_vec, (1,9)), force_3Nx3N)
        E_7 = har_E(np.reshape(c_7[i]*Q_7_bohr_vec, (1,9)), force_3Nx3N)
        E_8 = har_E(np.reshape(c_8[i]*Q_8_bohr_vec, (1,9)), force_3Nx3N)
        E_9 = har_E(np.reshape(c_9[i]*Q_9_bohr_vec, (1,9)), force_3Nx3N)

        E_123 = har_E(np.reshape(c_1[i]*Q_1_bohr_vec +c_2[i]*Q_2_bohr_vec +c_3[i]*Q_3_bohr_vec, (1,9) ), force_3Nx3N)
        E_123456789 = har_E(np.reshape(c_1[i]*Q_1_bohr_vec +c_2[i]*Q_2_bohr_vec +c_3[i]*Q_3_bohr_vec+c_4[i]*Q_4_bohr_vec +c_5[i]*Q_5_bohr_vec +c_6[i]*Q_6_bohr_vec+c_7[i]*Q_7_bohr_vec+c_8[i]*Q_8_bohr_vec+c_9[i]*Q_9_bohr_vec, (1,9) ), force_3Nx3N)
        E_456789 = har_E(np.reshape(c_4[i]*Q_4_bohr_vec +c_5[i]*Q_5_bohr_vec +c_6[i]*Q_6_bohr_vec+c_7[i]*Q_7_bohr_vec+c_8[i]*Q_8_bohr_vec+c_9[i]*Q_9_bohr_vec, (1,9) ), force_3Nx3N)
        E_har = har_E(np.reshape(dis_vec_nonmass[i], (1,9)), force_3Nx3N)
        E_diff = float(E_har) - float(E_123456789)
        E_portion = float(E_456789)/float(E_har)

        e_1.append(float(E_1))
        e_2.append(float(E_2))
        e_3.append(float(E_3))
        e_4.append(float(E_4))
        e_5.append(float(E_5))
        e_6.append(float(E_6))
        e_7.append(float(E_7))
        e_8.append(float(E_8))
        e_9.append(float(E_9))

        e_123.append(float(E_123))
        e_456789.append(float(E_456789))
        e_123456789.append(float(E_123456789))
        e_har.append(float(E_har))
        e_diff.append(float(E_diff))
        e_portion.append(float(E_portion))

        f.write('C_1= {} C_2= {} C_3= {}\nC_4= {} C_5= {} C_6= {}\nC_7= {} C_8= {} C_9= {}\n'.format(c_1[i], c_2[i], c_3[i], c_4[i], c_5[i], c_6[i], c_7[i], c_8[i], c_9[i]))
        f.write('E_1= {} E_2= {} E_3= {}\nE_4= {} E_5= {} E_6= {}\nE_7= {} E_8= {} E_9= {}\n'.format(E_1, E_2, E_3,E_4, E_5, E_6,E_7, E_8, E_9))
        f.write('E_123= {} E_456789 = {} E_har= {} E_har - E_123456789= {}\n'.format(E_123, E_456789, E_har, E_diff))
        f.write('Delta energy={} Abs_diff={} rot,trans portion={}\n'.format(energy[i], Abs_diff[positions[i]],E_portion))
        f.write('{}\n\n'.format(R_format(tempxxx[i].reshape((3,3)))))
print('Results written to {}'.format(file_log3))


# x = np.array(energy_difference)

# variables = ['c_1', 'c_2', 'c_3', 'c_4', 'c_5', 'c_6', 'c_7', 'c_8', 'c_9']
# fig, axs = plt.subplots(3, 3, figsize=(20, 10))
# for i, variable in enumerate(variables):
#     row = i // 3
#     col = i % 3
#     axs[row, col].plot(x, eval(variable), '.b')
#     axs[row, col].set_xlabel('ML Error')
#     axs[row, col].set_ylabel(variable)
# plt.tight_layout()
# plt.show()

# variables = ['e_1', 'e_2', 'e_3', 'e_4', 'e_5', 'e_6', 'e_7', 'e_8', 'e_9']
# fig, axs = plt.subplots(3, 3, figsize=(20, 10))
# for i, variable in enumerate(variables):
#     row = i // 3
#     col = i % 3
#     axs[row, col].plot(x, eval(variable), '.b')
#     axs[row, col].set_xlabel('ML Error')
#     axs[row, col].set_ylabel(variable)
# plt.tight_layout()
# plt.show()

# plt.plot(x, e_har, '.r' )
# plt.xlabel('ML error')
# plt.ylabel('E_har')
# plt.show()

# plt.plot(x, energy, '.r' )
# plt.xlabel('ML error')
# plt.ylabel('E_har - E_tot')
# plt.show()

# plt.plot(e_har, energy, '.b')
# plt.xlabel('Harmonic E')
# plt.ylabel('E_har - E_tot')
# plt.show()

# plt.plot(e_456789, energy, '.b')
# plt.xlabel('E_456789')
# plt.ylabel('E_har - E_tot')
# plt.show()

# plt.plot(e_456789, x, '.r' )
# plt.xlabel('E_456789')
# plt.ylabel('ML error')
# plt.show()

# plt.plot(e_portion, x, '.g')
# plt.xlabel('E_rot+E_trans / E_har')
# plt.ylabel('ML error')
# plt.show()

# plt.plot(x, e_1, '.b')
# plt.ylabel('e_1')
# plt.xlabel('ML error')

# plt.plot(x, e_5, '.g')
# plt.ylabel('e_5')
# plt.xlabel('ML error')
# plt.show()

plt.plot(e_1, e_5, '.g')
plt.ylabel('e_5')
plt.xlabel('e_1')
plt.show()