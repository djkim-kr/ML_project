import os
import numpy as np
import matplotlib.pyplot as plt
import glob

# Step 1: Recursively find all files that end with "_RMSE_test.dat" in sub-directories.
data_files = glob.glob("**/*.dat", recursive=True)

for data_file in data_files:
    # Identify the parent directory of the current data file
    parent_directory = os.path.basename(os.path.dirname(data_file))
    
    # Verify that the data file matches the pattern "{parent directory}_RMSE_test.dat"
    expected_filename = f"{parent_directory}_RMSE_test.dat"
    if os.path.basename(data_file) != expected_filename:
        continue  # Skip this file if it doesn't match the expected pattern

    # Step 2: Load data
    data = np.loadtxt(data_file, dtype=str)
    headers = np.loadtxt(data_file, dtype=str, max_rows=1, comments=None)[2:]
    # print(data)
    # print(headers)

    # Step 3: Plot data for each file
    x_values= [float(size) for size in headers]
    
    plt.figure(figsize=(15, 10))
    for i in range(len(data)):
        y_values = [float(RMSE) for RMSE in data[i][1:]]
        plt.loglog(x_values, y_values, 
                   marker='o', linestyle='-'
                   ,label=data[i][0])
        for x, y in zip(x_values,y_values):
            plt.annotate(f"{y:.5f}", (x, y), textcoords="offset points", xytext=(0,5), ha='center', fontsize=10)

    plt.title(f"{parent_directory}_RMSE_Analysis")
    plt.xlabel("Train_data_Size")
    plt.xticks(x_values, headers)
    plt.ylabel("test_RMSE_value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{parent_directory}_RMSE_plot.png", dpi=300)
    # plt.show()
        