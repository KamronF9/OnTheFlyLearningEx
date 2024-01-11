#!/bin/bash


cd ../DpmdTrainPotential


for dir in seed*/; do
  cd $dir
  # save lcurve for each iteration 
  mv lcurve.out lcurve${1}.out
  dp freeze -o frozenModel.pb
  # store a version of each model for now
  cp frozenModel.pb frozenModel${1}.pb
  cd ..
done