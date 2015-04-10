#!/bin/bash

MYFILEPATH="/Users/Sonata/Programs/SD/BACKEND/"


echo "Getting files from SD/BACKEND..."
for F in "machineAlgs" "graphDB" "getFeatures" "server" "reqHandler"
do 
	cp $MYFILEPATH$F.py backend

done
