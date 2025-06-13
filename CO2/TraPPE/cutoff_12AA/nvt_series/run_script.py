#!/bin/python3

import os, subprocess
lengths = [ 90, 95, 97]
lammps_cmd = lambda l : [ '/tikhome/rkajouri/Downloads/lammps-29Aug2024/build/lmp', \
    '-sf', 'gpu', '-pk', 'gpu', '1', 'gpuID', '0', \
    '-in', '../in.nvt.co2', '-log', 'nvt.log', '-v', 'nmols', '500', '-v', 'lbox', f"{l}"]

for l in lengths:
    rundir = f"len_{l:.1f}"

    os.makedirs(rundir, exist_ok=True)
    #print(lammps_cmd(l))

    subprocess.run(lammps_cmd(l), cwd=rundir)
    


    
    
