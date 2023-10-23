import numpy as np
import os
import subprocess

word = 'train'  
file_path = f'./data/wm_{word}.zmat'

distance_1_list = []
distance_2_list = []
angle_1_list = []
with open(file_path, 'r') as zmat_file:
    lines = zmat_file.readlines()

# Initialize variables to keep track of the current block
block = []
# Process the file line by line
for line in lines:
    if line.strip() == 'O':
        # Found the start of a new block
        if block:
            # Process the previous block
            if len(block) == 3:
                distance_1 = float(block[1].split()[2])
                distance_2 = float(block[2].split()[2])
                angle_1 = float(block[2].split()[4])
                distance_1_list.append(distance_1)
                distance_2_list.append(distance_2)
                angle_1_list.append(angle_1)
            block = []  # Reset the block
    block.append(line.strip())
# Process the last block (if it exists)
if len(block) == 3:
    distance_1 = float(block[1].split()[2])
    distance_2 = float(block[2].split()[2])
    angle_1 = float(block[2].split()[4])
    distance_1_list.append(distance_1)
    distance_2_list.append(distance_2)
    angle_1_list.append(angle_1)
# # Print the extracted data
# for i in range(len(distance_1_list)):
#     print(f'Block {i+1}:')
#     print(f'Distance_1: {distance_1_list[i]}')
#     print(f'Distance_2: {distance_2_list[i]}')
#     print(f'Angle_1: {angle_1_list[i]}')
#     print()
dis_1_min = min(distance_1_list)
dis_1_max = max(distance_1_list)
dis_2_min = min(distance_2_list)
dis_2_max = max(distance_2_list)
ang_1_min = min(angle_1_list)
ang_1_max = max(angle_1_list)

print(f"dis_1 Minimum value: {dis_1_min}")
print(f"dis_1 Maximum value: {dis_1_max}")
print(f"dis_2 Minimum value: {dis_2_min}")
print(f"dis_2 Maximum value: {dis_2_max}")
print(f"ang_1 Minimum value: {ang_1_min}")
print(f"ang_1 Maximum value: {ang_1_max}")

distance_1 = [0.75, 1.30]
distance_2 = [0.75, 1.30]
angle_1 = [67.5, 147.0]

# Create 13 evenly spaced values between the minimum and maximum values
num_values = 14
distance_1_min = min(distance_1)
distance_1_max = max(distance_1)
distance_1_values = np.linspace(distance_1_min, distance_1_max, num_values)

distance_2_min = min(distance_2)
distance_2_max = max(distance_2)
distance_2_values = np.linspace(distance_2_min, distance_2_max, num_values)

angle_1_min = min(angle_1)
angle_1_max = max(angle_1)
angle_1_values = np.linspace(angle_1_min, angle_1_max, num_values)

distance_1 = []
distance_2 = []
angle_1 = []

distance_1.extend(distance_1_values)
distance_2.extend(distance_2_values)
angle_1.extend(angle_1_values)

#origin point
# O
# H      1      0.95883
# H      1      0.95883    2    104.34240

output_folder = './data/e_training/'
dis1_xyz = './data/e_training/dis_1.xyz'
dis2_xyz = './data/e_training/dis_2.xyz'
ang1_xyz = './data/e_training/ang_1.xyz'

os.makedirs(output_folder, exist_ok=True)
for i, val in enumerate(distance_1):
    new_list = []
    new_list.append("O")
    new_list.append(f"H      1      {val:.5f}")
    new_list.append(f"H      1      0.95883    2    104.34240")
    formatted_output = "\n".join(new_list)
    output_file_path = os.path.join(output_folder, f'dis_1_{i+1}.zmat')
    with open(output_file_path, 'w') as output_file:
        output_file.write(formatted_output)
    command = f'python3 gc.py -zmat {output_file_path} >> {dis1_xyz}'
    subprocess.run(command, shell=True, cwd=os.getcwd())
    
# for i, val in enumerate(distance_1):
#     new_list = []
#     new_list.append("O")
#     new_list.append(f"H      1      0.95883")
#     new_list.append(f"H      1      {distance_2[i]:.5f}    2    104.34240")
#     formatted_output = "\n".join(new_list)
#     output_file_path = os.path.join(output_folder, f'dis_2_{i+1}.zmat')
#     with open(output_file_path, 'w') as output_file:
#         output_file.write(formatted_output)
#     command = f'python3 gc.py -zmat {output_file_path} >> {dis2_xyz}'
#     subprocess.run(command, shell=True, cwd=os.getcwd())
    
for i, val in enumerate(distance_1):
    new_list = []
    new_list.append("O")
    new_list.append(f"H      1      0.95883")
    new_list.append(f"H      1      0.95883    2    {angle_1[i]:.5f}")
    formatted_output = "\n".join(new_list)
    output_file_path = os.path.join(output_folder, f'ang_1_{i+1}.zmat')
    with open(output_file_path, 'w') as output_file:
        output_file.write(formatted_output)
    command = f'python3 gc.py -zmat {output_file_path} >> {ang1_xyz}'
    subprocess.run(command, shell=True, cwd=os.getcwd())   
    
print('Conversion complete.')