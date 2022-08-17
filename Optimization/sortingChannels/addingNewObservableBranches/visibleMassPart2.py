from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import glob
import argparse
import multiprocessing as  np


ROOT.PyConfig.IgnoreCommandLineOptions = True

class VisibleMassPart2(Module):
    def __init__(self, channel):
       print ("Running the Visible Mass and Delta R branches part 2")
       self.channel = channel # Specify the channel    


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

    def createBranches(self,prefix):
        self.out.branch(prefix+"MVis_LL", "F")
        self.out.branch(prefix+"DeltaR_LL","F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
    def analyze(self,event):

        self.createBranches("tt")
        self.createBranches("et")
        self.createBranches("mt")

        diTau = Collection(event, "ttallTau","ttnallTau")
        eTau = Collection(event, "etallTau","etnallTau")
        mTau = Collection(event, "mtallTau","mtnallTau")

        lepton1 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        lepton2 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)

        if event.tt == 1:
            lepton1.SetPtEtaPhiM(diTau[0].pt,diTau[0].eta,diTau[0].phi,diTau[0].mass)
            lepton2.SetPtEtaPhiM(diTau[1].pt,diTau[1].eta,diTau[1].phi,diTau[1].mass)
            self.out.fillBranch("ttMVis_LL",abs((lepton1 + lepton2).M()))
            self.out.fillBranch("ttDeltaR_LL",lepton1.DeltaR(lepton2))

        if event.et == 1:
            lepton1.SetPtEtaPhiM(eTau[0].pt,eTau[0].eta,eTau[0].phi,eTau[0].mass)
            lepton2.SetPtEtaPhiM(eTau[1].pt,eTau[1].eta,eTau[1].phi,eTau[1].mass)
            self.out.fillBranch("etMVis_LL",abs((lepton1 + lepton2).M()))
            self.out.fillBranch("etDeltaR_LL",lepton1.DeltaR(lepton2))
        
        if event.mt == 1:
            lepton1.SetPtEtaPhiM(mTau[0].pt,mTau[0].eta,mTau[0].phi,mTau[0].mass)
            lepton2.SetPtEtaPhiM(mTau[1].pt,mTau[1].eta,mTau[1].phi,mTau[1].mass)
            self.out.fillBranch("mtMVis_LL",abs((lepton1 + lepton2).M()))
            self.out.fillBranch("mtDeltaR_LL",lepton1.DeltaR(lepton2))

        return True        

