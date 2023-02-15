# I will use this script to see if current selections or Isolations applied at a base level in 
# NanoAOD affect significance - Because the efficiency of Signal may be increasing but then we select more background


import ROOT
import glob
import argparse
from re import search
from collections import OrderedDict
import math 
import subprocess
import os
#import uproot as up
#import numpy as np
#import awkward as ak

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(ROOT.kTRUE)


parser = argparse.ArgumentParser(description='Script to plot trees directly from root files. Right now I am writing it for singal Files')
#parser.add_argument('--inputFile1',help="Path to the directory that contains the signal files for all the cuts applied - Inside the directory there should be 2 sub directories that are labbeled Signal and Background")
#parser.add_argument('--inputFile2',help="Path to the directory that contains the signal files without Lepton Isolation - Inside the directory there should be 2 sub directories that are labbeled Signal and Background")
#parser.add_argument('--inputFile3',help="Path to the directory that contains the signal files without Lepton and Tau Isolation - Inside the directory there should be 2 sub directories that are labbeled Signal and Background")

parser.add_argument('--inputFile1','-i1',help="Set of Files with Loose WP for Light Leptons")
parser.add_argument('--inputFile2','-i2',help="Set of Files with Medium WP for Light Leptons")
parser.add_argument('--inputFile3','-i3',help="Set of Files with Tight WP for Light Leptons")
#parser.add_argument("--tauId",'-t',help="enter expected id of hps tau for verification")
#parser.add_argument("--btauId",'-b',help="enter expected id of the boosted tau for verification")
parser.add_argument('--outputDir','-o',help="Output directory for the plots.Will create it if doesnot exists")

args = parser.parse_args()

listOfInputDirs=[args.inputFile1,args.inputFile2,args.inputFile3]
listOfSignalFilesProcessing = ["RadionTohhTohtatahbb_narrow_M-1000","RadionTohhTohtatahbb_narrow_M-2000","RadionTohhTohtatahbb_narrow_M-2500","RadionTohhTohtatahbb_narrow_M-3000","RadionTohhTohtatahbb_narrow_M-3500","RadionTohhTohtatahbb_narrow_M-4000"]
listOfBackgroundSamples = []
listOfSignalSamples = []
Data = []

#totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
BackGroundCutDictionaryTT = {"1000":"FinalWeighting*((fastMTT_RadionLeg_m > 800) && (fastMTT_RadionLeg_m < 1100) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (tt==1))", 
                            "2000":"FinalWeighting*((fastMTT_RadionLeg_m > 1500) && (fastMTT_RadionLeg_m < 2200) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (tt==1))", 
                            "2500":"FinalWeighting*((fastMTT_RadionLeg_m > 1875) && (fastMTT_RadionLeg_m < 2750) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (tt==1))",
                            "3000":"FinalWeighting*((fastMTT_RadionLeg_m > 2250) && (fastMTT_RadionLeg_m < 3300) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0)&& (tt==1))", 
                            "3500":"FinalWeighting*((fastMTT_RadionLeg_m > 2625) && (fastMTT_RadionLeg_m < 3850)&& (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (tt==1))", 
                            "4000":"FinalWeighting*((fastMTT_RadionLeg_m > 3000) && (fastMTT_RadionLeg_m < 4400) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (tt==1))"}

BackGroundCutDictionaryET = {"1000":"FinalWeighting*((fastMTT_RadionLeg_m > 800) && (fastMTT_RadionLeg_m < 1100) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (et==1))", 
                            "2000":"FinalWeighting*((fastMTT_RadionLeg_m > 1500) && (fastMTT_RadionLeg_m < 2200) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (et==1))", 
                            "2500":"FinalWeighting*((fastMTT_RadionLeg_m > 1875) && (fastMTT_RadionLeg_m < 2750) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (et==1))",
                            "3000":"FinalWeighting*((fastMTT_RadionLeg_m > 2250) && (fastMTT_RadionLeg_m < 3300) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0)&& (et==1))", 
                            "3500":"FinalWeighting*((fastMTT_RadionLeg_m > 2625) && (fastMTT_RadionLeg_m < 3850)&& (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (et==1))", 
                            "4000":"FinalWeighting*((fastMTT_RadionLeg_m > 3000) && (fastMTT_RadionLeg_m < 4400) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (et==1))"}

BackGroundCutDictionaryMT = {"1000":"FinalWeighting*((fastMTT_RadionLeg_m > 800) && (fastMTT_RadionLeg_m < 1100) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (mt==1))", 
                            "2000":"FinalWeighting*((fastMTT_RadionLeg_m > 1500) && (fastMTT_RadionLeg_m < 2200) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (mt==1))", 
                            "2500":"FinalWeighting*((fastMTT_RadionLeg_m > 1875) && (fastMTT_RadionLeg_m < 2750) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (mt==1))",
                            "3000":"FinalWeighting*((fastMTT_RadionLeg_m > 2250) && (fastMTT_RadionLeg_m < 3300) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0)&& (mt==1))", 
                            "3500":"FinalWeighting*((fastMTT_RadionLeg_m > 2625) && (fastMTT_RadionLeg_m < 3850)&& (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (mt==1))", 
                            "4000":"FinalWeighting*((fastMTT_RadionLeg_m > 3000) && (fastMTT_RadionLeg_m < 4400) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (mt==1))"}


SignalCutDictionaryTT = {"1000":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 800) && (fastMTT_RadionLeg_m < 1100) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (tt==1))", 
                            "2000":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 1500) && (fastMTT_RadionLeg_m < 2200) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (tt==1))", 
                            "2500":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 1875) && (fastMTT_RadionLeg_m < 2750) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (tt==1))",
                            "3000":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 2250) && (fastMTT_RadionLeg_m < 3300) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0)&& (tt==1))", 
                            "3500":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 2625) && (fastMTT_RadionLeg_m < 3850)&& (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (tt==1))", 
                            "4000":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 3000) && (fastMTT_RadionLeg_m < 4400) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (tt==1))"}

SignalCutDictionaryET = {"1000":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 800) && (fastMTT_RadionLeg_m < 1100) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (et==1))", 
                            "2000":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 1500) && (fastMTT_RadionLeg_m < 2200) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (et==1))", 
                            "2500":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 1875) && (fastMTT_RadionLeg_m < 2750) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (et==1))",
                            "3000":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 2250) && (fastMTT_RadionLeg_m < 3300) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0)&& (et==1))", 
                            "3500":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 2625) && (fastMTT_RadionLeg_m < 3850)&& (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (et==1))", 
                            "4000":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 3000) && (fastMTT_RadionLeg_m < 4400) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (et==1))"}

SignalCutDictionaryMT = {"1000":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 800) && (fastMTT_RadionLeg_m < 1100) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (mt==1))", 
                            "2000":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 1500) && (fastMTT_RadionLeg_m < 2200) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (mt==1))", 
                            "2500":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 1875) && (fastMTT_RadionLeg_m < 2750) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (mt==1))",
                            "3000":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 2250) && (fastMTT_RadionLeg_m < 3300) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0)&& (mt==1))", 
                            "3500":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 2625) && (fastMTT_RadionLeg_m < 3850)&& (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (mt==1))", 
                            "4000":"genWeight*pileupWeighting*((fastMTT_RadionLeg_m > 3000) && (fastMTT_RadionLeg_m < 4400) && (gDeltaR_LL<1.5) && (gDeltaR_LL>0) && (gMVis_LL>0) && (mt==1))"}

for dir in listOfInputDirs:
    listOfBackgroundSamples = []
    listOfSignalSamples = []
    Data = []

    for files in  glob.glob(dir+ "/*.root"):
        nameStrip=files.strip()
        filename = (nameStrip.split('/')[-1]).split('.')[-2]
        if ((not search("Radion", filename)) and (not search("Data", filename)) and (not search("Run", filename))):
            listOfBackgroundSamples.append(filename)
        if (search("Radion", filename)):
            listOfSignalSamples.append(filename)
        if ((search("Data", filename)) or (search("Run", filename))):
            Data.append(filename)

    print ("Total signal files in ",dir," = ",len(listOfSignalSamples)," Total Background Files = ",len(listOfBackgroundSamples)," Total Data Files = ",len(Data)," Total Files = ",len(glob.glob(args.inputFile1+ "/*.root")))
    print('\n')

print('BackgroundFiles = ','\n')
print(listOfBackgroundSamples)
print('SignalFiles = ','\n')
print(listOfSignalSamples)
print('Data = ','\n')
print(Data)





def makeHistogram(name,tag, markerColor, markeyStyle, markerSize):
    temp = ROOT.TH1F("name",name,6,0,6)
    temp.GetXaxis().SetBinLabel(1,"1TeV")
    temp.GetXaxis().SetBinLabel(2,"2TeV")
    temp.GetXaxis().SetBinLabel(3,"2.5TeV")
    temp.GetXaxis().SetBinLabel(4,"3TeV")
    temp.GetXaxis().SetBinLabel(5,"3.5TeV")
    temp.GetXaxis().SetBinLabel(6,"4TeV")
    temp.GetXaxis().SetTitle("Mass Point")
    temp.SetMarkerColor(markerColor)
    temp.SetMarkerStyle(markeyStyle)
    temp.SetMarkerSize(markerSize)
    temp.GetYaxis().SetTitle(tag)
    return temp




def computeTotalBackgroundForVariousMPs(inputFolder,inputBackGroundCutDictionary,totalBackgroundDictionary):
    listed = sorted(inputBackGroundCutDictionary.keys())
    ver = False
    print (listed)
    for key in listed: 
        totBac = 0.0       
        print ("processing for signal = ",key)
        for filename in listOfBackgroundSamples:
            rootfile = ROOT.TFile(inputFolder+"/"+filename+".root")
            #tree_rootfile_Runs = rootfile.Get('Runs')
            #sumofweights = 0.0
           # nEntries = tree_rootfile_Runs.GetEntries()
           # for x in range(nEntries):
           #     tree_rootfile_Runs.GetEntry(x)
           #     sumofweights+=tree_rootfile_Runs.genEventSumw
           # oneOversumofweights = 1/sumofweights
            tree_rootfile = rootfile.Get('Events')
            if (tree_rootfile.GetEntries()==0):
                continue
            #print ('fastMTT_RadionLegWithMet_m >> histBack(100,0,70000)',str(oneOversumofweights)+"*"+inputBackGroundCutDictionary[key])
            #tree_rootfile.Draw('fastMTT_RadionLegWithMet_m >> histBack(100,0,70000)',str(oneOversumofweights)+"*"+inputBackGroundCutDictionary[key])
            tree_rootfile.Draw('fastMTT_RadionLegWithMet_m >> histBack(100,0,70000)',inputBackGroundCutDictionary[key])
            totBac += ROOT.gDirectory.Get("histBack").Integral()
        print ("Total Background estimated for ",key," is ",totBac)
        totalBackgroundDictionary[key] = totBac


def computeSoverbandSoverSplusBforMPs(inputFolder,inputBackGroundCutDictionary,SB,SSB):
    for index, file in enumerate(listOfSignalFilesProcessing):
        backgroundkey = (file.strip()).split('-')[-1]
        rootfile = ROOT.TFile(inputFolder+"/"+file+".root")
        tree_rootfile = rootfile.Get('Events')
        tree_rootfile_Runs = rootfile.Get('Runs')
        sumofweights = 0.0
        nEntries = tree_rootfile_Runs.GetEntries()
        for x in range(nEntries):
            tree_rootfile_Runs.GetEntry(x)
            sumofweights+=tree_rootfile_Runs.genEventSumw
        oneOversumofweights = 1/sumofweights
        print ('fastMTT_RadionLegWithMet_m >> histSig(100,0,70000)',str(oneOversumofweights)+"*"+inputBackGroundCutDictionary[backgroundkey])
        tree_rootfile.Draw('fastMTT_RadionLegWithMet_m >> histSig(100,0,70000)',str(oneOversumofweights)+"*"+inputBackGroundCutDictionary[backgroundkey])
        #finalEvents = ak.sum(ak.flatten(rootfile.arrays("FinalWeighting",BackGroundCutDictionary[backgroundkey]),axis=None))
        finalEvents = ROOT.gDirectory.Get("histSig").Integral()
        print ("Filling = ",backgroundkey,"Total Signal = ",finalEvents,"Total Background = ",totalBackgroundDictionary[backgroundkey])
        SB.SetBinContent(index+1,float(float(finalEvents)/float(totalBackgroundDictionary[backgroundkey]))) 
        SSB.SetBinContent(index+1,float(float(finalEvents)/math.sqrt((float(finalEvents)+float(totalBackgroundDictionary[backgroundkey])))))




ETLooseSB = makeHistogram("noIso","S/B",4, 34, 1)
ETLooseSSB = makeHistogram("noIso","S/sqrt(S+B)",4, 34, 1)
ETMediumSB = makeHistogram("defIso","S/B",2, 21, 1)
ETMediumSSB = makeHistogram("defIso","S/sqrt(S+B)",2, 21, 1)
ETTightSB = makeHistogram("corrIso","S/B",3, 22, 1)
ETTightSSB = makeHistogram("corrIso","S/sqrt(S+B)",3, 22, 1)

MTLooseSB = makeHistogram("noIso","S/B",4, 34, 1)
MTLooseSSB = makeHistogram("noIso","S/sqrt(S+B)",4, 34, 1)
MTMediumSB = makeHistogram("defIso","S/B",2, 21, 1)
MTMediumSSB = makeHistogram("defIso","S/sqrt(S+B)",2, 21, 1)
MTTightSB = makeHistogram("corrIso","S/B",3, 22, 1)
MTTightSSB = makeHistogram("corrIso","S/sqrt(S+B)",3, 22, 1)

TTLooseSB = makeHistogram("noIso","S/B",4, 34, 1)
TTLooseSSB = makeHistogram("noIso","S/sqrt(S+B)",4, 34, 1)
TTMediumSB = makeHistogram("defIso","S/B",2, 21, 1)
TTMediumSSB = makeHistogram("defIso","S/sqrt(S+B)",2, 21, 1)
TTTightSB = makeHistogram("corrIso","S/B",3, 22, 1)
TTTightSSB = makeHistogram("corrIso","S/sqrt(S+B)",3, 22, 1)

######################################################################################################################
print ("ET pairs processing ...........")
totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
computeTotalBackgroundForVariousMPs(args.inputFile1,BackGroundCutDictionaryET,totalBackgroundDictionary)
computeSoverbandSoverSplusBforMPs(args.inputFile1,SignalCutDictionaryET,ETLooseSB,ETLooseSSB)

totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
computeTotalBackgroundForVariousMPs(args.inputFile2,BackGroundCutDictionaryET,totalBackgroundDictionary)
computeSoverbandSoverSplusBforMPs(args.inputFile2,SignalCutDictionaryET,ETMediumSB,ETMediumSSB)

totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
computeTotalBackgroundForVariousMPs(args.inputFile3,BackGroundCutDictionaryET,totalBackgroundDictionary)
computeSoverbandSoverSplusBforMPs(args.inputFile3,SignalCutDictionaryET,ETTightSB,ETTightSSB)


##########################################################################################################################
print ("MT pairs processing ...........")
totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
computeTotalBackgroundForVariousMPs(args.inputFile1,BackGroundCutDictionaryMT,totalBackgroundDictionary)
computeSoverbandSoverSplusBforMPs(args.inputFile1,SignalCutDictionaryMT,MTLooseSB,MTLooseSSB)

totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
computeTotalBackgroundForVariousMPs(args.inputFile2,BackGroundCutDictionaryMT,totalBackgroundDictionary)
computeSoverbandSoverSplusBforMPs(args.inputFile2,SignalCutDictionaryMT,MTMediumSB,MTMediumSSB)

totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
computeTotalBackgroundForVariousMPs(args.inputFile3,BackGroundCutDictionaryMT,totalBackgroundDictionary)
computeSoverbandSoverSplusBforMPs(args.inputFile3,SignalCutDictionaryMT,MTTightSB,MTTightSSB)
############################################################################################################################
print ("TT pairs processing ...........")
totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
computeTotalBackgroundForVariousMPs(args.inputFile1,BackGroundCutDictionaryTT,totalBackgroundDictionary)
computeSoverbandSoverSplusBforMPs(args.inputFile1,SignalCutDictionaryTT,TTLooseSB,TTLooseSSB)

totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
computeTotalBackgroundForVariousMPs(args.inputFile2,BackGroundCutDictionaryTT,totalBackgroundDictionary)
computeSoverbandSoverSplusBforMPs(args.inputFile2,SignalCutDictionaryTT,TTMediumSB,TTMediumSSB)

totalBackgroundDictionary = {"1000":0.0, "2000":0.0, "2500":0.0, "3000":0.0, "3500":0.0, "4000":0.0}
computeTotalBackgroundForVariousMPs(args.inputFile3,BackGroundCutDictionaryTT,totalBackgroundDictionary)
computeSoverbandSoverSplusBforMPs(args.inputFile3,SignalCutDictionaryTT,TTTightSB,TTTightSSB)

########################################################################################################################


def setUpCanvasLegendLatex(canvasName,year):
    canvasName = ROOT.TCanvas(canvasName,canvasName)
    canvasName.SetFrameLineWidth(1)
    canvasName.SetGrid()
    #canvasName.SetLogy()
    legend = ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
    legend.SetFillStyle(1001)
    legend.SetLineWidth(0)
    legend.SetLineStyle(1)
    legend.SetFillColor(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.03)
    cmsLatex = ROOT.TLatex()
    cmsLatex.SetTextSize(0.06)
    cmsLatex.SetNDC(True)
    cmsLatex.SetTextFont(61)
    cmsLatex.SetTextAlign(11)
    #cmsLatex.DrawLatex(0.1,0.92,"CMS")
    cmsLatex.DrawLatex(0.1,0.91,"CMS")
    cmsLatex.SetTextFont(52)
    #cmsLatex.DrawLatex(0.1+0.08,0.95,"Preliminary")
    cmsLatex.DrawLatex(0.12+0.08,0.91,"Preliminary")
    if year==2016:
        lumiText = '16.81 fb^{-1}, 13 TeV'
    cmsLatex.SetTextFont(42)
    cmsLatex.SetTextSize(0.045)
    cmsLatex.DrawLatex(0.55,0.91,lumiText)
    return canvasName, legend, cmsLatex  

if not os.path.exists(args.outputDir):
    os.makedirs(args.outputDir)
    

canET,legET,latexET = setUpCanvasLegendLatex("canvasET",2016)
legET.SetFillStyle(1001)
legET.AddEntry(ETLooseSB,"noIso","ep")
legET.AddEntry(ETMediumSB,"defIso","ep")
legET.AddEntry(ETTightSB,"corrIso","ep")
maximum = max(ETLooseSB.GetMaximum(),ETMediumSB.GetMaximum(),ETTightSB.GetMaximum())
ETLooseSB.SetMaximum(maximum + 0.30*maximum)
ETLooseSB.Draw("P")
ETMediumSB.Draw("same P")
ETTightSB.Draw("same P")
legET.Draw("same")
latexET.Draw("same")
canET.SaveAs(args.outputDir+"/"+"ETSoverB.png")


canET2,legET2,latexET2 = setUpCanvasLegendLatex("canvasET2",2016)
legET2.SetFillStyle(1001)
legET2.AddEntry(ETLooseSSB,"noIso","ep")
legET2.AddEntry(ETMediumSSB,"defIso","ep")
legET2.AddEntry(ETTightSSB,"corrIso","ep")
maximum = max(ETLooseSSB.GetMaximum(),ETMediumSSB.GetMaximum(),ETTightSSB.GetMaximum())
ETLooseSSB.SetMaximum(maximum + 0.30*maximum)
ETLooseSSB.Draw("P")
ETMediumSSB.Draw("same P")
ETTightSSB.Draw("same P")
legET2.Draw("same")
latexET2.Draw("same")
canET2.SaveAs(args.outputDir+"/"+"ETSoversqrtSB.png")

################################################################################################################
canMT,legMT,latexMT = setUpCanvasLegendLatex("canvasMT",2016)
legMT.SetFillStyle(1001)
legMT.AddEntry(MTLooseSB,"noIso","ep")
legMT.AddEntry(MTMediumSB,"defIso","ep")
legMT.AddEntry(MTTightSB,"corrIso","ep")
maximum = max(MTLooseSB.GetMaximum(),MTMediumSB.GetMaximum(),MTTightSB.GetMaximum())
MTLooseSB.SetMaximum(maximum + 0.30*maximum)
MTLooseSB.Draw("P")
MTMediumSB.Draw("same P")
MTTightSB.Draw("same P")
legMT.Draw("same")
latexMT.Draw("same")
canMT.SaveAs(args.outputDir+"/"+"MTSoverB.png")


canMT2,legMT2,latexMT2 = setUpCanvasLegendLatex("canvasMT2",2016)
legMT2.SetFillStyle(1001)
legMT2.AddEntry(MTLooseSSB,"noIso","ep")
legMT2.AddEntry(MTMediumSSB,"defIso","ep")
legMT2.AddEntry(MTTightSSB,"corrIso","ep")
maximum = max(MTLooseSSB.GetMaximum(),MTMediumSSB.GetMaximum(),MTTightSSB.GetMaximum())
MTLooseSSB.SetMaximum(maximum + 0.30*maximum)
MTLooseSSB.Draw("P")
MTMediumSSB.Draw("same P")
MTTightSSB.Draw("same P")
legMT2.Draw("same")
latexMT2.Draw("same")
canMT2.SaveAs(args.outputDir+"/"+"MTSoversqrtSB.png")

############################################################################################################################

canTT,legTT,latexTT = setUpCanvasLegendLatex("canvasTT",2016)
legTT.SetFillStyle(1001)
legTT.AddEntry(TTLooseSB,"noIso","ep")
legTT.AddEntry(TTMediumSB,"defIso","ep")
legTT.AddEntry(TTTightSB,"corrIso","ep")
maximum = max(TTLooseSB.GetMaximum(),TTMediumSB.GetMaximum(),TTTightSB.GetMaximum())
TTLooseSB.SetMaximum(maximum + 0.30*maximum)
TTLooseSB.Draw("P")
TTMediumSB.Draw("same P")
TTTightSB.Draw("same P")
legTT.Draw("same")
latexTT.Draw("same")
canTT.SaveAs(args.outputDir+"/"+"TTSoverB.png")


canTT2,legTT2,latexTT2 = setUpCanvasLegendLatex("canvasTT2",2016)
legTT2.SetFillStyle(1001)
legTT2.AddEntry(TTLooseSSB,"noIso","ep")
legTT2.AddEntry(TTMediumSSB,"defIso","ep")
legTT2.AddEntry(TTTightSSB,"corrIso","ep")
maximum = max(TTLooseSSB.GetMaximum(),TTMediumSSB.GetMaximum(),TTTightSSB.GetMaximum())
TTLooseSSB.SetMaximum(maximum + 0.30*maximum)
TTLooseSSB.Draw("P")
TTMediumSSB.Draw("same P")
TTTightSSB.Draw("same P")
legTT2.Draw("same")
latexTT2.Draw("same")
canTT2.SaveAs(args.outputDir+"/"+"TTSoversqrtSB.png")
#################################################################################################################


