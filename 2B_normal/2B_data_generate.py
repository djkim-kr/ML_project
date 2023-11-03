import random
import numpy as np
from ase.io import read
import os

A = 0.529177249
O = 15.9994**(1/2)
H = 1.00797**(1/2)
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
def reshape_3X3(matrix_1X9):
    reshaped_matrix = matrix_1X9.reshape((3,3))
    with_atom = 'O: ' + str(reshaped_matrix[0]) + '\nH1: ' + str(reshaped_matrix[1]) + '\nH2: ' + str(reshaped_matrix[2])
    return with_atom

with open( 'data/raw.c1.int.log' , 'r') as f:
    lines = f.readlines()
    
    row3 = lines[2].split()
    row4 = lines[3].split()
    row5 = lines[4].split()

    O1 = [float(row3[2]), float(row3[3]), float(row3[4])]    
    H1 = [float(row4[2]), float(row4[3]), float(row4[4])]
    H2 = [float(row5[2]), float(row5[3]), float(row5[4])]

    init_coordinate = O1 + H1 + H2
    init_coordinate_bohr = np.mat(init_coordinate)

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

    #get Q_i from the raw file and covert to mass**(1/2) *bohr unit
    Q_1_bohr = []
    Q_2_bohr = []
    Q_3_bohr = []
    
    for i in range(23,32):
        if len(lines[i].split()) > 6: 
            Q_1_bohr.append(float(float(lines[i].split()[4])))
            Q_2_bohr.append(float(float(lines[i].split()[5])))
            Q_3_bohr.append(float(float(lines[i].split()[6])))
        else:
            Q_1_bohr.append(float(float(lines[i].split()[2])))
            Q_2_bohr.append(float(float(lines[i].split()[3])))
            Q_3_bohr.append(float(float(lines[i].split()[4])))

    Q_1_bohr_vec = np.array(Q_1_bohr)
    Q_2_bohr_vec = np.array(Q_2_bohr)
    Q_3_bohr_vec = np.array(Q_3_bohr)

    # print(Q_1_bohr_vec)
    # print(Q_2_bohr_vec)
    # print(Q_3_bohr_vec)

    Q_1_vec = np.array(modify_list1(Q_1_bohr, O, H))
    Q_2_vec = np.array(modify_list1(Q_2_bohr, O, H))
    Q_3_vec = np.array(modify_list1(Q_3_bohr, O, H))


def generate_2B(co_a, co_b,vec_a, vec_b):
    list = {}
    for i in range(len(co_a)):
        for j in range(len(co_b)):
            temp = (init_coordinate_bohr + 
                    (co_a[i] * vec_a)+(co_b[j] * vec_b))
            temp_ang = temp * A
            list[f'{co_a[i]} / {co_b[j]}']=temp_ang
    return(list)

# print(list(generate_2B(co_list_1, co_list_2, Q_1_bohr_vec, Q_2_bohr_vec).keys())[0])
# print(list(generate_2B(co_list_1, co_list_2, Q_1_bohr_vec, Q_2_bohr_vec).values())[0])
# print(type(generate_2B(co_list_1, co_list_2, Q_1_bohr_vec, Q_2_bohr_vec)['-0.9 / -0.5']))

co_list_1 = np.round(np.arange(-0.9, 0.9, 0.1).tolist(),2)
co_list_2 = np.round(np.arange(-0.5, 0.8, 0.1).tolist(),2)
co_list_3 = np.round(np.arange(-0.6, 0.8, 0.1).tolist(),2)

co_lists = {
    1: co_list_1,
    2: co_list_2,
    3: co_list_3
}
vec_lists = {
    1: Q_1_bohr_vec,
    2: Q_2_bohr_vec,
    3: Q_3_bohr_vec,
}

def write_file(a,b):
    dict = generate_2B(co_lists[a], co_lists[b], 
                       vec_lists[a], vec_lists[b])
    file_log = f"./data/2B_mode_{a}_{b}.xyz"
    if not os.path.exists("data"):
        os.makedirs("data")
    with open(file_log, 'w') as f:
        for i in range(len(dict)):
            coeffs = list(dict.keys())[i]
            structure = np.array(list(dict.values())[i].reshape((3,3)))
            f.write('3\n')
            f.write('Lattice="15.0 0.0 0.0 0.0 15.0 0.0 0.0 0.0 15.0" Properties=species:S:1:pos:R:3 energy={} pbc="T T T"\n'.format(coeffs))
            f.write('{}\n'.format(R_format(structure)))        
    print('Results written to {}'.format(file_log)) 
    
write_file(1,2)
write_file(2,3)
write_file(1,3)

# for i in range(num_data):
#     # ran_num = random.random()
#     ran_num_1 = random.uniform(-0.8,0.8)
#     ran_num_2 = random.uniform(-0.4,0.6)
#     ran_num_3 = random.uniform(-0.6,0.6)
#     # ran_num = 0
#     random_number_1.append(ran_num_1)
#     random_number_2.append(ran_num_2)
#     random_number_3.append(ran_num_3)
    
#     temp = init_coordinate_bohr + (ran_num_1 * Q_1_bohr_vec) + (ran_num_2 * Q_2_bohr_vec) + (ran_num_3 * Q_3_bohr_vec)
#     temp_ang = temp * A
#     only_123.append(temp_ang)

# # print(type(np.array(only_1[0].reshape((3,3)))))

# file_log = "data/wm_random123.xyz"
# if not os.path.exists("data"):
#     os.makedirs("data")
# with open(file_log, 'w') as f:
#     for i in range(num_data):
#         f.write('3\n')
#         f.write('Lattice="15.0 0.0 0.0 0.0 15.0 0.0 0.0 0.0 15.0" Properties=species:S:1:pos:R:3 energy={} pbc="T T T"\n'.format('{:.10f}'.format(random_number_1[i])))
#         f.write('{}\n'.format(R_format(np.array(only_123[i].reshape((3,3))))))        
# print('Results written to {}'.format(file_log))