from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from addingNewObservableBranches.visibleMassCamilla import VisibleMassCamilla  #Importing modules works if the folders are in the place where the scripts are
from addingNewObservableBranches.visibleMassPart2 import VisibleMassPart2
from addingNewObservableBranches.genMeasurementRadionBranches import genMeasurementRadionBranches
from addingNewObservableBranches.fastMTTBranches import fastMTTBranches
from addingNewObservableBranches.genMatchingForLeptons import LeptonMC_MatchingWithTausAndBQuark
from addingNewObservableBranches.tauSystemFatJetMatching import tauSystemFatJetMatching
#from genChannelSplit import *

#from addingNewObservableBranches.genMeasurementRadionBranches import genMeasurementRadionBranches
from sortingTausCamilla import mergeTauCamilla
from sortingTausPart2 import mergeTauPart2
import ROOT
import glob
from particleClass import particle
from FatJetClass import FatJet
from TauClass import Tau
from BoostedTauClass import BoostedTau
from ElectronClass import Electron
from MuonClass import Muon
import argparse
import traceback
import multiprocessing as  np
import os
from re import search

ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class ChannelCamilla(Module):
	def __init__(self,filename,eleID,muID,tauID,btauID):
		print ("Running the channel sorter Module")
		print ("processing file ",filename)
		self.filename = filename #filename passed cause we needed to count the events with zero divide errors
	
		self.boostedTau = BoostedTau("boostedTau")
		self.Tau = Tau("Tau")
		self.FatJet = FatJet("FatJet")
		self.Electron = Electron("Electron")    
		self.Muon = Muon("Muon")
		self.Jet = particle("Jet")

		self.diTauboostedTau = BoostedTau("boostedTau")
		self.diTauTau = Tau("Tau")
		self.diTauFatJet = FatJet("FatJet")
		self.diTauJet = particle("Jet")

		self.eTauboostedTau = BoostedTau("boostedTau")
		self.eTauTau = Tau("Tau")
		self.eTauFatJet = FatJet("FatJet")
		self.eTauJet = particle("Jet")
		self.eTauElectron = Electron("Electron")

		self.mTauboostedTau = BoostedTau("boostedTau")
		self.mTauTau = Tau("Tau")
		self.mTauFatJet = FatJet("FatJet")
		self.mTauJet = particle("Jet")
		self.mTauMuon = Muon("Muon")

		self.IsoRemElectron = Electron("Electron")
		self.LooseCutBasedElectron = Electron("Electron")

		#To store the addional information in the files as to which ID was applied for different objects
		self.eleID = int(eleID)
		self.muID = int(muID)
		self.tauID = int(tauID)
		self.btauID = int(btauID)


		self.setUp = None
	
	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		self.countBadevents = 0 #This is to keep track of bad events per file
		self.out = wrappedOutputTree
	
    
	def setup_branches(self):
		if self.setUp!=None:
			return
		self.Tau.setUpBranches(self.out) #creating the new branches
		self.FatJet.setUpBranches(self.out)
		self.boostedTau.setUpBranches(self.out)
		self.Electron.setUpBranches(self.out)
		self.Muon.setUpBranches(self.out)
		self.Jet.setUpBranches(self.out)

		self.diTauboostedTau.setUpBranches(self.out,"tt")
		self.diTauTau.setUpBranches(self.out,"tt")
		self.diTauFatJet.setUpBranches(self.out,"tt")
		self.diTauJet.setUpBranches(self.out,"tt")

		self.eTauboostedTau.setUpBranches(self.out,"et")
		self.eTauTau.setUpBranches(self.out,"et")
		self.eTauFatJet.setUpBranches(self.out,"et")
		self.eTauJet.setUpBranches(self.out,"et")
		self.eTauElectron.setUpBranches(self.out,"et")

		self.mTauboostedTau.setUpBranches(self.out,"mt")
		self.mTauTau.setUpBranches(self.out,"mt")
		self.mTauFatJet.setUpBranches(self.out,"mt")
		self.mTauJet.setUpBranches(self.out,"mt")
		self.mTauMuon.setUpBranches(self.out,"mt")

		self.IsoRemElectron.setUpBranches(self.out,"IsoRem")	
		self.LooseCutBasedElectron.setUpBranches(self.out,"LooseCB")

		self.out.branch("channel","I") # adding a new branch for channel 0-Di tau, 1- E-tau, 2- M-Tau
		self.out.branch("tt","I")
		self.out.branch("et","I")
		self.out.branch("mt","I")
		self.out.branch("eleID","I")
		self.out.branch("muID","I")
		self.out.branch("tauID","I")
		self.out.branch("btauID","I")

		self.out.branch("diTauCombPt","F")
		self.out.branch("eTauCombPt","F")
		self.out.branch("mTauCombPt","F")
		self.out.branch("combPt","F")



	def setup_collection(self, event):
		if self.setUp!=None:
			return
		self.Jet.setupCollectionforInitialization(event)
		self.Tau.setupCollectionforInitialization(event)
		self.boostedTau.setupCollectionforInitialization(event)
		self.FatJet.setupCollectionforInitialization(event)
		self.Electron.setupCollectionforInitialization(event)
		self.Muon.setupCollectionforInitialization(event)

		self.diTauboostedTau.setupCollectionforInitialization(event)
		self.diTauTau.setupCollectionforInitialization(event)
		self.diTauFatJet.setupCollectionforInitialization(event)
		self.diTauJet.setupCollectionforInitialization(event)

		self.eTauboostedTau.setupCollectionforInitialization(event)
		self.eTauTau.setupCollectionforInitialization(event)
		self.eTauFatJet.setupCollectionforInitialization(event)
		self.eTauJet.setupCollectionforInitialization(event)
		self.eTauElectron.setupCollectionforInitialization(event)

		self.mTauboostedTau.setupCollectionforInitialization(event)
		self.mTauTau.setupCollectionforInitialization(event)
		self.mTauFatJet.setupCollectionforInitialization(event)
		self.mTauJet.setupCollectionforInitialization(event)
		self.mTauMuon.setupCollectionforInitialization(event)

		self.IsoRemElectron.setupCollectionforInitialization(event)	
		self.LooseCutBasedElectron.setupCollectionforInitialization(event)		



	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		print ("Number of Bad Events ", self.countBadevents)
		if self.countBadevents!=0:
			save_path = MYDIR=os.getcwd() + "/badEvents"
			file_name = "badEvents_"+str(self.filename)+"_"+str(self.channel)
			complete_Name =  os. path. join(save_path, file_name)
			file = open(complete_Name,"w")
			file.write("The Bad events for this file "+str(self.filename)+" is "+str(self.countBadevents))
			file.close()	
	
	#Not used for now
	def HPStauVeto(self,tauCollectionObject):
		isTau =""
		tau1 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		tau2 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		tau1.SetPtEtaPhiM(tauCollectionObject.pt,tauCollectionObject.eta,tauCollectionObject.phi,tauCollectionObject.mass)
		for boostedtau in self.boostedTau.collection:
			tau2.SetPtEtaPhiM(boostedtau.pt,boostedtau.eta,boostedtau.phi,boostedtau.mass)
			deltaR = tau1.DeltaR(tau2)
			if deltaR <= 0.02:
				isTau = "bad"
				break
		
		if isTau != "bad":
			return True
		else:
			return False

	def FatJetConeIsolation(self,CollectionObject): # Function used by electron and muon
		#isObj =""
		obj1 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		obj2 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)	
		obj1.SetPtEtaPhiM(CollectionObject.pt,CollectionObject.eta,CollectionObject.phi,CollectionObject.mass)

		fatjet = self.FatJet.collection[0]
		obj2.SetPtEtaPhiM(fatjet.pt,fatjet.eta,fatjet.phi,fatjet.mass)
		deltaR = obj1.DeltaR(obj2)
		if deltaR > 0.8:
			return True
		else:
			return False	


		#for fatjet in self.FatJet.collection:
		#	obj2.SetPtEtaPhiM(fatjet.pt,fatjet.eta,fatjet.phi,fatjet.mass)
		#	deltaR = obj1.DeltaR(obj2)
		#	if deltaR <= 0.8:
		#		isObj = "bad"
		#		break
		#
		#if isObj != "bad":
		#	return True
		#else:
		#	return False
	
	#Used to filter AK4 Jets
	def JetFatJetIsolation(self,CollectionObject):
		#isObj =""
		Jet = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		bigJet = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		Jet.SetPtEtaPhiM(CollectionObject.pt,CollectionObject.eta,CollectionObject.phi,CollectionObject.mass)

		fatjet = self.FatJet.collection[0]
		bigJet.SetPtEtaPhiM(fatjet.pt,fatjet.eta,fatjet.phi,fatjet.mass)
		deltaR = Jet.DeltaR(bigJet)
		if deltaR > 1.2:
			return True
		else:
			return False




		#for fatjet in self.FatJet.collection:
		#	bigJet.SetPtEtaPhiM(fatjet.pt,fatjet.eta,fatjet.phi,fatjet.mass)
		#	deltaR = Jet.DeltaR(bigJet)
		#	if deltaR <= 1.2:
		#		isObj = "bad"
		#		break
		#
		#if isObj != "bad":
		#	return True
		#else:
		#	return False

	#Used to filter Taus taus
	def FatJetTauOverlap(self,CollectionObject):
		#isObj =""
		bigJet = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		tau = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		tau.SetPtEtaPhiM(CollectionObject.pt,CollectionObject.eta,CollectionObject.phi,CollectionObject.mass)

		fatjet = self.FatJet.collection[0]
		bigJet.SetPtEtaPhiM(fatjet.pt,fatjet.eta,fatjet.phi,fatjet.mass)

		deltaR = tau.DeltaR(bigJet)
		if deltaR > 1.5:
			return True
		else:
			return False

		

		#for fatjet in self.FatJet.collection:
		#	bigJet.SetPtEtaPhiM(fatjet.pt,fatjet.eta,fatjet.phi,fatjet.mass)
		#	deltaR = tau.DeltaR(bigJet)
		#	if deltaR <= 1.5:
		#		isObj = "bad"
		#	break
		#
		#if isObj != "bad":
		#	return True
		#else:
		#	return False

		
	
	def ElectronTauOverlap(self,CollectionObject):
		isObj =""
		tau = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		lepton = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		tau.SetPtEtaPhiM(CollectionObject.pt,CollectionObject.eta,CollectionObject.phi,CollectionObject.mass)
		for electron in self.Electron.collection:
			lepton.SetPtEtaPhiM(electron.pt,electron.eta,electron.phi,electron.mass)
			deltaR = tau.DeltaR(lepton)
			if deltaR <= 0.05:
				isObj = "bad"
				break
		
		if isObj != "bad":
			return True
		else:
			return False	


	def MuonTauOverlap(self,CollectionObject):
		isObj =""
		tau = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		lepton = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
		tau.SetPtEtaPhiM(CollectionObject.pt,CollectionObject.eta,CollectionObject.phi,CollectionObject.mass)
		for muon in self.Muon.collection:
			lepton.SetPtEtaPhiM(muon.pt,muon.eta,muon.phi,muon.mass)
			deltaR = tau.DeltaR(lepton)
			if deltaR <= 0.05:
				isObj = "bad"
				break
		
		if isObj != "bad":
			return True
		else:
			return False
		

	def selfPairing(self,col1):
		combinedPt = -10
		index1 =-1
		index2 = -1
		if len(col1)<=1:
			return (combinedPt,index1,index2)
		for i in range(len(col1)):
			for j in range(i+1,len(col1)):
				#Check with Camilla if this conditon is necesary at all
				#if ((col1[i].p4()).DeltaR(col1[j].p4()) < 0.05):
				#	continue
				sumFourVector = col1[i].p4() + col1[j].p4()	
				pt = sumFourVector.Pt()
				if pt >= combinedPt:
					combinedPt = pt
					index1 = i
					index2 = j
		
		return (combinedPt,index1,index2)
	
	def ElectronIsolationCut(self,tau,ele,tag): #passing the inidivial eletrons from the collection to apply the correction
		isolationCut = 0.0

		if abs(ele.eta) <= 1.479:
			isolationCut = 0.175
		elif (abs(ele.eta) > 1.479) and (abs(ele.eta) <= 2.5):
			isolationCut = 0.159
		else:
			return False

		if (tag == "te" or tag=="be"):
			if ((ele.pfRelIso03_all) < isolationCut):
				return True
			else:
				return False
		
	
	def MuonIsolationCut (self,tau,muo,tag):
		isolationCut = 0.25

		if (tag == "tm" or tag =="bm"):
			if ((muo.pfRelIso04_all) <  isolationCut):
				return True
			else:
				return False


			


	
	def crossPairing(self,col1,col2,tag):
		combinedPt = -10
		index1 =-1
		index2 = -1
		if (len(col1)==0 or len(col2)==0):
			return (combinedPt,index1,index2)
		for i in range(len(col1)):
			for j in range(len(col2)):
				if (tag == "be" or tag == "te"):
					if not self.ElectronIsolationCut(col1[i],col2[j],tag):
						continue
				
				elif (tag == "bm" or tag =="tm"):
					if not self.MuonIsolationCut(col1[i],col2[j],tag):
						continue

				sumFourVector = col1[i].p4() + col2[j].p4()
				pt = sumFourVector.Pt()
				if pt >= combinedPt:
					combinedPt = pt
					index1 = i
					index2 = j
		
		return (combinedPt,index1,index2)

	#def pass_cuts_EleID(bitmap,electronObject):
	#	for  cutnr in range(0,10):
	#		if cutnr==7:
	#			continue
	#		if (electronObject.vidNestedWPBitmap >> (cutnr*3) & 0x7) < 2:
	#			return False
	#	return True
			
	def pass_cuts_EleID(self,electronObject):
		for  cutnr in range(0,10):
			if cutnr==7:
				continue
			if (electronObject.vidNestedWPBitmap >> (cutnr*3) & 0x7) < self.eleID:
				return False
		return True



	def analyze(self, event): 

		#for nPart in range(event.nGenPart):
			#print ("Gen Part Status in first module = ",event.GenPart_status[nPart],event.GenPart_pdgId[nPart])
		list = {} # to store the combined pt and the indices of the pairs

		if self.setUp==None:
			self.setup_collection(event)
			self.setup_branches()
			self.out.fillBranch("eleID",self.eleID)
			self.out.fillBranch("muID",self.muID)
			self.out.fillBranch("tauID",self.tauID)
			self.out.fillBranch("btauID",self.btauID)
			self.setUp = "Done"



		#Select the AK4 Jets and keep choose Jets with Tight DeepJet ID
		self.Jet.setupCollection(event)
		#Apply a tight ID for ak4 jet - but not using it in for veto yet
		self.Jet.apply_cut(lambda x: (x.pt > 20) and (x.btagDeepB >= 0.8767))
		
		self.Tau.setupCollection(event)
		#self.Tau.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idDeepTau2017v2p1VSjet & 1 == 1))  #Deeptau ID for the standard Taus loosest WP
		self.Tau.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idDecayModeNewDMs) and (x.idDeepTau2017v2p1VSjet & self.tauID == self.tauID) and ((x.decayMode == 0) or (x.decayMode == 1) or (x.decayMode == 2) or (x.decayMode == 7) or (x.decayMode == 10) or (x.decayMode == 11))) #VVVLoose
		#self.Tau.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idDeepTau2017v2p1VSjet & 2 == 2)) #VVLoose
		#self.Tau.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idDeepTau2017v2p1VSjet & 4 == 4)) #VLoose


		self.boostedTau.setupCollection(event)
		#self.boostedTau.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 2 == 2)) # VLoose ID for newMVA for boosted Taus - but use oldMVA weight
		self.boostedTau.apply_cut(lambda x: (x.pt > 40) and (abs(x.eta) < 2.3) and (x.idDecayModeNewDMs) and (x.idMVAnewDM2017v2 & self.btauID == self.btauID) and ((x.decayMode == 0) or (x.decayMode == 1) or (x.decayMode == 2) or (x.decayMode == 7) or (x.decayMode == 10) or (x.decayMode == 11))) # VVLoose
		#self.boostedTau.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 2 == 2)) # VLoose
		#self.boostedTau.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 4 == 4)) # Loose

		#self.Tau.collection =  filter(self.HPStauVeto,self.Tau.collection) #HPS veto applied - if a HPS tau and a boosted Tau are on top of each other then throw away the HPS Tau

		self.FatJet.setupCollection(event)
		try:
			#self.FatJet.apply_cut(lambda x: (x.pt > 200) and (abs(x.eta) < 2.4) and (x.msoftdrop > 30) and (x.msoftdrop < 250) and ((x.tau2/x.tau1) < 0.75))
			#self.FatJet.apply_cut(lambda x: (x.pt > 200) and (abs(x.eta) < 2.4) and (x.msoftdrop > 30) and (x.msoftdrop < 250) and x.jetId>=2 and ((x.tau2/x.tau1) < 0.75))
			self.FatJet.apply_cut(lambda x: (x.pt > 200) and (abs(x.eta) < 2.4) and (x.msoftdrop > 30) and (x.msoftdrop < 250) and x.jetId>=2)	
		except ZeroDivisionError:
			self.countBadevents += 1
			print("Error:(")
			traceback.print_exc()
			return False
		
		if (len(self.FatJet.collection))==0:
			return False	


###################CutBased ID Check ##################################################################
		self.IsoRemElectron.setupCollection(event)
		self.IsoRemElectron.apply_cut(lambda x: x.pt > 10)
		self.IsoRemElectron.collection = filter (self.pass_cuts_EleID,self.IsoRemElectron.collection)

		self.LooseCutBasedElectron.setupCollection(event)
		self.LooseCutBasedElectron.apply_cut(lambda x: x.cutBased>=self.eleID and (x.pt > 10))

########################################################################################################


		self.Electron.setupCollection(event)
		#self.Electron.apply_cut(lambda x: x.cutBased>=2 and (x.pt > 10))
		self.Electron.apply_cut(lambda x: x.pt > 10)
		self.Electron.collection = filter(self.pass_cuts_EleID,self.Electron.collection)
		#self.Electron.collection = filter(self.Electron.relativeIso,self.Electron.collection)

		self.Muon.setupCollection(event)

		if self.muID == 2:
			self.Muon.apply_cut(lambda x: x.pt > 10 and x.looseId)
		elif self.muID == 3:
			self.Muon.apply_cut(lambda x: x.pt > 10 and x.mediumId)
		elif self.muID == 4:
			self.Muon.apply_cut(lambda x: x.pt > 10 and x.tightId)
		#self.Muon.apply_cut(lambda x: x.pt > 10 and x.mvaId >= 1 and ((x.pfRelIso03_all/x.pt) < 0.25))

		#filter Objects to remove those within the fatjet cone - only the leading FatJet Considered (0.8 is the distance measure)
		self.Electron.collection = filter(self.FatJetConeIsolation,self.Electron.collection)
		self.Muon.collection = filter(self.FatJetConeIsolation,self.Muon.collection)

		#Tau and FatJet should be more than 1.5 distance apart
		self.Tau.collection = filter(self.FatJetTauOverlap,self.Tau.collection)
		self.boostedTau.collection = filter(self.FatJetTauOverlap,self.boostedTau.collection)
	
		#filter the AK4 Jet collection for FatJet and Ak4 Jet overlap, 1.2 distance apart
		self.Jet.collection = filter(self.JetFatJetIsolation,self.Jet.collection)

		#remove light lepton and tau overlap dist 0.05 ->0.02()
		self.Tau.collection = filter(self.ElectronTauOverlap,self.Tau.collection)
		self.Tau.collection = filter(self.MuonTauOverlap,self.Tau.collection)

		self.boostedTau.collection = filter(self.ElectronTauOverlap,self.boostedTau.collection)
		self.boostedTau.collection = filter(self.MuonTauOverlap,self.boostedTau.collection)

		if (len(self.FatJet.collection)>0):
			list["bb"]=self.selfPairing(self.boostedTau.collection)
			list["tt"]=self.selfPairing(self.Tau.collection)
			#list["bt"]=self.crossPairing(self.boostedTau.collection,self.Tau.collection,"bt")
			list["be"]=self.crossPairing(self.boostedTau.collection,self.Electron.collection,"be")
			list["bm"]=self.crossPairing(self.boostedTau.collection,self.Muon.collection,"bm")
			list["te"]=self.crossPairing(self.Tau.collection,self.Electron.collection,"te")
			list["tm"]=self.crossPairing(self.Tau.collection,self.Muon.collection,"tm")

			#print (list)

			Keymax = max(list, key = lambda x: list[x][0])
			

			if (list[Keymax][0]>0):
				#Fill out combined pt as a branch
				self.out.fillBranch("combPt",list[Keymax][0])

				if (list["bb"][0]> 0 or list["tt"][0]>0):
					self.out.fillBranch("tt",1)
					self.diTauFatJet.collection = self.FatJet.collection
					self.diTauJet.collection=self.Jet.collection
					if (list["bb"][0] >= list["tt"][0]):
						self.diTauboostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==list["bb"][1] or self.boostedTau.collection.index(obj)==list["bb"][2]]
						self.diTauTau.collection=[]
						self.out.fillBranch("diTauCombPt",list["bb"][0])

					elif(list["bb"][0] < list["tt"][0]):
						self.diTauTau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==list["tt"][1] or self.Tau.collection.index(obj)==list["tt"][2]]
						self.diTauboostedTau.collection=[]
						self.out.fillBranch("diTauCombPt",list["tt"][0])
				else:
						self.diTauboostedTau.collection=[]
						self.diTauTau.collection=[]
						self.diTauFatJet.collection=[]
						self.diTauJet.collection=[]
						self.out.fillBranch("tt",0)
						self.out.fillBranch("diTauCombPt",-1.0)

				if (list["be"][0]> 0 or list["te"][0]>0):
					#print ("momentum = ",list["be"][0],list["te"][0])
					self.out.fillBranch("et",1)
					self.eTauFatJet.collection=self.FatJet.collection
					self.eTauJet.collection = self.Jet.collection
					if (list["be"][0] >= list["te"][0]):
						self.eTauboostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==list["be"][1]]
						self.eTauElectron.collection= [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==list["be"][2]]
						self.eTauTau.collection=[]
						self.out.fillBranch("eTauCombPt",list["be"][0])

					elif(list["be"][0] < list["te"][0]):
						self.eTauTau.collection =[obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==list["te"][1]]
						self.eTauElectron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==list["te"][2]]
						self.eTauboostedTau.collection=[]
						self.out.fillBranch("eTauCombPt",list["te"][0])

				else:
					self.eTauTau.collection=[]
					self.eTauElectron.collection=[]
					self.eTauboostedTau.collection=[]
					self.eTauFatJet.collection=[]
					self.eTauJet.collection=[]
					self.out.fillBranch("et",0)
					self.out.fillBranch("eTauCombPt",-1.0)

				if (list["bm"][0]> 0 or list["tm"][0]>0):
					self.out.fillBranch("mt",1)
					self.mTauFatJet.collection=self.FatJet.collection
					self.mTauJet.collection = self.Jet.collection				
					if (list["bm"][0] >= list["tm"][0]):
						self.mTauboostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==list["bm"][1]]
						self.mTauMuon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==list["bm"][2]]
						self.mTauTau.collection =[]
						self.out.fillBranch("mTauCombPt",list["bm"][0])
					elif (list["bm"][0] < list["tm"][0]):
						self.mTauTau.collection =  [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==list["tm"][1]]
						self.mTauMuon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==list["tm"][2]]
						self.mTauboostedTau.collection = []
						self.out.fillBranch("mTauCombPt",list["tm"][0])
				else:
					self.mTauboostedTau.collection = []
					self.mTauMuon.collection = []
					self.mTauTau.collection = []
					self.mTauFatJet.collection = []
					self.mTauJet.collection = []
					self.out.fillBranch("mt",0)
					self.out.fillBranch("mTauCombPt",-1.0)
				
				self.diTauboostedTau.fillBranches(self.out,"tt")
				self.diTauTau.fillBranches(self.out,"tt")
				self.diTauFatJet.fillBranches(self.out,"tt")
				self.diTauJet.fillBranches(self.out,"tt")

				self.eTauTau.fillBranches(self.out,"et")
				self.eTauElectron.fillBranches(self.out,"et")
				self.eTauboostedTau.fillBranches(self.out,"et")
				self.eTauFatJet.fillBranches(self.out,"et")
				self.eTauJet.fillBranches(self.out,"et")

				self.mTauboostedTau.fillBranches(self.out,"mt")
				self.mTauMuon.fillBranches(self.out,"mt")
				self.mTauTau.fillBranches(self.out,"mt")
				self.mTauFatJet.fillBranches(self.out,"mt")
				self.mTauJet.fillBranches(self.out,"mt")

				#Fill the branches created for Electron ID verification
				self.IsoRemElectron.fillBranches(self.out,"IsoRem")
				self.LooseCutBasedElectron.fillBranches(self.out,"LooseCB")

				#print(Keymax)
				if Keymax == "bb":
					self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==list[Keymax][1] or self.boostedTau.collection.index(obj)==list[Keymax][2]]
					#self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==-1 or self.Tau.collection.index(obj)==-1]
					self.Tau.collection=[]
					self.Muon.collection=[]
					self.Electron.collection=[]
					#self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==-1 or self.Electron.collection.index(obj)==-1]
					#self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==-1 or self.Muon.collection.index(obj)==-1]
					self.out.fillBranch("channel",0)
			#	elif Keymax == "bt":
			#		self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==list[Keymax][1]]
			#		self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==list[Keymax][2]]
			#		self.Muon.collection = []
			#		self.Electron.collection = []
			#		#print ("Channel = ",Keymax,"Tau collection length = ",len(self.Tau.collection))
			#		#self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==-1]
			#		#self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==-1]
			#		self.out.fillBranch("channel",0)					

				elif Keymax == "tt":
					#self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==-1]
					self.boostedTau.collection = []
					self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==list[Keymax][1] or self.Tau.collection.index(obj)==list[Keymax][2]]
					self.Electron.collection = []
					self.Muon.collection = []
					#print ("Channel = ",Keymax,"Tau collection length = ",len(self.Tau.collection))
					#self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==-1]
					#self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==-1]
					self.out.fillBranch("channel",0)

				elif Keymax == "te":
					#self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==-1]
					self.boostedTau.collection = []
					self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==list[Keymax][1]]
					self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==list[Keymax][2]]
					#self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==-1]
					#print ("Channel = ",Keymax,"Tau collection length = ",len(self.Tau.collection))
					self.Muon.collection = []
					self.out.fillBranch("channel",1)
				
				elif Keymax == "be":
					self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==list[Keymax][1]]
					#self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==-1]
					self.Tau.collection = []
					self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==list[Keymax][2]]
					#self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==-1]
					self.Muon.collection = []
					self.out.fillBranch("channel",1)

				elif Keymax == "tm":
					#self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==-1]
					self.boostedTau.collection = []
					self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==list[Keymax][1]]
					#self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==-1]
					self.Electron.collection = []
					#print ("Channel = ",Keymax,"Tau collection length = ",len(self.Tau.collection))
					self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==list[Keymax][2]]
					self.out.fillBranch("channel",2)

				elif Keymax == "bm":
					self.boostedTau.collection = [obj for obj in self.boostedTau.collection if self.boostedTau.collection.index(obj)==list[Keymax][1]]
					#self.Tau.collection = [obj for obj in self.Tau.collection if self.Tau.collection.index(obj)==-1]
					self.Tau.collection = []
					#self.Electron.collection = [obj for obj in self.Electron.collection if self.Electron.collection.index(obj)==-1]
					self.Electron.collection = []
					self.Muon.collection = [obj for obj in self.Muon.collection if self.Muon.collection.index(obj)==list[Keymax][2]]
					self.out.fillBranch("channel",2)
				else:
					print ("KeyMax = ",Keymax)
					print ("This also happens")
				
				self.Tau.fillBranches(self.out)
				self.FatJet.fillBranches(self.out)
				self.boostedTau.fillBranches(self.out)
				self.Muon.fillBranches(self.out)
				self.Electron.fillBranches(self.out)
				self.Jet.fillBranches(self.out)
				
				
				return True

			else:
				return False	
				
		else:
			return False	
			


def call_postpoc(files):
		letsSortChannels = lambda: ChannelCamilla(filename,args.eleID,args.muID,args.tauID,args.btauID)
		tauOdering = lambda: mergeTauCamilla(filename)
		tauOdering2 = lambda: mergeTauPart2(filename)
		visibleM = lambda:VisibleMassCamilla()
		visibleM2 = lambda:VisibleMassPart2()
		mttBranches = lambda:fastMTTBranches(filename)
		genMatch = lambda:LeptonMC_MatchingWithTausAndBQuark()
		genMeasurementRadion = lambda:genMeasurementRadionBranches(filename)
		twotauFatJetMatching = lambda:tauSystemFatJetMatching()

		#radBranches = lambda:genMeasurementRadionBranches(filename)
		nameStrip=files.strip()
		filename = (nameStrip.split('/')[-1]).split('.')[-2]
		try:
			#if filename == "Data":
			if (search("Data", filename) or search("2016", filename)):
				p = PostProcessor(outputDir,[files], cut=cutsData, branchsel=outputbranches,modules=[letsSortChannels(),tauOdering(),tauOdering2(),visibleM(),visibleM2(),mttBranches(),twotauFatJetMatching()], postfix=post,noOut=False,outputbranchsel=outputbranches)
			elif search("Radion", filename):
				p = PostProcessor(outputDir,[files], cut=cuts, branchsel=outputbranches,modules=[letsSortChannels(),tauOdering(),tauOdering2(),visibleM(),visibleM2(),mttBranches(),genMatch(),genMeasurementRadion(),twotauFatJetMatching()], postfix=post,noOut=False,outputbranchsel=outputbranches)
			else:
				p = PostProcessor(outputDir,[files], cut=cuts, branchsel=outputbranches,modules=[letsSortChannels(),tauOdering(),tauOdering2(),visibleM(),visibleM2(),mttBranches(),twotauFatJetMatching()], postfix=post,noOut=False,outputbranchsel=outputbranches)
		except SystemError:
			print ("File Causing Issue = ",filename)

		p.run()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
	#parser.add_argument('--Channel',help="enter either tt or et or mt. For boostedTau test enter test",required=True,choices=['tt', 'et', 'mt'])
	parser.add_argument('--inputLocation','-i',help="enter the path to the location of input file set",default="")
	parser.add_argument('--outputLocation','-o',help="enter the path where yu want the output files to be stored",default ="")
	parser.add_argument('--ncores','-n',help ="number of cores for parallel processing", default=1)
	parser.add_argument('--postfix',help="string at the end of output file names", default="")
	parser.add_argument('--year','-y',help='specify the run - to make sure right triggers are used',choices=['2016','2016APV','2017','2018'])
	parser.add_argument('--eleID','-eId',help="Specify the ID for the electrons to be selected 2-Loose, 3-Medium, 4-Tight",choices=['2','3','4'])
	parser.add_argument('--muID','-mId',help="Specify the ID for the muons to be selected 2-Loose, 3-Medium, 4-Tight (to keep it consistent with the electrons)",choices=['2','3','4'])
	parser.add_argument('--tauID','-tId',help="DeepTau 1 = VVVLoose, 2 = VVLoose, 4 = VLoose, 8 = Loose, 16 = Medium, 32 = Tight, 64 = VTight, 128 = VVTight",choices=['1','2','4','8','16','32','64','128'])
	parser.add_argument('--btauID','-btId',help="VAnewDM2017v2 1 = VVLoose, 2 = VLoose, 4 = Loose, 8 = Medium, 16 = Tight, 32 = VTight, 64 = VVTight",choices=['1','2','4','8','16','32','64'])

	#parser.add_argument('--bTauid',help="ID for the boosted taus",choices=[""],required=True)
	#parser.add_argument('--Tauid',help="ID for the hps taus",required=True)	
	args = parser.parse_args()

	#Define Event Selection - all those to be connected by and
	eventSelectionAND = ["MET_pt>200",
						"PV_ndof > 4",
						"abs(PV_z) < 24",
						"sqrt(PV_x*PV_x+PV_y*PV_y) < 2",
						"Flag_goodVertices",
						"Flag_globalSuperTightHalo2016Filter", 
						"Flag_HBHENoiseIsoFilter",
						"Flag_HBHENoiseFilter",
						"Flag_EcalDeadCellTriggerPrimitiveFilter",
						"Flag_BadPFMuonFilter",
						"Flag_eeBadScFilter"]
	
	eventSelectionANDData = ["MET_pt>200",
							"PV_ndof > 4",
							"abs(PV_z) < 24",
							"sqrt(PV_x*PV_x+PV_y*PV_y) < 2",
							"Flag_goodVertices",
							"Flag_globalSuperTightHalo2016Filter", 
							"Flag_HBHENoiseIsoFilter",
							"Flag_HBHENoiseFilter",
							"Flag_EcalDeadCellTriggerPrimitiveFilter",
							"Flag_BadPFMuonFilter",
							"Flag_eeBadScFilter"]

	#Define Eevnt Selection - all those to be connected by or

	eventSelectionOR_2016 = ["HLT_PFMETNoMu90_PFMHTNoMu90_IDTight",
            			"HLT_PFMETNoMu110_PFMHTNoMu110_IDTight",
            			"HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
            			"HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight",
            			"HLT_PFMET110_PFMHT110_IDTight",
            			"HLT_PFMET120_PFMHT120_IDTight",
            			#"HLT_PFMET170_NoiseCleaned",
            			"HLT_PFMET170_HBHECleaned",
            			"HLT_PFMET170_HBHE_BeamHaloCleaned"]
	
	eventSelectionOR_2016APV = ["HLT_PFMETNoMu90_PFMHTNoMu90_IDTight",
            			"HLT_PFMETNoMu110_PFMHTNoMu110_IDTight",
            			"HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
            			"HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight",
            			"HLT_PFMET110_PFMHT110_IDTight",
            			"HLT_PFMET120_PFMHT120_IDTight",
            			#"HLT_PFMET170_NoiseCleaned",
            			"HLT_PFMET170_HBHECleaned"]
            			#"HLT_PFMET170_HBHE_BeamHaloCleaned"]	


	#fnames = ["/data/aloeliger/bbtautauAnalysis/2016/Data.root"]
	fnames = glob.glob(args.inputLocation + "/*.root")  #making a list of input files
	#outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/{}_Channel".format(args.Channel)
	outputDir = args.outputLocation
	#outputDir = "."
	outputbranches = "keep_and_drop.txt"
	cut1 = "&&".join(eventSelectionAND)
	cut3 = "&&".join(eventSelectionANDData)

	if args.year == '2016':
		cut2 = "||".join(eventSelectionOR_2016)
	elif args.year == '2016APV':
		cut2 = "||".join(eventSelectionOR_2016APV)	
	
	cuts = "("+cut1+")"+"&&"+"("+cut2+")"
	cutsData = "("+cut3+")"+"&&"+"("+cut2+")"
	print ("cuts = ",cuts)
	#post ="_{}Channel".format(str(args.Channel))
	post = args.postfix
	argList = list()
	filename =""
	for file in fnames:
		argList.append(file)
		#nameStrip = file.strip()
    	#filename = (nameStrip.split('/')[-1]).split('.')[-2]
	
	#print (argList)

	if int(args.ncores) == 1:
		for arr in argList:
			#print ("This is what is passed ",arr[1])
			call_postpoc(arr)
	
	else:
		try:
			pool = np.Pool(int(args.ncores))
			#with np.Pool(object,ncores) as pool:
			print ("list", argList)
			res=pool.map(call_postpoc, argList)
		#except:
		except Exception:
			traceback.print_exc()
			print ("Error using the multiprocessing package")
