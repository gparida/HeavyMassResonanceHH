from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import glob
import argparse
import multiprocessing as  np


def call_postpoc(files):

		#radBranches = lambda:genMeasurementRadionBranches(filename)
		nameStrip=files.strip()
		filename = (nameStrip.split('/')[-1]).split('.')[-2]
		if filename == "Data":
			p = PostProcessor(outputDir,[files], cut=cutsData,branchsel=outputbranches,modules=[], postfix=post,noOut=False,outputbranchsel=outputbranches)
		else:
			p = PostProcessor(outputDir,[files], cut=cuts,branchsel=outputbranches,modules=[], postfix=post,noOut=False,outputbranchsel=outputbranches)


		p.run()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
	#parser.add_argument('--Channel',help="enter either tt or et or mt. For boostedTau test enter test",required=True,choices=['tt', 'et', 'mt'])
	parser.add_argument('--inputLocation',help="enter the path to the location of input file set",default="")
	parser.add_argument('--outputLocation',help="enter the path where yu want the output files to be stored",default ="")
	parser.add_argument('--ncores',help ="number of cores for parallel processing", default=1)
	parser.add_argument('--postfix',help="string at the end of output file names", default="")
	parser.add_argument('--year',help='specify the run - to make sure right triggers are used',choices=['2016','2016APV','2017','2018'])
	#parser.add_argument('--bTauid',help="ID for the boosted taus",choices=[""],required=True)
	#parser.add_argument('--Tauid',help="ID for the hps taus",required=True)	
	args = parser.parse_args()

	#Define Event Selection - all those to be connected by and
	eventSelectionAND = ["MET_pt>200",
						"genWeight>0",
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

	eventSelectionOR_2016 = [#"HLT_PFMETNoMu90_PFMHTNoMu90_IDTight",
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
	fnames = glob.glob(args.inputLocation + "/RadionTohhTohtatahbb_narrow_M-2000*.root")  #making a list of input files
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
		pool = np.Pool(int(args.ncores))
		#with np.Pool(object,ncores) as pool:
		print ("list", argList)
		res=pool.map(call_postpoc, argList)
