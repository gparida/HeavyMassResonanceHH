import ROOT
import glob
import argparse

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

from plotSettings import *


#Now we need to take inputs
parser = argparse.ArgumentParser(description='Script to plot trees directly from root files. Right now I am writing it for singal Files')
#parser.add_argument('--Channel',help="enter either tt or et or mt. For boostedTau test enter test",required=True,choices=['tt', 'et', 'mt'])
parser.add_argument('--inputFile',help="Full path to the signal file including the name")
#parser.add_argument('--outputLocation',help="enter the path where yu want the output files to be stored",default ="")
#parser.add_argument('--ncores',help ="number of cores for parallel processing", default=1)
#parser.add_argument('--postfix',help="string at the end of output file names", default="")
args = parser.parse_args()

#open the file
theFile = ROOT.TFile(args.inputFile) #opening the root file
 

 #Grab the Event tree as this is a nanoAOD file

theTree = theFile.Get("Events")
nEntries = theTree.GetEntries()



#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
RecoLeptondR_GenLepton_tt = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=840,min=-0.2,max=4,cond="channel==0")
RecoLeptondR_GenLepton_et = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=840,min=-0.2,max=4,cond="channel==1")
RecoLeptondR_GenLepton_mt = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=840,min=-0.2,max=4,cond="channel==2")
RecoLeptondR_GenLepton = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=840,min=-0.2,max=4,cond="")

RecoLeptondR_GenLepton_tt_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=840,min=-0.2,max=4,cond="channel==0 && gnboostedTau!=0")
RecoLeptondR_GenLepton_et_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=840,min=-0.2,max=4,cond="channel==1 && gnboostedTau!=0")
RecoLeptondR_GenLepton_mt_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=840,min=-0.2,max=4,cond="channel==2 && gnboostedTau!=0")
RecoLeptondR_GenLepton_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=840,min=-0.2,max=4,cond="gnboostedTau!=0")

RecoLeptondR_GenLepton_tt_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=840,min=-0.2,max=4,cond="channel==0 && gnTau!=0")
RecoLeptondR_GenLepton_et_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=840,min=-0.2,max=4,cond="channel==1 && gnTau!=0")
RecoLeptondR_GenLepton_mt_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=840,min=-0.2,max=4,cond="channel==2 && gnTau!=0")
RecoLeptondR_GenLepton_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=840,min=-0.2,max=4,cond="gnTau!=0")

#**************#
lep_lep_ChannelBased = setUpCanvas("lep_lep_ChannelBased")
lep_lep_ChannelBased.SetLogy()
maximum = max(RecoLeptondR_GenLepton_tt.GetMaximum(),RecoLeptondR_GenLepton_et.GetMaximum(),RecoLeptondR_GenLepton_mt.GetMaximum())
RecoLeptondR_GenLepton_tt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton_tt.Draw("Hist E1")
RecoLeptondR_GenLepton_et.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton_tt,"#tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et,"e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt,"m-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep_ChannelBased.SaveAs("lep_lep_ChannelBased.png")

#**************#
lep_lep_TauSplit = setUpCanvas("lep_lep_TauSplit")
lep_lep_TauSplit.SetLogy()
maximum = RecoLeptondR_GenLepton.GetMaximum()
RecoLeptondR_GenLepton.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton.Draw("Hist E1")
RecoLeptondR_GenLepton_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_hps.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.AddEntry(RecoLeptondR_GenLepton_b,"bt","el")
legend.AddEntry(RecoLeptondR_GenLepton_hps,"hps","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep_TauSplit.SaveAs("lep_lep_TauSplit.png")

#************#

lep_lep_tt_TauSplit = setUpCanvas("lep_lep_tt_TauSplit")
lep_lep_tt_TauSplit.SetLogy()
maximum = RecoLeptondR_GenLepton_tt.GetMaximum()
RecoLeptondR_GenLepton_tt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton_tt.Draw("Hist E1")
RecoLeptondR_GenLepton_tt_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_tt_hps.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton_tt,"all #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_tt_b,"bt #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_tt_hps,"hps #tau-#tau","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep_tt_TauSplit.SaveAs("lep_lep_tt_TauSplit.png")

#************#

lep_lep_et_TauSplit = setUpCanvas("lep_lep_et_TauSplit")
lep_lep_et_TauSplit.SetLogy()
maximum = RecoLeptondR_GenLepton_et.GetMaximum()
RecoLeptondR_GenLepton_et.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton_et.Draw("Hist E1")
RecoLeptondR_GenLepton_et_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_et_hps.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton_et,"all e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et_b,"bt e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et_hps,"hps e-#tau","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep_et_TauSplit.SaveAs("lep_lep_et_TauSplit.png")

#************#

lep_lep_mt_TauSplit = setUpCanvas("lep_lep_mt_TauSplit")
lep_lep_mt_TauSplit.SetLogy()
maximum = RecoLeptondR_GenLepton_mt.GetMaximum()
RecoLeptondR_GenLepton_mt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton_mt.Draw("Hist E1")
RecoLeptondR_GenLepton_mt_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt_hps.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton_mt,"all m-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt_b,"bt m-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt_hps,"hps m-#tau","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep_mt_TauSplit.SaveAs("lep_lep_mt_TauSplit.png")


#SAME AS BEFORE BUT ZOOOMED INNNNNNNNNNN

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
RecoLeptondR_GenLepton_tt = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=700,min=-0.2,max=0.5,cond="channel==0")
RecoLeptondR_GenLepton_et = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=700,min=-0.2,max=0.5,cond="channel==1")
RecoLeptondR_GenLepton_mt = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=700,min=-0.2,max=0.5,cond="channel==2")
RecoLeptondR_GenLepton = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=700,min=-0.2,max=0.5,cond="")

RecoLeptondR_GenLepton_tt_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=700,min=-0.2,max=0.5,cond="channel==0 && gnboostedTau!=0")
RecoLeptondR_GenLepton_et_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=700,min=-0.2,max=0.5,cond="channel==1 && gnboostedTau!=0")
RecoLeptondR_GenLepton_mt_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=700,min=-0.2,max=0.5,cond="channel==2 && gnboostedTau!=0")
RecoLeptondR_GenLepton_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=700,min=-0.2,max=0.5,cond="gnboostedTau!=0")

RecoLeptondR_GenLepton_tt_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=700,min=-0.2,max=0.5,cond="channel==0 && gnTau!=0")
RecoLeptondR_GenLepton_et_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=700,min=-0.2,max=0.5,cond="channel==1 && gnTau!=0")
RecoLeptondR_GenLepton_mt_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=700,min=-0.2,max=0.5,cond="channel==2 && gnTau!=0")
RecoLeptondR_GenLepton_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=700,min=-0.2,max=0.5,cond="gnTau!=0")

#**************#
lep_lep_ZOOM_ChannelBased = setUpCanvas("lep_lep_ZOOM_ChannelBased")
lep_lep_ZOOM_ChannelBased.SetLogy()
maximum = max(RecoLeptondR_GenLepton_tt.GetMaximum(),RecoLeptondR_GenLepton_et.GetMaximum(),RecoLeptondR_GenLepton_mt.GetMaximum())
RecoLeptondR_GenLepton_tt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton_tt.Draw("Hist E1")
RecoLeptondR_GenLepton_et.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton_tt,"#tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et,"e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt,"m-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep_ZOOM_ChannelBased.SaveAs("lep_lep_ZOOM_ChannelBased.png")

#**************#
lep_lep_ZOOM_TauSplit = setUpCanvas("lep_lep_ZOOM_TauSplit")
lep_lep_ZOOM_TauSplit.SetLogy()
maximum = RecoLeptondR_GenLepton.GetMaximum()
RecoLeptondR_GenLepton.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton.Draw("Hist E1")
RecoLeptondR_GenLepton_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_hps.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.AddEntry(RecoLeptondR_GenLepton_b,"bt","el")
legend.AddEntry(RecoLeptondR_GenLepton_hps,"hps","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep_ZOOM_TauSplit.SaveAs("lep_lep_ZOOM_TauSplit.png")

#************#

lep_lep_tt_ZOOM_TauSplit = setUpCanvas("lep_lep_tt_ZOOM_TauSplit")
lep_lep_tt_ZOOM_TauSplit.SetLogy()
maximum = RecoLeptondR_GenLepton_tt.GetMaximum()
RecoLeptondR_GenLepton_tt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton_tt.Draw("Hist E1")
RecoLeptondR_GenLepton_tt_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_tt_hps.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton_tt,"all #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_tt_b,"bt #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_tt_hps,"hps #tau-#tau","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep_tt_ZOOM_TauSplit.SaveAs("lep_lep_tt_ZOOM_TauSplit.png")

#************#

lep_lep_et_ZOOM_TauSplit = setUpCanvas("lep_lep_et_ZOOM_TauSplit")
lep_lep_et_ZOOM_TauSplit.SetLogy()
maximum = RecoLeptondR_GenLepton_et.GetMaximum()
RecoLeptondR_GenLepton_et.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton_et.Draw("Hist E1")
RecoLeptondR_GenLepton_et_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_et_hps.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton_et,"all e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et_b,"bt e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et_hps,"hps e-#tau","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep_et_ZOOM_TauSplit.SaveAs("lep_lep_et_ZOOM_TauSplit.png")

#************#

lep_lep_mt_ZOOM_TauSplit = setUpCanvas("lep_lep_mt_ZOOM_TauSplit")
lep_lep_mt_ZOOM_TauSplit.SetLogy()
maximum = RecoLeptondR_GenLepton_mt.GetMaximum()
RecoLeptondR_GenLepton_mt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton_mt.Draw("Hist E1")
RecoLeptondR_GenLepton_mt_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt_hps.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton_mt,"all m-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt_b,"bt m-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt_hps,"hps m-#tau","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep_mt_ZOOM_TauSplit.SaveAs("lep_lep_mt_ZOOM_TauSplit.png")

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#Plotting the Reco Leptons dR with genLeptons for the three channels and the combined
RecoLeptondR_GenQuark_tt = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=1,LineWidth=1,XTitle="LepdR_genQuark",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==0")
RecoLeptondR_GenQuark_et = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=2,LineWidth=1,XTitle="LepdR_genQuark",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==1")
RecoLeptondR_GenQuark_mt = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=3,LineWidth=1,XTitle="LepdR_genQuark",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==2")
RecoLeptondR_GenQuark = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=4,LineWidth=1,XTitle="LepdR_genQuark",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="")

RecoLeptondR_GenQuark_tt_b = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=1,LineWidth=1,LineStyle=2,XTitle="LepdR_genQuark",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==0 && gnboostedTau!=0")
RecoLeptondR_GenQuark_et_b = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=2,LineWidth=1,LineStyle=2,XTitle="LepdR_genQuark",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==1 && gnboostedTau!=0")
RecoLeptondR_GenQuark_mt_b = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=3,LineWidth=1,LineStyle=2,XTitle="LepdR_genQuark",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==2 && gnboostedTau!=0")
RecoLeptondR_GenQuark_b = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=4,LineWidth=1,LineStyle=2,XTitle="LepdR_genQuark",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="gnboostedTau!=0")

RecoLeptondR_GenQuark_tt_hps = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=1,LineWidth=1,LineStyle=3,XTitle="LepdR_genQuark",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==0 && gnTau!=0")
RecoLeptondR_GenQuark_et_hps = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=2,LineWidth=1,LineStyle=3,XTitle="LepdR_genQuark",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==1 && gnTau!=0")
RecoLeptondR_GenQuark_mt_hps = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=3,LineWidth=1,LineStyle=3,XTitle="LepdR_genQuark",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==2 && gnTau!=0")
RecoLeptondR_GenQuark_hps = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=4,LineWidth=1,LineStyle=3,XTitle="LepdR_genQuark",YTitle="Number of leptons",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="gnTau!=0")

#**************#
lep_jet_ChannelBased = setUpCanvas("lep_jet_ChannelBased")
maximum = max(RecoLeptondR_GenQuark_tt.GetMaximum(),RecoLeptondR_GenQuark_et.GetMaximum(),RecoLeptondR_GenQuark_mt.GetMaximum())
RecoLeptondR_GenQuark_tt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenQuark_tt.Draw("Hist E1")
RecoLeptondR_GenQuark_et.Draw("same Hist E1")
RecoLeptondR_GenQuark_mt.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenQuark_tt,"#tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_et,"e-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_mt,"m-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_jet_ChannelBased.SaveAs("lep_jet_ChannelBased.png")

#**************#
lep_jet_TauSplit = setUpCanvas("lep_jet_TauSplit")
maximum = RecoLeptondR_GenQuark.GetMaximum()
RecoLeptondR_GenQuark.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenQuark.Draw("Hist E1")
RecoLeptondR_GenQuark_b.Draw("same Hist E1")
RecoLeptondR_GenQuark_hps.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenQuark,"all","el")
legend.AddEntry(RecoLeptondR_GenQuark_b,"bt","el")
legend.AddEntry(RecoLeptondR_GenQuark_hps,"hps","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_jet_TauSplit.SaveAs("lep_jet_TauSplit.png")

#**************#
lep_jet_tt_TauSplit = setUpCanvas("lep_jet_tt_TauSplit")
maximum = RecoLeptondR_GenQuark_tt.GetMaximum()
RecoLeptondR_GenQuark_tt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenQuark_tt.Draw("Hist E1")
RecoLeptondR_GenQuark_tt_b.Draw("same Hist E1")
RecoLeptondR_GenQuark_tt_hps.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenQuark_tt,"all #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_tt_b,"bt #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_tt_hps,"hps #tau-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_jet_tt_TauSplit.SaveAs("lep_jet_tt_TauSplit.png")

#**************#
lep_jet_et_TauSplit = setUpCanvas("lep_jet_et_TauSplit")
maximum = RecoLeptondR_GenQuark_et.GetMaximum()
RecoLeptondR_GenQuark_et.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenQuark_et.Draw("Hist E1")
RecoLeptondR_GenQuark_et_b.Draw("same Hist E1")
RecoLeptondR_GenQuark_et_hps.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenQuark_et,"all e-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_et_b,"bt e-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_et_hps,"hps e-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_jet_et_TauSplit.SaveAs("lep_jet_et_TauSplit.png")

#**************#
lep_jet_mt_TauSplit = setUpCanvas("lep_jet_mt_TauSplit")
maximum = RecoLeptondR_GenQuark_mt.GetMaximum()
RecoLeptondR_GenQuark_mt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenQuark_mt.Draw("Hist E1")
RecoLeptondR_GenQuark_mt_b.Draw("same Hist E1")
RecoLeptondR_GenQuark_mt_hps.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenQuark_mt,"all m-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_mt_b,"bt m-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_mt_hps,"hps m-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_jet_mt_TauSplit.SaveAs("lep_jet_mt_TauSplit.png")


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#Plotting the Reco FatJet dR with bQuarks pair for the three channels and the combined

FatJetdR_GenCombinedQuark_tt = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=1,LineWidth=1,XTitle="FatJetdR_genQpair",YTitle="Number of FatJets",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=420,min=-0.2,max=4,cond="channel==0")
FatJetdR_GenCombinedQuark_et = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=2,LineWidth=1,XTitle="FatJetdR_genQpair",YTitle="Number of FatJets",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=420,min=-0.2,max=4,cond="channel==1")
FatJetdR_GenCombinedQuark_mt = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=3,LineWidth=1,XTitle="FatJetdR_genQpair",YTitle="Number of FatJets",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=420,min=-0.2,max=4,cond="channel==2")
FatJetdR_GenCombinedQuark = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=4,LineWidth=1,XTitle="FatJetdR_genQpair",YTitle="Number of FatJets",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=420,min=-0.2,max=4,cond="")

FatJetdR_GenCombinedQuark_tt_b = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=1,LineWidth=1,LineStyle=2,XTitle="FatJetdR_genQpair",YTitle="Number of FatJets",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=420,min=-0.2,max=4,cond="channel==0 && gnboostedTau!=0")
FatJetdR_GenCombinedQuark_et_b = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=2,LineWidth=1,LineStyle=2,XTitle="FatJetdR_genQpair",YTitle="Number of FatJets",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=420,min=-0.2,max=4,cond="channel==1 && gnboostedTau!=0")
FatJetdR_GenCombinedQuark_mt_b = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=3,LineWidth=1,LineStyle=2,XTitle="FatJetdR_genQpair",YTitle="Number of FatJets",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=420,min=-0.2,max=4,cond="channel==2 && gnboostedTau!=0")
FatJetdR_GenCombinedQuark_b = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=4,LineWidth=1,LineStyle=2,XTitle="FatJetdR_genQpair",YTitle="Number of FatJets",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=420,min=-0.2,max=4,cond="gnboostedTau!=0")

FatJetdR_GenCombinedQuark_tt_hps = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=1,LineWidth=1,LineStyle=3,XTitle="FatJetdR_genQpair",YTitle="Number of FatJets",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=420,min=-0.2,max=4,cond="channel==0 && gnTau!=0")
FatJetdR_GenCombinedQuark_et_hps = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=2,LineWidth=1,LineStyle=3,XTitle="FatJetdR_genQpair",YTitle="Number of FatJets",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=420,min=-0.2,max=4,cond="channel==1 && gnTau!=0")
FatJetdR_GenCombinedQuark_mt_hps = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=3,LineWidth=1,LineStyle=3,XTitle="FatJetdR_genQpair",YTitle="Number of FatJets",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=420,min=-0.2,max=4,cond="channel==2 && gnTau!=0")
FatJetdR_GenCombinedQuark_hps = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=4,LineWidth=1,LineStyle=3,XTitle="FatJetdR_genQpair",YTitle="Number of FatJets",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=420,min=-0.2,max=4,cond="gnTau!=0")

#**************#
jet_jet_ChannelBased = setUpCanvas("jet_jet_ChannelBased")
jet_jet_ChannelBased.SetLogy()
maximum = max(FatJetdR_GenCombinedQuark_tt.GetMaximum(),FatJetdR_GenCombinedQuark_et.GetMaximum(),FatJetdR_GenCombinedQuark_mt.GetMaximum())
FatJetdR_GenCombinedQuark_tt.SetMaximum(maximum + 0.30*maximum)

FatJetdR_GenCombinedQuark_tt.Draw("Hist E1")
FatJetdR_GenCombinedQuark_et.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_mt.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(FatJetdR_GenCombinedQuark_tt,"#tau-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_et,"e-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_mt,"m-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
jet_jet_ChannelBased.SaveAs("jet_jet_ChannelBased.png")

#**************#
jet_jet_TauSplit = setUpCanvas("jet_jet_TauSplit")
jet_jet_TauSplit.SetLogy()
maximum = FatJetdR_GenCombinedQuark.GetMaximum()
FatJetdR_GenCombinedQuark.SetMaximum(maximum + 0.30*maximum)

FatJetdR_GenCombinedQuark.Draw("Hist E1")
FatJetdR_GenCombinedQuark_et.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_mt.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(FatJetdR_GenCombinedQuark,"all","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_et,"bt","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_mt,"hps","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
jet_jet_TauSplit.SaveAs("jet_jet_TauSplit.png")

#**************#
jet_jet_tt_TauSplit = setUpCanvas("jet_jet_tt_TauSplit")
jet_jet_tt_TauSplit.SetLogy()
maximum = FatJetdR_GenCombinedQuark_tt.GetMaximum()
FatJetdR_GenCombinedQuark_tt.SetMaximum(maximum + 0.30*maximum)

FatJetdR_GenCombinedQuark_tt.Draw("Hist E1")
FatJetdR_GenCombinedQuark_tt_b.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_tt_hps.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(FatJetdR_GenCombinedQuark_tt,"all #tau-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_tt_b,"bt #tau-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_tt_hps,"hps #tau-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
jet_jet_tt_TauSplit.SaveAs("jet_jet_tt_TauSplit.png")

#**************#
jet_jet_et_TauSplit = setUpCanvas("jet_jet_et_TauSplit")
jet_jet_et_TauSplit.SetLogy()
maximum = FatJetdR_GenCombinedQuark_et.GetMaximum()
FatJetdR_GenCombinedQuark_et.SetMaximum(maximum + 0.30*maximum)

FatJetdR_GenCombinedQuark_et.Draw("Hist E1")
FatJetdR_GenCombinedQuark_et_b.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_et_hps.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(FatJetdR_GenCombinedQuark_et,"all e-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_et_b,"bt e-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_et_hps,"hps e-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
jet_jet_et_TauSplit.SaveAs("jet_jet_et_TauSplit.png")


#**************#
jet_jet_mt_TauSplit = setUpCanvas("jet_jet_mt_TauSplit")
jet_jet_mt_TauSplit.SetLogy()
maximum = FatJetdR_GenCombinedQuark_mt.GetMaximum()
FatJetdR_GenCombinedQuark_mt.SetMaximum(maximum + 0.30*maximum)

FatJetdR_GenCombinedQuark_mt.Draw("Hist E1")
FatJetdR_GenCombinedQuark_mt_b.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_mt_hps.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(FatJetdR_GenCombinedQuark_mt,"all m-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_mt_b,"bt m-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_mt_hps,"hps m-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
jet_jet_mt_TauSplit.SaveAs("jet_jet_mt_TauSplit.png")


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#Plotting the match type for all channels and combined 
RecoLepton_match_type_tt = setUpHistrogram(Name="RecoLepton_match_type",LineColor=1,LineWidth=1,XTitle="RecoLepton_match_type",YTitle="Number of Leptons",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==0")
RecoLepton_match_type_et = setUpHistrogram(Name="RecoLepton_match_type",LineColor=2,LineWidth=1,XTitle="RecoLepton_match_type",YTitle="Number of Leptons",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==1")
RecoLepton_match_type_mt = setUpHistrogram(Name="RecoLepton_match_type",LineColor=3,LineWidth=1,XTitle="RecoLepton_match_type",YTitle="Number of Leptons",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==2")
RecoLepton_match_type = setUpHistrogram(Name="RecoLepton_match_type",LineColor=4,LineWidth=1,XTitle="RecoLepton_match_type",YTitle="Number of Leptons",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="")

RecoLepton_match_type_tt_b = setUpHistrogram(Name="RecoLepton_match_type",LineColor=1,LineWidth=1,LineStyle=2,XTitle="RecoLepton_match_type",YTitle="Number of Leptons",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==0 && gnboostedTau!=0")
RecoLepton_match_type_et_b = setUpHistrogram(Name="RecoLepton_match_type",LineColor=2,LineWidth=1,LineStyle=2,XTitle="RecoLepton_match_type",YTitle="Number of Leptons",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==1 && gnboostedTau!=0")
RecoLepton_match_type_mt_b = setUpHistrogram(Name="RecoLepton_match_type",LineColor=3,LineWidth=1,LineStyle=2,XTitle="RecoLepton_match_type",YTitle="Number of Leptons",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==2 && gnboostedTau!=0")
RecoLepton_match_type_b = setUpHistrogram(Name="RecoLepton_match_type",LineColor=4,LineWidth=1,LineStyle=2,XTitle="RecoLepton_match_type",YTitle="Number of Leptons",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="gnboostedTau!=0")

RecoLepton_match_type_tt_hps = setUpHistrogram(Name="RecoLepton_match_type",LineColor=1,LineWidth=1,LineStyle=3,XTitle="RecoLepton_match_type",YTitle="Number of Leptons",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==0 && gnTau!=0")
RecoLepton_match_type_et_hps = setUpHistrogram(Name="RecoLepton_match_type",LineColor=2,LineWidth=1,LineStyle=3,XTitle="RecoLepton_match_type",YTitle="Number of Leptons",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==1 && gnTau!=0")
RecoLepton_match_type_mt_hps = setUpHistrogram(Name="RecoLepton_match_type",LineColor=3,LineWidth=1,LineStyle=3,XTitle="RecoLepton_match_type",YTitle="Number of Leptons",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==2 && gnTau!=0")
RecoLepton_match_type_hps = setUpHistrogram(Name="RecoLepton_match_type",LineColor=4,LineWidth=1,LineStyle=3,XTitle="RecoLepton_match_type",YTitle="Number of Leptons",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="gnTau!=0")

#**************#
matchtype_ChannelBased = setUpCanvas("matchtype_ChannelBased")
maximum = max(RecoLepton_match_type_tt.GetMaximum(),RecoLepton_match_type_et.GetMaximum(),RecoLepton_match_type_mt.GetMaximum())
RecoLepton_match_type_tt.SetMaximum(maximum + 0.30*maximum)

RecoLepton_match_type_tt.Draw("Hist E1")
RecoLepton_match_type_et.Draw("same Hist E1")
RecoLepton_match_type_mt.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(RecoLepton_match_type_tt,"#tau-#tau","el")
legend.AddEntry(RecoLepton_match_type_et,"e-#tau","el")
legend.AddEntry(RecoLepton_match_type_mt,"m-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
matchtype_ChannelBased.SaveAs("matchtype_ChannelBased.png")

#**************#
matchtype_TauSplit = setUpCanvas("matchtype_TauSplit")
maximum = RecoLepton_match_type.GetMaximum()
RecoLepton_match_type.SetMaximum(maximum + 0.30*maximum)

RecoLepton_match_type.Draw("Hist E1")
RecoLepton_match_type_et.Draw("same Hist E1")
RecoLepton_match_type_mt.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(RecoLepton_match_type,"all","el")
legend.AddEntry(RecoLepton_match_type_et,"bt","el")
legend.AddEntry(RecoLepton_match_type_mt,"hps","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
matchtype_TauSplit.SaveAs("matchtype_TauSplit.png")

#**************#
matchtype_tt_TauSplit = setUpCanvas("matchtype_tt_TauSplit")
maximum = RecoLepton_match_type_tt.GetMaximum()
RecoLepton_match_type_tt.SetMaximum(maximum + 0.30*maximum)

RecoLepton_match_type_tt.Draw("Hist E1")
RecoLepton_match_type_tt_b.Draw("same Hist E1")
RecoLepton_match_type_tt_hps.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(RecoLepton_match_type_tt,"all #tau-#tau","el")
legend.AddEntry(RecoLepton_match_type_tt_b,"bt #tau-#tau","el")
legend.AddEntry(RecoLepton_match_type_tt_hps,"hps #tau-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
matchtype_tt_TauSplit.SaveAs("matchtype_tt_TauSplit.png")

#**************#
matchtype_et_TauSplit = setUpCanvas("matchtype_et_TauSplit")
maximum = RecoLepton_match_type_et.GetMaximum()
RecoLepton_match_type_et.SetMaximum(maximum + 0.30*maximum)

RecoLepton_match_type_et.Draw("Hist E1")
RecoLepton_match_type_et_b.Draw("same Hist E1")
RecoLepton_match_type_et_hps.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(RecoLepton_match_type_et,"all e-#tau","el")
legend.AddEntry(RecoLepton_match_type_et_b,"bt e-#tau","el")
legend.AddEntry(RecoLepton_match_type_et_hps,"hps e-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
matchtype_et_TauSplit.SaveAs("matchtype_et_TauSplit.png")


#**************#
matchtype_mt_TauSplit = setUpCanvas("matchtype_mt_TauSplit")
maximum = RecoLepton_match_type_mt.GetMaximum()
RecoLepton_match_type_mt.SetMaximum(maximum + 0.30*maximum)

RecoLepton_match_type_mt.Draw("Hist E1")
RecoLepton_match_type_mt_b.Draw("same Hist E1")
RecoLepton_match_type_mt_hps.Draw("same Hist E1")

#RecoLeptondR_GenLepton.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(RecoLepton_match_type_mt,"all m-#tau","el")
legend.AddEntry(RecoLepton_match_type_mt_b,"bt m-#tau","el")
legend.AddEntry(RecoLepton_match_type_mt_hps,"hps m-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
matchtype_mt_TauSplit.SaveAs("matchtype_mt_TauSplit.png")


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#Plotting the gen Channel distribution#############################################
genchannel = setUpHistrogram(Name="genchannel",LineColor=1,LineWidth=1,XTitle="genchannel",YTitle="Events",ttree=theTree,branch="genchannel",Nbins=7,min=-2,max=5,cond="")
genchannel_b = setUpHistrogram(Name="genchannel",LineColor=1,LineWidth=1,LineStyle=2,XTitle="genchannel",YTitle="Events",ttree=theTree,branch="genchannel",Nbins=7,min=-2,max=5,cond="gnboostedTau!=0")
genchannel_hps = setUpHistrogram(Name="genchannel",LineColor=1,LineWidth=1,LineStyle=3,XTitle="genchannel",YTitle="Events",ttree=theTree,branch="genchannel",Nbins=7,min=-2,max=5,cond="gnTau!=0")

generatorChannel = setUpCanvas("generatorChannel")
maximum = genchannel.GetMaximum()
genchannel.SetMaximum(maximum + 0.30*maximum)


genchannel.Draw("Hist E1")
genchannel_b.Draw("same Hist E1 ")
genchannel_hps.Draw("same Hist E1")

legend.AddEntry(genchannel,"allTaus","el")
legend.AddEntry(genchannel_b,"boosted Taus","el")
legend.AddEntry(genchannel_hps,"hps Taus","el")
legend.Draw("same")


cmsLatex = setUpCmsLatex(2016)
generatorChannel.SaveAs("generatorChannel.png")

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#Plotting the gen Channel distribution
channel = setUpHistrogram(Name="channel",LineColor=1,LineWidth=1,XTitle="channel",YTitle="Events",ttree=theTree,branch="channel",Nbins=5,min=-1,max=4,cond="")
channel_b = setUpHistrogram(Name="channel",LineColor=1,LineWidth=1,LineStyle=2,XTitle="channel",YTitle="Events",ttree=theTree,branch="channel",Nbins=5,min=-1,max=4,cond="gnboostedTau!=0")
channel_hps = setUpHistrogram(Name="channel",LineColor=1,LineWidth=1,LineStyle=3,XTitle="channel",YTitle="Events",ttree=theTree,branch="channel",Nbins=5,min=-1,max=4,cond="gnTau!=0")

recoChannel = setUpCanvas("recoChannel")
maximum = channel.GetMaximum()
channel.SetMaximum(maximum + 0.30*maximum)

channel.Draw("Hist E1")
channel_b.Draw("same Hist E1")
channel_hps.Draw("same Hist E1")

legend.AddEntry(channel,"allTaus","el")
legend.AddEntry(channel_b,"boosted Taus","el")
legend.AddEntry(channel_hps,"hps Taus","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
recoChannel.SaveAs("recoChannel.png")



CB_Loose_Barrel = setUpHistrogram(Name="CB_Loose",LineColor=1,LineWidth=1,XTitle="LooseCBElectron_pfRelIso03_all",YTitle="Number of Electrons",ttree=theTree,branch="LooseCBElectron_pfRelIso03_all",Nbins=100,min=0,max=1.5,cond="LooseCBElectron_eta <= 1.479 || LooseCBElectron_eta >= -1.479 ")
CB_RemIso_Barrel = setUpHistrogram(Name="CB_RemIso",LineColor=2,LineWidth=1,LineStyle=2,XTitle="IsoRemElectron_pfRelIso03_all",YTitle="Number of Electrons",ttree=theTree,branch="IsoRemElectron_pfRelIso03_all",Nbins=100,min=0,max=1.5,cond="IsoRemElectron_eta <= 1.479 || IsoRemElectron_eta >= -1.479 ")

CB_Loose_EC = setUpHistrogram(Name="CB_Loose",LineColor=1,LineWidth=1,XTitle="LooseCBElectron_pfRelIso03_all",YTitle="Number of Electrons",ttree=theTree,branch="LooseCBElectron_pfRelIso03_all",Nbins=100,min=0,max=1.5,cond="LooseCBElectron_eta > 1.479 || LooseCBElectron_eta < -1.479 ")
CB_RemIso_EC = setUpHistrogram(Name="CB_RemIso",LineColor=2,LineWidth=1,LineStyle=2,XTitle="IsoRemElectron_pfRelIso03_all",YTitle="Number of Electrons",ttree=theTree,branch="IsoRemElectron_pfRelIso03_all",Nbins=100,min=0,max=1.5,cond="IsoRemElectron_eta > 1.479 || IsoRemElectron_eta < -1.479 ")

Electron_Barrel = setUpCanvas("Electron_Barrel")
Electron_Barrel.SetLogy()
maximum = max(CB_Loose_Barrel.GetMaximum(),CB_RemIso_Barrel.GetMaximum())
CB_Loose_Barrel.SetMaximum(maximum + 0.30*maximum)

CB_Loose_Barrel.Draw("Hist E1")
CB_RemIso_Barrel.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(CB_Loose_Barrel,"Loose","el")
legend.AddEntry(CB_RemIso_Barrel,"WO Iso","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
Electron_Barrel.SaveAs("Barrel_Electron.png")

Electron_Barrel_ratio = setUpCanvas("Electron_Barrel_ratio")
CB_Loose_Barrel_Num = CB_Loose_Barrel.Clone()
CB_Loose_Barrel_Den = CB_RemIso_Barrel.Clone()
CB_Loose_Barrel_Num.Divide(CB_Loose_Barrel_Den)
CB_Loose_Barrel_Num.SetMaximum(1 + 0.30*1)
CB_Loose_Barrel_Num.Draw("hist")
legend = setUpLegend()
legend.AddEntry(CB_Loose_Barrel_Num,"Ratio","el")
legend.Draw("same")
cmsLatex = setUpCmsLatex(2016)
Electron_Barrel_ratio.SaveAs("Barrel_Electron_Ratio.png")



Electron_EC = setUpCanvas("Electron_EC")
Electron_EC.SetLogy()
maximum = max(CB_Loose_EC.GetMaximum(),CB_RemIso_EC.GetMaximum())
CB_Loose_EC.SetMaximum(maximum + 0.30*maximum)

CB_Loose_EC.Draw("Hist E1")
CB_RemIso_EC.Draw("same Hist E1")
legend = setUpLegend()
legend.AddEntry(CB_Loose_EC,"Loose","el")
legend.AddEntry(CB_RemIso_EC,"WO Iso","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
Electron_EC.SaveAs("EC_Electron.png")








