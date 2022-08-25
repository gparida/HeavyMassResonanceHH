
import ROOT
import math 
import time
from plot_dict import *
import argparse

parser = argparse.ArgumentParser(description='Compute Reco + ID efficiency for a signal Sample')
parser.add_argument('--signal','-F',help="file name including the path",required=True)
parser.add_argument('--mp',help="goes in the file name of the plots",required=True)
args = parser.parse_args()




tt_higgspt_pass = [ROOT.TH1F("tt_higgspt_pass_{}".format(str(i)),"tt_higgspt_pass_{}".format(str(i)), 12,  400, 1000) for i in range(7)]
tt_higgspt_pass_b = [ROOT.TH1F("tt_higgspt_pass_b_{}".format(str(i)),"tt_higgspt_pass_b_{}".format(str(i)), 12,  400, 1000) for i in range(7)]
#tt_higgspt_total = [ROOT.TH1F("tt_higgspt_total_{}".format(str(i)),"tt_higgspt_total_{}".format(str(i)), 12,  400, 1000) for i in range(7)]
tt_higgspt_total = ROOT.TH1F("tt_higgspt_total","tt_higgspt_total",12,  400, 1000)


tt_one_higgspt_pass = [ROOT.TH1F("tt_one_higgspt_pass_{}".format(str(i)),"tt_one_higgspt_pass_{}".format(str(i)), 12,  400, 1000) for i in range(7)]
tt_one_higgspt_pass_b = [ROOT.TH1F("tt_one_higgspt_pass_b_{}".format(str(i)),"tt_one_higgspt_pass_b_{}".format(str(i)), 12,  400, 1000) for i in range(7)]
#tt_one_higgspt_total = ROOT.TH1F("tt_one_higgspt_total","tt_one_higgspt_total",12,  400, 1000)


et_higgspt_pass = [ROOT.TH1F("et_higgspt_pass_{}".format(str(i)),"et_higgspt_pass_{}".format(str(i)), 12,  400, 1000) for i in range(7)]
et_higgspt_pass_b = [ROOT.TH1F("et_higgspt_pass_b_{}".format(str(i)),"et_higgspt_pass_b_{}".format(str(i)), 12,  400, 1000) for i in range(7)]
#et_higgspt_total = [ROOT.TH1F("et_higgspt_total_{}".format(str(i)),"et_higgspt_total_{}".format(str(i)), 12,  400, 1000) for i in range(7)]
et_higgspt_total = ROOT.TH1F("et_higgspt_total","et_higgspt_total",12,  400, 1000)

mt_higgspt_pass = [ROOT.TH1F("mt_higgspt_pass_{}".format(str(i)),"mt_higgspt_pass_{}".format(str(i)), 12,  400, 1000) for i in range(7)]
mt_higgspt_pass_b = [ROOT.TH1F("mt_higgspt_pass_b_{}".format(str(i)),"mt_higgspt_pass_b_{}".format(str(i)), 12,  400, 1000) for i in range(7)]
#mt_higgspt_total = [ROOT.TH1F("mt_higgspt_total_{}".format(str(i)),"mt_higgspt_total_{}".format(str(i)),12,  400, 1000) for i in range(7)]
mt_higgspt_total = ROOT.TH1F("mt_higgspt_total","mt_higgspt_total",12,  400, 1000)

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



#The function to classify the event as a diTau, eTau or mTau for the signal files
def classifyTauDecayMode(theTree):
    
    #particlesWithTauMother = []
    decayMode = []
    visTauInd = []
    genTauInd = []

    for visInd in range(theTree.nGenVisTau):
        if theTree.GenVisTau_genPartIdxMother[visInd] < 0: #Ignore if the mother index is negative
            continue
        if ((abs(theTree.GenPart_pdgId[theTree.GenVisTau_genPartIdxMother[visInd]]) == 15) and ((theTree.GenPart_statusFlags[theTree.GenVisTau_genPartIdxMother[visInd]] & 4) == 4)): # Check if the parent is tau and if it is a decay product of Tau
            if (abs(theTree.GenPart_pdgId[theTree.GenPart_genPartIdxMother[theTree.GenVisTau_genPartIdxMother[visInd]]]) == 25):
                decayMode.append('t')
                visTauInd.append(visInd)
                genTauInd.append(theTree.GenVisTau_genPartIdxMother[visInd])
                continue
            
    if len(decayMode) == 2:
        return ''.join(decay for decay in decayMode), visTauInd
    elif len(decayMode) < 2:
        for nPart in range(theTree.nGenPart):
            if ((theTree.GenPart_genPartIdxMother[nPart] < 0) or (theTree.GenPart_genPartIdxMother[nPart] in genTauInd)):
                continue
            if ((abs(theTree.GenPart_pdgId[theTree.GenPart_genPartIdxMother[nPart]]) == 15) 
            and ((theTree.GenPart_statusFlags[nPart] & 4) == 4)
            and (abs(theTree.GenPart_pdgId[theTree.GenPart_genPartIdxMother[theTree.GenPart_genPartIdxMother[nPart]]]) == 25)):
                if ((abs(theTree.GenPart_pdgId[nPart]))==13):
                    decayMode.append('m')
                    genTauInd.append(theTree.GenPart_genPartIdxMother[nPart])
                elif ((abs(theTree.GenPart_pdgId[nPart]))==11):
                    decayMode.append('e')
                    genTauInd.append(theTree.GenPart_genPartIdxMother[nPart])
    else:
        print ("Moree hadronic Taus > 2")
        return None, None
    
    if (len(decayMode)<2):
        print ("less than 2 Taus!")
        return None, None

    if (len(decayMode)>2):
        print ("More leptonic Taus!")
        return None, None
    
    if (tree_bbtt.GenPart_genPartIdxMother[genTauInd[0]]!=tree_bbtt.GenPart_genPartIdxMother[genTauInd[1]]):
        print ("Error, Taus have different mothers")
        return None, None
    
    print (''.join(decay for decay in decayMode), len(visInd), '/n')
    return ''.join(decay for decay in decayMode), visTauInd

        

#def tauMatchedandPassed(tree_bbtt,genFourVec,tau_id):
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
#    and (i_counter !=0) 
#    #and (tree_bbtt.Tau_pt[i_least]>20) 
#    #and (abs(tree_bbtt.Tau_eta[i_least])<2.3) 
#    #and tree_bbtt.Tau_idDecayModeNewDMs[i_least]==1 
#    and ((tree_bbtt.Tau_idDeepTau2017v2p1VSjet[i_least] & tau_id) == tau_id)):
#        return True,i_least
#    else:
#        return False,i_least

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
    if((delta_r_least < 0.1) 
    and (i_counter !=0) 
    #and (tree_bbtt.boostedTau_pt[i_least]>20) 
    #and (abs(tree_bbtt.boostedTau_eta[i_least])<2.3) 
    #and tree_bbtt.boostedTau_idDecayModeNewDMs[i_least]==1 
    and ((tree_bbtt.boostedTau_idMVAoldDM2017v2[i_least] & tau_id) == tau_id)):
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
    if((delta_r_least < 0.1) 
    and (i_counter !=0)): 
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

for event_index in range(2000):
    if (event_index%1000 == 0):
         print("events_processed=",event_index)
    tree_bbtt.GetEntry(event_index)
    decay, tauIndices = classifyTauDecayMode(tree_bbtt)

    if decay == None:
        continue
    
    if decay == "tt":
        Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenVisTau_pt[tauIndices[0]],tree_bbtt.GenVisTau_eta[tauIndices[0]],tree_bbtt.GenVisTau_phi[tauIndices[0]],tree_bbtt.GenVisTau_mass[tauIndices[0]])
        Tau_gen_v2.SetPtEtaPhiM(tree_bbtt.GenVisTau_pt[tauIndices[1]],tree_bbtt.GenVisTau_eta[tauIndices[1]],tree_bbtt.GenVisTau_phi[tauIndices[1]],tree_bbtt.GenVisTau_mass[tauIndices[1]])
        tt_higgspt_total.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tree_bbtt.GenVisTau_genPartIdxMother[tauIndices[0]]]])

        for y in range(7):
            tau_id = tau_working[y]
            btau_id = boostedtau_working[y]
            if (boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v1,btau_id)[0] and boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v2,btau_id)[0]):
                if (boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v1,btau_id)[1] == boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v2,btau_id)[1]):
                    continue
                tt_higgspt_pass_b[y].Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tree_bbtt.GenVisTau_genPartIdxMother[tauIndices[0]]]])

            if (boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v1,btau_id)[0] or boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v2,btau_id)[0]):
                tt_one_higgspt_pass_b[y].Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tree_bbtt.GenVisTau_genPartIdxMother[tauIndices[0]]]])

    if (decay == "te"):
        Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenVisTau_pt[tauIndices[0]],tree_bbtt.GenVisTau_eta[tauIndices[0]],tree_bbtt.GenVisTau_phi[tauIndices[0]],tree_bbtt.GenVisTau_mass[tauIndices[0]])
        et_higgspt_total.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tree_bbtt.GenVisTau_genPartIdxMother[tauIndices[0]]]])

        for y in range(7):
            tau_id = tau_working[y]
            btau_id = boostedtau_working[y]

            if(boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v1,btau_id)[0]):
                et_higgspt_pass_b[y].Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tree_bbtt.GenVisTau_genPartIdxMother[tauIndices[0]]]])

    if (decay == "tm"):
        Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenVisTau_pt[tauIndices[0]],tree_bbtt.GenVisTau_eta[tauIndices[0]],tree_bbtt.GenVisTau_phi[tauIndices[0]],tree_bbtt.GenVisTau_mass[tauIndices[0]])
        mt_higgspt_total.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tree_bbtt.GenVisTau_genPartIdxMother[tauIndices[0]]]])

        for y in range(7):
            tau_id = tau_working[y]
            btau_id = boostedtau_working[y]

            if(boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v1,btau_id)[0]):
                mt_higgspt_pass_b[y].Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tree_bbtt.GenVisTau_genPartIdxMother[tauIndices[0]]]])             




def makeEfficiencies (passHist, totalHist, dictionary, name = "name"):
    for y in range(7):
        dictionary[y] = ROOT.TGraphAsymmErrors(passHist[y],totalHist,name)
        dictionary[y].SetLineColor(linecolor[y+1])
        dictionary[y].SetMarkerStyle(markerstylesolid[y+1])
        dictionary[y].SetMarkerColor(markercolor[y+1])
        dictionary[y].SetMarkerSize(1.5)
        dictionary[y].SetTitle("Reconstruction + Identification Efficiency")
        dictionary[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
        dictionary[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
        dictionary[y].GetYaxis().SetRangeUser(-0.05,1.1)

def drawOncanvas (eff_dict,headerString,savefile,type,wp):
    can = ROOT.TCanvas("can", "efficiency")
    can.SetGrid()
    can_leg=ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
    can_leg.SetHeader(headerString)
    can_leg.SetFillStyle(1001)
    can_leg.SetLineWidth(0)

    for  y in range(7):
        if y == 0:
            eff_dict[y].Draw("ap")
        else:
            eff_dict[y].Draw("same p")
        
        can_leg.AddEntry(eff_dict[y],type+wp[y],"ep")

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

makeEfficiencies(tt_higgspt_pass_b,tt_higgspt_total,tt_eff_b,"bb")
drawOncanvas(tt_eff_b,"Di tau both pass","test.pdf","boosted",btau_wp)
        
    





