#!/bin/bash

LMP_modified=/work/rkajouri/LAMMPS_GCMC/fork/lammps/build-modified/lmp
LMP_official=/work/rkajouri/LAMMPS_GCMC/fork/lammps/build-official/lmp


mpirun -np 4 ${LMP_official} -in  ../in.GCMC.CO2.in.ACN.official    \
        -v temp 300.0       \
        -v MDsteps 400      \
        -v MCsteps 100      \
        -v seed1 12442      \
        -v seed2 10116      \
        -v co2mu -8.30      \
        -v acnmu -10.70     \
        -v runsteps 1000000

    
    
