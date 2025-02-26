'''
Comparison of the pt distribution of the single -tau_h bkg and the Bs-> tauhtaux, where all the tau_h are included
'''

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

# bs tau tau nanoAOD
signal_file = ROOT.TFile.Open("root://storage01.lcg.cscs.ch:1096//pnfs/lcg.cscs.ch/cms/trivcat/store/user/friti/bstt_nano_2024Jun25/CRAB_UserFiles/crab_bstt/240625_125910/0000/bstt_job_226.root")

## ttbar background nanoAOD
bkg_file = ROOT.TFile.Open("root://cms-xrd-global.cern.ch//store/user/friti/ttbar_nano_2024Sep15/CRAB_UserFiles/crab_dylowmass/240915_143630/0000/ttbar_job_50.root")        
#infile = ROOT.TFile.Open("root://cms-xrd-global.cern.ch//store/user/friti/ttbar_nano_2024Sep15/CRAB_UserFiles/crab_dylowmass/240915_143630/0000/ttbar_job_5.root")        

tree_signal = InputTree(signal_file.Events)
tree_bkg = InputTree(bkg_file.Events)

histo_sig = ROOT.TH1F("B_{s}#rightarrow#tau_{h}#tau_{X}","B_{s}#to#tau_{h}#tau_{X}",50,0,140)
histo_bkg = ROOT.TH1F("single-#tau_{h} from t#bar{t}","t#bar{t}",50,0,140)

## bkg matching
for i in range(tree_bkg.GetEntries()):
    event = Event(tree_bkg,i)

    ## look for single tau events matching with ak4 jets
    genvistaus = Collection(event, "GenVisTau")
    jets = Collection(event, "Jet")
    genparts = Collection(event, "GenPart")

    # loop over only hadronic taus
    for genvistau in genvistaus:
        gentau_idx = genvistau.genPartIdxMother
        # all genvistaus that match with jet with dr<0.4 are selected for the training
        jet,dr = closest(genvistau,jets)
        if dr<0.4:
            histo_bkg.Fill(genvistau.pt)


## signal matching
for i in range(tree_signal.GetEntries()):
    event = Event(tree_signal,i)

    ## look for Bs->tau_h tau_X candidates matching with ak4 jets
    genvistaus = Collection(event, "GenVisTau")
    jets = Collection(event, "Jet")
    genparts = Collection(event, "GenPart")

    tot_dau_tauh = []
    for bs_idx,bs in enumerate(genparts):
        if abs(bs.pdgId)!=531: continue #if not Bs continue
        all_dau_taus = []
        dau_tauh = []
        for tau_idx,tau in enumerate(genparts):
            if abs(tau.pdgId)==15:
                if tau.genPartIdxMother == bs_idx:
                    all_dau_taus.append(tau_idx)
        if len(all_dau_taus) != 2: continue
        # one of them has to decay hadronically
        for genvistau in genvistaus:
            tauh_idx = genvistau.genPartIdxMother
            if tauh_idx in all_dau_taus: # it's one of the bs daughters
                jet,dr = closest(genvistau,jets)
                if dr<0.4:
                    histo_sig.Fill(genvistau.pt)
                

c1 = ROOT.TCanvas()
c1.Draw()
histo_sig.SetFillStyle(0)
histo_sig.SetLineColor(ROOT.kBlue)
histo_sig.SetTitle(";GEN visible #tau_{h} p_{T} (GeV); norm")
histo_sig.DrawNormalized("HIST")
histo_bkg.SetFillStyle(0)
histo_bkg.SetLineColor(ROOT.kRed)
histo_bkg.DrawNormalized("HIST same")

leg = ROOT.TLegend(0.60,.75,.90,.90)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(histo_sig,histo_sig.GetName(),'L')
leg.AddEntry(histo_bkg,histo_bkg.GetName(),'L')
leg.Draw("same")
c1.Update()
c1.SaveAs("genvisible_tauh_pt_sig_vs_singletauh.png")

## bkg matching (only single-tauh from W decays)
for i in range(tree_bkg.GetEntries()):
    event = Event(tree_bkg,i)

    ## look for single tau events matching with ak4 jets
    genvistaus = Collection(event, "GenVisTau")
    jets = Collection(event, "Jet")
    genparts = Collection(event, "GenPart")

    # loop over only hadronic taus
    for genvistau in genvistaus:
        gentau_idx = genvistau.genPartIdxMother
        ## tau coming from a W
        #print(genparts[genvistau.genPartIdxMother].genPartIdxMother)
        if abs(genparts[genparts[genvistau.genPartIdxMother].genPartIdxMother].pdgId) != 24 : continue
        # all genvistaus that match with jet with dr<0.4 are selected for the training
        jet,dr = closest(genvistau,jets)
        if dr<0.4:
            histo_bkg.Fill(genvistau.pt)

            
c1 = ROOT.TCanvas()
c1.Draw()
histo_sig.SetFillStyle(0)
histo_sig.SetLineColor(ROOT.kBlue)
histo_sig.SetTitle(";GEN visible #tau_{h} p_{T} (GeV); norm")
histo_sig.DrawNormalized("HIST")
histo_bkg.SetFillStyle(0)
histo_bkg.SetLineColor(ROOT.kRed)
histo_bkg.DrawNormalized("HIST same")

leg = ROOT.TLegend(0.60,.75,.90,.90)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(histo_sig,histo_sig.GetName(),'L')
leg.AddEntry(histo_bkg,'single-#tau_{h} from W','L')
leg.Draw("same")
c1.Update()
c1.SaveAs("genvisible_tauh_pt_sig_vs_singletauh_fromW.png")


#### GEN TAUS and not GEN VISIBLE TAUS
## signal matching
for i in range(tree_signal.GetEntries()):
    event = Event(tree_signal,i)

    ## look for Bs->tau_h tau_X candidates matching with ak4 jets
    #genvistaus = Collection(event, "GenVisTau")
    jets = Collection(event, "Jet")
    genparts = Collection(event, "GenPart")

    tot_dau_tauh = []
    for bs_idx,bs in enumerate(genparts):
        if abs(bs.pdgId)!=531: continue #if not Bs continue
        all_dau_taus = []
        dau_tauh = []
        for tau_idx,tau in enumerate(genparts):
            if abs(tau.pdgId)==15:
                if tau.genPartIdxMother == bs_idx:
                    all_dau_taus.append(tau_idx)
        if len(all_dau_taus) != 2: continue
        # one of them has to decay hadronically
        for genvistau in genvistaus:
            tauh_idx = genvistau.genPartIdxMother
            if tauh_idx in all_dau_taus: # it's one of the bs daughters
                jet,dr = closest(genvistau,jets)
                if dr<0.4:
                    histo_sig.Fill(genparts[genvistau.genPartIdxMother].pt)

## bkg matching (only single-tauh from W decays)
for i in range(tree_bkg.GetEntries()):
    event = Event(tree_bkg,i)

    ## look for single tau events matching with ak4 jets
    genvistaus = Collection(event, "GenVisTau")
    jets = Collection(event, "Jet")
    genparts = Collection(event, "GenPart")

    # loop over only hadronic taus
    for genvistau in genvistaus:
        gentau_idx = genvistau.genPartIdxMother
        ## tau coming from a W
        #print(genparts[genvistau.genPartIdxMother].genPartIdxMother)
        if abs(genparts[genparts[genvistau.genPartIdxMother].genPartIdxMother].pdgId) != 24 : continue
        # all genvistaus that match with jet with dr<0.4 are selected for the training
        jet,dr = closest(genvistau,jets)
        if dr<0.4:
            histo_bkg.Fill(genparts[genvistau.genPartIdxMother].pt)


c1 = ROOT.TCanvas()
c1.Draw()
histo_sig.SetFillStyle(0)
histo_sig.SetLineColor(ROOT.kBlue)
histo_sig.SetTitle(";GEN #tau_{h} p_{T} (GeV); norm")
histo_sig.DrawNormalized("HIST")
histo_bkg.SetFillStyle(0)
histo_bkg.SetLineColor(ROOT.kRed)
histo_bkg.DrawNormalized("HIST same")

leg = ROOT.TLegend(0.60,.75,.90,.90)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(histo_sig,histo_sig.GetName(),'L')
leg.AddEntry(histo_bkg,'single-#tau_{h} from W','L')
leg.Draw("same")
c1.Update()
c1.SaveAs("gen_tauh_pt_sig_vs_singletauh_fromW.png")


## bkg matching (only single-tauh from W decays)
for i in range(tree_bkg.GetEntries()):
    event = Event(tree_bkg,i)

    ## look for single tau events matching with ak4 jets
    genvistaus = Collection(event, "GenVisTau")
    jets = Collection(event, "Jet")
    genparts = Collection(event, "GenPart")

    # loop over only hadronic taus
    for genvistau in genvistaus:
        gentau_idx = genvistau.genPartIdxMother
        # all genvistaus that match with jet with dr<0.4 are selected for the training
        jet,dr = closest(genvistau,jets)
        if dr<0.4:
            histo_bkg.Fill(genparts[genvistau.genPartIdxMother].pt)


c1 = ROOT.TCanvas()
c1.Draw()
histo_sig.SetFillStyle(0)
histo_sig.SetLineColor(ROOT.kBlue)
histo_sig.SetTitle(";GEN #tau_{h} p_{T} (GeV); norm")
histo_sig.DrawNormalized("HIST")
histo_bkg.SetFillStyle(0)
histo_bkg.SetLineColor(ROOT.kRed)
histo_bkg.DrawNormalized("HIST same")

leg = ROOT.TLegend(0.60,.75,.90,.90)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(histo_sig,histo_sig.GetName(),'L')
leg.AddEntry(histo_bkg,histo_bkg.GetName(),'L')
leg.Draw("same")
c1.Update()
c1.SaveAs("gen_tauh_pt_sig_vs_singletauh.png")
