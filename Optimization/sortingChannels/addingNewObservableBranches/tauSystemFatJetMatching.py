from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
#from .genChannelSplit import *
import ROOT
import itertools

from re import search

ROOT.PyConfig.IgnoreCommandLineOptions = True

class tauSystemFatJetMatching(Module):
    def __init__(self):
        print ("Running FatJet Tau System Matching Algo")
        #Create the collections at initialization
        self.setUp= None
        self.gMuonCollection = None
        self.allTauCollection = None
        self.gElectronCollection = None
        self.FatJetCollection = None

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

    def createBranches(self):
        self.out.branch("indexClosestFatJet","I")
        self.out.branch("deltaR","F")
        self.out.branch("tauSysFatJetMatchTruth","I")


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
    def findMatchingFatJet(self,tauSysFV):
        indexMatch = -1
        matchTruth = 0
        dR_least = 100
        for i in range(len(self.FatJetCollection)):
            fatjet = self.FatJetCollection[i].p4()
            dR = fatjet.DeltaR(tauSysFV)
            if ((dR < dR_least)):
                dR_least = dR
                indexMatch = i
        if (dR_least)<0.3:
            matchTruth = 1
        return (dR_least,i,matchTruth)


    def analyze(self,event):
        if self.setUp == None:
            self.createBranches()
            self.setUp = "Done"

        #Create a host of collections to be used in the code later
        #####################################################################################
        self.allTauCollection = Collection(event, "allTau","nallTau")
        self.gElectronCollection = Collection(event, "gElectron","gnElectron")
        self.gMuonCollection = Collection(event, "gMuon","gnMuon")
        self.FatJetCollection = Collection(event, "FatJet","nFatJet")
        #####################################################################################

        if (len(self.allTauCollection)==1):
            if (len(self.gElectronCollection)==1 and len(self.gMuonCollection)==0):
                tauFourVector = self.allTauCollection[0].p4() + self.gElectronCollection[0].p4()
            elif (len(self.gElectronCollection)==0 and len(self.gMuonCollection)==1): 
                tauFourVector = self.allTauCollection[0].p4() + self.gMuonCollection[0].p4()
        elif (len(self.allTauCollection)==2):
            tauFourVector = self.allTauCollection[0].p4() + self.allTauCollection[1].p4()
        else:
            print("length of allTau is unexpected = ",len(self.allTauCollection))
        
        dR_least,index,matchTruth = self.findMatchingFatJet(tauFourVector)

        self.out.fillBranch("indexClosestFatJet",index)
        self.out.fillBranch("deltaR",dR_least)
        self.out.fillBranch("tauSysFatJetMatchTruth",matchTruth)
        return True