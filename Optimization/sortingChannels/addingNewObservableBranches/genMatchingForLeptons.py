
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from .genChannelSplit import *
import ROOT
import itertools

from re import search

ROOT.PyConfig.IgnoreCommandLineOptions = True


class LeptonMC_MatchingWithTausAndBQuark(Module):
    def __init__(self):
        print ("Running MC lepton matching algorithm")
        #Create the collections at initialization
        self.setUp= None
        self.GenPartCollection =  None
        self.gMuonCollection = None
        self.visTauCollection = None
        self.allTauCollection = None
        self.gElectronCollection = None
        self.gMuonCollection = None
        self.gFatJetCollection = None


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
    
    def createBranches(self):
        self.out.branch("RecoLeptondR_GenLepton","F", n=2)
        self.out.branch("RecoLepton_match_type","I",n=2)
     

        self.out.branch("RecoLeptondR_GenQuark","F", n=2)
        self.out.branch("RecoLeptondR_MadGenQuark","F", n=2)

        self.out.branch("FatJetdR_GenCombinedQuark","F")
        self.out.branch("FatJetdR_MadCombinedGenQuark","F")

        self.out.branch("genchannel","I")
        self.out.branch("noPythiaEvent","I")
        #self.out.branch("channelMismatch","I")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self,event):

        if self.setUp == None:
            self.createBranches()
            self.setUp = "Done"
        RecoLeptondR_GenLepton=[]
        RecoLepton_match_type=[]
        RecoLeptondR_GenQuark=[]
        #RecoLeptondR_MadQuark=[]


        #Create a host of collections to be used in the code later
        #####################################################################################
        self.GenPartCollection = Collection(event, "GenPart","nGenPart")
        self.visTauCollection = Collection(event, "GenVisTau","nGenVisTau")
        self.allTauCollection = Collection(event, "allTau","nallTau")
        self.gElectronCollection = Collection(event, "gElectron","gnElectron")
        self.gMuonCollection = Collection(event, "gMuon","gnMuon")
        self.gFatJetCollection = Collection(event, "gFatJet","gnFatJet")
        #####################################################################################
        decay,tauIndices,genlep, extraFV = classifyTauDecayMode(event)

        if decay == "tt":
            self.out.fillBranch("genchannel",0)
        elif decay == "te":
            self.out.fillBranch("genchannel",1)
        elif decay == "tm":
            self.out.fillBranch("genchannel",2)
        elif ((decay == "ee") or (decay =="mm") or (decay =="me") or (decay == "em")):
            self.out.fillBranch("genchannel",3)
        else:
            self.out.fillBranch("genchannel",-1)


        genFatJetMad, genFatJetPythia, MadPos, MadNeg, PythiaPos, PythiaNeg,noPythiaEvent = findingBQuarks(event)
        bJet_fourVec = [PythiaPos,PythiaNeg]
        bJet_MadfourVec = [MadPos,MadNeg]

        if noPythiaEvent:
            self.out.fillBranch("noPythiaEvent",1)
        else:
            self.out.fillBranch("noPythiaEvent",0)

        
        #allreco = self.allTauCollection
        #if (len(self.allTauCollection)>0):
        #    allreco.append(self.allTauCollection)
        #if (len(self.gElectronCollection)>0):
        #    allreco.append(self.gElectronCollection)
        #if (len(self.gMuonCollection)>0):
        #    allreco.append(self.gMuonCollection)

        #print (allreco)
        recoFV = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        genTauVector = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)

        for object in itertools.chain(self.allTauCollection,self.gElectronCollection,self.gMuonCollection):
            #print ("type of object = ",type(object),object.phi)
            recoFV.SetPtEtaPhiM(object.pt,object.eta,object.phi,object.mass)
            typeOfMatch = -1
            dR = -1
            #dR_MadLeast = -1
            dR_Least = -1
            dR_lepton = -1
            dR_bquark = -1
            for genObj in tauIndices:
                genTauVector.SetPtEtaPhiM(self.visTauCollection[genObj].pt,self.visTauCollection[genObj].eta,self.visTauCollection[genObj].phi,self.visTauCollection[genObj].mass)
                dR = genTauVector.DeltaR(recoFV)
                if ((dR < dR_lepton) or (dR_lepton < 0)):
                    dR_lepton = dR
                if (dR <= 0.3):             
                    if ((dR < dR_Least) or (dR_Least < 0)):
                        dR_Least = dR
                        #dR_lepton = dR
                        typeOfMatch = 0
            
            if extraFV !=None:
                dR = extraFV.DeltaR(recoFV)
                if ((dR < dR_lepton) or (dR_lepton < 0)):
                    dR_lepton = dR
                if (dR <= 0.3):
                    if ((dR < dR_Least) or (dR_Least < 0)):
                        dR_Least = dR
                        #dR_lepton = dR
                        typeOfMatch = 0
            
            for genObj in genlep:
                genTauVector.SetPtEtaPhiM(self.GenPartCollection[genObj].pt,self.GenPartCollection[genObj].eta,self.GenPartCollection[genObj].phi,self.GenPartCollection[genObj].mass)
                dR = genTauVector.DeltaR(recoFV)
                if ((dR < dR_lepton) or (dR_lepton < 0)):
                    dR_lepton = dR
                if (dR <= 0.3):
                    if ((dR < dR_Least) or (dR_Least < 0)):
                        dR_Least = dR
                        #dR_lepton = dR
                        if (abs(self.GenPartCollection[genObj].pdgId)==11):
                            typeOfMatch = 1
                        elif (abs(self.GenPartCollection[genObj].pdgId)==13):
                            typeOfMatch = 2
            
            for genObjFV in bJet_fourVec:
                dR = genObjFV.DeltaR(recoFV)
                if ((dR < dR_bquark) or (dR_bquark < 0)):
                    dR_bquark = dR
                if (dR <= 0.3):
                    if ((dR < dR_Least) or (dR_Least < 0)):
                        dR_Least = dR
                        typeOfMatch = 3
                
                
                    
            
            #for genObjFV in bJet_MadfourVec:
            #    dR = genObjFV.DeltaR(recoFV)
            #    if ((dR < dR_MadLeast) or (dR < 0)):
            #        dR_MadLeast = dR



            RecoLeptondR_GenLepton.append(dR_lepton)
            RecoLeptondR_GenQuark.append(dR_bquark)
            #RecoLeptondR_MadQuark.append(dR_MadLeast)
            RecoLepton_match_type.append(typeOfMatch)
            FatJetdR_GenCombinedQuark = genFatJetPythia.DeltaR(self.gFatJetCollection[0].p4())
            FatJetdR_MadCombinedQuark = genFatJetMad.DeltaR(self.gFatJetCollection[0].p4())

        self.out.fillBranch("RecoLeptondR_GenLepton",RecoLeptondR_GenLepton)
        self.out.fillBranch("RecoLeptondR_GenQuark",RecoLeptondR_GenQuark)
        self.out.fillBranch("RecoLepton_match_type",RecoLepton_match_type)
        self.out.fillBranch("FatJetdR_GenCombinedQuark",FatJetdR_GenCombinedQuark)
        self.out.fillBranch("FatJetdR_MadCombinedGenQuark",FatJetdR_MadCombinedQuark)


        return True















                



