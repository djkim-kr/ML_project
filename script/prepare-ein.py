import os
import shutil

# Fill out these settings ##############################################
# What dir and what size of training set?
Dir = "nor"
Dir_size = {
    f'{Dir}': [2, 5, 20, 50, 100, 250, 500, 1000, 2000, 3000, 4329
          ] 
}

with open("gap_fit.sh.template") as f:
    GAP_IN = f.read()
with open("mpi_quip_eins.sh.template") as f:
    RUN_SH_QUIP = f.read()
with open("plot_gap.py.template") as f:
    PLOT_IN = f.read()
with open(f'./data/{Dir}_train.xyz', 'r') as file:
    lines = file.readlines() 

####gap_fit optimized variable , needs to be fixed.
l_max =3
n_max =9
atom_sigma =0.34
zeta =3
cutoff =3.72
cutoff_transition_width =1.77
central_weight=0.95         
n_sparse=1019               
delta=1.94                  
radial_scaling=-0.39
####files to copy from current folder
files_to_copy = [f'./data/{Dir}_valid.xyz',f'./data/{Dir}_test.xyz']
################################################################
for Dir_name, size_list in Dir_size.items():
    for size in size_list:
        dirname = f"{Dir}_size_{size:04.0f}"
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        inpath = os.path.join(dirname, "gap_fit.sh")
        if not os.path.exists(inpath):
            sigma_value = "{0.01 0.1 1 0}"
            first = '{'
            last = '}'
            SLURM_JOB_ID="{SLURM_JOB_ID}"
            e0='{H:0:O:0}'
            
            name = Dir
            out = 'quip'
            rmse= "{'rmse': average, 'std': std_}"
            
            with open(os.path.join(dirname, f"{Dir}_train.xyz"), "w") as f:
                (start, end) = (1, size*5)
                for line in lines[start -1:end]:
                    f.write(line)
            
            with open(inpath, "w") as f:
                f.write(GAP_IN.format(name=name, 
                                      sigma_value=sigma_value,
                                      first=first,
                                      last=last,
                                      e0=e0,
                                      l_max=l_max,
                                      n_max=n_max,
                                      atom_sigma=atom_sigma,
                                      zeta=zeta,
                                      cutoff=cutoff,
                                      cutoff_transition_width=cutoff_transition_width,
                                      central_weight=central_weight,
                                      n_sparse=n_sparse,
                                      delta=delta,
                                      radial_scaling=radial_scaling))
            os.chmod(inpath, 0o744)
            
            with open(os.path.join(dirname, "quip_run.sh"), "w") as f:
                f.write(RUN_SH_QUIP.format(subdir=dirname,
                                            time="01:00:00",
                                            mol=name,
                                            SLURM_JOB_ID=SLURM_JOB_ID,
                                            out=out))
            with open(os.path.join(dirname, "plot_gap.py"), "w") as f:
                f.write(PLOT_IN.format(name=name,
                                       rmse = rmse,
                                       result =dirname))
            for file in files_to_copy:
                if os.path.exists(file):
                    shutil.copy(file, dirname)
                    
print('Folders are ready')
