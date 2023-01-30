
import ROOT
import math 
import time
from plot_dict import *
import argparse

parser = argparse.ArgumentParser(description='Compute Reco + ID efficiency for a signal Sample')
parser.add_argument('--signal','-F',help="file name including the path",required=True)
parser.add_argument('--mp',help="goes in the file name of the plots",required=True)
args = parser.parse_args()


#rejected = 0
#rejected_one = 0

tt_higgspt_pass = [ROOT.TH1F("tt_higgspt_pass_{}".format(str(i)),"tt_higgspt_pass_{}".format(str(i)), 24,  400, 1000) for i in range(1)]
tt_higgspt_pass_b = [ROOT.TH1F("tt_higgspt_pass_b_{}".format(str(i)),"tt_higgspt_pass_b_{}".format(str(i)), 24,  400, 1000) for i in range(1)]
#tt_higgspt_total = [ROOT.TH1F("tt_higgspt_total_{}".format(str(i)),"tt_higgspt_total_{}".format(str(i)), 24,  400, 1000) for i in range(1)]
tt_higgspt_total = ROOT.TH1F("tt_higgspt_total","tt_higgspt_total",24,  400, 1000)

tt_taupt_pass = [ROOT.TH1F("tt_taupt_pass_{}".format(str(i)),"tt_taupt_pass_{}".format(str(i)), 80,  0, 2000) for i in range(1)]
tt_taupt_pass_b = [ROOT.TH1F("tt_taupt_pass_b_{}".format(str(i)),"tt_taupt_pass_b_{}".format(str(i)), 80,  0, 2000) for i in range(1)]
#tt_higgspt_total = [ROOT.TH1F("tt_higgspt_total_{}".format(str(i)),"tt_higgspt_total_{}".format(str(i)), 80,  0, 2000) for i in range(1)]
tt_taupt_total = ROOT.TH1F("tt_taupt_total","tt_taupt_total",80,  0, 2000)


tt_delR_pass = [ROOT.TH1F("tt_delR_pass_{}".format(str(i)),"tt_delR_pass_{}".format(str(i)), 40, 0, 2) for i in range(1)]
tt_delR_pass_b = [ROOT.TH1F("tt_delR_pass_b_{}".format(str(i)),"tt_delR_pass_b_{}".format(str(i)), 40, 0, 2) for i in range(1)]
#tt_delR_total = [ROOT.TH1F("tt_delR_total_{}".format(str(i)),"tt_delR_total_{}".format(str(i)), 40, 0, 2) for i in range(1)]
tt_delR_total = ROOT.TH1F("tt_delR_total","tt_delR_total",40, 0, 2)



tt_one_higgspt_pass = [ROOT.TH1F("tt_one_higgspt_pass_{}".format(str(i)),"tt_one_higgspt_pass_{}".format(str(i)), 24,  400, 1000) for i in range(1)]
tt_one_higgspt_pass_b = [ROOT.TH1F("tt_one_higgspt_pass_b_{}".format(str(i)),"tt_one_higgspt_pass_b_{}".format(str(i)), 24,  400, 1000) for i in range(1)]
#tt_one_higgspt_total = ROOT.TH1F("tt_one_higgspt_total","tt_one_higgspt_total",24,  400, 1000)

tt_one_delR_pass = [ROOT.TH1F("tt_one_delR_pass_{}".format(str(i)),"tt_one_delR_pass_{}".format(str(i)), 40, 0, 2) for i in range(1)]
tt_one_delR_pass_b = [ROOT.TH1F("tt_one_delR_pass_b_{}".format(str(i)),"tt_one_delR_pass_b_{}".format(str(i)), 40, 0, 2) for i in range(1)]

tt_one_taupt_pass = [ROOT.TH1F("tt_one_taupt_pass_{}".format(str(i)),"tt_one_taupt_pass_{}".format(str(i)), 80,  0, 2000) for i in range(1)]
tt_one_taupt_pass_b = [ROOT.TH1F("tt_one_taupt_pass_b_{}".format(str(i)),"tt_one_taupt_pass_b_{}".format(str(i)), 80,  0, 2000) for i in range(1)]


et_higgspt_pass = [ROOT.TH1F("et_higgspt_pass_{}".format(str(i)),"et_higgspt_pass_{}".format(str(i)), 24,  400, 1000) for i in range(1)]
et_higgspt_pass_b = [ROOT.TH1F("et_higgspt_pass_b_{}".format(str(i)),"et_higgspt_pass_b_{}".format(str(i)), 24,  400, 1000) for i in range(1)]
#et_higgspt_total = [ROOT.TH1F("et_higgspt_total_{}".format(str(i)),"et_higgspt_total_{}".format(str(i)), 24,  400, 1000) for i in range(1)]
et_higgspt_total = ROOT.TH1F("et_higgspt_total","et_higgspt_total",24,  400, 1000)

et_taupt_pass = [ROOT.TH1F("et_taupt_pass_{}".format(str(i)),"et_taupt_pass_{}".format(str(i)), 80,  0, 2000) for i in range(1)]
et_taupt_pass_b = [ROOT.TH1F("et_taupt_pass_b_{}".format(str(i)),"et_taupt_pass_b_{}".format(str(i)), 80,  0, 2000) for i in range(1)]
#et_taupt_total = [ROOT.TH1F("et_taupt_total_{}".format(str(i)),"et_taupt_total_{}".format(str(i)), 80,  0, 2000) for i in range(1)]
et_taupt_total = ROOT.TH1F("et_taupt_total","et_taupt_total",80,  0, 2000)


et_delR_pass = [ROOT.TH1F("et_delR_pass_{}".format(str(i)),"et_delR_pass_{}".format(str(i)), 40, 0, 2) for i in range(1)]
et_delR_pass_b = [ROOT.TH1F("et_delR_pass_b_{}".format(str(i)),"et_delR_pass_b_{}".format(str(i)), 40, 0, 2) for i in range(1)]
#et_delR_total = [ROOT.TH1F("et_delR_total_{}".format(str(i)),"et_delR_total_{}".format(str(i)), 40, 0, 2) for i in range(1)]
et_delR_total = ROOT.TH1F("et_delR_total","et_delR_total",40, 0, 2)



mt_higgspt_pass = [ROOT.TH1F("mt_higgspt_pass_{}".format(str(i)),"mt_higgspt_pass_{}".format(str(i)), 24,  400, 1000) for i in range(1)]
mt_higgspt_pass_b = [ROOT.TH1F("mt_higgspt_pass_b_{}".format(str(i)),"mt_higgspt_pass_b_{}".format(str(i)), 24,  400, 1000) for i in range(1)]
#mt_higgspt_total = [ROOT.TH1F("mt_higgspt_total_{}".format(str(i)),"mt_higgspt_total_{}".format(str(i)),24,  400, 1000) for i in range(1)]
mt_higgspt_total = ROOT.TH1F("mt_higgspt_total","mt_higgspt_total",24,  400, 1000)

mt_taupt_pass = [ROOT.TH1F("mt_taupt_pass_{}".format(str(i)),"mt_taupt_pass_{}".format(str(i)), 80,  0, 2000) for i in range(1)]
mt_taupt_pass_b = [ROOT.TH1F("mt_taupt_pass_b_{}".format(str(i)),"mt_taupt_pass_b_{}".format(str(i)), 80,  0, 2000) for i in range(1)]
#mt_taupt_total = [ROOT.TH1F("mt_taupt_total_{}".format(str(i)),"mt_taupt_total_{}".format(str(i)), 80,  0, 2000) for i in range(1)]
mt_taupt_total = ROOT.TH1F("mt_taupt_total","mt_taupt_total",80,  0, 2000)

mt_delR_pass = [ROOT.TH1F("mt_delR_pass_{}".format(str(i)),"mt_delR_pass_{}".format(str(i)), 40, 0, 2) for i in range(1)]
mt_delR_pass_b = [ROOT.TH1F("mt_delR_pass_b_{}".format(str(i)),"mt_delR_pass_b_{}".format(str(i)), 40, 0, 2) for i in range(1)]
#mt_delR_total = [ROOT.TH1F("mt_delR_total_{}".format(str(i)),"mt_delR_total_{}".format(str(i)),40, 0, 2) for i in range(1)]
mt_delR_total = ROOT.TH1F("mt_delR_total","mt_delR_total",40, 0, 2)

Tau_gen_v1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
Tau_gen_v2 =ROOT.TLorentzVector(0.0,0.0,0.0,0.0) 
Tau_reco=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)

tt_one_eff={}
tt_one_eff_b={}
tt_eff ={}
tt_eff_b={}
et_eff ={}
et_eff_b={}
mt_eff ={}
mt_eff_b={}

delR_tt_one_eff={}
delR_tt_one_eff_b={}
delR_tt_eff ={}
delR_tt_eff_b={}
delR_et_eff ={}
delR_et_eff_b={}
delR_mt_eff ={}
delR_mt_eff_b={}

taupt_tt_one_eff={}
taupt_tt_one_eff_b={}
taupt_tt_eff ={}
taupt_tt_eff_b={}
taupt_et_eff ={}
taupt_et_eff_b={}
taupt_mt_eff ={}
taupt_mt_eff_b={}

def VerfindingMotherPart(tree,Ind,parentId, interId):
    print ("Finding Tau Parent: Current pdg ",tree.GenPart_pdgId[Ind], " Parent pdg = ",tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]])
    if abs(tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]]) == parentId:
        return True
    elif abs(tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]]) == interId:
        return VerfindingMotherPart(tree,tree.GenPart_genPartIdxMother[Ind],parentId,interId)
    else:
        return False

def findingMotherPart(tree,Ind,parentId, interId):
    if abs(tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]]) == parentId:
        return True
    elif abs(tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]]) == interId:
        return findingMotherPart(tree,tree.GenPart_genPartIdxMother[Ind],parentId,interId)
    else:
        return False

def getParentPt(tree,Ind,parentId, interId):
    if abs(tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]]) == parentId:
        return tree.GenPart_pt[tree.GenPart_genPartIdxMother[Ind]]
    elif abs(tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]]) == interId:
        return getParentPt(tree,tree.GenPart_genPartIdxMother[Ind],parentId,interId)
    else:
        return 0

def isTauParent(tree,Ind):
    if (abs(tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]]) == 15):
        if (findingMotherPart(tree,tree.GenPart_genPartIdxMother[Ind],25,15)):
            return True
        else:
            return False 
    #elif(tree.GenPart_genPartIdxMother[Ind]>=0):
    #    return isTauParent(tree,tree.GenPart_genPartIdxMother[Ind])
    #elif(tree.GenPart_genPartIdxMother[Ind]<0):
    else:
        return False

def VerisTauParent(tree,Ind):
    print (("Current pdg = ",tree.GenPart_pdgId[Ind],"Parent pdg = ", tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]]))
    if (abs(tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]]) == 15):
        if (VerfindingMotherPart(tree,tree.GenPart_genPartIdxMother[Ind],25,15)):
            return True
        else:
            return False 
    elif(tree.GenPart_genPartIdxMother[Ind]>=0):
        print ("Parent is not a Tau, Index of the parent = ",tree.GenPart_genPartIdxMother[Ind])
        return VerisTauParent(tree,tree.GenPart_genPartIdxMother[Ind])
    elif(tree.GenPart_genPartIdxMother[Ind]<0):
        print ("Parent is not a Tau, Index of the parent = ",tree.GenPart_genPartIdxMother[Ind])
        return False


#The function to classify the event as a diTau, eTau or mTau for the signal files
def classifyTauDecayMode(theTree):
    
    #particlesWithTauMother = []
    decayMode = []
    visTauInd = []
    genTauInd = []
    genlep = []

    for visInd in range(theTree.nGenVisTau):
        #print (visInd)
        if theTree.GenVisTau_genPartIdxMother[visInd] < 0: #Ignore if the mother index is negative
            #print ("comes here")
            continue
	#print (abs(theTree.GenPart_pdgId[theTree.GenVisTau_genPartIdxMother[visInd]]),(theTree.GenPart_statusFlags[theTree.GenVisTau_genPartIdxMother[visInd]] & 4)== 4,abs(theTree.GenPart_pdgId[theTree.GenPart_genPartIdxMother[theTree.GenVisTau_genPartIdxMother[visInd]]]))
        if ((abs(theTree.GenPart_pdgId[theTree.GenVisTau_genPartIdxMother[visInd]]) == 15)): # Check if the parent is tau and if it is a decay product of Tau
            #if (abs(theTree.GenPart_pdgId[theTree.GenPart_genPartIdxMother[theTree.GenVisTau_genPartIdxMother[visInd]]]) == 25):
            #print (findingMotherPart(theTree,theTree.GenVisTau_genPartIdxMother[visInd],25,15))
            if (findingMotherPart(theTree,theTree.GenVisTau_genPartIdxMother[visInd],25,15)):
                decayMode.append('t')
               
                visTauInd.append(visInd)
                genTauInd.append(theTree.GenVisTau_genPartIdxMother[visInd])
                continue
            
    if len(decayMode) == 2:
        return ''.join(decay for decay in decayMode), visTauInd, genlep, None
    elif len(decayMode) < 2:
        for nPart in range(theTree.nGenPart):
            if ((theTree.GenPart_genPartIdxMother[nPart] < 0) or abs(theTree.GenPart_pdgId[nPart])>100):
                continue
            if(((abs(theTree.GenPart_pdgId[nPart])==13)  or (abs(theTree.GenPart_pdgId[nPart])==11)) and (theTree.GenPart_genPartIdxMother[nPart] not in genTauInd) and ((theTree.GenPart_statusFlags[nPart] & 4)==4)):
                if not (isTauParent(theTree,nPart)):
                    continue
                if ((abs(theTree.GenPart_pdgId[nPart]))==13):
                    decayMode.append('m')
                    #print("here m",decayMode)
                    genlep.append(nPart)
                    genTauInd.append(theTree.GenPart_genPartIdxMother[nPart])
                elif ((abs(theTree.GenPart_pdgId[nPart]))==11):
                    decayMode.append('e')
                    #print("here e",decayMode)
                    genlep.append(nPart)
                    genTauInd.append(theTree.GenPart_genPartIdxMother[nPart])
    else:
        print ("Moree hadronic Taus > 2")
        return "moreh", None, None, None
    
    if (len(decayMode)==1):
        #print ("")
        #print("")
        #print("")
        #print ("One tau", decayMode)
        tau_four_vec_tot = ROOT.TLorentzVector(0.0,0.0,0.0,0.0) 
        ##tau_count = 0
        for nPart in range(theTree.nGenPart):
            if ((theTree.GenPart_genPartIdxMother[nPart] < 0)):
                continue
            if((abs(theTree.GenPart_pdgId[nPart])>100) and (theTree.GenPart_genPartIdxMother[nPart] not in genTauInd) and ((theTree.GenPart_statusFlags[nPart] & 4)==4)):
                if not (isTauParent(theTree,nPart)):
                    continue
                comp_four_vec = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
                comp_four_vec.SetPtEtaPhiM(tree_bbtt.GenPart_pt[nPart],tree_bbtt.GenPart_eta[nPart],tree_bbtt.GenPart_phi[nPart],tree_bbtt.GenPart_mass[nPart])
                tau_four_vec_tot = tau_four_vec_tot + comp_four_vec
        if (tau_four_vec_tot.Pt > 0):
            decayMode.insert(0,'t')
            #print ("Fixed",''.join(decay for decay in decayMode), visTauInd, genlep, tau_four_vec_tot)
            return ''.join(decay for decay in decayMode), visTauInd, genlep, tau_four_vec_tot
        else:
            return "one", None, None, None



        #    if (abs(theTree.GenPart_pdgId[nPart])==15):
        #        tau_count = tau_count + 1
        #        print ("genTauInd = ",genTauInd,"Current Index = ",nPart )
        #        if nPart in genTauInd:
        #            continue
        #        for nPart2 in range(theTree.nGenPart):
        #            if (theTree.GenPart_genPartIdxMother[nPart2]==nPart):
        #                print ("Daugher of the other tau", theTree.GenPart_pdgId[nPart2])
        #    #print ("Start next gen particle")
            
        #       continue
        #    if(((abs(theTree.GenPart_pdgId[nPart])==13)  or (abs(theTree.GenPart_pdgId[nPart])==11))):
        #        print ("#########################################")
        #        a = VerisTauParent(theTree,nPart)
        #        print ("#########################################")
        #        print ("Printing return Value a = ", a)
        #print ("Gen Tau Count = ",tau_count,"Visible gen Taus = ",theTree.nGenVisTau)

                



	#if len(decayMode)==0:
		#rejected = rejected + 1
	#if len(decayMode)==1:
		#rejected_one = rejected_one + 1
        #print ("less than 2 Taus!", decayMode)
	#print (theTree.GenPart_pdgId[theTree.GenVisTau_genPartIdxMother[0]],theTree.GenPart_pdgId[theTree.GenPart_genPartIdxMother[theTree.GenVisTau_genPartIdxMother[0]]],theTree.nGenPart)
        
    
    if(len(decayMode)==0):
        print ("Empty List")
        return "zero",None,None,None

    if (len(decayMode)>2):
        print ("")
        print("")
        print("")
        print ("More leptonic Taus!", decayMode)
        #print ("One tau", decayMode)
        tau_count = 0
        for nPart in range(theTree.nGenPart):
            if (abs(theTree.GenPart_pdgId[nPart])==15):
                tau_count = tau_count + 1
                print ("genTauInd = ",genTauInd,"Current Index = ",nPart, "Index of Parent of this tau = ",theTree.GenPart_genPartIdxMother[nPart],"pdg of parent of tau = ",theTree.GenPart_pdgId[theTree.GenPart_genPartIdxMother[nPart]])
                #if nPart in genTauInd:
                #    continue
                for nPart2 in range(theTree.nGenPart):
                    if (theTree.GenPart_genPartIdxMother[nPart2]==nPart):
                        print ("Daugher of the other tau", theTree.GenPart_pdgId[nPart2])
            #print ("Start next gen particle")
            if ((theTree.GenPart_genPartIdxMother[nPart] < 0)):
                continue
            if(((abs(theTree.GenPart_pdgId[nPart])==13)  or (abs(theTree.GenPart_pdgId[nPart])==11))):
                print ("#########################################")
                a = VerisTauParent(theTree,nPart)
                print ("#########################################")
                print ("Printing return Value a = ", a)
        print ("Gen Tau Count = ",tau_count,"Visible gen Taus = ",theTree.nGenVisTau)
        #print ("More leptonic Taus!", decayMode)
        return "more", None, None, None
    
    #if (tree_bbtt.GenPart_genPartIdxMother[genTauInd[0]]!=tree_bbtt.GenPart_genPartIdxMother[genTauInd[1]]):
    if (findingMotherPart(theTree,genTauInd[0],25,15) != findingMotherPart(theTree,genTauInd[1],25,15)):
        print ("Error, Taus have different mothers",findingMotherPart(theTree,genTauInd[0],25,15) and findingMotherPart(theTree,genTauInd[1],25,15))
        return None, None, None, None
    
    #print ("eventloop return",''.join(decay for decay in decayMode), len(genlep), theTree.GenPart_pdgId[genlep[0]])
    return ''.join(decay for decay in decayMode), visTauInd, genlep, None

        

def tauMatchedandPassed(tree_bbtt,genFourVec,tau_id):
    i_counter=0
    i_least=0
    delta_r=0
    delta_r_least=0
    for j in range(len(tree_bbtt.Tau_pt)):
        if ((tree_bbtt.Tau_pt[i_least]<20) or (abs(tree_bbtt.Tau_eta[i_least])>2.3)):
            continue
        Tau_reco.SetPtEtaPhiM(tree_bbtt.Tau_pt[j],tree_bbtt.Tau_eta[j],tree_bbtt.Tau_phi[j],tree_bbtt.Tau_mass[j])
        delta_r = genFourVec.DeltaR(Tau_reco)
        #print ("delta R = ", delta_r)
        if ((i_counter==0) or delta_r<delta_r_least):
            i_least=j
            i_counter=i_counter + 1
            delta_r_least=delta_r

    if((delta_r_least < 0.1) 
    and (i_counter !=0) 
    #and (tree_bbtt.Tau_pt[i_least]>20) 
    #and (abs(tree_bbtt.Tau_eta[i_least])<2.3) 
    #and tree_bbtt.Tau_idDecayModeNewDMs[i_least]==1 
    and ((tree_bbtt.Tau_idDeepTau2017v2p1VSjet[i_least] & tau_id) == tau_id)):
        return True,i_least
    else:
        return False,i_least

#def tauMatched(tree_bbtt,genFourVec):
#    i_counter=0
#    i_least=0
#    delta_r=0
#    delta_r_least=0
#    for j in range(len(tree_bbtt.Tau_pt)):
#        if ((tree_bbtt.Tau_pt[i_least]<20) or (abs(tree_bbtt.Tau_eta[i_least])>2.3)):
#            continue
#        Tau_reco.SetPtEtaPhiM(tree_bbtt.Tau_pt[j],tree_bbtt.Tau_eta[j],tree_bbtt.Tau_phi[j],tree_bbtt.Tau_mass[j])
#        delta_r = genFourVec.DeltaR(Tau_reco)
#        #print ("delta R = ", delta_r)
#        if ((i_counter==0) or delta_r<delta_r_least):
#            i_least=j
#            i_counter=i_counter + 1
#            delta_r_least=delta_r
#
#    if((delta_r_least < 0.1) 
#    and (i_counter !=0)): 
#    #and (tree_bbtt.Tau_pt[i_least]>20) 
#    #and (abs(tree_bbtt.Tau_eta[i_least])<2.3) 
#    #and tree_bbtt.Tau_idDecayModeNewDMs[i_least]==1 
#    #and ((tree_bbtt.Tau_idDeepTau2017v2p1VSjet[i_least] & tau_id) == tau_id)):
#        return True,i_least
#    else:
#        return False,i_least

    
def boostedtauMatchedandPassed(tree_bbtt,genFourVec,tau_id):
    i_counter=0
    i_least=0
    delta_r=0
    delta_r_least=0
    #print (len(tree_bbtt.boostedTau_pt))
    for j in range(len(tree_bbtt.boostedTau_pt)):
        if ((tree_bbtt.boostedTau_pt[i_least]<20) or (abs(tree_bbtt.boostedTau_eta[i_least])>2.3)):
            continue 
        Tau_reco.SetPtEtaPhiM(tree_bbtt.boostedTau_pt[j],tree_bbtt.boostedTau_eta[j],tree_bbtt.boostedTau_phi[j],tree_bbtt.boostedTau_mass[j])
        delta_r = genFourVec.DeltaR(Tau_reco)
        if ((i_counter==0) or delta_r<delta_r_least):
            i_least=j
            i_counter=i_counter + 1
            delta_r_least=delta_r
        #print (tau_id," delta_R = ",delta_r, " ID Value = ",tree_bbtt.boostedTau_idMVAnewDM2017v2[i_least]," passed = ",(tree_bbtt.boostedTau_idMVAnewDM2017v2[i_least] & tau_id) == tau_id)
    #print ("type = ",type(tau_id), type(tree_bbtt.boostedTau_idMVAnewDM2017v2[i_least]), tree_bbtt.boostedTau_idMVAnewDM2017v2[i_least], i_least, tree_bbtt.boostedTau_idMVAnewDM2017v2[i_least]==0)
    if((delta_r_least < 0.3) 
    and (i_counter !=0)
    and  ((tree_bbtt.boostedTau_idAntiEle2018[i_least] & 2) == 2)
    and  ((tree_bbtt.boostedTau_idAntiMu[i_least] & 1) == 1)
    #and (tree_bbtt.boostedTau_pt[i_least]>20) 
    #and (abs(tree_bbtt.boostedTau_eta[i_least])<2.3) 
    #and tree_bbtt.boostedTau_idDecayModeNewDMs[i_least]==1 
    and ((tree_bbtt.boostedTau_idMVAnewDM2017v2[i_least] & tau_id) == tau_id)):
        return True,i_least
    else:
        return False,i_least

def boostedtauMatched(tree_bbtt,genFourVec):
    i_counter=0
    i_least=0
    delta_r=0
    delta_r_least=0
    #print (len(tree_bbtt.boostedTau_pt))
    for j in range(len(tree_bbtt.boostedTau_pt)):
        if ((tree_bbtt.boostedTau_pt[i_least]<20) or (abs(tree_bbtt.boostedTau_eta[i_least])>2.3)):
            continue 
        Tau_reco.SetPtEtaPhiM(tree_bbtt.boostedTau_pt[j],tree_bbtt.boostedTau_eta[j],tree_bbtt.boostedTau_phi[j],tree_bbtt.boostedTau_mass[j])
        delta_r = genFourVec.DeltaR(Tau_reco)
        if ((i_counter==0) or delta_r<delta_r_least):
            i_least=j
            i_counter=i_counter + 1
            delta_r_least=delta_r
        #print (tau_id," delta_R = ",delta_r, " ID Value = ",tree_bbtt.boostedTau_idMVAnewDM2017v2[i_least]," passed = ",(tree_bbtt.boostedTau_idMVAnewDM2017v2[i_least] & tau_id) == tau_id)
    #print ("type = ",type(tau_id), type(tree_bbtt.boostedTau_idMVAnewDM2017v2[i_least]), tree_bbtt.boostedTau_idMVAnewDM2017v2[i_least], i_least, tree_bbtt.boostedTau_idMVAnewDM2017v2[i_least]==0)
    if((delta_r_least < 0.3) 
    and (i_counter !=0)
    and  ((tree_bbtt.boostedTau_idAntiEle2018[i_least] & 2)==2) 
    and  ((tree_bbtt.boostedTau_idAntiMu[i_least] & 1) == 1)): 
    #and (tree_bbtt.boostedTau_pt[i_least]>20) 
    #and (abs(tree_bbtt.boostedTau_eta[i_least])<2.3) 
    #and tree_bbtt.boostedTau_idDecayModeNewDMs[i_least]==1 
    #and ((tree_bbtt.boostedTau_idMVAnewDM2017v2[i_least] & tau_id) == tau_id)):
        return True,i_least
    else:
        return False,i_least



tau_working = [1,2,4,8,16,32,64]
tau_wp = ["VVVL","VVL","VL","L","M","T","VT"]
boostedtau_working = [1,2,4,8,16,32,64]
btau_wp = ["VVL","VL","L","M","T","VT","VVT"]



file_bbtt = ROOT.TFile(args.signal)
tree_bbtt = file_bbtt.Get('Events')
nEntries = tree_bbtt.GetEntries()
nEntries = tree_bbtt.GetEntries()
print ("Total Events = ",nEntries)
#rejected = 0
#rejected_one = 0

tt_eve = 0
te_eve = 0
tm_eve = 0
other = 0
nil = 0
one = 0
moreh = 0
more = 0
diffMo = 0

for event_index in range(nEntries):
    if (event_index%1000 == 0):
         print("events_processed=",event_index)
    tree_bbtt.GetEntry(event_index)
    #print (classifyTauDecayMode(tree_bbtt))
    decay,tauIndices,genlep, extraFV = classifyTauDecayMode(tree_bbtt)

    if decay == None:
        diffMo = diffMo + 1
        continue

    if decay == "one":
        one = one + 1
        continue

    if decay == "zero":
        nil = nil + 1
        continue

    if decay == "moreh":
        moreh = moreh + 1
        continue

    if decay == "more":
        more = more + 1
        continue
    
    if ((decay == "ee") or (decay =="mm") or (decay =="me") or (decay == "em")):
        other =  other + 1
    
    if decay == "tt":
        tt_eve = tt_eve + 1
        if (extraFV == None):
            Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenVisTau_pt[tauIndices[0]],tree_bbtt.GenVisTau_eta[tauIndices[0]],tree_bbtt.GenVisTau_phi[tauIndices[0]],tree_bbtt.GenVisTau_mass[tauIndices[0]])
            Tau_gen_v2.SetPtEtaPhiM(tree_bbtt.GenVisTau_pt[tauIndices[1]],tree_bbtt.GenVisTau_eta[tauIndices[1]],tree_bbtt.GenVisTau_phi[tauIndices[1]],tree_bbtt.GenVisTau_mass[tauIndices[1]])
        elif (extraFV != None):
            Tau_gen_v1 = extraFV
            Tau_gen_v2.SetPtEtaPhiM(tree_bbtt.GenVisTau_pt[tauIndices[0]],tree_bbtt.GenVisTau_eta[tauIndices[0]],tree_bbtt.GenVisTau_phi[tauIndices[0]],tree_bbtt.GenVisTau_mass[tauIndices[0]])
        Higgs_pt = getParentPt(tree_bbtt,tree_bbtt.GenVisTau_genPartIdxMother[tauIndices[0]],25,15)
        if Higgs_pt ==0:
            print ("Higgs_Pt_tt = Zeeero CHECK!!!!!",Higgs_pt)
            continue
        tt_higgspt_total.Fill(Higgs_pt)
        tt_delR_total.Fill(Tau_gen_v1.DeltaR(Tau_gen_v2))
        #tt_taupt_total.Fill(tree_bbtt.GenVisTau_pt[tauIndices[0]])
        #tt_taupt_total.Fill(tree_bbtt.GenVisTau_pt[tauIndices[1]])
        tt_taupt_total.Fill(Tau_gen_v1.Pt())
        tt_taupt_total.Fill(Tau_gen_v2.Pt())

        for y in range(1):
            tau_id = tau_working[y]
            btau_id = boostedtau_working[y]
            if (boostedtauMatched(tree_bbtt,Tau_gen_v1)[0] and boostedtauMatched(tree_bbtt,Tau_gen_v2)[0]):
                if (boostedtauMatched(tree_bbtt,Tau_gen_v1)[1] != boostedtauMatched(tree_bbtt,Tau_gen_v2)[1]):
                    tt_higgspt_pass_b[y].Fill(Higgs_pt)
                    tt_delR_pass_b[y].Fill(Tau_gen_v1.DeltaR(Tau_gen_v2))
                    tt_taupt_pass_b[y].Fill(Tau_gen_v1.Pt())
                    tt_taupt_pass_b[y].Fill(Tau_gen_v2.Pt())

            if (boostedtauMatched(tree_bbtt,Tau_gen_v1)[0] or boostedtauMatched(tree_bbtt,Tau_gen_v2)[0]):
                tt_one_higgspt_pass_b[y].Fill(Higgs_pt)
                tt_one_delR_pass_b[y].Fill(Tau_gen_v1.DeltaR(Tau_gen_v2))
                tt_one_taupt_pass_b[y].Fill(Tau_gen_v1.Pt())
                tt_one_taupt_pass_b[y].Fill(Tau_gen_v2.Pt())

    if (decay == "te"):
        te_eve = te_eve + 1
        if (extraFV == None):
            Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenVisTau_pt[tauIndices[0]],tree_bbtt.GenVisTau_eta[tauIndices[0]],tree_bbtt.GenVisTau_phi[tauIndices[0]],tree_bbtt.GenVisTau_mass[tauIndices[0]])
            Tau_gen_v2.SetPtEtaPhiM(tree_bbtt.GenPart_pt[genlep[0]],tree_bbtt.GenPart_eta[genlep[0]],tree_bbtt.GenPart_phi[genlep[0]],tree_bbtt.GenPart_mass[genlep[0]])
        elif (extraFV !=None):
            Tau_gen_v1 = extraFV
            Tau_gen_v2.SetPtEtaPhiM(tree_bbtt.GenPart_pt[genlep[0]],tree_bbtt.GenPart_eta[genlep[0]],tree_bbtt.GenPart_phi[genlep[0]],tree_bbtt.GenPart_mass[genlep[0]])
        Higgs_pt = getParentPt(tree_bbtt,tree_bbtt.GenPart_genPartIdxMother[genlep[0]],25,15)
        if Higgs_pt ==0:
            print ("Higgs_Pt_te = Zeeero CHECK!!!!!",Higgs_pt)
            continue
        et_higgspt_total.Fill(Higgs_pt)
        et_delR_total.Fill(Tau_gen_v1.DeltaR(Tau_gen_v2))
        et_taupt_total.Fill(Tau_gen_v1.Pt())

        for y in range(1):
            tau_id = tau_working[y]
            btau_id = boostedtau_working[y]

            if(boostedtauMatched(tree_bbtt,Tau_gen_v1)[0]):
                et_higgspt_pass_b[y].Fill(Higgs_pt)
                et_delR_pass_b[y].Fill(Tau_gen_v1.DeltaR(Tau_gen_v2))
                et_taupt_pass_b[y].Fill(Tau_gen_v1.Pt())

    if (decay == "tm"):
        tm_eve = tm_eve + 1
        if (extraFV == None):
            Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenVisTau_pt[tauIndices[0]],tree_bbtt.GenVisTau_eta[tauIndices[0]],tree_bbtt.GenVisTau_phi[tauIndices[0]],tree_bbtt.GenVisTau_mass[tauIndices[0]])
            Tau_gen_v2.SetPtEtaPhiM(tree_bbtt.GenPart_pt[genlep[0]],tree_bbtt.GenPart_eta[genlep[0]],tree_bbtt.GenPart_phi[genlep[0]],tree_bbtt.GenPart_mass[genlep[0]])
        elif (extraFV !=None):
            Tau_gen_v1 = extraFV
            Tau_gen_v2.SetPtEtaPhiM(tree_bbtt.GenPart_pt[genlep[0]],tree_bbtt.GenPart_eta[genlep[0]],tree_bbtt.GenPart_phi[genlep[0]],tree_bbtt.GenPart_mass[genlep[0]])
        Higgs_pt = getParentPt(tree_bbtt,tree_bbtt.GenPart_genPartIdxMother[genlep[0]],25,15)
        if Higgs_pt ==0:
            print ("Higgs_Pt_tn = Zeeero CHECK!!!!!",Higgs_pt)
            continue        
        mt_higgspt_total.Fill(Higgs_pt)
        mt_delR_total.Fill(Tau_gen_v1.DeltaR(Tau_gen_v2))
        mt_taupt_total.Fill(Tau_gen_v1.Pt())

        for y in range(1):
            tau_id = tau_working[y]
            btau_id = boostedtau_working[y]

            if(boostedtauMatched(tree_bbtt,Tau_gen_v1)[0]):
                mt_higgspt_pass_b[y].Fill(Higgs_pt)
                mt_delR_pass_b[y].Fill(Tau_gen_v1.DeltaR(Tau_gen_v2))
                mt_taupt_pass_b[y].Fill(Tau_gen_v1.Pt())             




def makeEfficiencies (passHist, totalHist, dictionary, xtitle, name = "name"):
    for y in range(1):
        dictionary[y] = ROOT.TGraphAsymmErrors(passHist[y],totalHist,name)
        dictionary[y].SetLineColor(linecolor[y+1])
        dictionary[y].SetMarkerStyle(markerstylesolid[y+1])
        dictionary[y].SetMarkerColor(markercolor[y+1])
        dictionary[y].SetMarkerSize(1.5)
        dictionary[y].SetTitle("Reconstruction Efficiency")
        dictionary[y].GetXaxis().SetTitle(xtitle)
        dictionary[y].GetYaxis().SetTitle("Reconstruction Efficiency")
        dictionary[y].GetYaxis().SetRangeUser(-0.05,1.1)


def drawOncanvas (eff_dict,headerString,savefile,type,wp):
    can = ROOT.TCanvas("can", "efficiency")
    can.SetGrid()
    can_leg=ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
    can_leg.SetHeader(headerString)
    can_leg.SetFillStyle(1001)
    can_leg.SetLineWidth(0)

    for  y in range(1):
        if y == 0:
            eff_dict[y].Draw("ap")
        else:
            eff_dict[y].Draw("same p")
        
        can_leg.AddEntry(type+" Reconstruction","ep")

    can_leg.Draw("same")
    
    cmsLatex = ROOT.TLatex()
    cmsLatex.SetTextSize(0.04)
    cmsLatex.SetNDC(True)
    cmsLatex.SetTextFont(61)
    cmsLatex.SetTextAlign(11)
    cmsLatex.DrawLatex(0.1,0.92,"CMS")
    cmsLatex.SetTextFont(52)
    cmsLatex.DrawLatex(0.1+0.07,0.92,"Preliminary")
    can.SaveAs(savefile)

makeEfficiencies(tt_higgspt_pass_b,tt_higgspt_total,tt_eff_b,"Gen Higgs p_{T}(GeV)","bb")
makeEfficiencies(tt_delR_pass_b,tt_delR_total, delR_tt_eff_b,"del_R","delbb")
makeEfficiencies(tt_taupt_pass_b,tt_taupt_total,taupt_tt_eff_b,"Tau p_{T}","taubb")
drawOncanvas(tt_eff_b,"Di tau both pass","{}_tt_eff_b.pdf".format(args.mp),"boosted",btau_wp)
drawOncanvas(delR_tt_eff_b,"Di tau both pass","{}_delR_tt_eff_b.pdf".format(args.mp),"boosted",btau_wp )
drawOncanvas(taupt_tt_eff_b,"Di tau both pass","{}_taupt_tt_eff_b.pdf".format(args.mp),"boosted",btau_wp)

makeEfficiencies(tt_one_higgspt_pass_b,tt_higgspt_total,tt_one_eff_b,"Gen Higgs p_{T}(GeV)","one b")
makeEfficiencies(tt_one_delR_pass_b,tt_delR_total, delR_tt_one_eff_b,"del_R","del one bb")
makeEfficiencies(tt_one_taupt_pass_b,tt_taupt_total,taupt_tt_one_eff_b,"Tau p_{T}","one tau b")
drawOncanvas(tt_one_eff_b,"Di tau either pass","{}_tt_one_eff_b.pdf".format(args.mp),"boosted",btau_wp)
drawOncanvas(delR_tt_one_eff_b,"Di tau either pass","{}_delR_tt_one_eff_b.pdf".format(args.mp),"boosted",btau_wp)
drawOncanvas(taupt_tt_one_eff_b,"Di tau either pass","{}_taupt_tt_one_eff_b.pdf".format(args.mp),"boosted",btau_wp)

makeEfficiencies(et_higgspt_pass_b,et_higgspt_total,et_eff_b,"Gen Higgs p_{T}(GeV)","et")
makeEfficiencies(et_delR_pass_b,et_delR_total,delR_et_eff_b,"del_R","del et")
makeEfficiencies(et_taupt_pass_b,et_taupt_total,taupt_et_eff_b,"Tau p_{T}","one tau et")
drawOncanvas(et_eff_b,"e Tau","{}_et_eff_b.pdf".format(args.mp),"boosted",btau_wp)
drawOncanvas(delR_et_eff_b,"e Tau","{}_delR_et_eff_b.pdf".format(args.mp),"boosted",btau_wp)
drawOncanvas(taupt_et_eff_b,"Di tau either pass","{}_taupt_et_eff_b.pdf".format(args.mp),"boosted",btau_wp)

makeEfficiencies(mt_higgspt_pass_b,mt_higgspt_total,mt_eff_b,"Gen Higgs p_{T}(GeV)","mt")
makeEfficiencies(mt_delR_pass_b,mt_delR_total,delR_mt_eff_b,"del_R","del mt")
makeEfficiencies(mt_taupt_pass_b,mt_taupt_total,taupt_mt_eff_b,"Tau p_{T}","tau_mt_pt")
drawOncanvas(mt_eff_b,"m Tau","{}_mt_eff_b.pdf".format(args.mp),"boosted",btau_wp)
drawOncanvas(delR_mt_eff_b,"m Tau","{}_del_mt_eff_b.pdf".format(args.mp),"boosted",btau_wp)
drawOncanvas(taupt_mt_eff_b,"m Tau","{}_taupt_mt_eff_b.pdf".format(args.mp),"boosted",btau_wp)    

with open('{}_EventCount.txt'.format(args.mp), 'w') as f:
    f.write("Di - Tau Events = " + str(tt_eve) +'\n')
    f.write("E - Tau Events = " + str(te_eve) +'\n')
    f.write("M - Tau Events = " + str(tm_eve) +'\n')
    f.write("Other Channels = " + str(other) +'\n')
    f.write("No Leptons = " + str(nil) +'\n')
    f.write("One lepton = " + str(one) +'\n')
    f.write("More handronic taus = " + str(moreh) +'\n')
    f.write("More taus = " + str(more) +'\n')
    f.write("differnet mothers = " + str(diffMo) +'\n')

print ("Di - Tau Events = ", tt_eve)
print ("E - Tau Events = ", te_eve)
print ("M - Tau Events = ", tm_eve)
print ("Other Channels = ", other)
print ("No Leptons = ", nil)
print ("One lepton = ", one)
print ("More handronic taus = ", moreh)
print ("More taus = ", more)
print ("differnet mothers = ",diffMo)



#print("rejected = ",rejected)
#print("rejected_one =", rejected_one)
