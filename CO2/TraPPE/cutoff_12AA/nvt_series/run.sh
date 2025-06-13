#!/bin/bash

for len in 270 216 189 170 158 148 139 133 129 125;
do

    mkdir "len_${len}";
    cd "len_${len}"

    /tikhome/rkajouri/Downloads/lammps-29Aug2024/build/lmp -sf gpu -pk gpu 1 gpuID 0 -in ../in.nvt.co2 -log nvt.log -v nmols 500 -v lbox ${len}

    cd ../

done
