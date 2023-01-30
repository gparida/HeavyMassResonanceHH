import ROOT
import glob
import argparse

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

from plotSettings import *


#Now we need to take inputs
parser = argparse.ArgumentParser(description='Script to plot trees directly from root files. Right now I am writing it for singal Files')
#parser.add_argument('--Channel',help="enter either tt or et or mt. For boostedTau test enter test",required=True,choices=['tt', 'et', 'mt'])
parser.add_argument('--inputFile',help="Full path to the signal file where the signals are")
args = parser.parse_args()

listOfSignalFilesProcessing = ["RadionTohhTohtatahbb_narrow_M-1000","RadionTohhTohtatahbb_narrow_M-2000","RadionTohhTohtatahbb_narrow_M-2500","RadionTohhTohtatahbb_narrow_M-3000","RadionTohhTohtatahbb_narrow_M-3500","RadionTohhTohtatahbb_narrow_M-4000"]



rootfile={}
radionResoMTT = {0:ROOT.TH1F(),1:ROOT.TH1F(),2:ROOT.TH1F(),3:ROOT.TH1F(),4:ROOT.TH1F(),5:ROOT.TH1F()}
radionResoWithMETMTT = {0:ROOT.TH1F(),1:ROOT.TH1F(),2:ROOT.TH1F(),3:ROOT.TH1F(),4:ROOT.TH1F(),5:ROOT.TH1F()}
for index, file in enumerate(listOfSignalFilesProcessing):
    #def setUpHistrogram(dict,index,Name,XTitle,YTitle,LineColor,ttree,branch,Nbins,min,max,LineWidth=2,LineStyle=1,Title='',HistName='',cond="",intHis="hist"):
    #    #ROOT.TH1F.AddDirectory(False);
    #    if HistName=='':
    #        ttree.Draw(branch+">>"+intHis+"("+str(Nbins)+","+str(min)+","+str(max)+")",cond)
    #        Name = ROOT.gDirectory.Get(intHis).Clone()
    #    else:
    #        Name = ROOT.TH1F(HistName,HistName,Nbins,min,max)
    #    Name.SetLineColor(LineColor)
    #    Name.SetLineWidth(LineWidth)
    #    Name.SetLineStyle(LineStyle)
    #    Name.SetTitle(Title)
    #    Name.GetXaxis().SetTitle(XTitle)
    #    Name.GetYaxis().SetTitle(YTitle)
    #    dict[index] = Name
    #    print ("Integral = ",Name.Integral())
    #    #return Name
    
    #print ("processing signal file = ",file)
    rootfile[index] = ROOT.TFile(args.inputFile+"/"+file+".root")
    theTree = rootfile[index].Get("Events")
    radionResoMTT[index]=setUpHistrogram(Name="RadionMassResoMTT{}".format(index),LineColor=linecolor[index+1],LineWidth=2,XTitle="Mass^{Reco}/Mass^{True}",YTitle="Events",ttree=theTree,branch="ResoGenRadion_mass",Nbins=60,min=0,max=2)
    print("after first draw ",radionResoMTT,radionResoWithMETMTT)
    radionResoWithMETMTT[index]=setUpHistrogram(Name="RadionMassWithMetResoMTT{}".format(index),LineColor=linecolor[index+1],LineWidth=2,LineStyle=2,XTitle="Mass^{Reco}/Mass^{True}",YTitle="Events",ttree=theTree,branch="ResoGenRadionWithMet_mass",Nbins=60,min=0,max=2)
    print("after second draw ",radionResoMTT,radionResoWithMETMTT)
    #print (type(RadionMassResoMTT),type(RadionMassWithMetResoMTT))
    #radionResoMTT[index]=RadionMassResoMTT.Clone()
    #radionResoWithMETMTT[index] = RadionMassWithMetResoMTT.Clone()
    #print (radionResoMTT,radionResoWithMETMTT)

print(radionResoMTT,radionResoWithMETMTT)
Reso = setUpCanvas("Reso")
maximum = max(radionResoMTT[0].GetMaximum(),radionResoMTT[1].GetMaximum(),radionResoMTT[2].GetMaximum(),radionResoMTT[3].GetMaximum(),radionResoMTT[4].GetMaximum(),radionResoMTT[5].GetMaximum())
radionResoMTT[0].SetMaximum(maximum + 0.30*maximum)

radionResoMTT[0].Draw("Hist E1")
radionResoMTT[1].Draw("same Hist E1")
radionResoMTT[2].Draw("same Hist E1")
radionResoMTT[3].Draw("same Hist E1")
radionResoMTT[4].Draw("same Hist E1")
radionResoMTT[5].Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(radionResoMTT[0],"1TeV","el")
legend.AddEntry(radionResoMTT[1],"2TeV","el")
legend.AddEntry(radionResoMTT[2],"2.5Tev","el")
legend.AddEntry(radionResoMTT[3],"3TeV","el")
legend.AddEntry(radionResoMTT[4],"3.5TeV","el")
legend.AddEntry(radionResoMTT[5],"4TeV","el")
legend.Draw("same")


cmsLatex=setUpCmsLatex(2016)
cmsLatex.Draw("same")
Reso.SaveAs("ResolutionForMP.png")

ResoMTT = setUpCanvas("ResoMTT")
maximum = max(radionResoWithMETMTT[0].GetMaximum(),radionResoWithMETMTT[1].GetMaximum(),radionResoWithMETMTT[2].GetMaximum(),radionResoWithMETMTT[3].GetMaximum(),radionResoWithMETMTT[4].GetMaximum(),radionResoWithMETMTT[5].GetMaximum())
radionResoWithMETMTT[0].SetMaximum(maximum + 0.30*maximum)

radionResoWithMETMTT[0].Draw("Hist E1")
radionResoWithMETMTT[1].Draw("same Hist E1")
radionResoWithMETMTT[2].Draw("same Hist E1")
radionResoWithMETMTT[3].Draw("same Hist E1")
radionResoWithMETMTT[4].Draw("same Hist E1")
radionResoWithMETMTT[5].Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(radionResoWithMETMTT[0],"1TeV","el")
legend.AddEntry(radionResoWithMETMTT[1],"2TeV","el")
legend.AddEntry(radionResoWithMETMTT[2],"2.5Tev","el")
legend.AddEntry(radionResoWithMETMTT[3],"3TeV","el")
legend.AddEntry(radionResoWithMETMTT[4],"3.5TeV","el")
legend.AddEntry(radionResoWithMETMTT[5],"4TeV","el")
legend.Draw("same")


cmsLatex=setUpCmsLatex(2016)
cmsLatex.Draw("same")
ResoMTT.SaveAs("ResolutionWithMETForMP.png")
