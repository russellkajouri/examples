#!/bin/bash

LMP=/work/rkajouri/LAMMPS_GCMC/lammps-stable_29Aug2024_update2/build/lmp
mpirun -np 4 ${LMP} -in  ../share/in.GCMC.CO2.in.ACN    \
        -v temp 300.0       \
        -v MDsteps 4000     \
        -v MCsteps 100     \
        -v seed1 $RANDOM    \
        -v seed2 $RANDOM    \
        -v co2mu -8.30       \
        -v acnmu -10.73     \
        -v runsteps 200000000

    
    
