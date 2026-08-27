


Implementing a GCMC simulation of two or more rigid molecules via LAMMPS need to maintain two distinct thermostats, as

``` LAMMPS

molecule Mol1 mol1.txt
molecule Mol2 mol2.txt

fig RIG1 t1 rigid/nvt/small molecule ... mol Mol1 ..
fix RIG2 t2 rigid/nvt/small molecule ... mol Mol2 ..


fix GCMC1 t1 gcmc ... mol Mol1 rigid RIG1
fix GCMC2 t2 gcmc ... mol Mol2 rigid RIG2


```

However, we can modify the GCMC fix CPP/HPP files on LAMMPS via defining a new keyword `molindex` that specifies which 
molecule template within a multiple molecule template array (definitions) should be selected for interacting with the GCMC
fix.

So we can rewrite our LAMMPS script as below,

```
molecule MOLs mol1.txt mol2.txt
fix RIG12 all rigid/nvt/small molecule ... mol MOLs ...


fix GCMC1 t1 gcmc ... mol MOLs molindex 1 rigid RIG12 ...
fix GCMC2 t2 gcmc ... mol MOLs molindex 2 rigid RIG12 ...

```


