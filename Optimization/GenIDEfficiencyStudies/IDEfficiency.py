import ROOT
import math 
import time
from plot_dict import *
import argparse

parser = argparse.ArgumentParser(description='Compute Reco + ID efficiency for a signal Sample')
parser.add_argument('--signal','-F',help="file name including the path",required=True)
args = parser.parse_args()



tt_higgspt_pass = ROOT.TH1F("tt_higgspt_pass","tt_higgspt_pass", 40, 0, 2000)
tt_higgspt_pass_b = ROOT.TH1F("tt_higgspt_pass_b","tt_higgspt_pass_b", 40, 0, 2000)
tt_higgspt_total = ROOT.TH1F("tt_higgspt_total","tt_higgspt_total",40, 0, 2000)

et_higgspt_pass = ROOT.TH1F("et_higgspt_pass","et_higgspt_pass", 40, 0, 2000)
et_higgspt_pass_b = ROOT.TH1F("et_higgspt_pass_b","et_higgspt_pass_b", 40, 0, 2000)
et_higgspt_total = ROOT.TH1F("et_higgspt_total","et_higgspt_total",40, 0, 2000)

mt_higgspt_pass = ROOT.TH1F("mt_higgspt_pass","mt_higgspt_pass", 40, 0, 2000)
mt_higgspt_pass_b = ROOT.TH1F("mt_higgspt_pass_b","mt_higgspt_pass_b", 40, 0, 2000)
mt_higgspt_total = ROOT.TH1F("mt_higgspt_total","mt_higgspt_total",40, 0, 2000)

Tau_gen_v1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
Tau_gen_v2 =ROOT.TLorentzVector(0.0,0.0,0.0,0.0) 
Tau_reco=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)

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
        if theTree.GenPart_genPartIdxMother[nPart] < 0:
            continue
        if (abs(theTree.GenPart_pdgId[theTree.GenPart_genPartIdxMother[nPart]]) == 15 and theTree.GenPart_statusFlags[theTree.GenPart_genPartIdxMother[nPart]] == 2 ):
            if (abs(theTree.GenPart_pdgId[theTree.GenPart_genPartIdxMother[theTree.GenPart_genPartIdxMother[nPart]]]) == 25):
                particlesWithTauMother.append((nPart,theTree.GenPart_pdgId[nPart],theTree.GenPart_genPartIdxMother[nPart]))
                continue
            
    decayMode = []
    alreadyAssignedTaus = []
    for particle in particlesWithTauMother:
        if particle[2] not in alreadyAssignedTaus:
            if abs(particle[1]) == 13:
                decayMode.append('m')
                alreadyAssignedTaus.append(particle[2])

            if abs(particle[1]) == 11:
                decayMode.append('e')
                alreadyAssignedTaus.append(particle[2])
            
            if abs(particle[1] > 0):
                decayMode.append('t')
                alreadyAssignedTaus.append(particle[2])

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
        return None 
        


    if len(decayMode) < 2:
        print('too few taus!')
        for tau in particlesWithTauMother:
            if tau[2] not in alreadyAssignedTaus:
                print("{:3n}".format(tau[1])+' Was part of a tau that was not assigned')
                return None
        
    #decayMode.sort()
    return ''.join(decay for decay in decayMode), alreadyAssignedTaus

def tauMatchedandPassed(tree_bbtt,genFourVec,tau_id):
    for j in range(len(tree_bbtt.Tau_pt)):
        i_counter=0
        i_least=0
        delta_r=0
        delta_r_least=0
        Tau_reco.SetPtEtaPhiM(tree_bbtt.Tau_pt[j],tree_bbtt.Tau_eta[j],tree_bbtt.Tau_phi[j],tree_bbtt.Tau_mass[j])
        delta_r = genFourVec.DeltaR(Tau_reco)
        if (i_counter==0 or delta_r<delta_r_least):
            i_least=j
            i_counter=i_counter + 1
            delta_r_least=delta_r
        
        if(delta_r_least < 0.1 
        and i_counter !=0 
        and tree_bbtt.Tau_pt[i_least]>20 
        and abs(tree_bbtt.Tau_eta[i_least])<2.3 
        #and tree_bbtt.Tau_idDecayModeNewDMs[i_least]==1 
        and (tree_bbtt.Tau_idDeepTau2017v2p1VSjet[i_least] & tau_id == tau_id)):
            return True
        else:
            return False

    
def boostedtauMatchedandPassed(tree_bbtt,genFourVec,tau_id):
    for j in range(len(tree_bbtt.boostedTau_pt)):
        i_counter=0
        i_least=0
        delta_r=0
        delta_r_least=0
        Tau_reco.SetPtEtaPhiM(tree_bbtt.Tau_pt[j],tree_bbtt.Tau_eta[j],tree_bbtt.Tau_phi[j],tree_bbtt.Tau_mass[j])
        delta_r = genFourVec.DeltaR(Tau_reco)
        if (i_counter==0 or delta_r<delta_r_least):
            i_least=j
            i_counter=i_counter + 1
            delta_r_least=delta_r
        
        if(delta_r_least < 0.1 
        and i_counter !=0 
        and tree_bbtt.boostedTau_pt[i_least]>20 
        and abs(tree_bbtt.boostedTau_eta[i_least])<2.3 
        #and tree_bbtt.boostedTau_idDecayModeNewDMs[i_least]==1 
        and (tree_bbtt.boostedTau_idMVAnewDM2017v2[i_least] & tau_id == tau_id)):
            return True
        else:
            return False









tau_working = [1,2,4,8,16,32,64]
boostedtau_working = [1,2,4,8,16,32,64]

for y in range(len(tau_working)):
    tau_selected = 0
    tau_passed = 0
    tau_passed_b = 0
    tau_id = tau_working[y]
    btau_id = boostedtau_working[y]
    tt_higgspt_pass.Reset()
    tt_higgspt_pass_b.Reset()
    tt_higgspt_total.Reset()

    et_higgspt_pass.Reset()
    et_higgspt_pass_b.Reset()
    et_higgspt_total.Reset()

    mt_higgspt_pass.Reset()
    mt_higgspt_pass_b.Reset()
    mt_higgspt_total.Reset()

    file_bbtt = ROOT.TFile(args.signal)
    tree_bbtt = file_bbtt.Get('Events')
    nEntries = tree_bbtt.GetEntries()
    print ("Total Events = ",nEntries)


    for event_index in range(nEntries):
        if (event_index%1000 == 0):
            print("events_processed=",event_index)
        tree_bbtt.GetEntry(event_index)
        decay, tauIndices = classifyTauDecayMode(tree_bbtt)
        genTauIndex = []
        if len(tauIndices!=2):
            print("Error, Not exactly two taus")
            continue
        if (tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]!=tree_bbtt.GenPart_genPartIdxMother[tauIndices[1]]):
            print ("Error, Taus have different mothers")
            continue

        if decay == "tt":
            Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[tauIndices[0]],tree_bbtt.GenPart_eta[tauIndices[0]],tree_bbtt.GenPart_phi[tauIndices[0]],tree_bbtt.GenPart_mass[tauIndices[0]])
            Tau_gen_v2.SetPtEtaPhiM(tree_bbtt.GenPart_pt[tauIndices[1]],tree_bbtt.GenPart_eta[tauIndices[1]],tree_bbtt.GenPart_phi[tauIndices[1]],tree_bbtt.GenPart_mass[tauIndices[1]])
            tt_higgspt_total.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
            if (tauMatchedandPassed(tree_bbtt,Tau_gen_v1,tau_id) and tauMatchedandPassed(tree_bbtt,Tau_gen_v2,tau_id)):
                tt_higgspt_pass.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
            if (boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v1,btau_id) and boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v2,btau_id)):
                tt_higgspt_pass_b.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
        
        if (decay == "et" or decay == "te"):
            if decay == "te":
                Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[tauIndices[0]],tree_bbtt.GenPart_eta[tauIndices[0]],tree_bbtt.GenPart_phi[tauIndices[0]],tree_bbtt.GenPart_mass[tauIndices[0]])
            elif decay == "et":
                Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[tauIndices[1]],tree_bbtt.GenPart_eta[tauIndices[1]],tree_bbtt.GenPart_phi[tauIndices[1]],tree_bbtt.GenPart_mass[tauIndices[1]])
            et_higgspt_total.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
            if(tauMatchedandPassed(tree_bbtt,Tau_gen_v1,tau_id)):
                et_higgspt_pass.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
            if(boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v1,btau_id)):
                et_higgspt_pass_b.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
        
        if (decay == "mt" or decay == "tm"):
            if decay == "tm":
                Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[tauIndices[0]],tree_bbtt.GenPart_eta[tauIndices[0]],tree_bbtt.GenPart_phi[tauIndices[0]],tree_bbtt.GenPart_mass[tauIndices[0]])
            elif decay == "mt":
                Tau_gen_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[tauIndices[1]],tree_bbtt.GenPart_eta[tauIndices[1]],tree_bbtt.GenPart_phi[tauIndices[1]],tree_bbtt.GenPart_mass[tauIndices[1]])
            et_higgspt_total.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
            if(tauMatchedandPassed(tree_bbtt,Tau_gen_v1,tau_id)):
                et_higgspt_pass.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])
            if(boostedtauMatchedandPassed(tree_bbtt,Tau_gen_v1,btau_id)):
                et_higgspt_pass_b.Fill(tree_bbtt.GenPart_pt[tree_bbtt.GenPart_genPartIdxMother[tauIndices[0]]])        

                
    tt_eff[y] = ROOT.TGraphAsymmErrors(tt_higgspt_pass,tt_higgspt_total,'e1000')
    tt_eff[y].SetLineColor(linecolor[y+1])
    tt_eff[y].SetMarkerStyle(markerstylesolid[y+1])
    tt_eff[y].SetMarkerColor(markercolor[y+1])
    tt_eff[y].SetMarkerSize(1.5)
    tt_eff[y].SetTitle("Reconstruction + Identification Efficiency")
    tt_eff[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
    tt_eff[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
    tt_eff[y].GetYaxis().SetRangeUser(-0.05,1.1)

    tt_eff_b[y] = ROOT.TGraphAsymmErrors(tt_higgspt_pass_b,tt_higgspt_total,'e1000')
    tt_eff_b[y].SetLineColor(linecolor[y+1])
    tt_eff_b[y].SetMarkerStyle(markerstylesolid[y+1])
    tt_eff_b[y].SetMarkerColor(markercolor[y+1])
    tt_eff_b[y].SetMarkerSize(1.5)
    tt_eff_b[y].SetTitle("Reconstruction + Identification Efficiency")
    tt_eff_b[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
    tt_eff_b[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
    tt_eff_b[y].GetYaxis().SetRangeUser(-0.05,1.1)

    et_eff[y] = ROOT.TGraphAsymmErrors(et_higgspt_pass,et_higgspt_total,'e1000')
    et_eff[y].SetLineColor(linecolor[y+1])
    et_eff[y].SetMarkerStyle(markerstylesolid[y+1])
    et_eff[y].SetMarkerColor(markercolor[y+1])
    et_eff[y].SetMarkerSize(1.5)
    et_eff[y].SetTitle("Reconstruction + Identification Efficiency")
    et_eff[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
    et_eff[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
    et_eff[y].GetYaxis().SetRangeUser(-0.05,1.1)

    et_eff_b[y] = ROOT.TGraphAsymmErrors(et_higgspt_pass_b,et_higgspt_total,'e1000')
    et_eff_b[y].SetLineColor(linecolor[y+1])
    et_eff_b[y].SetMarkerStyle(markerstylesolid[y+1])
    et_eff_b[y].SetMarkerColor(markercolor[y+1])
    et_eff_b[y].SetMarkerSize(1.5)
    et_eff_b[y].SetTitle("Reconstruction + Identification Efficiency")
    et_eff_b[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
    et_eff_b[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
    et_eff_b[y].GetYaxis().SetRangeUser(-0.05,1.1)

    mt_eff[y] = ROOT.TGraphAsymmErrors(mt_higgspt_pass,mt_higgspt_total,'e1000')
    mt_eff[y].SetLineColor(linecolor[y+1])
    mt_eff[y].SetMarkerStyle(markerstylesolid[y+1])
    mt_eff[y].SetMarkerColor(markercolor[y+1])
    mt_eff[y].SetMarkerSize(1.5)
    mt_eff[y].SetTitle("Reconstruction + Identification Efficiency")
    mt_eff[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
    mt_eff[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
    mt_eff[y].GetYaxis().SetRangeUser(-0.05,1.1)

    mt_eff_b[y] = ROOT.TGraphAsymmErrors(mt_higgspt_pass_b,mt_higgspt_total,'e1000')
    mt_eff_b[y].SetLineColor(linecolor[y+1])
    mt_eff_b[y].SetMarkerStyle(markerstylesolid[y+1])
    mt_eff_b[y].SetMarkerColor(markercolor[y+1])
    mt_eff_b[y].SetMarkerSize(1.5)
    mt_eff_b[y].SetTitle("Reconstruction + Identification Efficiency")
    mt_eff_b[y].GetXaxis().SetTitle( "Gen Higgs p_{T}(GeV)")
    mt_eff_b[y].GetYaxis().SetTitle("Reconstruction + Identification Efficiency")
    mt_eff_b[y].GetYaxis().SetRangeUser(-0.05,1.1)





tt = ROOT.TCanvas("tt", "efficiency")
tt.SetGrid()
tt_eff[0].Draw("ap")
tt_eff[1].Draw("same p")
tt_eff[2].Draw("same p")
tt_eff[3].Draw("same p")
tt_eff[4].Draw("same p")
tt_eff[5].Draw("same p")
tt_eff[6].Draw("same p")
tt_leg = ROOT.TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
tt_leg.SetFillStyle(1001)
tt_leg.AddEntry(tt_eff[0],"hps_VVVL","ep")
tt_leg.AddEntry(tt_eff[1],"hps_VVL","ep")
tt_leg.AddEntry(tt_eff[2],"hps_VL","ep")
tt_leg.AddEntry(tt_eff[3],"hps_L","ep")
tt_leg.AddEntry(tt_eff[4],"hps_M","ep")
tt_leg.AddEntry(tt_eff[0],"hps_T","ep")
tt_leg.AddEntry(tt_eff[0],"hps_VT","ep")
tt_leg.Draw("same")
cmsLatex = ROOT.TLatex()
cmsLatex.SetTextSize(0.04)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.DrawLatex(0.1,0.92,"CMS")
cmsLatex.SetTextFont(52)
cmsLatex.DrawLatex(0.1+0.07,0.92,"Preliminary")
tt.SaveAs("hps_tt.pdf")

bb = ROOT.TCanvas("tt", "efficiency")
bb.SetGrid()
tt_eff_b[0].Draw("ap")
tt_eff_b[1].Draw("same p")
tt_eff_b[2].Draw("same p")
tt_eff_b[3].Draw("same p")
tt_eff_b[4].Draw("same p")
tt_eff_b[5].Draw("same p")
tt_eff_b[6].Draw("same p")
bb_leg = ROOT.TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
bb_leg.SetFillStyle(1001)
bb_leg.AddEntry(tt_eff_b[0],"boosted_VVL","ep")
bb_leg.AddEntry(tt_eff_b[1],"boosted_VL","ep")
bb_leg.AddEntry(tt_eff_b[2],"boosted_L","ep")
bb_leg.AddEntry(tt_eff_b[3],"boosted_M","ep")
bb_leg.AddEntry(tt_eff_b[4],"boosted_T","ep")
bb_leg.AddEntry(tt_eff_b[0],"boosted_VT","ep")
bb_leg.AddEntry(tt_eff_b[0],"boosted_VVT","ep")
bb_leg.Draw("same")
cmsLatex = ROOT.TLatex()
cmsLatex.SetTextSize(0.04)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.DrawLatex(0.1,0.92,"CMS")
cmsLatex.SetTextFont(52)
cmsLatex.DrawLatex(0.1+0.07,0.92,"Preliminary")
bb.SaveAs("boosted_tt.pdf")


