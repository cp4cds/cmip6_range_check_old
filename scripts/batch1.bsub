#!/bin/bash
#BSUB -q short-serial
#BSUB -oo rg-%J-%I.o
#BSUB -eo rg-%J-%I.e 
#BSUB -W 8:00
####BSUB -J R_job[1051-1100]

source activate myenv38

## jaspy load is faster .. but there is a numpy issue at the moment
##
##module load jaspy

python consol_to_json.py -d sh_02/Omon.sos
