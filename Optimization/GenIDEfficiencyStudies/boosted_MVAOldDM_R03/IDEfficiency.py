
import ROOT
import math 
import time
from plot_dict import *
import argparse

parser = argparse.ArgumentParser(description='Compute Reco + ID efficiency for a signal Sample')
parser.add_argument('--signal','-F',help="file name including the path",required=True)
parser.add_argument('--mp',help="goes in the file name of the plots",required=True)
args = parser.parse_args()




tt_higgspt_pass = ROOT.TH1F("tt_higgspt_pass","tt_higgspt_pass", 12,  400, 1000)
tt_higgspt_pass_b = ROOT.TH1F("tt_higgspt_pass_b","tt_higgspt_pass_b",12,  400, 1000)
tt_higgspt_total = ROOT.TH1F("tt_higgspt_total","tt_higgspt_total",12,  400, 1000)


tt_one_higgspt_pass = ROOT.TH1F("tt_one_higgspt_pass","tt_one_higgspt_pass", 12,  400, 1000)
tt_one_higgspt_pass_b = ROOT.TH1F("tt_one_higgspt_pass_b","tt_one_higgspt_pass_b",12,  400, 1000)
#tt_one_higgspt_total = ROOT.TH1F("tt_one_higgspt_total","tt_one_higgspt_total",12,  400, 1000)


et_higgspt_pass = ROOT.TH1F("et_higgspt_pass","et_higgspt_pass", 12,  400, 1000)
et_higgspt_pass_b = ROOT.TH1F("et_higgspt_pass_b","et_higgspt_pass_b", 12,  400, 1000)
et_higgspt_total = ROOT.TH1F("et_higgspt_total","et_higgspt_total",12,  400, 1000)

mt_higgspt_pass = ROOT.TH1F("mt_higgspt_pass","mt_higgspt_pass", 12,  400, 1000)
mt_higgspt_pass_b = ROOT.TH1F("mt_higgspt_pass_b","mt_higgspt_pass_b", 12,  400, 1000)
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
    
    particlesWithTauMother = []

    for nPart in range(theTree.nGenPart):
        if theTree.GenPart_genPartIdxMother[nPart] < 0: #Ignore if the mother index is negative
            continue
        if ((abs(theTree.GenPart_pdgId[theTree.GenPart_genPartIdxMother[nPart]]) == 15) and ((theTree.GenPart_statusFlags[nPart] & 4) == 4)): # Check if the parent is tau and if it is a decay product of Tau
            if (abs(theTree.GenPart_pdgId[theTree.GenPart_genPartIdxMother[theTree.GenPart_genPartIdxMother[nPart]]]) == 25):
                particlesWithTauMother.append((nPart,theTree.GenPart_pdgId[nPart],theTree.GenPart_genPartIdxMother[nPart]))
                continue
            
    decayMode = []
    alreadyAssignedTaus = []
    #print ("particlesWithTauMother",particlesWithTauMother)
    if len(particlesWithTauMother) == 0:
        return None, None
    for particle in particlesWithTauMother:
        if particle[2] not in alreadyAssignedTaus:
            if (abs(particle[1]) == 13):
                decayMode.append('m')
                alreadyAssignedTaus.append(particle[2])

            if (abs(particle[1]) == 11):
                decayMode.append('e')
                alreadyAssignedTaus.append(particle[2])
            
            if (abs(particle[1]) > 100):
                decayMode.append('t')
                alreadyAssignedTaus.append(particle[2])
    #print ("decay mode = ", decayMode, particlesWithTauMother)
    if len(decayMode) < 2:
        #assume we decayed to some other hadron
        for i in range (2-len(decayMode)):
            print ("Less than 2 taus")
            decayMode.append('t')

    if len(decayMode) > 2:
        print('too many assigned taus!')
        for tau in alreadyAssignedTaus:
            print('{:3n}'.format(tau)+': '+'{0:b}'.format(theTree.GenPart_statusFlags[tau]))
        print('returning none!')
        return None, None
        


    if len(decayMode) < 2:
        print('too few taus!')
        for tau in particlesWithTauMother:
            if tau[2] not in alreadyAssignedTaus:
                print("{:3n}".format(tau[1])+' Was part of a tau that was not assigned')
                return None, None
        
    #decayMode.sort()
    #print (''.join(decay for decay in decayMode),'/n')
    return ''.join(decay for decay in decayMode), alreadyAssignedTaus

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
    and ((tree_bbtt.boostedTau_idMVAoldDMdR032017v2[i_least] & tau_id) == tau_id)):
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
boostedtau_working = [1,2,4,8,16,32,64]

#Loop over all the working points
for y in range(7):
    #Setting the tau and boosted tau working points
    tau_id = tau_working[y]
    btau_id = boostedtau_working[y]

    #Reset the histograms that is used to compute efficiency
    tt_higgspt_pass.Reset()
    tt_higgspt_pass_b.Reset()
    tt_higgspt_total.Reset()

    tt_one_higgspt_pass.Reset()
    tt_one_higgspt_pass_b.Reset()

    et_higgspt_pass.Reset()
    et_higgspt_pass_b.Reset()
    et_higgspt_total.Reset()

    mt_higgspt_pass.Reset()
    mt_higgspt_pass_b.Reset()
    mt_higgspt_total.Reset()

    # Open the file
    file_bbtt = ROOT.TFile(args.signal)
    tree_bbtt = file_bbtt.Get('Events')
    nEntries = tree_bbtt.GetEntries()
    print ("Total Events = ",nEntries)


    count_tt_same = 0
    count_one_tt_same = 0
    count_bb_same = 0
    count_one_bb_same = 0

    for event_index in range(nEntries):
        if (event_index%1000 == 0):
            print("events_processed=",event_index)
        tree_bbtt.GetEntry(event_index)


        #Call the function to classify the decay mode
        decay, tauIndices = classifyTauDecayMode(tree_bbtt)


        if decay == None:
            continue

        if (len(tauIndices)!=2):
            print("Error, Not exactly two taus")
            continue
        
        if (tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]!=tree_bbtt.GenPart_genPartIdxMother[tauIndices[1]]):
            print ("Error, Taus have different mothers")
            continue

        if decay == "tt":
            Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[tauIndices[0]],tree_bbtt.GenPart_eta[tauIndices[0]],tree_bbtt.GenPart_phi[tauIndices[0]],tree_bbtt.GenPart_mass[tauIndices[0]])
            Tau_gen_v2.SetPtEtaPhiM(tree_bbtt.GenPart_pt[tauIndices[1]],tree_bbtt.GenPart_eta[tauIndices[1]],tree_bbtt.GenPart_phi[tauIndices[1]],tree_bbtt.GenPart_mass[tauIndices[1]])
            tt_higgspt_total.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
            #print (tauMatchedandPassed(tree_bbtt,Tau_gen_v1,tau_id)[0],tauMatchedandPassed(tree_bbtt,Tau_gen_v1,tau_id)[1])
#            if (tauMatchedandPassed(tree_bbtt,Tau_gen_v1,tau_id)[0] and tauMatchedandPassed(tree_bbtt,Tau_gen_v2,tau_id)[0]):
#                if (tauMatchedandPassed(tree_bbtt,Tau_gen_v1,tau_id)[1] == tauMatchedandPassed(tree_bbtt,Tau_gen_v2,tau_id)[1]):
#                    count_tt_same = count_one_tt_same + 1
#                    #print ("both taus matched to same reco, reduce deltaR, skip event")
#                    continue
#                tt_higgspt_pass.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
            if (boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v1,btau_id)[0] and boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v2,btau_id)[0]):
                #print ("here b")
                if (boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v1,btau_id)[1] == boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v2,btau_id)[1]):
                    count_bb_same = count_bb_same + 1
                    #print ("both boosted taus matched to same reco, reduce deltaR, skip event")
                    continue
                tt_higgspt_pass_b.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
#            if ((tauMatched(tree_bbtt,Tau_gen_v1)[0] and tauMatched(tree_bbtt,Tau_gen_v2)[0]) and (tauMatched(tree_bbtt,Tau_gen_v1)[1] != tauMatched(tree_bbtt,Tau_gen_v2)[1])):
#                if (((tree_bbtt.Tau_idDeepTau2017v2p1VSjet[tauMatched(tree_bbtt,Tau_gen_v1)[1]] & tau_id) == tau_id) or ((tree_bbtt.Tau_idDeepTau2017v2p1VSjet[tauMatched(tree_bbtt,Tau_gen_v2)[1]] & tau_id) == tau_id)):
#                    #count_one_tt_same = count_one_tt_same + 1
#                    tt_one_higgspt_pass.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
#                    #print ("both taus matched(one) to same reco, reduce deltaR, skip event")
#                    #continue                    
                
            if ((boostedtauMatched(tree_bbtt,Tau_gen_v1)[0] and boostedtauMatched(tree_bbtt,Tau_gen_v2)[0]) and (boostedtauMatched(tree_bbtt,Tau_gen_v1)[1] != boostedtauMatched(tree_bbtt,Tau_gen_v2)[1])):
                if (((tree_bbtt.boostedTau_idMVAoldDMdR032017v2[boostedtauMatched(tree_bbtt,Tau_gen_v1)[1]] & btau_id) == btau_id) or ((tree_bbtt.boostedTau_idMVAoldDMdR032017v2[boostedtauMatched(tree_bbtt,Tau_gen_v2)[1]] & btau_id) == btau_id)):
                    #count_one_bb_same = count_one_bb_same + 1
                    tt_one_higgspt_pass_b.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
                    #print ("both boosted taus matched(one) to same reco, reduce deltaR, skip event")
                    #continue
                
        
        if (decay == "et" or decay == "te"):
            if decay == "te":
                Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[tauIndices[0]],tree_bbtt.GenPart_eta[tauIndices[0]],tree_bbtt.GenPart_phi[tauIndices[0]],tree_bbtt.GenPart_mass[tauIndices[0]])
            elif decay == "et":
                Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[tauIndices[1]],tree_bbtt.GenPart_eta[tauIndices[1]],tree_bbtt.GenPart_phi[tauIndices[1]],tree_bbtt.GenPart_mass[tauIndices[1]])
            et_higgspt_total.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
#            if(tauMatchedandPassed(tree_bbtt,Tau_gen_v1,tau_id)[0]):
#                et_higgspt_pass.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
            if(boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v1,btau_id)[0]):
                et_higgspt_pass_b.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
        
        if (decay == "mt" or decay == "tm"):
            if decay == "tm":
                Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[tauIndices[0]],tree_bbtt.GenPart_eta[tauIndices[0]],tree_bbtt.GenPart_phi[tauIndices[0]],tree_bbtt.GenPart_mass[tauIndices[0]])
            elif decay == "mt":
                Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[tauIndices[1]],tree_bbtt.GenPart_eta[tauIndices[1]],tree_bbtt.GenPart_phi[tauIndices[1]],tree_bbtt.GenPart_mass[tauIndices[1]])
            mt_higgspt_total.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
#           if(tauMatchedandPassed(tree_bbtt,Tau_gen_v1,tau_id)[0]):
#               mt_higgspt_pass.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
            if(boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v1,btau_id)[0]):
                mt_higgspt_pass_b.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])        

                
#    tt_eff[y] = ROOT.TGraphAsymmErrors(tt_higgspt_pass,tt_higgspt_total,'e1000')
#    tt_eff[y].SetLineColor(linecolor[y+1])
#    tt_eff[y].SetMarkerStyle(markerstylesolid[y+1])
#    tt_eff[y].SetMarkerColor(markercolor[y+1])
#    tt_eff[y].SetMarkerSize(1.5)
#    tt_eff[y].SetTitle("Reconstruction + Identification Efficiency")
#    tt_eff[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
#    tt_eff[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
#    tt_eff[y].GetYaxis().SetRangeUser(-0.05,1.1)

    tt_eff_b[y] = ROOT.TGraphAsymmErrors(tt_higgspt_pass_b,tt_higgspt_total,'e1000')
    tt_eff_b[y].SetLineColor(linecolor[y+1])
    tt_eff_b[y].SetMarkerStyle(markerstylesolid[y+1])
    tt_eff_b[y].SetMarkerColor(markercolor[y+1])
    tt_eff_b[y].SetMarkerSize(1.5)
    tt_eff_b[y].SetTitle("Reconstruction + Identification Efficiency")
    tt_eff_b[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
    tt_eff_b[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
    tt_eff_b[y].GetYaxis().SetRangeUser(-0.05,1.1)

#    tt_one_eff[y] = ROOT.TGraphAsymmErrors(tt_one_higgspt_pass,tt_higgspt_total,'e1000')
#    tt_one_eff[y].SetLineColor(linecolor[y+1])
#    tt_one_eff[y].SetMarkerStyle(markerstylesolid[y+1])
#    tt_one_eff[y].SetMarkerColor(markercolor[y+1])
#    tt_one_eff[y].SetMarkerSize(1.5)
#    tt_one_eff[y].SetTitle("Reconstruction + Identification Efficiency")
#    tt_one_eff[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
#    tt_one_eff[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
#    tt_one_eff[y].GetYaxis().SetRangeUser(-0.05,1.1)

    tt_one_eff_b[y] = ROOT.TGraphAsymmErrors(tt_one_higgspt_pass_b,tt_higgspt_total,'e1000')
    tt_one_eff_b[y].SetLineColor(linecolor[y+1])
    tt_one_eff_b[y].SetMarkerStyle(markerstylesolid[y+1])
    tt_one_eff_b[y].SetMarkerColor(markercolor[y+1])
    tt_one_eff_b[y].SetMarkerSize(1.5)
    tt_one_eff_b[y].SetTitle("Reconstruction + Identification Efficiency")
    tt_one_eff_b[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
    tt_one_eff_b[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
    tt_one_eff_b[y].GetYaxis().SetRangeUser(-0.05,1.1)



#    et_eff[y] = ROOT.TGraphAsymmErrors(et_higgspt_pass,et_higgspt_total,'e1000')
#    et_eff[y].SetLineColor(linecolor[y+1])
#    et_eff[y].SetMarkerStyle(markerstylesolid[y+1])
#    et_eff[y].SetMarkerColor(markercolor[y+1])
#    et_eff[y].SetMarkerSize(1.5)
#    et_eff[y].SetTitle("Reconstruction + Identification Efficiency")
#    et_eff[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
#    et_eff[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
#    et_eff[y].GetYaxis().SetRangeUser(-0.05,1.1)

    et_eff_b[y] = ROOT.TGraphAsymmErrors(et_higgspt_pass_b,et_higgspt_total,'e1000')
    et_eff_b[y].SetLineColor(linecolor[y+1])
    et_eff_b[y].SetMarkerStyle(markerstylesolid[y+1])
    et_eff_b[y].SetMarkerColor(markercolor[y+1])
    et_eff_b[y].SetMarkerSize(1.5)
    et_eff_b[y].SetTitle("Reconstruction + Identification Efficiency")
    et_eff_b[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
    et_eff_b[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
    et_eff_b[y].GetYaxis().SetRangeUser(-0.05,1.1)
    
#    mt_eff[y] = ROOT.TGraphAsymmErrors(mt_higgspt_pass,mt_higgspt_total,'e1000')
#    mt_eff[y].SetLineColor(linecolor[y+1])
#    mt_eff[y].SetMarkerStyle(markerstylesolid[y+1])
#    mt_eff[y].SetMarkerColor(markercolor[y+1])
#    mt_eff[y].SetMarkerSize(1.5)
#    mt_eff[y].SetTitle("Reconstruction + Identification Efficiency")
#    mt_eff[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
#    mt_eff[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
#    mt_eff[y].GetYaxis().SetRangeUser(-0.05,1.1)

    mt_eff_b[y] = ROOT.TGraphAsymmErrors(mt_higgspt_pass_b,mt_higgspt_total,'e1000')
    mt_eff_b[y].SetLineColor(linecolor[y+1])
    mt_eff_b[y].SetMarkerStyle(markerstylesolid[y+1])
    mt_eff_b[y].SetMarkerColor(markercolor[y+1])
    mt_eff_b[y].SetMarkerSize(1.5)
    mt_eff_b[y].SetTitle("Reconstruction + Identification Efficiency")
    mt_eff_b[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
    mt_eff_b[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
    mt_eff_b[y].GetYaxis().SetRangeUser(-0.05,1.1)





#tt = ROOT.TCanvas("tt", "efficiency")
#tt.SetGrid()
#tt_eff[0].Draw("ap")
#tt_eff[1].Draw("same p")
#tt_eff[2].Draw("same p")
#tt_eff[3].Draw("same p")
#tt_eff[4].Draw("same p")
#tt_eff[5].Draw("same p")
#tt_eff[6].Draw("same p")
#tt_leg = ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
#tt_leg.SetHeader("#tau_{h}-#tau_{h} both pass")
#tt_leg.SetFillStyle(1001)
#tt_leg.SetLineWidth(0)
#tt_leg.AddEntry(tt_eff[0],"hps_VVVL","ep")
#tt_leg.AddEntry(tt_eff[1],"hps_VVL","ep")
#tt_leg.AddEntry(tt_eff[2],"hps_VL","ep")
#tt_leg.AddEntry(tt_eff[3],"hps_L","ep")
#tt_leg.AddEntry(tt_eff[4],"hps_M","ep")
#tt_leg.AddEntry(tt_eff[5],"hps_T","ep")
#tt_leg.AddEntry(tt_eff[6],"hps_VT","ep")
#tt_leg.Draw("same")
#cmsLatex = ROOT.TLatex()
#cmsLatex.SetTextSize(0.04)
#cmsLatex.SetNDC(True)
#cmsLatex.SetTextFont(61)
#cmsLatex.SetTextAlign(11)
#cmsLatex.DrawLatex(0.1,0.92,"CMS")
#cmsLatex.SetTextFont(52)
#cmsLatex.DrawLatex(0.1+0.07,0.92,"Preliminary")
#tt.SaveAs("{}_hps_tt.pdf".format(args.mp))

#tt_one = ROOT.TCanvas("tt_one", "efficiency")
#tt_one.SetGrid()
#tt_one_eff[0].Draw("ap")
#tt_one_eff[1].Draw("same p")
#tt_one_eff[2].Draw("same p")
#tt_one_eff[3].Draw("same p")
#tt_one_eff[4].Draw("same p")
#tt_one_eff[5].Draw("same p")
#tt_one_eff[6].Draw("same p")
#tt_one_leg = ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
#tt_one_leg.SetHeader("#tau_{h}-#tau_{h} either pass")
#tt_one_leg.SetFillStyle(1001)
#tt_one_leg.SetLineWidth(0)
#tt_one_leg.AddEntry(tt_one_eff[0],"hps_VVVL","ep")
#tt_one_leg.AddEntry(tt_one_eff[1],"hps_VVL","ep")
#tt_one_leg.AddEntry(tt_one_eff[2],"hps_VL","ep")
#tt_one_leg.AddEntry(tt_one_eff[3],"hps_L","ep")
#tt_one_leg.AddEntry(tt_one_eff[4],"hps_M","ep")
#tt_one_leg.AddEntry(tt_one_eff[5],"hps_T","ep")
#tt_one_leg.AddEntry(tt_one_eff[6],"hps_VT","ep")
#tt_one_leg.Draw("same")
#cmsLatex = ROOT.TLatex()
#cmsLatex.SetTextSize(0.04)
#cmsLatex.SetNDC(True)
#cmsLatex.SetTextFont(61)
#cmsLatex.SetTextAlign(11)
#cmsLatex.DrawLatex(0.1,0.92,"CMS")
#cmsLatex.SetTextFont(52)
#cmsLatex.DrawLatex(0.1+0.07,0.92,"Preliminary")
#tt_one.SaveAs("{}_hps_one_tt.pdf".format(args.mp))

bb = ROOT.TCanvas("bb", "efficiency")
bb.SetGrid()
tt_eff_b[0].Draw("ap")
tt_eff_b[1].Draw("same p")
tt_eff_b[2].Draw("same p")
tt_eff_b[3].Draw("same p")
tt_eff_b[4].Draw("same p")
tt_eff_b[5].Draw("same p")
tt_eff_b[6].Draw("same p")
bb_leg=ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
bb_leg.SetHeader("#tau_{h}-#tau_{h} both pass")
bb_leg.SetFillStyle(1001)
bb_leg.SetLineWidth(0)
bb_leg.AddEntry(tt_eff_b[0],"boosted_VVL","ep")
bb_leg.AddEntry(tt_eff_b[1],"boosted_VL","ep")
bb_leg.AddEntry(tt_eff_b[2],"boosted_L","ep")
bb_leg.AddEntry(tt_eff_b[3],"boosted_M","ep")
bb_leg.AddEntry(tt_eff_b[4],"boosted_T","ep")
bb_leg.AddEntry(tt_eff_b[5],"boosted_VT","ep")
bb_leg.AddEntry(tt_eff_b[6],"boosted_VVT","ep")
bb_leg.Draw("same")
cmsLatex = ROOT.TLatex()
cmsLatex.SetTextSize(0.04)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.DrawLatex(0.1,0.92,"CMS")
cmsLatex.SetTextFont(52)
cmsLatex.DrawLatex(0.1+0.07,0.92,"Preliminary")
bb.SaveAs("{}_boosted_tt.pdf".format(args.mp))

bb_one = ROOT.TCanvas("bb_one", "efficiency")
bb_one.SetGrid()
tt_one_eff_b[0].Draw("ap")
tt_one_eff_b[1].Draw("same p")
tt_one_eff_b[2].Draw("same p")
tt_one_eff_b[3].Draw("same p")
tt_one_eff_b[4].Draw("same p")
tt_one_eff_b[5].Draw("same p")
tt_one_eff_b[6].Draw("same p")
bb_one_leg=ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
bb_one_leg.SetHeader("#tau_{h}-#tau_{h} either pass")
bb_one_leg.SetFillStyle(1001)
bb_one_leg.SetLineWidth(0)
bb_one_leg.AddEntry(tt_one_eff_b[0],"boosted_VVL","ep")
bb_one_leg.AddEntry(tt_one_eff_b[1],"boosted_VL","ep")
bb_one_leg.AddEntry(tt_one_eff_b[2],"boosted_L","ep")
bb_one_leg.AddEntry(tt_one_eff_b[3],"boosted_M","ep")
bb_one_leg.AddEntry(tt_one_eff_b[4],"boosted_T","ep")
bb_one_leg.AddEntry(tt_one_eff_b[5],"boosted_VT","ep")
bb_one_leg.AddEntry(tt_one_eff_b[6],"boosted_VVT","ep")
bb_one_leg.Draw("same")
cmsLatex = ROOT.TLatex()
cmsLatex.SetTextSize(0.04)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.DrawLatex(0.1,0.92,"CMS")
cmsLatex.SetTextFont(52)
cmsLatex.DrawLatex(0.1+0.07,0.92,"Preliminary")
bb_one.SaveAs("{}_boosted_one_tt.pdf".format(args.mp))

#et = ROOT.TCanvas("et", "efficiency")
#et.SetGrid()
#et_eff[0].Draw("ap")
#et_eff[1].Draw("same p")
#et_eff[2].Draw("same p")
#et_eff[3].Draw("same p")
#et_eff[4].Draw("same p")
#et_eff[5].Draw("same p")
#et_eff[6].Draw("same p")
#et_leg = ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
#et_leg.SetHeader("e-#tau_{h}")
#et_leg.SetFillStyle(1001)
#et_leg.SetLineWidth(0)
#et_leg.AddEntry(et_eff[0],"hps_VVVL","ep")
#et_leg.AddEntry(et_eff[1],"hps_VVL","ep")
#et_leg.AddEntry(et_eff[2],"hps_VL","ep")
#et_leg.AddEntry(et_eff[3],"hps_L","ep")
#et_leg.AddEntry(et_eff[4],"hps_M","ep")
#et_leg.AddEntry(et_eff[5],"hps_T","ep")
#et_leg.AddEntry(et_eff[6],"hps_VT","ep")
#et_leg.Draw("same")
#cmsLatex = ROOT.TLatex()
#cmsLatex.SetTextSize(0.04)
#cmsLatex.SetNDC(True)
#cmsLatex.SetTextFont(61)
#cmsLatex.SetTextAlign(11)
#cmsLatex.DrawLatex(0.1,0.92,"CMS")
#cmsLatex.SetTextFont(52)
#cmsLatex.DrawLatex(0.1+0.07,0.92,"Preliminary")
#et.SaveAs("{}_hps_et.pdf".format(args.mp))

eb = ROOT.TCanvas("eb", "efficiency")
eb.SetGrid()
et_eff_b[0].Draw("ap")
et_eff_b[1].Draw("same p")
et_eff_b[2].Draw("same p")
et_eff_b[3].Draw("same p")
et_eff_b[4].Draw("same p")
et_eff_b[5].Draw("same p")
et_eff_b[6].Draw("same p")
eb_leg=ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
eb_leg.SetHeader("e-#tau_{h}")
eb_leg.SetFillStyle(1001)
eb_leg.SetLineWidth(0)
eb_leg.AddEntry(et_eff_b[0],"boosted_VVL","ep")
eb_leg.AddEntry(et_eff_b[1],"boosted_VL","ep")
eb_leg.AddEntry(et_eff_b[2],"boosted_L","ep")
eb_leg.AddEntry(et_eff_b[3],"boosted_M","ep")
eb_leg.AddEntry(et_eff_b[4],"boosted_T","ep")
eb_leg.AddEntry(et_eff_b[5],"boosted_VT","ep")
eb_leg.AddEntry(et_eff_b[6],"boosted_VVT","ep")
eb_leg.Draw("same")
cmsLatex = ROOT.TLatex()
cmsLatex.SetTextSize(0.04)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.DrawLatex(0.1,0.92,"CMS")
cmsLatex.SetTextFont(52)
cmsLatex.DrawLatex(0.1+0.07,0.92,"Preliminary")
eb.SaveAs("{}_boosted_et.pdf".format(args.mp))

#mt = ROOT.TCanvas("mt", "efficiency")
#mt.SetGrid()
#mt_eff[0].Draw("ap")
#mt_eff[1].Draw("same p")
#mt_eff[2].Draw("same p")
#mt_eff[3].Draw("same p")
#mt_eff[4].Draw("same p")
#mt_eff[5].Draw("same p")
#mt_eff[6].Draw("same p")
#mt_leg = ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
#mt_leg.SetHeader("m-#tau_{h}")
#mt_leg.SetFillStyle(1001)
#mt_leg.SetLineWidth(0)
#mt_leg.AddEntry(mt_eff[0],"hps_VVVL","ep")
#mt_leg.AddEntry(mt_eff[1],"hps_VVL","ep")
#mt_leg.AddEntry(mt_eff[2],"hps_VL","ep")
#mt_leg.AddEntry(mt_eff[3],"hps_L","ep")
#mt_leg.AddEntry(mt_eff[4],"hps_M","ep")
#mt_leg.AddEntry(mt_eff[5],"hps_T","ep")
#mt_leg.AddEntry(mt_eff[6],"hps_VT","ep")
#mt_leg.Draw("same")
#cmsLatex = ROOT.TLatex()
#cmsLatex.SetTextSize(0.04)
#cmsLatex.SetNDC(True)
#cmsLatex.SetTextFont(61)
#cmsLatex.SetTextAlign(11)
#cmsLatex.DrawLatex(0.1,0.92,"CMS")
#cmsLatex.SetTextFont(52)
#cmsLatex.DrawLatex(0.1+0.07,0.92,"Preliminary")
#mt.SaveAs("{}_hps_mt.pdf".format(args.mp))

mb = ROOT.TCanvas("mb", "efficiency")
mb.SetGrid()
mt_eff_b[0].Draw("ap")
mt_eff_b[1].Draw("same p")
mt_eff_b[2].Draw("same p")
mt_eff_b[3].Draw("same p")
mt_eff_b[4].Draw("same p")
mt_eff_b[5].Draw("same p")
mt_eff_b[6].Draw("same p")
mb_leg=ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
mb_leg.SetHeader("m-#tau_{h}")
mb_leg.SetFillStyle(1001)
mb_leg.SetLineWidth(0)
mb_leg.AddEntry(mt_eff_b[0],"boosted_VVL","ep")
mb_leg.AddEntry(mt_eff_b[1],"boosted_VL","ep")
mb_leg.AddEntry(mt_eff_b[2],"boosted_L","ep")
mb_leg.AddEntry(mt_eff_b[3],"boosted_M","ep")
mb_leg.AddEntry(mt_eff_b[4],"boosted_T","ep")
mb_leg.AddEntry(mt_eff_b[5],"boosted_VT","ep")
mb_leg.AddEntry(mt_eff_b[6],"boosted_VVT","ep")
mb_leg.Draw("same")
cmsLatex = ROOT.TLatex()
cmsLatex.SetTextSize(0.04)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.DrawLatex(0.1,0.92,"CMS")
cmsLatex.SetTextFont(52)
cmsLatex.DrawLatex(0.1+0.07,0.92,"Preliminary")
mb.SaveAs("{}_boosted_mt.pdf".format(args.mp))
