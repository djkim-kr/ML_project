import numpy as np
from ase.io import read
import os

#average = RMSE(Root Mean Square Error) 평균 제곱근 오차, std_ = Standard deviation 표준편차
def rms_dict(in_file, out_file):
    
    in_atoms = read(in_file, ':')
    out_atoms = read(out_file, ':')
    ener_in = [at.get_potential_energy() / len(at.get_chemical_symbols()) for at in in_atoms]
    ener_out = [at.get_potential_energy() / len(at.get_chemical_symbols()) for at in out_atoms]
    x_ref = np.array(ener_in)
    x_pred = np.array(ener_out)
    if np.shape(x_pred) != np.shape(x_ref):
        raise ValueError('WARNING: not matching shapes in rms')
    
    error_2 = (x_ref - x_pred) ** 2
    average = np.sqrt(np.average(error_2))
    std_ = np.sqrt(np.var(error_2))
    
    return {'rmse': average, 'std': std_}

main_folders = ['internal', 'direct', 'normal', 'harmonic']
prefix_map = {
    'internal': 'int',
    'direct': 'dir',
    'normal': 'nor',
    'harmonic': 'har'
}

rmse_data = {}
# Iterate over each folder to calculate RMSE values
for main_folder in main_folders:
    prefix = prefix_map[main_folder]
    for sub_folder in os.listdir(main_folder):
        if sub_folder.startswith(f"{prefix}_size_"):
            in_file = os.path.join(main_folder, sub_folder, f"{prefix}_test.xyz")
            out_file = os.path.join(main_folder, sub_folder, "quip_test.xyz")
            if os.path.exists(in_file) and os.path.exists(out_file):
                rmse = np.round(rms_dict(in_file, out_file)['rmse'], 5)
                size = sub_folder.split('_')[-1]
                if main_folder not in rmse_data:
                    rmse_data[main_folder] = {}
                rmse_data[main_folder][size] = rmse

# Save RMSE data in a table format
sizes = sorted(list(rmse_data['internal'].keys()))
header = ['Folder'] + sizes
data = []

for main_folder in main_folders:
    row = [main_folder] + [rmse_data[main_folder].get(size, 'N/A') for size in sizes]
    data.append(row)

current_directory_name = os.path.basename(os.getcwd())
output_file = f"{current_directory_name}_RMSE_test.dat"
np.savetxt(output_file, data, header=' '.join(header), delimiter=' ', fmt='%s')

if os.path.exists(output_file):
    print(f"{output_file} is successfully written")