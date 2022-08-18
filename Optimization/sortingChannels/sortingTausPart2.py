from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
#from visibleMass import VisibleMass
import ROOT
import glob
#from particleClass import particle
#from branchesList import *
import multiprocessing as  np
import argparse

ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?


class mergeTauPart2(Module):
    def __init__(self,filename):
        print ("Running the sorting Taus Module")
        #self.channel = channel # Specify the channel
        self.filename = filename
        self.event =None
        self.branch_names_tau = dict()
        self.branch_names_btau = dict()
        self.tauCollection = None
        self.boostedtauCollection = None
        self.diTauboostedTauCollection =  None
        self.diTauTauCollection = None
        self.eTauboostedTauCollection = None
        self.eTauTauCollection = None
        self.mTauboostedTauCollection = None
        self.mTauTauCollection = None
        self.event = None
        self.setUp = None

    #lets define the branches that need to be filled
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

    def createBranches(self,prefix):
        if self.setUp != None:
            return
        self.out.branch("{}".format(prefix+"nallTau"),"I")
        type_dict = {"Float_t" : "F", "Int_t": "I", "Bool_t" : "O", "UChar_t": "I"}
        for leaf in self.tauCollection._event._tree.GetListOfLeaves():
            lName = leaf.GetName()
            if "_" not in lName:
                continue
            partName = lName[:lName.index("_")]
            varName = lName[lName.index("_")+1:]
            if partName == "boostedTau":
                self.branch_names_btau[varName] = type_dict[leaf.GetTypeName()]
            if partName == "Tau":
                self.branch_names_tau[varName] = type_dict[leaf.GetTypeName()]
        
        
        for branch,branchType in self.branch_names_btau.iteritems(): 
            for branch2, branchType2 in self.branch_names_tau.iteritems():
                if branch==branch2:
                    if (self.filename == "Data" and (branch == "genPartFlav" or branch =="genPartIdx")):
                        break
                    self.out.branch("{}_{}".format(prefix+"allTau",branch),"{}".format(branchType),lenVar="{}".format(prefix+"nallTau"))
                    break
    

    def fillBranches(self,colllist,prefix):
        if prefix=="tt":
            length = 2
        else:
            length = 0
        if (prefix=="et" or prefix=="mt"):
            length = 1
        else:
            length = 0
        self.out.fillBranch("{}".format(prefix+"nallTau"),length)
        for branch in self.branch_names_tau.keys():           
            for branch2 in self.branch_names_btau.keys():
                if branch==branch2:
                    if (self.filename == "Data" and (branch == "genPartFlav" or branch=="genPartIdx")):
                        break
                    self.out.fillBranch("{}_{}".format(prefix+"allTau",branch),self.get_attributes(branch,colllist))
                    break    
    
    def get_attributes(self,variable,collList):
        list = []
        for coll in collList:
            for obj in coll:
                list.append(obj[variable])
        return list


    def analyze(self,event):
        self.event = event
        self.tauCollection = Collection(event, "gTau","gnTau")
        self.boostedtauCollection = Collection(event, "gboostedTau","gnboostedTau")
        self.diTauboostedTauCollection =  Collection(event, "ttboostedTau","ttnboostedTau")
        self.diTauTauCollection = Collection(event, "ttTau","ttnTau")
        self.eTauboostedTauCollection = Collection(event, "etboostedTau","etnboostedTau")
        self.eTauTauCollection = Collection(event, "etTau","etnTau")
        self.mTauboostedTauCollection = Collection(event, "mtboostedTau","mtnboostedTau")
        self.mTauTauCollection = Collection(event, "mtTau","mtnTau")


        if self.setUp == None:
            self.createBranches("tt")
            self.createBranches("et")
            self.createBranches("mt")
            self.setUp = "Done"

        colllist_tt =[]
        collist_et=[]
        collist_mt = []

        if event.tt == 1:
            if (len(self.diTauboostedTauCollection)==2):
                colllist_tt.append(self.diTauboostedTauCollection)
            elif (len(self.diTauTauCollection)==2):
                colllist_tt.append(self.diTauTauCollection)
            self.fillBranches(colllist_tt,"tt")
        else:
            self.fillBranches(colllist_tt,"tt")
        
        if event.et == 1:
            if (len(self.eTauboostedTauCollection)==1):
                collist_et.append(self.eTauboostedTauCollection)
            elif (len(self.eTauTauCollection)==1):
                collist_et.append(self.eTauTauCollection)
            self.fillBranches(collist_et,"et")
        else:
            self.fillBranches(collist_et,"et")


        if event.mt == 1:
            if (len(self.mTauboostedTauCollection)==1):
                collist_mt.append(self.mTauboostedTauCollection)
            elif (len(self.mTauTauCollection)==1):
                collist_mt.append(self.mTauTauCollection)
            self.fillBranches(collist_mt,"mt")
        else:
            self.fillBranches(collist_mt,"mt")   
        return True     


