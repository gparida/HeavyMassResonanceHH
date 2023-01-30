# I will use this script to see if current selections or Isolations applied at a base level in 
# NanoAOD affect significance - Because the efficiency of Signal may be increasing but then we select more background


import ROOT
import glob
import argparse
from re import search
from collections import OrderedDict
import math 
#import uproot as up
#import numpy as np
#import awkward as ak

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(ROOT.kTRUE)


parser = argparse.ArgumentParser(description='Script to plot trees directly from root files. Right now I am writing it for singal Files')
parser.add_argument('--inputFile1',help="Path to the directory that contains the signal files for all the cuts applied - Inside the directory there should be 2 sub directories that are labbeled Signal and Background")
parser.add_argument('--inputFile2',help="Path to the directory that contains the signal files without Lepton Isolation - Inside the directory there should be 2 sub directories that are labbeled Signal and Background")
parser.add_argument('--inputFile3',help="Path to the directory that contains the signal files without Lepton and Tau Isolation - Inside the directory there should be 2 sub directories that are labbeled Signal and Background")
args = parser.parse_args()

#histDict = []

print ("here")

listOfSignalFilesProcessing = ["RadionTohhTohtatahbb_narrow_M-1000","RadionTohhTohtatahbb_narrow_M-2000","RadionTohhTohtatahbb_narrow_M-2500","RadionTohhTohtatahbb_narrow_M-3000","RadionTohhTohtatahbb_narrow_M-3500","RadionTohhTohtatahbb_narrow_M-4000"]

#totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
BackGroundCutDictionary = {"1000":"FinalWeighting*((fastMTT_RadionLeg_m > 800) && (fastMTT_RadionLeg_m < 1100))", 
                            "2000":"FinalWeighting*((fastMTT_RadionLeg_m > 1500) && (fastMTT_RadionLeg_m < 2200))", 
                            "2500":"FinalWeighting*((fastMTT_RadionLeg_m > 1875) && (fastMTT_RadionLeg_m < 2750))",
                            "3000":"FinalWeighting*((fastMTT_RadionLeg_m > 2250) && (fastMTT_RadionLeg_m < 3300))", 
                            "3500":"FinalWeighting*((fastMTT_RadionLeg_m > 2625) && (fastMTT_RadionLeg_m < 3850))", 
                            "4000":"FinalWeighting*((fastMTT_RadionLeg_m > 3000) && (fastMTT_RadionLeg_m < 4400))"}


def makeHistogram(name,tag):
    temp = ROOT.TH1F(name,name,6,0,6)
    temp.GetXaxis().SetBinLabel(1,"1TeV")
    temp.GetXaxis().SetBinLabel(2,"2TeV")
    temp.GetXaxis().SetBinLabel(3,"2.5TeV")
    temp.GetXaxis().SetBinLabel(4,"3TeV")
    temp.GetXaxis().SetBinLabel(5,"3.5TeV")
    temp.GetXaxis().SetBinLabel(6,"4TeV")
    temp.GetXaxis().SetTitle("Mass Point")
    temp.GetYaxis().SetTitle(tag)
    return temp


def computeTotalBackgroundForVariousMPs(inputFolder,totalBackgroundDictionary):
    listed = sorted(BackGroundCutDictionary.keys())
    print (listed)
    for key in listed: 
        totBac = 0.0       
        print ("processing for signal = ",key)
        for files in  glob.glob(inputFolder+ "/*.root"):
            nameStrip=files.strip()
            filename = (nameStrip.split('/')[-1]).split('.')[-2]
            #print (filename)
            if (not search("Radion", filename)) and (not search("Data", filename)):
                #print (inputFolder+"/"+filename+".root")
                #print (filename)
                rootfile = ROOT.TFile(inputFolder+"/"+filename+".root")
                #rootfile = up.open(inputFolder+"/"+filename+".root:Events")
                #btag_variables_arr = rootfile["Events/finalWeighting"].arrays()
                tree_rootfile = rootfile.Get('Events')
                if (tree_rootfile.GetEntries()==0):
                    continue
                tree_rootfile.Draw('fastMTT_RadionLegWithMet_m >> histBack(100,0,70000)',BackGroundCutDictionary[key])
                #if tree_rootfile.GetEntries() ==0:
                #    continue
                #tempArray = rootfile.arrays("FinalWeighting",BackGroundCutDictionary[key])
                #print (BackGroundCutDictionary[key])
                #tempArray = ak.flatten(rootfile.arrays("FinalWeighting",BackGroundCutDictionary[key]),axis=None)
                #tempArray0 = ak.flatten(rootfile.arrays("FinalWeighting"),axis=None)
                #print ("Beofre cut = ",ak.count(tempArray0, axis=None),"After cut = ",ak.count(tempArray, axis=None))
                #print (type (tempArray),tempArray)
                totBac += ROOT.gDirectory.Get("histBack").Integral()
        print ("Total Background estimated for ",key," is ",totBac)
        totalBackgroundDictionary[key] = totBac

def computeSoverbandSoverSplusBforMPs(SB,SSB):
    for index, file in enumerate(listOfSignalFilesProcessing):
        #rootfile = up.open(args.inputFile1+"/"+file+".root:Events")
        backgroundkey = (file.strip()).split('-')[-1]
        #print ("While Filling Singnal = ", backgroundkey)
        rootfile = ROOT.TFile(args.inputFile1+"/"+file+".root")
        tree_rootfile = rootfile.Get('Events')
        tree_rootfile.Draw('fastMTT_RadionLegWithMet_m >> histSig(100,0,70000)',BackGroundCutDictionary[backgroundkey])
        #finalEvents = ak.sum(ak.flatten(rootfile.arrays("FinalWeighting",BackGroundCutDictionary[backgroundkey]),axis=None))
        finalEvents = ROOT.gDirectory.Get("histSig").Integral()
        print ("Filling = ",backgroundkey,"Total Signal = ",finalEvents,"Total Background = ",totalBackgroundDictionary[backgroundkey])
        SB.SetBinContent(index+1,float(float(finalEvents)/float(totalBackgroundDictionary[backgroundkey]))) 
        SSB.SetBinContent(index+1,float(float(finalEvents)/math.sqrt((float(finalEvents)+float(totalBackgroundDictionary[backgroundkey])))))




lepIDwoCorrSB = makeHistogram("lepIDwoCorrSB","S/B")
lepIDwoCorrSSB = makeHistogram("lepIDwoCorrSSB","S/sqrt(S+B)")

lepIDwCorrwoIsoSB = makeHistogram("lepIDwCorrwoIsoSB","S/B")
lepIDwCorrwoIsoSSB = makeHistogram("lepIDwCorrwoIsoSSB","S/sqrt(S+B)")

lepIDCorrIsoSB = makeHistogram("lepIDCorrIsoSB","S/B")
lepIDCorrIsoSSB = makeHistogram("lepIDCorrIsoSSB","S/sqrt(S+B)")

totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
computeTotalBackgroundForVariousMPs(args.inputFile1,totalBackgroundDictionary)
computeSoverbandSoverSplusBforMPs(lepIDwoCorrSB,lepIDwoCorrSSB)

totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
computeTotalBackgroundForVariousMPs(args.inputFile2,totalBackgroundDictionary)
computeSoverbandSoverSplusBforMPs(lepIDwCorrwoIsoSB,lepIDwCorrwoIsoSSB)

totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
computeTotalBackgroundForVariousMPs(args.inputFile3,totalBackgroundDictionary)
computeSoverbandSoverSplusBforMPs(lepIDCorrIsoSB,lepIDCorrIsoSSB)


lepIDwoCorrSB.SetMarkerColor(4)
lepIDwoCorrSB.SetMarkerStyle(34)
lepIDwoCorrSB.SetMarkerSize(1.5)

lepIDwoCorrSSB.SetMarkerColor(4)
lepIDwoCorrSSB.SetMarkerStyle(34)
lepIDwoCorrSSB.SetMarkerSize(1.5)

lepIDwCorrwoIsoSB.SetMarkerColor(2)
lepIDwCorrwoIsoSB.SetMarkerStyle(21)
lepIDwCorrwoIsoSB.SetMarkerSize(1.5)
#
lepIDwCorrwoIsoSSB.SetMarkerColor(2)
lepIDwCorrwoIsoSSB.SetMarkerStyle(21)
lepIDwCorrwoIsoSSB.SetMarkerSize(1.5)

lepIDCorrIsoSB.SetMarkerColor(3)
lepIDCorrIsoSB.SetMarkerStyle(22)
lepIDCorrIsoSB.SetMarkerSize(1.5)
#
lepIDCorrIsoSSB.SetMarkerColor(3)
lepIDCorrIsoSSB.SetMarkerStyle(22)
lepIDCorrIsoSSB.SetMarkerSize(1.5)


legend = ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
#legend.SetHeader("#tau_{h}-#tau_{h} channels","C")
legend.SetFillStyle(1001)
legend.AddEntry(lepIDwoCorrSB,"elewithDefaltID","ep")
legend.AddEntry(lepIDwCorrwoIsoSB,"elewithmodID","ep")
legend.AddEntry(lepIDCorrIsoSB,"eleWithmodIDcorIso","ep")


can1 = ROOT.TCanvas("canvas1", "efficiency")
can1.SetGrid()
#can1.SetLogy()
maximum = max(lepIDwoCorrSB.GetMaximum(),lepIDwCorrwoIsoSB.GetMaximum(),lepIDCorrIsoSB.GetMaximum())
lepIDwoCorrSB.SetMaximum(maximum + 0.30*maximum)
lepIDwoCorrSB.Draw("P")
lepIDwCorrwoIsoSB.Draw("same P")
lepIDCorrIsoSB.Draw("same P")
legend.Draw("same")
can1.SaveAs("SignalOverBackground.pdf")

legend = ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
#legend.SetHeader("#tau_{h}-#tau_{h} channels","C")
legend.SetFillStyle(1001)
legend.AddEntry(lepIDwoCorrSSB,"elewithDefaltID","ep")
legend.AddEntry(lepIDwCorrwoIsoSSB,"elewithmodID","ep")
legend.AddEntry(lepIDCorrIsoSSB,"eleWithmodIDcorIso","ep")

can2 = ROOT.TCanvas("canvas2", "efficiency")
can2.SetGrid()
#can2.SetLogy()
maximum = max(lepIDwoCorrSSB.GetMaximum(),lepIDwCorrwoIsoSSB.GetMaximum(),lepIDCorrIsoSSB.GetMaximum())
lepIDwoCorrSSB.SetMaximum(maximum + 0.30*maximum)
lepIDwoCorrSSB.Draw("P")
lepIDwCorrwoIsoSSB.Draw("same P")
lepIDCorrIsoSSB.Draw("same P")
legend.Draw("same")
can2.SaveAs("SignalOverSignalBackground.pdf")



