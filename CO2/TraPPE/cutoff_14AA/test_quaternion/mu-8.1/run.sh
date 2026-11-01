#!/bin/bash

LMP=/Users/russellkajouri/simulations/quaternion_issue/lammps/build/lmp
mpirun -np 4 ${LMP} -in ../src/in.gcmc.co2
