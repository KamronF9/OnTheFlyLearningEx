#!/bin/bash

cd AIMD


for sys in */; do
    cd $sys
    sysNum=$(echo "$sys" | sed 's/\///g')  # remove the / from the folder name

    # if not empty launch AIMD jobs
    if    ls -A1q . | grep -q .
    then

        for runFol in */; do
            cd $runFol
            runNum=$(echo "$runFol" | sed 's/\///g')  # remove the / from the folder name
            cp ../../../../md.in .
            sbatch ../../../../../singleMultiGPUoneNode.job $sysNum $runNum 
            cd ..
        done      

    else  
        echo empty - no runs in $sys
    fi
    cd ..
done
