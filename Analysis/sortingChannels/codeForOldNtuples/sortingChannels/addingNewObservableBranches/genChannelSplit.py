import ROOT

def VerfindingMotherPart(tree,Ind,parentId, interId):
    print ("Finding Tau Parent: Current pdg ",tree.GenPart_pdgId[Ind], " Parent pdg = ",tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]])
    if abs(tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]]) == parentId:
        return True
    elif abs(tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]]) == interId:
        return VerfindingMotherPart(tree,tree.GenPart_genPartIdxMother[Ind],parentId,interId)
    else:
        return False

def findingMotherPart(tree,Ind,parentId, interId):
    if tree.GenPart_genPartIdxMother[Ind] < 0:
        return False
    if abs(tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]]) == parentId:
        return True
    elif abs(tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[Ind]]) == interId:
        #print ("What is index of the parent",tree.GenPart_genPartIdxMother[Ind])
        #print ("event_info=",tree.run,tree.luminosityBlock,tree.event)
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
        #return "moreh", None, None, None
        return "moreh",visTauInd,genlep,None #This fix is required since if I return "None" type to the genMatchingForLepton.py it will crash as it is not iterable
    
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
                comp_four_vec.SetPtEtaPhiM(theTree.GenPart_pt[nPart],theTree.GenPart_eta[nPart],theTree.GenPart_phi[nPart],theTree.GenPart_mass[nPart])
                tau_four_vec_tot = tau_four_vec_tot + comp_four_vec
        if (tau_four_vec_tot.Pt > 0):
            decayMode.insert(0,'t')
            #print ("Fixed",''.join(decay for decay in decayMode), visTauInd, genlep, tau_four_vec_tot)
            return ''.join(decay for decay in decayMode), visTauInd, genlep, tau_four_vec_tot
        else:
            #return "one", None, None, None
            return "one", visTauInd, genlep, None #Cannot return None type in interables

    if(len(decayMode)==0):
        print ("Empty List",theTree.event,theTree.luminosityBlock,theTree.run)
        #return "zero",None,None,None
        return "zero",visTauInd,genlep,None #Cannot return None type in interables

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
        #return "more", None, None, None
        return "more",visTauInd,genlep,None #Cannot return None type in interables
    
    #if (tree_bbtt.GenPart_genPartIdxMother[genTauInd[0]]!=tree_bbtt.GenPart_genPartIdxMother[genTauInd[1]]):
    if (findingMotherPart(theTree,genTauInd[0],25,15) != findingMotherPart(theTree,genTauInd[1],25,15)):
        print ("Error, Taus have different mothers",findingMotherPart(theTree,genTauInd[0],25,15) and findingMotherPart(theTree,genTauInd[1],25,15))
        #return None, None, None, None
        return None,visTauInd,genlep,None #Cannot return None type in interables
    
    #print ("eventloop return",''.join(decay for decay in decayMode), len(genlep), theTree.GenPart_pdgId[genlep[0]])
    return ''.join(decay for decay in decayMode), visTauInd, genlep, None


def findingBQuarks(theTree):
    MadgenBQuarkIndexPostive = -1
    MadgenBQuarkIndexNegative = -1
    PythiagenBQuarkIndexPositive=-1
    PythiagenBQuarkIndexNegative=-1
    noPythiaEvent = False
    for nPart in range(theTree.nGenPart):
        #print ("Gen Part Status = ",theTree.GenPart_status[nPart],theTree.GenPart_pdgId[nPart])
        if ((theTree.GenPart_genPartIdxMother[nPart] < 0) or abs(theTree.GenPart_pdgId[nPart])!=5):
            continue
        #print ("the status before = ",theTree.GenPart_status[nPart],theTree.GenPart_pdgId[nPart],theTree.GenPart_pdgId[theTree.GenPart_genPartIdxMother[nPart]])
        if (findingMotherPart(theTree,nPart,25,5)):
            if (theTree.GenPart_pdgId[nPart] == 5):
                #print ("the status = ",theTree.GenPart_status[nPart],theTree.GenPart_pdgId[nPart],theTree.GenPart_pdgId[theTree.GenPart_genPartIdxMother[nPart]])
                if(theTree.GenPart_status[nPart]==23):
                    MadgenBQuarkIndexPostive=nPart
                else:
                    PythiagenBQuarkIndexPositive=nPart
            elif (theTree.GenPart_pdgId[nPart] == -5):
                if(theTree.GenPart_status[nPart]==23):
                    MadgenBQuarkIndexNegative=nPart
                else:
                    PythiagenBQuarkIndexNegative=nPart
    if (PythiagenBQuarkIndexPositive < 0):
        #print ("Pythia b+ quark not found")
        PythiagenBQuarkIndexPositive = MadgenBQuarkIndexPostive
        noPythiaEvent = True 
    if (PythiagenBQuarkIndexNegative < 0):
        #print ("Pythia b- quark not found")
        noPythiaEvent = True
        PythiagenBQuarkIndexNegative = MadgenBQuarkIndexNegative
    #print ("bquark index",MadgenBQuarkIndexPostive,MadgenBQuarkIndexNegative,PythiagenBQuarkIndexPositive,PythiagenBQuarkIndexNegative,theTree.run,theTree.luminosityBlock,theTree.event)
    MadPos = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
    MadPos.SetPtEtaPhiM(theTree.GenPart_pt[MadgenBQuarkIndexPostive],theTree.GenPart_eta[MadgenBQuarkIndexPostive],theTree.GenPart_phi[MadgenBQuarkIndexPostive],theTree.GenPart_mass[MadgenBQuarkIndexPostive])
    MadNeg = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
    MadNeg.SetPtEtaPhiM(theTree.GenPart_pt[MadgenBQuarkIndexNegative],theTree.GenPart_eta[MadgenBQuarkIndexNegative],theTree.GenPart_phi[MadgenBQuarkIndexNegative],theTree.GenPart_mass[MadgenBQuarkIndexNegative])
    PythiaPos= ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
    PythiaPos.SetPtEtaPhiM(theTree.GenPart_pt[PythiagenBQuarkIndexPositive],theTree.GenPart_eta[PythiagenBQuarkIndexPositive],theTree.GenPart_phi[PythiagenBQuarkIndexPositive],theTree.GenPart_mass[PythiagenBQuarkIndexPositive])
    PythiaNeg = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
    PythiaNeg.SetPtEtaPhiM(theTree.GenPart_pt[PythiagenBQuarkIndexNegative],theTree.GenPart_eta[PythiagenBQuarkIndexNegative],theTree.GenPart_phi[PythiagenBQuarkIndexNegative],theTree.GenPart_mass[PythiagenBQuarkIndexNegative])
    return MadPos+MadNeg, PythiaPos+PythiaNeg, MadPos, MadNeg, PythiaPos, PythiaNeg, noPythiaEvent   


    


            



