import numpy as np
from ase.io import read
import os
import re
from scipy import interpolate
from scipy.interpolate import interp1d 
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

#1 Hartree = 27.2114079527eV
#1 Bohr = 0.529177249 Angstrom
A = 0.529177249
O = 15.99491**(1/2)
H = 1.00782**(1/2)
E = 27.2114079527

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
#extracting the position from input file
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
with open( 'raw.OHalongX.log' , 'r') as f:
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
 

#get Q_i from the raw file and covert to mass*(1/2)*bohr unit
    Q_1 = []
    Q_2 = []
    Q_3 = []
    for i in range(9,18):
        if i <= 11:
            if len(lines[i].split()) > 6: 
                Q_1.append(float(float(lines[i].split()[4])*O))
                Q_2.append(float(float(lines[i].split()[5])*O))
                Q_3.append(float(float(lines[i].split()[6])*O))
            else:
                Q_1.append(float(float(lines[i].split()[2])*O))
                Q_2.append(float(float(lines[i].split()[3])*O))
                Q_3.append(float(float(lines[i].split()[4])*O))
        else:
            if len(lines[i].split()) > 6: 
                Q_1.append(float(float(lines[i].split()[4])*H))
                Q_2.append(float(float(lines[i].split()[5])*H))
                Q_3.append(float(float(lines[i].split()[6])*H))
            else:
                Q_1.append(float(float(lines[i].split()[2])*H))
                Q_2.append(float(float(lines[i].split()[3])*H))
                Q_3.append(float(float(lines[i].split()[4])*H)) 
    Q_1_vec = np.array(Q_1)
    Q_2_vec = np.array(Q_2)
    Q_3_vec = np.array(Q_3)
# print(Q_2_vec)

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
R_ang = [np.reshape(b, 9) for b in tempxx]
# print(R_ang[0])
R_ang_amu_vec=[]
init_coordinate_mass=[]
for i in range(len(R_ang)):
    temp_a = R_ang[i][0:3]*(1/A)*O
    temp_b = R_ang[i][3:9]*(1/A)*H
    R_ang_amu_vec.append(np.concatenate((temp_a,temp_b)))
# print(R_ang_amu_vec[0])

#displacement vector, R-R_0
dis_vec=[]
for i in range(len(R_ang)):
    dis_vec.append(R_ang_amu_vec[i]-R0_amu_vec)

c_1= []
c_2= []
c_3= []
energy_difference = []
#calculate coefficient by dot product and write the result
file_log2 = "data/OUT_co_{}".format(base_filename)
with open(file_log2, 'w') as f:
    f.write('v_1=1641.37, Bending \nv_2=3839.46, Symmetric stretching \nv_3=3943.42, Antisymmetric stretching\n')
    f.write('\nR_O in Angstrom\n')
    f.write('{}\n'.format(R_format(init_coordinate_ang_mat.reshape((3,3)))))
    f.write('\n')   
    for i in range(len(dis_vec)):
        C_1 = np.dot(dis_vec[i],Q_1_vec)
        C_2 = np.dot(dis_vec[i],Q_2_vec)
        C_3 = np.dot(dis_vec[i],Q_3_vec)
        f.write('C_1= {} C_2= {} C_3= {}\n'.format(C_1, C_2, C_3))
        f.write('energy={} Abs_diff={}\n'.format(energy[i], Abs_diff[positions[i]]))
        f.write('{}\n\n'.format(R_format(R_ang[i].reshape((3,3)))))
        if abs(C_1) not in c_1:
            c_1.append(abs(C_1))
        if abs(C_2) not in c_2:
            c_2.append(abs(C_2))        
        if abs(C_3) not in c_3:
            c_3.append(abs(C_3))
        if Abs_diff[positions[i]] not in energy_difference:
            energy_difference.append(Abs_diff[positions[i]])       

print('Results written to {}'.format(file_log2))

# #making a interpolation plot and its 1st derivative
# energy_difference.reverse()
# c_1.reverse()
# c_2.reverse()
# c_3.reverse()

x = np.array(energy_difference)
# y1 = np.array(c_1)
# y2 = np.array(c_2)
# y3 = np.array(c_3)

# f1 = UnivariateSpline(x, y1, s=0.5, k=2)
# f2 = UnivariateSpline(x, y2, s=0.5, k=2)
# f3 = UnivariateSpline(x, y3, s=0.5, k=2)

# xint = np.linspace(x.min(), x.max(), 1000)
# yint1 = f1(xint)
# yint2 = f2(xint)
# yint3 = f3(xint)

# plt.subplot(2,1,1)
# plt.plot(xint, yint1, color='blue', linewidth=2)
# plt.plot(xint, yint2, color='green', linewidth=2)
# plt.plot(xint, yint3, color='red', linewidth=2)
# plt.legend(['c_1', 'c_2' , 'c_3'], loc=2)
# plt.plot(x, y3, 'o', color='red')
# plt.plot(x, y1, 'o', color='blue')
# plt.plot(x, y2, 'o', color='green')
# plt.ylim(0, 1)

# plt.subplot(2,1,2)
# spl1 = CubicSpline(xint, yint1)
# spl2 = CubicSpline(xint, yint2)
# spl3 = CubicSpline(xint, yint3)
# plt.plot(xint, spl1(xint, nu=1),'--', color = 'blue' ,label = 'c_1')
# plt.plot(xint, spl2(xint, nu=1), '--' ,color = 'green',label = 'c_2')
# plt.plot(xint, spl3(xint, nu=1), '--',color ='red',label = 'c_3')
# plt.axhline(y=0, color = 'black')
# plt.legend(['c_1', 'c_2' , 'c_3'], loc=2)
# plt.ylim(-2, 2)
# plt.title("First Derivative")
# plt.xlabel("Abs. E. diff.")

plt.plot(x,c_1, 'or')
plt.show()