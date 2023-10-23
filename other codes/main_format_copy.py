import re
import numpy as np
import os
from ase.io import read

#1 Hartree = 27.2114079527eV
#1 Bohr = 0.529177249 Angstrom
A = 0.529177249
O = 15.9994**(1/2)
H = 1.00797**(1/2)
E = 27.2114079527
#E0 is in hartree
E0_h2o = -76.3575310289

with open( 'raw.c1.int.log' , 'r') as f:
    lines = f.readlines()
    
    row3 = lines[2].split()
    row4 = lines[3].split()
    row5 = lines[4].split()

    O1 = [float(row3[2]), float(row3[3]), float(row3[4])]    
    H1 = [float(row4[2]), float(row4[3]), float(row4[4])]
    H2 = [float(row5[2]), float(row5[3]), float(row5[4])]

    init_coordinate = O1 + H1 + H2
    init_coordinate_bohr = np.mat(init_coordinate)

    #exporting force constant data from raw.log and make it to 9x9 matrix
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
    # print(force_3Nx3N)
    # force_3Nx3N 은 9x9 hessian matrix, OHH 순서

#file에서 정보 가져오기
filename = str(input('enter the xyz file to read : '))
a = read(filename ,index = ':')

E_anh_eV=[]
for i in a:
    E_anh_eV.append(i.get_total_energy())

tempx=[]
for i in a:
    tempx.append(i.get_positions())
tempxx = [np.array(d) for d in tempx]
R_ang = [np.reshape(b, 9) for b in tempxx]

R_ang_amu_vec=[]
for i in range(len(R_ang)):
    temp_a = R_ang[i][0:3]*(1/A)
    temp_b = R_ang[i][3:9]*(1/A)
    R_ang_amu_vec.append(np.concatenate((temp_a,temp_b)))

dis_vec=[]
for i in range(len(R_ang)):
    dis_vec.append(R_ang_amu_vec[i]-init_coordinate_bohr)

#Energy difference between E_harmonic & E_anharmonic is now called DE in eV

#matrix형식으로 되어 있는 DE 를 float으로 바꿔주는 함수
def make_float(x):
    x_float = float(x[0,0])
    return x_float
#3가지 변수를 넣어 harmonic E 와 anharmonic E를 구하고 그 차이를 har - anhar 하여 DE 로 표현한 것
def calculate_DE(dis_vec, force_3Nx3N, E_anh_eV):
    cQT = np.array(dis_vec)
    cQ = np.transpose(cQT)
    pro1 = np.dot(force_3Nx3N, cQ)
    E_har_hartree = (1/2) * np.dot(cQT, pro1)
    E_har_eV = E_har_hartree * E
    DE = E_har_eV - E_anh_eV
    E_har_eV_str = 'E_har_eV: '+ str(make_float(E_har_eV))
    E_anh_eV_str = 'E_anh_eV: '+ str(E_anh_eV)
    DE_str= 'DE_eV: '+ str(make_float(DE))
    return E_har_eV_str, E_anh_eV_str, DE_str
# print(calculate_DE(R0_amu_vec-R0_amu_vec, force_3Nx3N, np.array([0])))
#DE만 뽑아내며, 소수점 아래 10개까지 표현한 것
def DE_only(dis_vec, force_3Nx3N, E_anh_eV):
    cQT = np.array(dis_vec)
    cQ = np.transpose(cQT)
    pro1 = np.dot(force_3Nx3N, cQ)
    E_har_hartree = (1/2) * np.dot(cQT, pro1)
    E_har_eV = E_har_hartree * E
    DE = E_har_eV - E_anh_eV
    A = make_float(DE)
    X = '{:.10f}'.format(A)
    return(str(X))
#harmonic E의 aboslute energy만 구하기
def absolute_harE(dis_vec, force_3Nx3N, E_anh_eV):
    cQT = np.array(dis_vec)
    cQ = np.transpose(cQT)
    pro1 = np.dot(force_3Nx3N, cQ)
    E_har_hartree = (1/2) * np.dot(cQT, pro1)
    E_har_eV = E_har_hartree * E
    abs_harE = E0_h2o + E_har_eV*(1/E)
    A = make_float(abs_harE)
    X = '{:.10f}'.format(A)
    return(str(X))
#1x9로 되어있는 함수를 3x3으로 바꾸는 것
def reshape_3X3(matrix_1X9):
    reshaped_matrix = matrix_1X9.reshape((3,3))
    with_atom = 'O: ' + str(reshaped_matrix[0]) + '\nH1: ' + str(reshaped_matrix[1]) + '\nH2: ' + str(reshaped_matrix[2])
    return with_atom
#atom의 coordinate를 특정 순서와 형식에 맞게 표현하는 것
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

#writing the results in the log file in data directory in the right format for quippy
base_filename = os.path.basename(filename)
file_log = "data/DE_{}".format(base_filename)

if not os.path.exists("data"):
    os.makedirs("data")

with open(file_log, 'w') as f:

    for i in range(len(dis_vec)):
        if R_ang[i].reshape((3,3))[0].any() is np.array([0., 0., 0.]).any():
            f.write('3\n')
            f.write('Lattice="15.0 0.0 0.0 0.0 15.0 0.0 0.0 0.0 15.0" Properties=species:S:1:pos:R:3 energy={} pbc="T T T"\n'.format(DE_only(dis_vec[i], force_3Nx3N, E_anh_eV[i])))
            f.write('{}\n'.format(R_format(R_ang[i].reshape((3,3)))))

# Print a message indicating the file has been written
print('Results written to {}'.format(file_log))