#!/bin/bash

# copy in AIMD files 

cd AIMD

for sys in */; do
    cd $sys

    # if not empty check for complete
    if    ls -A1q . | grep -q .
    then

        # echo 'Waiting for squeue to clear completely from job'
        while [ ! -f doneAIMDflag ]
        do
            # only jobid output if complete
            if [ "$(squeue -u kamron -n singleMultiGPUoneNode.job -o %A)" = "JOBID" ]; then
                echo DONE $sys
                touch doneAIMDflag
            fi 
            sleep 2 # or less like 0.2
        done
        rm doneAIMDflag

        # copy out 
        
        for runFol in */; do
            cd $runFol
            cp *.jdftxout ../../../../DpmdTrainPotential/train/
            cd ..
        done    

    fi

    cd ..
done


# process jdftxouts to DeePMD input
cd ../../DpmdTrainPotential
# parse jdftxout with custom dpdata
python /global/homes/k/kamron/dpdatajdftx/VariableParseAIMDtoDPMD.py 10 > conversionInfo$1

for dir in seed*/; do
  cd $dir
  
  cp ../../inputInitial.json input.json

  cd ..
done


# launch training
# remove done flag in case it was there before
rm doneTrainingFlag
sbatch ../multiTrainInit.job

# wait until done training
echo 'Waiting for doneTrainingflag'
while [ ! -f doneTrainingFlag ]
do
  sleep 2 # or less like 0.2
done
echo 'Detected doneTrainingflag!'
rm doneTrainingFlag
