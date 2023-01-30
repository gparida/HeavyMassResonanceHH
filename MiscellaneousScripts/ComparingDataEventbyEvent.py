import awkward1 as ak
import uproot4 as up
import numpy as np
import glob
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser(description='Comapre and Pick up mismatch events between two data files')
#parser.add_argument('--Channel',help="enter either tt or et or mt. For boostedTau test enter test",required=True,choices=['tt', 'et', 'mt'])
parser.add_argument('--p1',help="Path to the first data file",required=True)
parser.add_argument('--p2',help="path to the second data file",required=True)
args = parser.parse_args()

#Open the files in uproot
data1 = up.open(args.p1)
data2 = up.open(args.p2)


RunLumEve1 = data1["Events"].arrays(["run","luminosityBlock","event"],"(gDeltaR_LL<1.5)  & (gDeltaR_LL>0) & (fastMTT_RadionLegWithMet_m>750) & (fastMTT_RadionLegWithMet_m<4250) & (channel==0)",library="np")
RunLumEve2 = data2["Events"].arrays(["run","luminosityBlock","event"],"(gDeltaR_LL<1.5)  & (gDeltaR_LL>0) & (fastMTT_RadionLegWithMet_m>750) & (fastMTT_RadionLegWithMet_m<4250) & (channel==0)",library="np")


for i in range (len(RunLumEve1.run())):
    match = False
    for j in range (len(RunLumEve2.run)):
        if ( (RunLumEve1.run[i] == RunLumEve2.run[j]) and (RunLumEve1.luminosityBlock[i] == RunLumEve2.luminosityBlock[j]) and (RunLumEve1.event[i] == RunLumEve2.event[j]) ):
            match = True
            break
    
    if match == False:
        print("Not present in second file = ",(RunLumEve1.run[i],RunLumEve1.luminosityBlock[i],RunLumEve1.event[i]))

for i in range (len(RunLumEve2.run)):
    match = False
    for j in range (len(RunLumEve1.run)):
        if ( (RunLumEve2.run[i] == RunLumEve1.run[j]) and (RunLumEve2.luminosityBlock[i] == RunLumEve1.luminosityBlock[j]) and (RunLumEve2.event[i] == RunLumEve1.event[j]) ):
            match = True
            break
    
    if match == False:
        print("Not present in second file = ",(RunLumEve2.run[i],RunLumEve2.luminosityBlock[i],RunLumEve2.event[i]))





#print (len(RunLumEve1))
print (np.array_equal(RunLumEve1, RunLumEve1))
#print (np.setdiff1d(RunLumEve1, RunLumEve2))


