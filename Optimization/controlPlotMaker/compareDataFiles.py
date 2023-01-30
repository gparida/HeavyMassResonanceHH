from numbers import Integral
import ROOT
import argparse  ##Importing root and package to take arguments 
from controlPlotDictionaryCamilla import *
import os
from array import array
import glob
from re import search

#This is a class that I burrowed from Control Plot Script to create the histograms for the different datasets -
# The histograms are stored as objects and Draw command is used to create the histogram
class MakeHistograms(object):
    #constructor to initialize the objects
    def __init__(self,RootFilePath,RootFileName, userWeight = "1.0"):
        self.RootFileName = ROOT.TFile(RootFilePath+RootFileName+'.root')
        self.HistogramName = None
        self.userWeight = userWeight

    #Cut creating member function
    def CreateCutString(self,standardCutString,
                    otherCuts,
                    weighting):
    #cutString = weighting+'*('+standardCutString+' && '
        if standardCutString != None:
            cutString =weighting+'*('+'('+standardCutString+')'+' && '
            if otherCuts!=None:
                for cut in otherCuts:
                    cutString += '('+cut+')' + ' && '
        else:
            cutString=weighting +' && '
        cutString = cutString[:len(cutString)-3] # removing the && at the very end of the final cutstring
        cutString+=')'
        return cutString
        
    #Histogram Making member function and storing it in an attribute
    def StandardDraw(self,theFile,
                 variable,
                 standardCutString,
                 additionalSelections,
                 histogramName,
                 theWeight = 'FinalWeighting'):

        theTree = theFile.Get('Events')

        print (variable+'>>'+histogramName+'('+variableSettingDictionary[variable]+')',
                         self.CreateCutString(standardCutString,
                                         additionalSelections,theWeight))
        
        theTree.Draw(variable+'>>'+histogramName+'('+variableSettingDictionary[variable]+')',
                self.CreateCutString(standardCutString,
                                additionalSelections,theWeight))
            
    #so, if the tree has no entries, root doesn't even hand back an empty histogram
    #and therefore this ends up trying to get clone a none type
    #pass the None forward, and we can let the Add handle this
        try:
            theHisto = ROOT.gDirectory.Get(histogramName).Clone()
        except ReferenceError:
            theHisto = None
        #return theHisto
        self.HistogramName=theHisto
    


#Helps to add hostograms of the binned datasets
def clubHistograms(list,histObjects):
    clubHist = None
    for name in list:
        if histObjects[name].HistogramName != None:
            if clubHist == None:
                clubHist = histObjects[name].HistogramName.Clone()
            clubHist.Add(histObjects[name].HistogramName)
    return clubHist

#The histogram styling function
def setStyleOfPlot(hist1,hist2,plotVar):
    hist1.SetMarkerStyle(20)
    hist1.SetMarkerSize(0.7)
    hist1.Sumw2()
    hist1.GetXaxis().SetTitle(plotVar)

    hist2.SetMarkerStyle(21)
    hist2.SetMarkerSize(0.7)
    hist2.SetMarkerColor(2)
    hist2.Sumw2()
    hist2.GetXaxis().SetTitle(plotVar)

    maxi =max(hist1.GetMaximum(),hist2.GetMaximum())
    hist1.SetMaximum(maxi + 0.5*maxi)

#Canvas styling function
def drawOncanvas (hist1,hist2,savefile):
    can = ROOT.TCanvas("hist1", "hist2")
    can.SetGrid()
    can_leg=ROOT.TLegend(0.90, 0.45, 1.0, 0.75, "", "brNDC")
    can_leg.SetFillStyle(1001)
    can_leg.SetLineWidth(0)
    hist1.Draw("p")
    hist2.Draw("same p")
    can_leg.AddEntry(hist1,"old_Set","ep")
    can_leg.AddEntry(hist2,"new_Set","ep")
    can_leg.Draw("same")
    can.SaveAs(savefile+".pdf")

def main():
    parser = argparse.ArgumentParser(description='Compare plots for different data files ')

    parser.add_argument('--dp1',help='path of first set of files',required=True)
    parser.add_argument('--dp2',help='path of second set of files',required=True)
    parser.add_argument('--variables',
                    nargs='+',
                    help='Variables to draw the control plots for',
                    default=["gFatJet_pt",
                            "gFatJet_eta",
                            "gFatJet_msoftdrop",
                            "MET_ pt",
                            "allTau_pt",
                            "allTau_eta",
                            "gDeltaR_LL"])
    parser.add_argument('--additionalSelections','-C2',
                        nargs='+',
                        help='additional region selections',
                        default=["gDeltaR_LL<1.5","gDeltaR_LL>0","fastMTT_RadionLegWithMet_m>750","fastMTT_RadionLegWithMet_m<4250"])
    parser.add_argument('--standardCutString','-C1',
                        nargs='?',
                        help='Change the standard cutting definition',
                        default="")
    parser.add_argument('--Channel',choices=["tt","et","mt"], required=True)
    parser.add_argument('--Weight',help='weight to be added to MC', default='FinalWeighting')

    args = parser.parse_args()

    ROOT.gStyle.SetOptStat(0)

    #First we need to sort files into different datasets
    fileSet_1 = glob.glob(args.dp1 + "*.root")
    DatasetNameList_one=[]
    DYlow_HistoList_one=[]
    DY_HistoList_one=[]
    ST_HistoList_one=[]
    QCD_HistoList_one=[]
    WJets_HistoList_one=[]
    TT_HistoList_one=[]
    DiBoson_HistoList_one=[]
    Other_HistoList_one=[]
    Data_HistoList_one=[]
    SignalNameList_one =[]

    for file in fileSet_1:
        nameStrip=file.strip()
        filename = (nameStrip.split('/')[-1]).split('.')[-2]
        if (not search("Radion",filename)):
            DatasetNameList_one.append(filename)
        #else:
        #    SignalNameList_one.append(filename)
        #    if (search(args.massPoint,filename)):
        #        SignalToPlot = filename


        if search("TTT", filename):
            TT_HistoList_one.append(filename)
        if ((search("DY",filename) and search("M-10to50",filename)) or (search("DY",filename) and search("M-4to50",filename))):
            DYlow_HistoList_one.append(filename)
        if ((search("DY",filename))):
            if (( not search("M-10to50",filename)) and ((not search("M-4to50",filename)))): 
                DY_HistoList_one.append(filename)
        if search("WJet", filename):
            WJets_HistoList_one.append(filename)
        if search("ST_", filename):
            ST_HistoList_one.append(filename)
        if search("QCD", filename):
            QCD_HistoList_one.append(filename)
        if (search("WW", filename) or search("WZ", filename) or search("ZZ", filename)):
            DiBoson_HistoList_one.append(filename)
        if (search("Data",filename)):
            Data_HistoList_one.append(filename)
            

    Other_HistoList_one= QCD_HistoList_one + DiBoson_HistoList_one + ST_HistoList_one

    print ("##########################################################################")
    print ("For the file set 1:")
    print ("TT = ",TT_HistoList_one)
    print ("DY Low = ", DYlow_HistoList_one)
    print ("DY = ", DY_HistoList_one)
    print ("WJets = ", WJets_HistoList_one)
    print ("ST = ", ST_HistoList_one)
    print ("QCD = ", QCD_HistoList_one)
    print ("Diboson = ", DiBoson_HistoList_one)
    print ("##########################################################################")        
    #Now do it for the other set of files

    fileSet_2 = glob.glob(args.dp2 + "*.root")
    DatasetNameList_two=[]
    DYlow_HistoList_two=[]
    DY_HistoList_two=[]
    ST_HistoList_two=[]
    QCD_HistoList_two=[]
    WJets_HistoList_two=[]
    TT_HistoList_two=[]
    DiBoson_HistoList_two=[]
    Other_HistoList_two=[]
    Data_HistoList_two=[]

    #SignalNameList_two =[]

    for file in fileSet_2:
        nameStrip=file.strip()
        filename = (nameStrip.split('/')[-1]).split('.')[-2]
        if (not search("Radion",filename)):
            DatasetNameList_two.append(filename)
        #else:
        #    SignalNameList_two.append(filename)
        #    if (search(args.massPoint,filename)):
        #        SignalToPlot = filename


        if search("TTT", filename):
            TT_HistoList_two.append(filename)
        if ((search("DY",filename) and search("M-10to50",filename)) or (search("DY",filename) and search("M-4to50",filename))):
            DYlow_HistoList_two.append(filename)
        if ((search("DY",filename))):
            if (( not search("M-10to50",filename)) and ((not search("M-4to50",filename)))): 
                DY_HistoList_two.append(filename)
        if search("WJet", filename):
            WJets_HistoList_two.append(filename)
        if search("ST_", filename):
            ST_HistoList_two.append(filename)
        if search("QCD", filename):
            QCD_HistoList_two.append(filename)
        if (search("WW", filename) or search("WZ", filename) or search("ZZ", filename)):
            DiBoson_HistoList_two.append(filename)            
        if (search("Data",filename)):
            Data_HistoList_two.append(filename)
    Other_HistoList_two= QCD_HistoList_two + DiBoson_HistoList_two + ST_HistoList_two
    print ("##########################################################################")
    print ("For the file set 2:")
    print ("TT = ",TT_HistoList_two)
    print ("DY Low = ", DYlow_HistoList_two)
    print ("DY = ", DY_HistoList_two)
    print ("WJets = ", WJets_HistoList_two)
    print ("ST = ", ST_HistoList_two)
    print ("QCD = ", QCD_HistoList_two)
    print ("Diboson = ", DiBoson_HistoList_two)
    print ("##########################################################################")    

    
    #For loop to draw histograms
    for variable in args.variables:
        try:
            variableSettingDictionary[variable] != None
        except KeyError:
            print("No defined histogram settings for variable: "+variable)
            continue
        try:
            variableAxisTitleDictionary[variable]
        except KeyError:
            print("No defined title information for variable: "+variable)
            continue

        DatasetObjects_one={}
        DatasetObjects_two={}

        for index in range(len(DatasetNameList_one)) :
            #DatasetObjects[DatasetNameList[index]]=MakeHistograms(dataPath,DatasetNameList[index],str(DatasetNameXSWeightDictionary[DatasetNameList[index]]))
            DatasetObjects_one[DatasetNameList_one[index]]=MakeHistograms(args.dp1,DatasetNameList_one[index])

        for index in range(len(DatasetNameList_one)):
            #print DatasetNameList[index]
            if DatasetNameList_one[index] == "Data":
                DatasetObjects_one[DatasetNameList_one[index]].StandardDraw(DatasetObjects_one[DatasetNameList_one[index]].RootFileName,
                variable,
                args.standardCutString,
                args.additionalSelections,
                DatasetNameList_one[index],theWeight='1')
            else:
                DatasetObjects_one[DatasetNameList_one[index]].StandardDraw(DatasetObjects_one[DatasetNameList_one[index]].RootFileName,
                    variable,
                    args.standardCutString,
                    args.additionalSelections,
                    DatasetNameList_one[index],theWeight=args.Weight)
                   # DatasetObjects[DatasetNameList[index]].userWeight)  
                #DatasetObjects[DatasetNameList[index]].FillEvents((DatasetObjects[DatasetNameList[index]].RootFileName),DatasetNameList[index])

        for index in range(len(DatasetNameList_two)) :
            #DatasetObjects[DatasetNameList[index]]=MakeHistograms(dataPath,DatasetNameList[index],str(DatasetNameXSWeightDictionary[DatasetNameList[index]]))
            DatasetObjects_two[DatasetNameList_two[index]]=MakeHistograms(args.dp2,DatasetNameList_two[index])

        for index in range(len(DatasetNameList_two)):
            #print DatasetNameList[index]
            if DatasetNameList_two[index] == "Data":
                DatasetObjects_two[DatasetNameList_two[index]].StandardDraw(DatasetObjects_two[DatasetNameList_two[index]].RootFileName,
                variable,
                args.standardCutString,
                args.additionalSelections,
                DatasetNameList_two[index],theWeight='1')
            else:
                DatasetObjects_two[DatasetNameList_two[index]].StandardDraw(DatasetObjects_two[DatasetNameList_two[index]].RootFileName,
                    variable,
                    args.standardCutString,
                    args.additionalSelections,
                    DatasetNameList_two[index],theWeight=args.Weight)
                   # DatasetObjects[DatasetNameList[index]].userWeight)  
                #DatasetObjects[DatasetNameList[index]].FillEvents((DatasetObjects[DatasetNameList[index]].RootFileName),DatasetNameList[index])

        DYlow_Histo_one = clubHistograms(DYlow_HistoList_one,DatasetObjects_one)
        DYlow_Histo_two = clubHistograms(DYlow_HistoList_two,DatasetObjects_two)

        DY_Histo_one = clubHistograms(DY_HistoList_one,DatasetObjects_one)
        DY_Histo_two = clubHistograms(DY_HistoList_two,DatasetObjects_two)

        ST_Histo_one = clubHistograms(ST_HistoList_one,DatasetObjects_one)
        ST_Histo_two = clubHistograms(ST_HistoList_two,DatasetObjects_two)

        QCD_Histo_one = clubHistograms(QCD_HistoList_one,DatasetObjects_one)
        QCD_Histo_two = clubHistograms(QCD_HistoList_two,DatasetObjects_two)

        WJets_Histo_one = clubHistograms(WJets_HistoList_one,DatasetObjects_one)
        WJets_Histo_two = clubHistograms(WJets_HistoList_two,DatasetObjects_two)

        TT_Histo_one = clubHistograms(TT_HistoList_one,DatasetObjects_one)
        TT_Histo_two = clubHistograms(TT_HistoList_two,DatasetObjects_two)        

        DiBoson_Histo_one = clubHistograms(DiBoson_HistoList_one,DatasetObjects_one)
        DiBoson_Histo_two = clubHistograms(DiBoson_HistoList_two,DatasetObjects_two)

        Other_Histo_one = clubHistograms(Other_HistoList_one,DatasetObjects_one)
        Other_Histo_two = clubHistograms(Other_HistoList_two,DatasetObjects_two)

        Data_Histo_one = clubHistograms(Data_HistoList_one,DatasetObjects_one)
        Data_Histo_two = clubHistograms(Data_HistoList_two,DatasetObjects_two)


        setStyleOfPlot(DYlow_Histo_one,DYlow_Histo_two,variableAxisTitleDictionary[variable])
        setStyleOfPlot(DY_Histo_one,DY_Histo_two,variableAxisTitleDictionary[variable])
        setStyleOfPlot(ST_Histo_one,ST_Histo_two,variableAxisTitleDictionary[variable])        
        setStyleOfPlot(QCD_Histo_one,QCD_Histo_two,variableAxisTitleDictionary[variable])
        setStyleOfPlot(WJets_Histo_one,WJets_Histo_two,variableAxisTitleDictionary[variable])        
        setStyleOfPlot(TT_Histo_one,TT_Histo_two,variableAxisTitleDictionary[variable])        
        setStyleOfPlot(DiBoson_Histo_one,DiBoson_Histo_two,variableAxisTitleDictionary[variable])        
        setStyleOfPlot(Other_Histo_one,Other_Histo_two,variableAxisTitleDictionary[variable])
        setStyleOfPlot(Data_Histo_one,Data_Histo_two,variableAxisTitleDictionary[variable])
        setStyleOfPlot(DatasetObjects_one["TTToSemiLeptonic"].HistogramName,DatasetObjects_two["TTToSemiLeptonic"].HistogramName,variableAxisTitleDictionary[variable])
        setStyleOfPlot(DatasetObjects_one["WJets_HT-1200to2500"].HistogramName,DatasetObjects_two["WJetsToLNu_HT-1200To2500"].HistogramName,variableAxisTitleDictionary[variable])        

        drawOncanvas(DYlow_Histo_one,DYlow_Histo_two,"DYlow_"+variableAxisTitleDictionary[variable]+"_"+args.Channel)
        drawOncanvas(DY_Histo_one,DY_Histo_two,"DY_"+variableAxisTitleDictionary[variable]+"_"+args.Channel)
        drawOncanvas(ST_Histo_one,ST_Histo_two,"ST_"+variableAxisTitleDictionary[variable]+"_"+args.Channel)        
        drawOncanvas(QCD_Histo_one,QCD_Histo_two,"QCD_"+variableAxisTitleDictionary[variable]+"_"+args.Channel)
        drawOncanvas(WJets_Histo_one,WJets_Histo_two,"WJets_"+variableAxisTitleDictionary[variable]+"_"+args.Channel)    
        drawOncanvas(TT_Histo_one,TT_Histo_two,"TT_"+variableAxisTitleDictionary[variable]+"_"+args.Channel)        
        drawOncanvas(DiBoson_Histo_one,DiBoson_Histo_two,"DiBoson_"+variableAxisTitleDictionary[variable]+"_"+args.Channel)
        drawOncanvas(Other_Histo_one,Other_Histo_two,"Other_"+variableAxisTitleDictionary[variable]+"_"+args.Channel)
        drawOncanvas(Data_Histo_one,Data_Histo_two,"Data_"+variableAxisTitleDictionary[variable]+"_"+args.Channel)
        drawOncanvas(DatasetObjects_one["TTToSemiLeptonic"].HistogramName,DatasetObjects_two["TTToSemiLeptonic"].HistogramName,"TTSemiLeptonic_"+variableAxisTitleDictionary[variable]+"_"+args.Channel)
        drawOncanvas(DatasetObjects_one["WJets_HT-1200to2500"].HistogramName,DatasetObjects_two["WJetsToLNu_HT-1200To2500"].HistogramName,"WJets_HT-1200to2500"+variableAxisTitleDictionary[variable]+"_"+args.Channel)            

if __name__ == '__main__':
    main()