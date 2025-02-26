''' Check the composition of the single-tauh background from ttbar'''

from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
import ROOT
import math
from officialStyle import officialStyle
from cmsstyle import CMS_lumi
from efficiency_plots_functions import *

ROOT.gROOT.SetBatch()   
ROOT.gStyle.SetOptStat(0)
officialStyle(ROOT.gStyle, ROOT.TGaxis)


## ttbar background
#infile = ROOT.TFile.Open("root://cms-xrd-global.cern.ch//store/user/friti/ttbar_nano_2024Sep15/CRAB_UserFiles/crab_dylowmass/240915_143630/0000/ttbar_job_5.root")        
infile = ROOT.TFile.Open("root://cms-xrd-global.cern.ch//store/user/friti/ttbar_nano_2024Sep15/CRAB_UserFiles/crab_dylowmass/240915_143630/0000/ttbar_job_1.root")        
tree = InputTree(infile.Events)

total = 0
b_decays = 0
w_decays = 0
w_ind_decays = 0
b_baryon_decay = 0
notidrect_w_decay = 0
gluons  = 0
nothing = 0
for i in range(tree.GetEntries()):
    event = Event(tree,i)

    ## look for single-tauh events matching with ak4 jets
    genvistaus = Collection(event, "GenVisTau")
    jets = Collection(event, "Jet")
    genparts = Collection(event, "GenPart")

    # loop over hadronic taus
    for genvistau in genvistaus:
        gentau_idx = genvistau.genPartIdxMother
        # match with jet
        jet,dr = closest(genvistau,jets)
        if dr<0.4:
            total +=1
            ## find ancestors of the tauh
            for genpart in genparts:
                if genpart._index != genparts[gentau_idx].genPartIdxMother : continue
                tau_mother = genpart._index
            for genpart in genparts:
                if genpart._index != genparts[tau_mother].genPartIdxMother : continue
                tau_grandmother = genpart._index
            for genpart in genparts:
                if genpart._index != genparts[tau_grandmother].genPartIdxMother : continue
                tau_grandgrandmother = genpart._index
            for genpart in genparts:
                if genpart._index != genparts[tau_grandgrandmother].genPartIdxMother : continue
                tau_grandgrandgrandmother = genpart._index

            ## print decay modes
            print(genparts[tau_grandgrandgrandmother].pdgId," ---> ")
            for genpart in genparts:
                if genpart.genPartIdxMother != tau_grandgrandgrandmother: continue
                print(genpart.pdgId," + ")

            print(genparts[tau_grandgrandmother].pdgId," ---> ")
            for genpart in genparts:
                if genpart.genPartIdxMother != tau_grandgrandmother: continue
                print(genpart.pdgId," + ")

            print(genparts[tau_grandmother].pdgId," ---> ")
            for genpart in genparts:
                if genpart.genPartIdxMother != tau_grandmother: continue
                print(genpart.pdgId," + ")

            print(genparts[tau_mother].pdgId," ---> ")
            for genpart in genparts:
                if genpart.genPartIdxMother != tau_mother: continue
                print(genpart.pdgId," + ")


            if abs(genparts[tau_mother].pdgId) == 511 or abs(genparts[tau_mother].pdgId) == 521 or abs(genparts[tau_mother].pdgId) == 531 or abs(genparts[tau_grandmother].pdgId) == 511 or abs(genparts[tau_grandmother].pdgId) == 521 or abs(genparts[tau_grandmother].pdgId) == 531 or abs(genparts[tau_grandgrandmother].pdgId) == 511 or abs(genparts[tau_grandgrandmother].pdgId) == 521 or abs(genparts[tau_grandgrandmother].pdgId) == 531 or abs(genparts[tau_mother].pdgId) == 541 or abs(genparts[tau_grandmother].pdgId) == 541 or abs(genparts[tau_grandgrandmother].pdgId) == 541 :
                b_decays += 1
                print("A b-decay!!")
            elif abs(genparts[tau_mother].pdgId)==24: 
                w_decays += 1
                print("A direct W-decay!!")
            elif abs(genparts[tau_grandmother].pdgId)==24:
                w_ind_decays += 1
                print("A W-decay with photon!!")
            elif abs(genparts[tau_grandgrandmother].pdgId)==24 or abs(genparts[tau_grandgrandgrandmother].pdgId)==24:
                notidrect_w_decay +=1
                print("A W2-decay!!")
            elif abs(genparts[tau_mother].pdgId) == 5122 or abs(genparts[tau_grandmother].pdgId) == 5122 or abs(genparts[tau_grandgrandmother].pdgId) == 5122 or abs(genparts[tau_mother].pdgId) == 5132 or abs(genparts[tau_grandmother].pdgId) == 5132 or abs(genparts[tau_grandgrandmother].pdgId) == 5132 or abs(genparts[tau_mother].pdgId) == 5232 or abs(genparts[tau_grandmother].pdgId) == 5232 or abs(genparts[tau_grandgrandmother].pdgId) == 5232:
                b_baryon_decay += 1
                print("A baryon decay!!")
            elif abs(genparts[tau_mother].pdgId) == 21 or abs(genparts[tau_grandmother].pdgId) == 21 or abs(genparts[tau_grandgrandmother].pdgId) == 21 or abs(genparts[tau_grandgrandgrandmother].pdgId) == 21 or abs(genparts[tau_mother].pdgId) == 22 or abs(genparts[tau_grandmother].pdgId) == 22 or abs(genparts[tau_grandgrandmother].pdgId) == 22 or abs(genparts[tau_grandgrandgrandmother].pdgId) == 22:
                gluons += 1
                print("A gluon-decay!!")
            else:
                print("NOTHING")
                nothing += 1
                
        print(" ")


print("total", total,"w decays ",w_decays, w_decays/total,"w decay + photon",w_ind_decays,w_ind_decays/total," b decays ",b_decays," other w decays ",notidrect_w_decay, notidrect_w_decay/total," b_baryon_decay ",b_baryon_decay," gluons ",gluons, "nothing", nothing)
