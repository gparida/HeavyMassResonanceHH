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

#Now we Just directly plot the branches in the ttree
#First doing it for Higgs..................................

#Higgs mass

#HiggsMassResoMTT= setUpHistrogram(Name="HiggsMassResoMTT",LineColor=1,LineWidth=2,XTitle="Higgs Mass^{Reco}/Higgs Mass^{True}",YTitle="Events",ttree=theTree,branch="ResoGenHiggs_mass",Nbins=40,min=0,max=2)
#HiggsMassResoVis= setUpHistrogram(Name="HiggsMassResoVis",LineColor=4,LineWidth=2,XTitle="Higgs Mass^{Reco}/Higgs Mass^{True}",YTitle="Events",ttree=theTree,branch="ResoVisHiggs_mass",Nbins=40,min=0,max=2)
#
#HiggsMass = setUpCanvas("HiggsMass")
#HiggsMassResoMTT.SetMaximum(max(HiggsMassResoMTT.GetMaximum(),HiggsMassResoVis.GetMaximum())+50)
##HiggsMassResoMTT.Draw("C")
##HiggsMassResoVis.Draw("C same")
#HiggsMassResoMTT.Draw("Hist E1")
#HiggsMassResoVis.Draw("same Hist E1")
#
#
#legend = setUpLegend()
#legend.AddEntry(HiggsMassResoMTT,"FastMTT","ep")
#legend.AddEntry(HiggsMassResoVis,"Visible","ep")
#legend.Draw("same")
#
#cmsLatex = setUpCmsLatex(2016)
#
#HiggsMass.SaveAs("HiggsM_Reso.png")
#
#
#
##Higgs pt
#HiggsptResoMTT= setUpHistrogram(Name="HiggsptResoMTT",LineColor=1,LineWidth=2,XTitle="Higgs Pt^{Reco}/Higgs Pt^{True}",YTitle="Events",ttree=theTree,branch="ResoGenHiggs_pt",Nbins=40,min=0,max=2)
#HiggsptResoVis= setUpHistrogram(Name="HiggsptResoVis",LineColor=4,LineWidth=2,XTitle="Higgs Pt^{Reco}/Higgs Pt^{True}",YTitle="Events",ttree=theTree,branch="ResoVisHiggs_pt",Nbins=40,min=0,max=2)
#
#
#HiggsPt = setUpCanvas("HiggsPt")
#HiggsptResoMTT.SetMaximum(max(HiggsMassResoMTT.GetMaximum(),HiggsMassResoVis.GetMaximum())+50)
##HiggsptResoMTT.Draw("C")
##HiggsptResoVis.Draw("C same")
#HiggsptResoMTT.Draw("Hist E1")
#HiggsptResoVis.Draw("same Hist E1")
#
#legend = setUpLegend()
#legend.AddEntry(HiggsptResoMTT,"FastMTT","ep")
#legend.AddEntry(HiggsptResoVis,"Visible","ep")
#legend.Draw("same")
#
#cmsLatex = setUpCmsLatex(2016)
#HiggsPt.SaveAs("HiggsPt_Reso.png")
#
##Next we do it for Radion
#
##Radion Mass##
#RadionMassResoMTT= setUpHistrogram(Name="RadionMassResoMTT",LineColor=1,LineWidth=2,XTitle="Mass^{Reco}/Mass^{True}",YTitle="Events",ttree=theTree,branch="ResoGenRadion_mass",Nbins=40,min=0,max=2)
#RadionMassWithMetResoMTT= setUpHistrogram(Name="RadionMassWithMetResoMTT",LineColor=2,LineWidth=2,XTitle="Mass^{Reco}/Mass^{True}",YTitle="Events",ttree=theTree,branch="ResoGenRadionWithMet_mass",Nbins=40,min=0,max=2)
#RadionMassVisReso = setUpHistrogram(Name="RadionMassVisReso",LineColor=4,LineWidth=2,XTitle="Mass^{Reco}/Mass^{True}",YTitle="Events",ttree=theTree,branch="ResoVisRadion_mass",Nbins=40,min=0,max=2)
#
#RadionMass = setUpCanvas("RadionMass")
#HiggsMassResoMTT.SetMaximum(max(RadionMassResoMTT.GetMaximum(),RadionMassWithMetResoMTT.GetMaximum(),RadionMassVisReso.GetMaximum())+50)
##RadionMassResoMTT.Draw("C")
##RadionMassWithMetResoMTT.Draw("C same")
##RadionMassVisReso.Draw("C same")
##RadionMassResoMTT.Draw("Hist E1")
#RadionMassWithMetResoMTT.Draw("same Hist E1")
#RadionMassVisReso.Draw("same Hist E1")
#
#
#legend = setUpLegend()
#legend.AddEntry(RadionMassResoMTT,"FastMTT","ep")
#legend.AddEntry(RadionMassWithMetResoMTT,"FastMTT + MET","ep")
#legend.AddEntry(RadionMassVisReso,"Visible","ep")
#legend.Draw("same")
#
#
#cmsLatex = setUpCmsLatex(2016)
#RadionMass.SaveAs("RadionM_Reso.png")
#
##Radion Momemtum##
#RadionptResoMTT= setUpHistrogram(Name="RadionptResoMTT",LineColor=1,LineWidth=2,XTitle="Pt^{Reco}/Pt^{True}",YTitle="Events",ttree=theTree,branch="ResoGenRadion_pt",Nbins=30,min=0,max=2)
#RadionptWithMetResoMTT= setUpHistrogram(Name="RadionptWithMetResoMTT",LineColor=2,LineWidth=2,XTitle="Pt^{Reco}/Pt^{True}",YTitle="Events",ttree=theTree,branch="ResoGenRadionWithMet_pt",Nbins=30,min=0,max=2)
#RadionptVisReso = setUpHistrogram(Name="RadionptVisReso",LineColor=4,LineWidth=2,XTitle="Pt^{Reco}/Pt^{True}",YTitle="Events",ttree=theTree,branch="ResoVisRadion_pt",Nbins=30,min=0,max=2)
#
#Radionpt = setUpCanvas("Radionpt")
#RadionptResoMTT.SetMaximum(max(RadionptResoMTT.GetMaximum(),RadionptWithMetResoMTT.GetMaximum(),RadionptVisReso.GetMaximum())+50)
##RadionptResoMTT.Draw("Hist E1")
#RadionptWithMetResoMTT.Draw("same Hist E1")
#RadionptVisReso.Draw("same Hist E1")
#
#
#
#legend = setUpLegend()
##legend.AddEntry(RadionptResoMTT,"FastMTT","ep")
#legend.AddEntry(RadionptWithMetResoMTT,"FastMTT + MET","ep")
#legend.AddEntry(RadionptVisReso,"Visible","ep")
#legend.Draw("same")
#
#
#cmsLatex = setUpCmsLatex(2016)
#Radionpt.SaveAs("RadionPt_Reso.png")
#
#
##Plotting Higgs Mass
#HiggsMassbb = setUpHistrogram(Name="HiggsMassbb",LineColor=1,LineWidth=2,XTitle="Softdrop Mass^{Reco}/Higgs Mass^{True}",YTitle="Events",ttree=theTree,branch="(gFatJet_msoftdrop/125)",Nbins=40,min=0,max=2,cond="(FatJet_particleNetMD_Xbb/(FatJet_particleNetMD_Xbb+FatJet_particleNetMD_QCD))>0.87")
#
#HiggsbbMass = setUpCanvas("Soft Drop Mass")
#HiggsMassbb.SetMaximum(HiggsMassbb.GetMaximum()+50)
#HiggsMassbb.Draw("Hist E1")
#
#legend = setUpLegend()
#legend.AddEntry(HiggsMassbb,"SoftDrop Mass","el")
#legend.Draw("same")
#
#cmsLatex = setUpCmsLatex(2016)
#HiggsbbMass.SaveAs("HMass_bb.png")
#

#plotting for Muon Isolation New and Old

#Muon_IsoNew= setUpHistrogram(Name="NewIso",LineColor=1,LineWidth=1,XTitle="Corrected_RelIso",YTitle="Events",ttree=theTree,branch="Muon_TauCorrPfIso/Muon_pt",Nbins=50,min=0,max=10)
#Muon_IsoOld = setUpHistrogram(Name="OldIso",LineColor=2,LineWidth=1,XTitle="Old_RelIso",YTitle="Events",ttree=theTree,branch="Muon_pfRelIso04_all",Nbins=50,min=0,max=10)
##RadionptVisReso = setUpHistrogram(Name="RadionptVisReso",LineColor=4,LineWidth=2,XTitle="Pt^{Reco}/Pt^{True}",YTitle="Events",ttree=theTree,branch="ResoVisRadion_pt",Nbins=30,min=0,max=2)
#
#Muon_Iso = setUpCanvas("MuonIso")
#Muon_IsoNew.SetMaximum(max(Muon_IsoNew.GetMaximum(),Muon_IsoOld.GetMaximum())+5000)
##RadionptResoMTT.Draw("Hist E1")
#Muon_IsoNew.Draw("same Hist E1")
#Muon_IsoOld.Draw("same Hist E1")
#
#legend = setUpLegend()
#legend.AddEntry(Muon_IsoNew,"Muon_IsoNew","el")
#legend.AddEntry(Muon_IsoOld,"Muon_IsoOld","el")
#legend.Draw("same")
#
#cmsLatex = setUpCmsLatex(2016)
#Muon_Iso.SaveAs("Muon_Iso.png")
#
#
##plotting for electron Isolation New and Old
#
#Electron_IsoNew= setUpHistrogram(Name="NewIso",LineColor=1,LineWidth=1,XTitle="Corrected_RelIso",YTitle="Events",ttree=theTree,branch="Electron_TauCorrPfIso/Electron_pt",Nbins=50,min=0,max=10)
#Electron_IsoOld = setUpHistrogram(Name="OldIso",LineColor=2,LineWidth=1,XTitle="Old_RelIso",YTitle="Events",ttree=theTree,branch="Electron_pfRelIso03_all",Nbins=50,min=0,max=10)
##RadionptVisReso = setUpHistrogram(Name="RadionptVisReso",LineColor=4,LineWidth=2,XTitle="Pt^{Reco}/Pt^{True}",YTitle="Events",ttree=theTree,branch="ResoVisRadion_pt",Nbins=30,min=0,max=2)
#
#Electron_Iso = setUpCanvas("ElectronIso")
#Electron_IsoNew.SetMaximum(max(Electron_IsoNew.GetMaximum(),Electron_IsoOld.GetMaximum())+5000)
##RadionptResoMTT.Draw("Hist E1")
#Electron_IsoNew.Draw("same Hist E1")
#Electron_IsoOld.Draw("same Hist E1")
#
#legend = setUpLegend()
#legend.AddEntry(Electron_IsoNew,"Electron_IsoNew","el")
#legend.AddEntry(Electron_IsoOld,"Electron_IsoOld","el")
#legend.Draw("same")
#
#cmsLatex = setUpCmsLatex(2016)
#Electron_Iso.SaveAs("Electron_Iso.png")

#Plotting the Reco Leptons dR with genLeptons for the three channels and the combined
RecoLeptondR_GenLepton_tt = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=800,min=-1,max=3,cond="channel==0")
RecoLeptondR_GenLepton_et = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=800,min=-1,max=3,cond="channel==1")
RecoLeptondR_GenLepton_mt = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=800,min=-1,max=3,cond="channel==2")
RecoLeptondR_GenLepton = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=800,min=-1,max=3,cond="")

RecoLeptondR_GenLepton_tt_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=800,min=-1,max=3,cond="channel==0 && gnboostedTau!=0")
RecoLeptondR_GenLepton_et_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=800,min=-1,max=3,cond="channel==1 && gnboostedTau!=0")
RecoLeptondR_GenLepton_mt_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=800,min=-1,max=3,cond="channel==2 && gnboostedTau!=0")
RecoLeptondR_GenLepton_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=800,min=-1,max=3,cond="gnboostedTau!=0")

RecoLeptondR_GenLepton_tt_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=800,min=-1,max=3.5,cond="channel==0 && gnTau!=0")
RecoLeptondR_GenLepton_et_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=800,min=-1,max=3,cond="channel==1 && gnTau!=0")
RecoLeptondR_GenLepton_mt_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=800,min=-1,max=3,cond="channel==2 && gnTau!=0")
RecoLeptondR_GenLepton_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=800,min=-1,max=3,cond="gnTau!=0")


lep_lep = setUpCanvas("lep_lep")
maximum = max(RecoLeptondR_GenLepton_tt.GetMaximum(),RecoLeptondR_GenLepton_et.GetMaximum(),RecoLeptondR_GenLepton_mt.GetMaximum(),RecoLeptondR_GenLepton.GetMaximum())
RecoLeptondR_GenLepton_tt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton_tt.Draw("Hist E1")
RecoLeptondR_GenLepton_et.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt.Draw("same Hist E1")
#RecoLeptondR_GenLepton.Draw("same Hist E1")

RecoLeptondR_GenLepton_tt_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_et_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt_b.Draw("same Hist E1")

RecoLeptondR_GenLepton_tt_hps.Draw("same Hist E1")
RecoLeptondR_GenLepton_et_hps.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt_hps.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton_tt,"#tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et,"e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt,"m-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")

legend.AddEntry(RecoLeptondR_GenLepton_tt_b,"bt #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et_b,"bt e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt_b,"bt m-#tau","el")

legend.AddEntry(RecoLeptondR_GenLepton_tt_hps,"hps #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et_hps,"hps e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt_hps,"hps m-#tau","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep.SaveAs("lep_lep.png")

#######################Same with different Binning ##########################################################################################################
#Plotting the Reco Leptons dR with genLeptons for the three channels and the combined
RecoLeptondR_GenLepton_tt = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=280,min=-0.2,max=0.5,cond="channel==0")
RecoLeptondR_GenLepton_et = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=280,min=-0.2,max=0.5,cond="channel==1")
RecoLeptondR_GenLepton_mt = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=280,min=-0.2,max=0.5,cond="channel==2")
RecoLeptondR_GenLepton = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=280,min=-0.2,max=1,cond="")

RecoLeptondR_GenLepton_tt_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=280,min=-0.2,max=0.5,cond="channel==0 && gnboostedTau!=0")
RecoLeptondR_GenLepton_et_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=280,min=-0.2,max=0.5,cond="channel==1 && gnboostedTau!=0")
RecoLeptondR_GenLepton_mt_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=280,min=-0.2,max=0.5,cond="channel==2 && gnboostedTau!=0")
RecoLeptondR_GenLepton_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=280,min=-0.2,max=1,cond="gnboostedTau!=0")

RecoLeptondR_GenLepton_tt_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=280,min=-0.2,max=0.5,cond="channel==0 && gnTau!=0")
RecoLeptondR_GenLepton_et_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=280,min=-0.2,max=0.5,cond="channel==1 && gnTau!=0")
RecoLeptondR_GenLepton_mt_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=280,min=-0.2,max=0.5,cond="channel==2 && gnTau!=0")
RecoLeptondR_GenLepton_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=280,min=-0.2,max=1,cond="gnTau!=0")

lep_lep = setUpCanvas("lep_lep")
maximum = max(RecoLeptondR_GenLepton_tt.GetMaximum(),RecoLeptondR_GenLepton_et.GetMaximum(),RecoLeptondR_GenLepton_mt.GetMaximum())
RecoLeptondR_GenLepton_tt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton_tt.Draw("Hist E1")
RecoLeptondR_GenLepton_et.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt.Draw("same Hist E1")

RecoLeptondR_GenLepton_tt_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_et_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt_b.Draw("same Hist E1")

RecoLeptondR_GenLepton_tt_hps.Draw("same Hist E1")
RecoLeptondR_GenLepton_et_hps.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt_hps.Draw("same Hist E1")
#RecoLeptondR_GenLepton.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton_tt,"#tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et,"e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt,"m-#tau","el")

legend.AddEntry(RecoLeptondR_GenLepton_tt_b,"bt #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et_b,"bt e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt_b,"bt m-#tau","el")

legend.AddEntry(RecoLeptondR_GenLepton_tt_hps,"hps #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et_hps,"hps e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt_hps,"hps m-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep.SaveAs("lep_lep_2.png")

########################################################################################################################################################################3


#######################Same with different Binning-3 ##########################################################################################################
#Plotting the Reco Leptons dR with genLeptons for the three channels and the combined
RecoLeptondR_GenLepton_tt = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=810,min=-0.05,max=4,cond="channel==0")
RecoLeptondR_GenLepton_et = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=810,min=-0.05,max=4,cond="channel==1")
RecoLeptondR_GenLepton_mt = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=810,min=-0.05,max=4,cond="channel==2")
RecoLeptondR_GenLepton = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=810,min=-0.05,max=4,cond="")

RecoLeptondR_GenLepton_tt_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=810,min=-0.05,max=4,cond="channel==0 && gnboostedTau!=0")
RecoLeptondR_GenLepton_et_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=810,min=-0.05,max=4,cond="channel==1 && gnboostedTau!=0")
RecoLeptondR_GenLepton_mt_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=810,min=-0.05,max=4,cond="channel==2 && gnboostedTau!=0")
RecoLeptondR_GenLepton_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=810,min=-0.05,max=4,cond="gnboostedTau!=0")

RecoLeptondR_GenLepton_tt_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=810,min=-0.05,max=4,cond="channel==0 && gnTau!=0")
RecoLeptondR_GenLepton_et_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=810,min=-0.05,max=4,cond="channel==1 && gnTau!=0")
RecoLeptondR_GenLepton_mt_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=810,min=-0.05,max=4,cond="channel==2 && gnTau!=0")
RecoLeptondR_GenLepton_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=810,min=-0.05,max=4,cond="gnTau!=0")

lep_lep = setUpCanvas("lep_lep")
maximum = max(RecoLeptondR_GenLepton_tt.GetMaximum(),RecoLeptondR_GenLepton_et.GetMaximum(),RecoLeptondR_GenLepton_mt.GetMaximum())
RecoLeptondR_GenLepton_tt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton_tt.Draw("Hist E1")
RecoLeptondR_GenLepton_et.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt.Draw("same Hist E1")

RecoLeptondR_GenLepton_tt_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_et_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt_b.Draw("same Hist E1")

RecoLeptondR_GenLepton_tt_hps.Draw("same Hist E1")
RecoLeptondR_GenLepton_et_hps.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt_hps.Draw("same Hist E1")
#RecoLeptondR_GenLepton.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton_tt,"#tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et,"e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt,"m-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")

legend.AddEntry(RecoLeptondR_GenLepton_tt_b,"bt #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et_b,"bt e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt_b,"bt m-#tau","el")

legend.AddEntry(RecoLeptondR_GenLepton_tt_hps,"hps #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et_hps,"hps e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt_hps,"hps m-#tau","el")

legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep.SaveAs("lep_lep_3.png")

########################################################################################################################################################################3

#######################Same with different Binning-3 ##########################################################################################################
#Plotting the Reco Leptons dR with genLeptons for the three channels and the combined
RecoLeptondR_GenLepton_tt = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=30,min=2,max=5,cond="channel==0")
RecoLeptondR_GenLepton_et = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=30,min=2,max=5,cond="channel==1")
RecoLeptondR_GenLepton_mt = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=30,min=2,max=5,cond="channel==2")
RecoLeptondR_GenLepton = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=30,min=2,max=5,cond="")

RecoLeptondR_GenLepton_tt_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=30,min=2,max=5,cond="channel==0 && gnboostedTau!=0")
RecoLeptondR_GenLepton_et_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=30,min=2,max=5,cond="channel==1 && gnboostedTau!=0")
RecoLeptondR_GenLepton_mt_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=30,min=2,max=5,cond="channel==2 && gnboostedTau!=0")
RecoLeptondR_GenLepton_b = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,LineStyle=2,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=30,min=2,max=5,cond="gnboostedTau!=0")

RecoLeptondR_GenLepton_tt_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=1,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=30,min=2,max=5,cond="channel==0 && gnTau!=0")
RecoLeptondR_GenLepton_et_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=2,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=30,min=2,max=5,cond="channel==1 && gnTau!=0")
RecoLeptondR_GenLepton_mt_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=3,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=30,min=2,max=5,cond="channel==2 && gnTau!=0")
RecoLeptondR_GenLepton_hps = setUpHistrogram(Name="RecoLeptondR_GenLepton",LineColor=4,LineWidth=1,LineStyle=3,XTitle="LepdR_genLepton",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenLepton",Nbins=30,min=2,max=5,cond="gnTau!=0")

lep_lep = setUpCanvas("lep_lep")
maximum = max(RecoLeptondR_GenLepton_tt.GetMaximum(),RecoLeptondR_GenLepton_et.GetMaximum(),RecoLeptondR_GenLepton_mt.GetMaximum())
RecoLeptondR_GenLepton_tt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenLepton_tt.Draw("Hist E1")
RecoLeptondR_GenLepton_et.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt.Draw("same Hist E1")

RecoLeptondR_GenLepton_tt_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_et_b.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt_b.Draw("same Hist E1")

RecoLeptondR_GenLepton_tt_hps.Draw("same Hist E1")
RecoLeptondR_GenLepton_et_hps.Draw("same Hist E1")
RecoLeptondR_GenLepton_mt_hps.Draw("same Hist E1")
#RecoLeptondR_GenLepton.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenLepton_tt,"#tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et,"e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt,"m-#tau","el")
#legend.AddEntry(RecoLeptondR_GenLepton,"all","el")

legend.AddEntry(RecoLeptondR_GenLepton_tt_b,"bt #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et_b,"bt e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt_b,"bt m-#tau","el")

legend.AddEntry(RecoLeptondR_GenLepton_tt_hps,"hps #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_et_hps,"hps e-#tau","el")
legend.AddEntry(RecoLeptondR_GenLepton_mt_hps,"hps m-#tau","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_lep.SaveAs("lep_lep_4.png")

########################################################################################################################################################################3




#Plotting the Reco Leptons dR with genLeptons for the three channels and the combined
RecoLeptondR_GenQuark_tt = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=1,LineWidth=1,XTitle="LepdR_genQuark",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==0")
RecoLeptondR_GenQuark_et = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=2,LineWidth=1,XTitle="LepdR_genQuark",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==1")
RecoLeptondR_GenQuark_mt = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=3,LineWidth=1,XTitle="LepdR_genQuark",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==2")
RecoLeptondR_GenQuark = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=4,LineWidth=1,XTitle="LepdR_genQuark",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="")

RecoLeptondR_GenQuark_tt_b = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=1,LineWidth=1,LineStyle=2,XTitle="LepdR_genQuark",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==0 && gnboostedTau!=0")
RecoLeptondR_GenQuark_et_b = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=2,LineWidth=1,LineStyle=2,XTitle="LepdR_genQuark",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==1 && gnboostedTau!=0")
RecoLeptondR_GenQuark_mt_b = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=3,LineWidth=1,LineStyle=2,XTitle="LepdR_genQuark",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==2 && gnboostedTau!=0")
RecoLeptondR_GenQuark_b = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=4,LineWidth=1,LineStyle=2,XTitle="LepdR_genQuark",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="gnboostedTau!=0")

RecoLeptondR_GenQuark_tt_hps = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=1,LineWidth=1,LineStyle=3,XTitle="LepdR_genQuark",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==0 && gnTau!=0")
RecoLeptondR_GenQuark_et_hps = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=2,LineWidth=1,LineStyle=3,XTitle="LepdR_genQuark",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==1 && gnTau!=0")
RecoLeptondR_GenQuark_mt_hps = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=3,LineWidth=1,LineStyle=3,XTitle="LepdR_genQuark",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="channel==2 && gnTau!=0")
RecoLeptondR_GenQuark_hps = setUpHistrogram(Name="RecoLeptondR_GenQuark",LineColor=4,LineWidth=1,LineStyle=3,XTitle="LepdR_genQuark",YTitle="Events",ttree=theTree,branch="RecoLeptondR_GenQuark",Nbins=140,min=-1,max=6,cond="gnTau!=0")

lep_jet = setUpCanvas("lep_jet")
maximum = max(RecoLeptondR_GenQuark_tt.GetMaximum(),RecoLeptondR_GenQuark_et.GetMaximum(),RecoLeptondR_GenQuark_mt.GetMaximum())
RecoLeptondR_GenQuark_tt.SetMaximum(maximum + 0.30*maximum)

RecoLeptondR_GenQuark_tt.Draw("Hist E1")
RecoLeptondR_GenQuark_et.Draw("same Hist E1")
RecoLeptondR_GenQuark_mt.Draw("same Hist E1")

RecoLeptondR_GenQuark_tt_b.Draw("same Hist E1")
RecoLeptondR_GenQuark_et_b.Draw("same Hist E1")
RecoLeptondR_GenQuark_mt_b.Draw("same Hist E1")

RecoLeptondR_GenQuark_tt_hps.Draw("same Hist E1")
RecoLeptondR_GenQuark_et_hps.Draw("same Hist E1")
RecoLeptondR_GenQuark_mt_hps.Draw("same Hist E1")
#RecoLeptondR_GenQuark.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLeptondR_GenQuark_tt,"#tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_et,"e-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_mt,"m-#tau","el")

legend.AddEntry(RecoLeptondR_GenQuark_tt_b,"bt #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_et_b,"bt e-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_mt_b,"bt m-#tau","el")

legend.AddEntry(RecoLeptondR_GenQuark_tt_hps,"hps #tau-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_et_hps,"hps e-#tau","el")
legend.AddEntry(RecoLeptondR_GenQuark_mt_hps,"hps m-#tau","el")
#legend.AddEntry(RecoLeptondR_GenQuark,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
lep_jet.SaveAs("lep_jet.png")


#Plotting the Reco FatJet dR with bQuarks pair for the three channels and the combined

FatJetdR_GenCombinedQuark_tt = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=1,LineWidth=1,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=300,min=0,max=3,cond="channel==0")
FatJetdR_GenCombinedQuark_et = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=2,LineWidth=1,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=300,min=0,max=3,cond="channel==1")
FatJetdR_GenCombinedQuark_mt = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=3,LineWidth=1,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=300,min=0,max=3,cond="channel==2")
FatJetdR_GenCombinedQuark = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=4,LineWidth=1,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=300,min=0,max=3,cond="")

FatJetdR_GenCombinedQuark_tt_b = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=1,LineWidth=1,LineStyle=2,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=300,min=0,max=3,cond="channel==0 && gnboostedTau!=0")
FatJetdR_GenCombinedQuark_et_b = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=2,LineWidth=1,LineStyle=2,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=300,min=0,max=3,cond="channel==1 && gnboostedTau!=0")
FatJetdR_GenCombinedQuark_mt_b = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=3,LineWidth=1,LineStyle=2,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=300,min=0,max=3,cond="channel==2 && gnboostedTau!=0")
FatJetdR_GenCombinedQuark_b = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=4,LineWidth=1,LineStyle=2,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=300,min=0,max=3,cond="gnboostedTau!=0")

FatJetdR_GenCombinedQuark_tt_hps = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=1,LineWidth=1,LineStyle=3,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=300,min=0,max=3,cond="channel==0 && gnTau!=0")
FatJetdR_GenCombinedQuark_et_hps = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=2,LineWidth=1,LineStyle=3,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=300,min=0,max=3,cond="channel==1 && gnTau!=0")
FatJetdR_GenCombinedQuark_mt_hps = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=3,LineWidth=1,LineStyle=3,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=300,min=0,max=3,cond="channel==2 && gnTau!=0")
FatJetdR_GenCombinedQuark_hps = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=4,LineWidth=1,LineStyle=3,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=300,min=0,max=3,cond="gnTau!=0")

jet_jet = setUpCanvas("jet_jet")
maximum = max(FatJetdR_GenCombinedQuark_tt.GetMaximum(),FatJetdR_GenCombinedQuark_et.GetMaximum(),FatJetdR_GenCombinedQuark_mt.GetMaximum())
FatJetdR_GenCombinedQuark_tt.SetMaximum(maximum + 0.30*maximum)

FatJetdR_GenCombinedQuark_tt.Draw("Hist E1")
FatJetdR_GenCombinedQuark_et.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_mt.Draw("same Hist E1")

FatJetdR_GenCombinedQuark_tt_b.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_et_b.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_mt_b.Draw("same Hist E1")

FatJetdR_GenCombinedQuark_tt_hps.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_et_hps.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_mt_hps.Draw("same Hist E1")
#FatJetdR_GenCombinedQuark.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(FatJetdR_GenCombinedQuark_tt,"#tau-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_et,"e-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_mt,"m-#tau","el")

legend.AddEntry(FatJetdR_GenCombinedQuark_tt_b,"bt #tau-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_et_b,"bt e-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_mt_b,"bt m-#tau","el")

legend.AddEntry(FatJetdR_GenCombinedQuark_tt_hps,"hps #tau-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_et_hps,"hps e-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_mt_hps,"hps m-#tau","el")
#legend.AddEntry(FatJetdR_GenCombinedQuark,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
jet_jet.SaveAs("jet_jet.png")

#####################################Different Binning###################################################################################################

#Plotting the Reco FatJet dR with bQuarks pair for the three channels and the combined

FatJetdR_GenCombinedQuark_tt = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=1,LineWidth=1,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=140,min=-0.2,max=0.5,cond="channel==0")
FatJetdR_GenCombinedQuark_et = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=2,LineWidth=1,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=140,min=-0.2,max=0.5,cond="channel==1")
FatJetdR_GenCombinedQuark_mt = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=3,LineWidth=1,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=140,min=-0.2,max=0.5,cond="channel==2")
FatJetdR_GenCombinedQuark = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=4,LineWidth=1,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=140,min=-0.2,max=0.5,cond="")

FatJetdR_GenCombinedQuark_tt_b = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=1,LineWidth=1,LineStyle=2,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=140,min=-0.2,max=0.5,cond="channel==0 && gnboostedTau!=0")
FatJetdR_GenCombinedQuark_et_b = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=2,LineWidth=1,LineStyle=2,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=140,min=-0.2,max=0.5,cond="channel==1 && gnboostedTau!=0")
FatJetdR_GenCombinedQuark_mt_b = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=3,LineWidth=1,LineStyle=2,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=140,min=-0.2,max=0.5,cond="channel==2 && gnboostedTau!=0")
FatJetdR_GenCombinedQuark_b = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=4,LineWidth=1,LineStyle=2,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=140,min=-0.2,max=0.5,cond="gnboostedTau!=0")

FatJetdR_GenCombinedQuark_tt_hps = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=1,LineWidth=1,LineStyle=3,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=140,min=-0.2,max=0.5,cond="channel==0 && gnTau!=0")
FatJetdR_GenCombinedQuark_et_hps = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=2,LineWidth=1,LineStyle=3,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=140,min=-0.2,max=0.5,cond="channel==1 && gnTau!=0")
FatJetdR_GenCombinedQuark_mt_hps = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=3,LineWidth=1,LineStyle=3,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=140,min=-0.2,max=0.5,cond="channel==2 && gnTau!=0")
FatJetdR_GenCombinedQuark_hps = setUpHistrogram(Name="FatJetdR_GenCombinedQuark",LineColor=4,LineWidth=1,LineStyle=3,XTitle="FatJetdR_genQpair",YTitle="Events",ttree=theTree,branch="FatJetdR_GenCombinedQuark",Nbins=140,min=-0.2,max=0.5,cond="gnTau!=0")

jet_jet = setUpCanvas("jet_jet")
maximum = max(FatJetdR_GenCombinedQuark_tt.GetMaximum(),FatJetdR_GenCombinedQuark_et.GetMaximum(),FatJetdR_GenCombinedQuark_mt.GetMaximum())
FatJetdR_GenCombinedQuark_tt.SetMaximum(maximum + 0.30*maximum)

FatJetdR_GenCombinedQuark_tt.Draw("Hist E1")
FatJetdR_GenCombinedQuark_et.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_mt.Draw("same Hist E1")

FatJetdR_GenCombinedQuark_tt_b.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_et_b.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_mt_b.Draw("same Hist E1")

FatJetdR_GenCombinedQuark_tt_hps.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_et_hps.Draw("same Hist E1")
FatJetdR_GenCombinedQuark_mt_hps.Draw("same Hist E1")
#FatJetdR_GenCombinedQuark.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(FatJetdR_GenCombinedQuark_tt,"#tau-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_et,"e-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_mt,"m-#tau","el")

legend.AddEntry(FatJetdR_GenCombinedQuark_tt_b,"bt #tau-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_et_b,"bt e-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_mt_b,"bt m-#tau","el")

legend.AddEntry(FatJetdR_GenCombinedQuark_tt_hps,"hps #tau-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_et_hps,"hps e-#tau","el")
legend.AddEntry(FatJetdR_GenCombinedQuark_mt_hps,"hps m-#tau","el")
#legend.AddEntry(FatJetdR_GenCombinedQuark,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
jet_jet.SaveAs("jet_jet_2.png")

#Plotting the match type for all channels and combined 
RecoLepton_match_type_tt = setUpHistrogram(Name="RecoLepton_match_type",LineColor=1,LineWidth=1,XTitle="RecoLepton_match_type",YTitle="Events",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==0")
RecoLepton_match_type_et = setUpHistrogram(Name="RecoLepton_match_type",LineColor=2,LineWidth=1,XTitle="RecoLepton_match_type",YTitle="Events",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==1")
RecoLepton_match_type_mt = setUpHistrogram(Name="RecoLepton_match_type",LineColor=3,LineWidth=1,XTitle="RecoLepton_match_type",YTitle="Events",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==2")
RecoLepton_match_type = setUpHistrogram(Name="RecoLepton_match_type",LineColor=4,LineWidth=1,XTitle="RecoLepton_match_type",YTitle="Events",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="")

RecoLepton_match_type_tt_b = setUpHistrogram(Name="RecoLepton_match_type",LineColor=1,LineWidth=1,LineStyle=2,XTitle="RecoLepton_match_type",YTitle="Events",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==0 && gnboostedTau!=0")
RecoLepton_match_type_et_b = setUpHistrogram(Name="RecoLepton_match_type",LineColor=2,LineWidth=1,LineStyle=2,XTitle="RecoLepton_match_type",YTitle="Events",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==1 && gnboostedTau!=0")
RecoLepton_match_type_mt_b = setUpHistrogram(Name="RecoLepton_match_type",LineColor=3,LineWidth=1,LineStyle=2,XTitle="RecoLepton_match_type",YTitle="Events",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==2 && gnboostedTau!=0")
RecoLepton_match_type_b = setUpHistrogram(Name="RecoLepton_match_type",LineColor=4,LineWidth=1,LineStyle=2,XTitle="RecoLepton_match_type",YTitle="Events",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="gnboostedTau!=0")

RecoLepton_match_type_tt_hps = setUpHistrogram(Name="RecoLepton_match_type",LineColor=1,LineWidth=1,LineStyle=3,XTitle="RecoLepton_match_type",YTitle="Events",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==0 && gnTau!=0")
RecoLepton_match_type_et_hps = setUpHistrogram(Name="RecoLepton_match_type",LineColor=2,LineWidth=1,LineStyle=3,XTitle="RecoLepton_match_type",YTitle="Events",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==1 && gnTau!=0")
RecoLepton_match_type_mt_hps = setUpHistrogram(Name="RecoLepton_match_type",LineColor=3,LineWidth=1,LineStyle=3,XTitle="RecoLepton_match_type",YTitle="Events",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="channel==2 && gnTau!=0")
RecoLepton_match_type_hps = setUpHistrogram(Name="RecoLepton_match_type",LineColor=4,LineWidth=1,LineStyle=3,XTitle="RecoLepton_match_type",YTitle="Events",ttree=theTree,branch="RecoLepton_match_type",Nbins=7,min=-2,max=5,cond="gnTau!=0")

matchtype = setUpCanvas("matchtype")
maximum = max(RecoLepton_match_type_tt.GetMaximum(),RecoLepton_match_type_et.GetMaximum(),RecoLepton_match_type_mt.GetMaximum())
RecoLepton_match_type_tt.SetMaximum(maximum + 0.30*maximum)

RecoLepton_match_type_tt.Draw("Hist E1")
RecoLepton_match_type_et.Draw("same Hist E1")
RecoLepton_match_type_mt.Draw("same Hist E1")

RecoLepton_match_type_tt_b.Draw("same Hist E1")
RecoLepton_match_type_et_b.Draw("same Hist E1")
RecoLepton_match_type_mt_b.Draw("same Hist E1")

RecoLepton_match_type_tt_hps.Draw("same Hist E1")
RecoLepton_match_type_et_hps.Draw("same Hist E1")
RecoLepton_match_type_mt_hps.Draw("same Hist E1")
#RecoLepton_match_type.Draw("same Hist E1")

legend = setUpLegend()
legend.AddEntry(RecoLepton_match_type_tt,"#tau-#tau","el")
legend.AddEntry(RecoLepton_match_type_et,"e-#tau","el")
legend.AddEntry(RecoLepton_match_type_mt,"m-#tau","el")

legend.AddEntry(RecoLepton_match_type_tt_b,"bt #tau-#tau","el")
legend.AddEntry(RecoLepton_match_type_et_b,"bt e-#tau","el")
legend.AddEntry(RecoLepton_match_type_mt_b,"bt m-#tau","el")

legend.AddEntry(RecoLepton_match_type_tt_hps,"hps #tau-#tau","el")
legend.AddEntry(RecoLepton_match_type_et_hps,"hps e-#tau","el")
legend.AddEntry(RecoLepton_match_type_mt_hps,"hps m-#tau","el")
#legend.AddEntry(RecoLepton_match_type,"all","el")
legend.Draw("same")

cmsLatex = setUpCmsLatex(2016)
matchtype.SaveAs("matchtype.png")

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
