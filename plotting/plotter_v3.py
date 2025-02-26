''' Plotter for BsTauTau analysis; 5 final state categories'''

import ROOT
from datetime import datetime
import os
import json
import numpy as np 
#https://indico.cern.ch/event/1330797/contributions/5796853/attachments/2819980/4924122/CAT_ACAT24.pdf
#import cmsstyle as CMS
from cmsstyle import CMS_lumi
from officialStyle import officialStyle
import correctionlib
correctionlib.register_pyroot_binding()

from samples import data_samples, mc_samples_names, files_names, cross_sections,luminosity_2018, titles, colours
from selection import trigger_selections, trigger_exclusions, preselection
from histos import histos

ROOT.ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch()   
ROOT.gStyle.SetOptStat(0)

officialStyle(ROOT.gStyle, ROOT.TGaxis)


compute_sfs = False
compute_btag_sfs = False
use_ntuples_with_sfs = True
use_ntuples_with_btag_sfs = False


def make_directories(label):
    for ch in channels:
        os.system('mkdir -p plots/%s/%s/png/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/pdf/' %(label,ch))
    #os.system('mkdir -p plots/%s/log/' %(label))
    
def save_selection(label, preselection):
    with open('plots_ul/%s/selection.py' %label, 'w') as ff:
        total_expected = 0.
        print("selection = ' & '.join([", file=ff)
        for isel in preselection.split(' & '): 
            print("    '%s'," %isel, file=ff)
        print('])', file=ff)
        print('pass: %s'%pass_id, file=ff)
        print('fail: %s'%fail_id, file=ff)

def create_legend(temp_hists, sample_names, titles):
    # Legend gymnastics
    leg = ROOT.TLegend(0.24,.67,.95,.90)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.035)
    leg.SetNColumns(3)
    k = list(temp_hists.keys())[0]
    for kk in sample_names:
        leg.AddEntry(temp_hists[k]['%s_%s' %(k, kk)].GetValue(), titles[kk], 'EP' if 'data' in kk else 'F')
            
    return leg

def get_genEventSumw(file_path):
    """Retrieve the sum of genEventSumw from the Runs tree in a ROOT file."""
    f = ROOT.TFile.Open(file_path)
    runs_tree = f.Get("Runs")
    if not runs_tree:
        raise RuntimeError(f"No Runs tree found in file {file_path}")
    
    sumw = 0
    for entry in runs_tree:
        sumw += entry.genEventSumw

    #print("The sumw is ",sumw)
    f.Close()
    return sumw


# Canvas 
c1 = ROOT.TCanvas('c1', '', 700, 700)
c1.Draw()
c1.cd()
main_pad = ROOT.TPad('main_pad', '', 0., 0.25, 1. , 1.  )
main_pad.Draw()
c1.cd()
ratio_pad = ROOT.TPad('ratio_pad', '', 0., 0., 1., 0.25)
ratio_pad.Draw()
main_pad.SetTicks(True)
main_pad.SetBottomMargin(0.)
ratio_pad.SetTopMargin(0.)   
ratio_pad.SetGridy()
ratio_pad.SetBottomMargin(0.45)

label = '%s'%(datetime.now().strftime('%d%b%Y_%Hh%Mm%Ss'))

print(label)

channels = ['mumu','emu','ee']
#channels = ['emu','ee','mumu','e','mu']
#channels = ['ee']

eras_2018 = ['A','B','C','D']

#########################################################
############ SFS GLOBAL OBJECTS AND FUNCTIONS ###########
#########################################################

ROOT.gInterpreter.Declare('auto csetEl = correction::CorrectionSet::from_file("sfs/electron.json");')
ROOT.gInterpreter.Declare('auto csetEl_2018 = csetEl->at("UL-Electron-ID-SF");')
ROOT.gInterpreter.Declare('auto csetMu = correction::CorrectionSet::from_file("sfs/muon_Z.json");')
ROOT.gInterpreter.Declare('auto csetMu_id = csetMu->at("NUM_TightID_DEN_genTracks");') # ID + RECO
ROOT.gInterpreter.Declare('auto csetMu_iso = csetMu->at("NUM_TightRelIso_DEN_TightIDandIPCut");') # ISO
ROOT.gInterpreter.Declare('auto csetMu_trg = csetMu->at("NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight");') # TRG 


'''
## for mumu trigger SFs
ROOT.gInterpreter.Declare("""
    // Define a function to calculate SF for mumu channel
    double get_mumu_trigger_sf(double mu1_pt, double mu2_pt, double mu1_eta, double mu2_eta) {
        // Check conditions for muons
        double sf_mu1 = 1.0;
        double sf_mu2 = 1.0;

//std::cout<<mu1_pt<<" "<<mu2_pt<<std::endl;
        if (mu1_pt >= 26 && mu2_pt < 26) {
            // If mu1 pt > 26, calculate SF for mu1
            sf_mu1 = csetMu_trg->evaluate({std::abs(mu1_eta), mu1_pt, "nominal"});
//std::cout<<"SF "<<sf_mu1<<std::endl;
            return sf_mu1;
        } 
        else if (mu2_pt >= 26 && mu1_pt < 26) {
            // If mu2 pt > 26, calculate SF for mu2
            sf_mu2 = csetMu_trg->evaluate({std::abs(mu2_eta), mu2_pt, "nominal"});
//std::cout<<"SF "<<sf_mu2<<std::endl;
            return sf_mu2;
        } 
        else if (mu1_pt > 26 && mu2_pt > 26) {
            // If both muons have pt > 26, calculate SF for both and combine the probabilities
            double sf_mu1 = csetMu_trg->evaluate({std::abs(mu1_eta), mu1_pt, "nominal"});
            double sf_mu2 = csetMu_trg->evaluate({std::abs(mu2_eta), mu2_pt, "nominal"});
            
            // Combined probability that at least one of them passed the trigger
            double combined_sf = 1 - (1 - sf_mu1) * (1 - sf_mu2);
//std::cout<<"SF "<<combined_sf<<std::endl;
return combined_sf;
        } 
        return 1.0; // Default SF if no conditions match
    }
""")
'''

## for mumu channel trigger SFs
ROOT.gInterpreter.Declare("""
    TFile* mumu_trg_sf_file = nullptr;
    TH2F* sfshisto_mumu = nullptr;

    void load_sfshistomumu() {
        // Open the file only once if it's not already opened
        if (mumu_trg_sf_file == nullptr) {
            mumu_trg_sf_file = TFile::Open("sfs/dilepton_trigger_sfs_2018.root", "READ");
            if (!mumu_trg_sf_file || !mumu_trg_sf_file->IsOpen()) {
                std::cerr << "Error: File not found or unable to open!" << std::endl;
            }
            sfshisto_mumu = (TH2F*)mumu_trg_sf_file->Get("h2D_SF_mumu_lepABpt_FullError");
            if (!sfshisto_mumu) {
                std::cerr << "Error: Histogram not found!" << std::endl;
            }
        }
    }

    double get_mumu_trigger_sf(double e1_pt, double mu1_pt) {
        if (sfshisto_mumu == nullptr) {
            load_sfshistomumu();  // Load the histogram if it's not loaded yet
        }

        int bin_x = sfshisto_mumu->GetXaxis()->FindBin(e1_pt);
        int bin_y = sfshisto_mumu->GetYaxis()->FindBin(mu1_pt);
        //std::cout<<"mumu sf "<<sfshisto->GetBinContent(bin_x, bin_y)<<std::endl;
        return sfshisto_mumu->GetBinContent(bin_x, bin_y);
       
    }
""")

## for emu channel trigger SFs
ROOT.gInterpreter.Declare("""
    TFile* emu_trg_sf_file = nullptr;
    TH2F* sfshisto_emu = nullptr;

    void load_sfshisto() {
        // Open the file only once if it's not already opened
        if (emu_trg_sf_file == nullptr) {
            emu_trg_sf_file = TFile::Open("sfs/dilepton_trigger_sfs_2018.root", "READ");
            if (!emu_trg_sf_file || !emu_trg_sf_file->IsOpen()) {
                std::cerr << "Error: File not found or unable to open!" << std::endl;
            }
            sfshisto_emu = (TH2F*)emu_trg_sf_file->Get("h2D_SF_emu_lepABpt_FullError");
            if (!sfshisto_emu) {
                std::cerr << "Error: Histogram not found!" << std::endl;
            }
        }
    }

    double get_emu_trigger_sf(double e1_pt, double mu1_pt) {
        if (sfshisto_emu == nullptr) {
            load_sfshisto();  // Load the histogram if it's not loaded yet
        }

        int bin_x = sfshisto_emu->GetXaxis()->FindBin(e1_pt);
        int bin_y = sfshisto_emu->GetYaxis()->FindBin(mu1_pt);
        //std::cout<<"emu sf "<<sfshisto->GetBinContent(bin_x, bin_y)<<std::endl;
        return sfshisto_emu->GetBinContent(bin_x, bin_y);
       
    }
""")

## for ee channel trigger SFs
ROOT.gInterpreter.Declare("""
    TFile* ee_trg_sf_file = nullptr;
    TH2F* sfshisto_ee = nullptr;

    void load_sfshisto_ee() {
        // Open the file only once if it's not already opened
        if (ee_trg_sf_file == nullptr) {
            ee_trg_sf_file = TFile::Open("sfs/dilepton_trigger_sfs_2018.root", "READ");
            if (!ee_trg_sf_file || !ee_trg_sf_file->IsOpen()) {
                std::cerr << "Error: File not found or unable to open!" << std::endl;
            }
            sfshisto_ee = (TH2F*)ee_trg_sf_file->Get("h2D_SF_ee_lepABpt_FullError");
            if (!sfshisto_ee) {
                std::cerr << "Error: Histogram not found!" << std::endl;
            }
        }
    }

    double get_ee_trigger_sf(double e1_pt, double e2_pt) {
        if (sfshisto_ee == nullptr) {
            load_sfshisto_ee();  // Load the histogram if it's not loaded yet
        }

        int bin_x = sfshisto_ee->GetXaxis()->FindBin(e1_pt);
        int bin_y = sfshisto_ee->GetYaxis()->FindBin(e2_pt);
//std::cout<<"ee sf "<<sfshisto_ee->GetBinContent(bin_x, bin_y)<<std::endl;

        return sfshisto_ee->GetBinContent(bin_x, bin_y);
       
    }
""")


## top pt weights
ROOT.gInterpreter.Declare("""
    float top_ptweight(ROOT::RVecF genPart_pt, ROOT::RVecI genPart_pdgId) {
        float gentoppt = -1.0, genantitoppt = -1.0;
        float maxtoppt = 500.0;
        float weight = 1.0;
        
        int top_count = 0, antitop_count = 0;

        for (size_t i = 0; i < genPart_pdgId.size(); i++) {
            if (genPart_pdgId[i] == 6) { 
                top_count++;
                if (top_count == 2) gentoppt = genPart_pt[i];  // Take the second top
            }
            if (genPart_pdgId[i] == -6) { 
                antitop_count++;
                if (antitop_count == 2) genantitoppt = genPart_pt[i];  // Take the second antitop
            }
        }

        if (gentoppt > 0 && genantitoppt > 0) {
            float w1 = exp(0.0615 - 0.0005 * std::min(gentoppt, maxtoppt));
            float w2 = exp(0.0615 - 0.0005 * std::min(genantitoppt, maxtoppt));
            weight = sqrt(w1 * w2);
        }

        return weight;
    }
""");


## btaggin SFs
ROOT.gInterpreter.Declare("""
    ROOT::RVec<double> get_loose_btag_sf(ROOT::RVec<double> pt) {
        ROOT::RVec<double> sf;
        for (auto p : pt) {
            double p0 = 0.986697;
            double p1 = 5.6664e-07;
            double p2 = -105.134;
            double p3 = 0.0;
            sf.push_back(p0 + p1 * log(p + 19) * log(p + 18) * (3 + p2 * log(p + 18)) + p3);
        }
        return sf;
    }
""");

ROOT.gInterpreter.Declare("""
    ROOT::RVec<double> get_medium_btag_sf(ROOT::RVec<double> pt) {
        ROOT::RVec<double> sf;
        for (auto p : pt) {
            double p0 = 1.0252;
            double p1 = -0.00263732;
            double p2 = -0.372237;
            double p3 = 0.0;
            sf.push_back(p0 + p1 * log(p + 19) * log(p + 18) * (3 + p2 * log(p + 18)) + p3);
        }
        return sf;
    }
""");

'''
## top pt SFs
ROOT.gInterpreter.Declare("""
    double get_top_pt_sf(double pt) {
        double sf;
        for (auto p : pt) {
            double p0 = 0.103;
            double p1 = -0.0118;
            double p2 = -0.000134;
            double p3 = 0.973;
            sf.push_back(p0 + exp(p1 * p) + p2 * p + p3);
        }
        return sf;
    }
""");
'''

##### invariant mass function
ROOT.gInterpreter.Declare("""
double compute_inv_mass(double pt1, double eta1, double phi1, double mass1,
double pt2, double eta2, double phi2, double mass2) {
TLorentzVector v1, v2;
v1.SetPtEtaPhiM(pt1, eta1, phi1, mass1);
v2.SetPtEtaPhiM(pt2, eta2, phi2, mass2);
return (v1 + v2).M();
}
""")


##########################################################################################
##########################################################################################




if __name__ == '__main__':
    
    # create plot directories
    make_directories(label)
    
    samples = dict()

    tree_name = 'Events'


    #load the samples 
    for ch in channels:
        print("=============================")
        print("========= Channel %s ========"%ch)
        print("=============================")


        print("=============================")
        print("====== Loading Samples ======")
        print("=============================")




        tree_dir_data = '/eos/cms/store/group/cmst3/group/bpark/ccaillol/ntuples_%s_2018'%(ch)
        if use_ntuples_with_sfs or compute_btag_sfs:
            tree_dir_mc = '/eos/cms/store/group/cmst3/group/bpark/friti/bstautau/samples_wsf/%s'%(ch)
        elif use_ntuples_with_btag_sfs:
            tree_dir_mc = '/eos/cms/store/group/cmst3/group/bpark/friti/bstautau/samples_wsf_wbtagsf/%s'%(ch)
        else: # take ntuples with sfs already (and trigger selection)
            tree_dir_mc = '/eos/cms/store/group/cmst3/group/bpark/ccaillol/ntuples_%s_2018'%(ch)
            
        samples[ch] = dict()

        # handle MC samples
        for k in mc_samples_names:
            file_name = files_names[k]
            print("Loaded", f'{tree_dir_mc}/{file_name}.root')

            samples[ch][k] = ROOT.RDataFrame(tree_name, f'{tree_dir_mc}/{file_name}.root')
            # reweight only mc
            if not use_ntuples_with_sfs and not compute_btag_sfs and not use_ntuples_with_btag_sfs:
                norm_weight = luminosity_2018 * cross_sections[k] *1000/get_genEventSumw(f'{tree_dir_mc}/{file_name}.root')
                samples[ch][k] = samples[ch][k].Define('norm_weight', 'L1PreFiringWeight_Nom*genWeight*puWeight*%f' %norm_weight)

                ## trigger selection (OR of data triggers)
                mc_trigger_selection = [trigger_selections[ch][k] for k in trigger_selections[ch]]
                mc_trigger_condition = ' | '.join(mc_trigger_selection)
                print(f"Applying MC trigger selection for {k} in channel {ch}: {mc_trigger_condition}")
                samples[ch][k] = samples[ch][k].Filter(mc_trigger_condition)
            else:
                print("Trigger selections and normalisation weights precomputed in the ntuples...")

            if compute_sfs:
                ### Compute object SFs                

                if ch =='emu' or ch =='mu' or ch =='mumu':
                    samples[ch][k] = samples[ch][k].Filter("mu1_pt>20") 
                    samples[ch][k] = samples[ch][k].Define("mu1_idsf",('csetMu_id->evaluate({std::abs(mu1_eta), mu1_pt,"nominal"})'))
                    samples[ch][k] = samples[ch][k].Define("mu1_isosf",('csetMu_iso->evaluate({std::abs(mu1_eta), mu1_pt,"nominal"})'))

                    if ch!='mumu':
                        samples[ch][k] = samples[ch][k].Define('mu_sf_weight', 'mu1_idsf*mu1_isosf')

                if ch == 'mumu': 
                    samples[ch][k] = samples[ch][k].Filter("mu2_pt>20")
                    samples[ch][k] = samples[ch][k].Define("mu2_idsf",('csetMu_id->evaluate({std::abs(mu2_eta), mu2_pt,"nominal"})'))
                    samples[ch][k] = samples[ch][k].Define("mu2_isosf",('csetMu_iso->evaluate({std::abs(mu2_eta), mu2_pt,"nominal"})'))

                    samples[ch][k] = samples[ch][k].Define('mu_sf_weight', 'mu1_idsf*mu1_isosf*mu2_idsf*mu2_isosf')
                    
                if ch =='emu' or ch =='e' or ch =='ee':
                    ## pt cut on e1 already applied on saved ntuples
                    samples[ch][k] = samples[ch][k].Filter("e1_pt>20")
                    samples[ch][k] = samples[ch][k].Define("e1_recosf",('csetEl_2018->evaluate({"2018", "sf", "RecoAbove20", std::abs(e1_eta), e1_pt})'))
                    samples[ch][k] = samples[ch][k].Define("e1_idsf",('csetEl_2018->evaluate({"2018", "sf", "Tight", std::abs(e1_eta), e1_pt})'))

                    if ch != 'ee':
                        samples[ch][k] = samples[ch][k].Define('e_sf_weight', 'e1_recosf*e1_idsf')
                if ch == 'ee':
                    samples[ch][k] = samples[ch][k].Filter("e2_pt>20")
                    samples[ch][k] = samples[ch][k].Define("e2_recosf",('csetEl_2018->evaluate({"2018", "sf", "RecoAbove20", std::abs(e2_eta), e2_pt})'))
                    samples[ch][k] = samples[ch][k].Define("e2_idsf",('csetEl_2018->evaluate({"2018", "sf", "Tight", std::abs(e2_eta), e2_pt})'))
                    samples[ch][k] = samples[ch][k].Define('e_sf_weight', 'e1_recosf*e1_idsf*e2_recosf*e2_idsf')
                    

                ### Trigger Scale Factors FSs
                if ch =='mu': 
                    samples[ch][k] = samples[ch][k].Filter("mu1_pt>25") 
                    samples[ch][k] = samples[ch][k].Define("mu1_trgsf",('csetMu_trg->evaluate({std::abs(mu1_eta), mu1_pt,"nominal"})'))
                    samples[ch][k] = samples[ch][k].Define('tot_sf_weight', 'mu_sf_weight*mu1_trgsf')

                if ch =='mumu':
                    samples[ch][k] = samples[ch][k].Define("trg_sf_weight","get_mumu_trigger_sf(mu1_pt, mu2_pt)")
                    samples[ch][k] = samples[ch][k].Define('tot_sf_weight', 'mu_sf_weight*trg_sf_weight')

                    
                #elif ch =='e' or ch =='ee':
                    #samples[ch][k] = samples[ch][k].Define("mu1_trgsf",('csetMu_trg->evaluate({std::abs(mu1_eta), mu1_pt,"nominal"})'))
                    #samples[ch][k] = samples[ch][k].Define('tot_sf_weight', 'e_sf_weight')
                    
                elif ch =='emu':
                    samples[ch][k] = samples[ch][k].Define("trg_sf_weight", "get_emu_trigger_sf(e1_pt, mu1_pt)")
                    
                    samples[ch][k] = samples[ch][k].Define('tot_sf_weight', 'e_sf_weight*mu_sf_weight*trg_sf_weight')

                elif ch =='ee':
                    samples[ch][k] = samples[ch][k].Define("trg_sf_weight", "get_ee_trigger_sf(e1_pt, e2_pt)")
                    
                    samples[ch][k] = samples[ch][k].Define('tot_sf_weight', 'e_sf_weight*trg_sf_weight')


                ## top pt sfs

                if 'TTT' in files_names[k]:
                    samples[ch][k] = samples[ch][k].Define("top_pt_weight", "top_ptweight(GenCand_pt, GenCand_id)");

                
                samples[ch][k].Snapshot("Events","/eos/cms/store/group/cmst3/group/bpark/friti/bstautau/samples_wsf/%s/%s.root"%(ch, files_names[k]))

            
            
        # handle data samples    
        tmp_chains = dict()
        for k in data_samples[ch]:
            file_name = files_names[k]
            tmp_chains[k]= ROOT.TChain(tree_name)

            # add the eras for each data sample
            for era in eras_2018:
                print("Loaded", f'{tree_dir_data}/{file_name}{era}.root')
                tmp_chains[k].Add(f'{tree_dir_data}/{file_name}{era}.root')

            tmp_data_rdf = ROOT.RDataFrame(tmp_chains[k])

            ## apply trigger selection for data samples
            trigger_selection = trigger_selections[ch][k]
            exclusions = trigger_exclusions[ch][k]
            
            exclusion_filter = ' & '.join([f'!({exclusion})' for exclusion in exclusions]) if exclusions else ''
            final_trigger_filter = f'({trigger_selection}) & ({exclusion_filter})' if exclusion_filter else trigger_selection
            print(f"Applying combined trigger selection and exclusion for {k} in channel {ch}: {final_trigger_filter}")

            samples[ch][k] = tmp_data_rdf.Filter(final_trigger_filter)
            #print("data events",samples[ch][k].Count().GetValue())

            ##normalisation for data is just 1
            samples[ch][k] = samples[ch][k].Define('tot_weight', '1' )

        ##############################################
        ##### Preselection ###########################
        ##############################################

        print("===================================")
        print("====== Applying Preselection ======")
        print("===================================")

        for k, v in samples[ch].items():


            minimum_jet_conditions = '(j_pt > 5 & j_jetid>=2)'

            ## mc samples already have them defined
            if 'data' in k or compute_btag_sfs or compute_sfs or use_ntuples_with_sfs :
                # define new branches of jets with pt higher than 5 GeV
                samples[ch][k] = samples[ch][k].Define("selected_jets_pt", f"j_pt[{minimum_jet_conditions}]")
                samples[ch][k] = samples[ch][k].Define("selected_njets", f"selected_jets_pt.size()")
                samples[ch][k] = samples[ch][k].Define("selected_jets_eta", f"j_eta[{minimum_jet_conditions} ]")
                samples[ch][k] = samples[ch][k].Define("selected_jets_phi", f"j_phi[{minimum_jet_conditions} ]")
                samples[ch][k] = samples[ch][k].Define("selected_jets_mass", f"j_m[{minimum_jet_conditions} ]")
                samples[ch][k] = samples[ch][k].Define("selected_jets_puid", f"j_puid[{minimum_jet_conditions} ]")
                samples[ch][k] = samples[ch][k].Define("selected_jets_jetid", f"j_jetid[{minimum_jet_conditions} ]")
                samples[ch][k] = samples[ch][k].Define("selected_jets_deepflavB", f"j_deepflavB[{minimum_jet_conditions} ]")
                samples[ch][k] = samples[ch][k].Define("selected_jets_hadronFlavour", f"j_hadronFlavour[{minimum_jet_conditions} ]")
                
                
                
                # define b tag WP
                samples[ch][k] = samples[ch][k].Define("btagged_m_jets", f"selected_jets_pt[selected_jets_deepflavB > 0.2770]")
                samples[ch][k] = samples[ch][k].Define("btagged_m_jets_10gev", f"selected_jets_pt[selected_jets_deepflavB > 0.2770 & selected_jets_pt>10]")
                samples[ch][k] = samples[ch][k].Define("btagged_m_jets_30gev", f"selected_jets_pt[selected_jets_deepflavB > 0.2770 & selected_jets_pt>30]")
                samples[ch][k] = samples[ch][k].Define("btagged_m_jets_20gev", f"selected_jets_pt[selected_jets_deepflavB > 0.2770 & selected_jets_pt>20]")
                
                samples[ch][k] = samples[ch][k].Define("btagged_l_jets", f"selected_jets_pt[selected_jets_deepflavB > 0.049]")
                samples[ch][k] = samples[ch][k].Define("btagged_l_jets_10gev", f"selected_jets_pt[selected_jets_deepflavB > 0.049 & selected_jets_pt>10]")
                samples[ch][k] = samples[ch][k].Define("btagged_l_jets_30gev", f"selected_jets_pt[selected_jets_deepflavB > 0.049 & selected_jets_pt>30]")
                samples[ch][k] = samples[ch][k].Define("btagged_l_jets_20gev", f"selected_jets_pt[selected_jets_deepflavB > 0.049 & selected_jets_pt>20]")
                
                
                samples[ch][k] = samples[ch][k].Define("btagging_condition_emu", "btagged_l_jets.size()>=2 & btagged_l_jets_20gev.size()>=2")
                samples[ch][k] = samples[ch][k].Define("btagging_condition_mumu", "btagged_m_jets_20gev.size()>=2")
                samples[ch][k] = samples[ch][k].Define("btagging_condition_ee", "btagged_m_jets_20gev.size()>=2 ")
                samples[ch][k] = samples[ch][k].Define("btagging_condition_mu", "btagged_m_jets_20gev.size()>=2")
                samples[ch][k] = samples[ch][k].Define("btagging_condition_e", "btagged_m_jets_20gev.size()>=2")
                

            ## btagging Sfs
            if 'data' not in k:
                if compute_btag_sfs:
                    print("### Computing btagging Sfs ########")
                    if ch=='emu' or ch=='mumu' or ch =='ee':
                        samples[ch][k] = samples[ch][k].Define("btag_loose_sf", "get_loose_btag_sf(selected_jets_pt)");
                        samples[ch][k] = samples[ch][k].Define("btag_medium_sf", "get_medium_btag_sf(selected_jets_pt)");
                        if ch =='emu':
                            ## 2 loose btagged jets
                            samples[ch][k] = samples[ch][k].Define("btagged_l_jets_sf", "btag_loose_sf[selected_jets_deepflavB > 0.049 & selected_jets_pt>20]");
                            samples[ch][k] = samples[ch][k].Define("btag_event_weight", "btagged_l_jets_sf.size() >= 2 ? btagged_l_jets_sf[0] * btagged_l_jets_sf[1] : 1.0");

                        if ch =='mumu' or ch =='ee':
                            ## 2 medium btagged jets
                            samples[ch][k] = samples[ch][k].Define("btagged_m_jets_sf", "btag_medium_sf[selected_jets_deepflavB > 0.2770 & selected_jets_pt>20]");
                            samples[ch][k] = samples[ch][k].Define("btag_event_weight", "btagged_m_jets_sf.size() >= 2 ? btagged_m_jets_sf[0] * btagged_m_jets_sf[1] : 1.0");

                        samples[ch][k].Snapshot("Events","/eos/cms/store/group/cmst3/group/bpark/friti/bstautau/samples_wsf_wbtagsf/%s/%s.root"%(ch, files_names[k]))
            

                weight_string = 'norm_weight'
                if compute_sfs or  use_ntuples_with_sfs:
                    print("Samples with SF applied")
                    weight_string+='*tot_sf_weight'
                elif compute_btag_sfs or use_ntuples_with_btag_sfs:
                    print("Samples with btag SF applied")
                    weight_string+='*tot_sf_weight*btag_event_weight'
                if 'TTT' in files_names[k]:
                    weight_string+='*top_pt_weight'                    


                print("weights applied ",k,weight_string)                    
                samples[ch][k] = samples[ch][k].Define('tot_weight', weight_string)

            # jets selections
            samples[ch][k] = samples[ch][k].Define("jet_conditions_emu", f"ROOT::VecOps::Any({minimum_jet_conditions}) & (selected_jets_pt.size()>=2)")
            samples[ch][k] = samples[ch][k].Define("jet_conditions_mumu", f"ROOT::VecOps::Any({minimum_jet_conditions}) & (selected_jets_pt.size()>=2)")
            samples[ch][k] = samples[ch][k].Define("jet_conditions_ee", f"ROOT::VecOps::Any({minimum_jet_conditions}) & (selected_jets_pt.size()>=2)")
            samples[ch][k] = samples[ch][k].Define("jet_conditions_mu", f"ROOT::VecOps::Any({minimum_jet_conditions}) & (selected_jets_pt.size()>=4)")
            samples[ch][k] = samples[ch][k].Define("jet_conditions_e", f"ROOT::VecOps::Any({minimum_jet_conditions}) & (selected_jets_pt.size()>=4)")




            
            ## ht definition
            samples[ch][k] = samples[ch][k].Define("selected_jets_ht", "Sum(selected_jets_pt)")

            ## invariant mass definition
            if ch == 'mumu':
                samples[ch][k] = samples[ch][k].Define("inv_mass", "compute_inv_mass(mu1_pt, mu1_eta, mu1_phi, 0.105, mu2_pt, mu2_eta, mu2_phi, 0.105)")

            if ch == 'emu':
                samples[ch][k] = samples[ch][k].Define("inv_mass", "compute_inv_mass(mu1_pt, mu1_eta, mu1_phi, 0.105, e1_pt, e1_eta, e1_phi, 0.000511)")

            if ch =='ee':
                samples[ch][k] = samples[ch][k].Define("inv_mass", "compute_inv_mass(e1_pt, e1_eta, e1_phi, 0.000511, e2_pt, e2_eta, e2_phi, 0.000511)")
                

            
            filter = preselection[ch]
            print(filter, k, v, ch)
            samples[ch][k] = samples[ch][k].Filter(filter)
            #if 'data' in k: print("data content ",samples[ch][k].Count().GetValue())


        dateTimeObj = datetime.now()
        print(dateTimeObj.hour, ':', dateTimeObj.minute, ':', dateTimeObj.second, '.', dateTimeObj.microsecond)


        ##################################
        ###### HISTOS ###################
        ##################################
        
        
        # first create all the pointers
        print('====> creating pointers to histo')
        temp_hists      = {} # pass muon ID category

        # loop over the distributions
        for k, v in histos[ch].items():    
            temp_hists     [k] = {}
            # loop over the ttbar samples
            for kk, vv in samples[ch].items():
                branch_name = k
                temp_hists     [k]['%s_%s' %(k, kk)] = vv.Histo1D(v[0], branch_name, 'tot_weight')
                #temp_hists     [k]['%s_%s' %(k, kk)] = vv.Histo1D(, branch_name, 'norm_weight')
        
        for k, v in histos[ch].items():
            c1.cd()

            if ch == 'emu' or ch== 'mumu' or ch =='mu':
                data_smpl = 'data_sm'
            else:
                data_smpl = 'data_eg'
            samples_for_legend = [str(k) for k in samples[ch] if 'data' not in k and 'ext' not in k] + [data_smpl] 
            
            leg = create_legend(temp_hists, samples_for_legend, titles)
            main_pad.cd()
            main_pad.SetLogy(False)
            
            # some look features
            maxima = [] 
            maxima_data = [] 
            data_max = 0.
            for i, kv in enumerate(temp_hists[k].items()):
                key = kv[0]
                ihist = kv[1]
                sample_name = key.split(k+'_')[1]
                    
                ihist.GetXaxis().SetTitle(v[1])
                ihist.GetYaxis().SetTitle('events')                
                ihist.SetFillColor(colours[sample_name] if '%s_data'%k not in key else ROOT.kWhite)
                ihist.SetLineColor(colours[sample_name] if '%s_data'%k not in key else ROOT.kWhite)
                if '%s_data'%k not in key:
                    maxima.append(ihist.GetMaximum())
                else:
                    maxima_data.append(ihist.GetMaximum())
                    
            # Definition of stack histos
            ths1      = ROOT.THStack('stack', '') #what I want to show

            data_ths      = ROOT.THStack('data_stack', '') #stack of datasets
                
            for i, kv in enumerate(temp_hists[k].items()):
                
                key = kv[0]
                if '%s_data'%k in key: continue
                ihist = kv[1]
                ihist.SetMaximum(1.6*max(maxima_data))
                ihist.Draw('hist' + 'same'*(i>0))
                ths1.Add(ihist.GetValue())

            ths1.Draw('hist')
            try:
                ths1.GetXaxis().SetTitle(v[1])
            except:
                continue
            ths1.GetYaxis().SetTitle('events')
            ths1.SetMaximum(1.6*max(sum(maxima), sum(maxima_data)))
            ths1.SetMinimum(0.0001)

            # statistical uncertainty
            stats = ths1.GetStack().Last().Clone()
            stats.SetLineColor(0)
            stats.SetFillColor(ROOT.kGray+1)
            stats.SetFillStyle(3344)
            stats.SetMarkerSize(0)
            stats.Draw('E2 SAME')
            
            leg.AddEntry(stats, 'stat. unc.', 'F')
            leg.Draw('same')

            ## stack of data samples
            for i, kv in enumerate(temp_hists[k].items()):                
                key = kv[0]
                if '%s_data'%k not in key: continue
                ihist = kv[1]
                print("I am adding data!!!", key)
                ihist.Draw('hist' + 'same'*(i>0))
                ihist.SetLineWidth(0)
                data_ths.Add(ihist.GetValue())

            #data_ths.SetLineStyle(0)
            data_ths.GetStack().Last().SetLineColor(ROOT.kBlack)
            print("DATA integral ",data_ths.GetStack().Last().Integral(0,data_ths.GetStack().Last().GetNbinsX()+1))
            data_ths.GetStack().Last().Draw('EP same')
            main_pad.Update()
            #ths1.Draw('hist same')

            CMS_lumi(main_pad, 4, 0, cmsText = 'CMS', extraText = ' Preliminary', lumi_13TeV = 'L = 59.7 fb^{-1}')
            main_pad.cd()
            
            # Ratio for pass region
            ratio_pad.cd()
            ratio = data_ths.GetStack().Last().Clone()
            ratio.SetName(ratio.GetName()+'_ratio')
            ratio.Divide(stats)
            ratio_stats = stats.Clone()
            ratio_stats.SetName(ratio.GetName()+'_ratiostats')
            ratio_stats.Divide(stats)
            ratio_stats.SetMaximum(1.19999) # avoid displaying 2, that overlaps with 0 in the main_pad
            ratio_stats.SetMinimum(0.79999) # and this is for symmetry
            ratio_stats.GetYaxis().SetTitle('obs/exp')
            ratio_stats.GetYaxis().SetTitleOffset(0.5)
            ratio_stats.GetYaxis().SetNdivisions(405)
            ratio_stats.GetXaxis().SetLabelSize(3.* ratio.GetXaxis().GetLabelSize())
            ratio_stats.GetYaxis().SetLabelSize(3.* ratio.GetYaxis().GetLabelSize())
            ratio_stats.GetXaxis().SetTitleSize(3.* ratio.GetXaxis().GetTitleSize())
            ratio_stats.GetYaxis().SetTitleSize(3.* ratio.GetYaxis().GetTitleSize())
            
            norm_stack = ROOT.THStack('norm_stack', '')
            
            for kk, vv in temp_hists[k].items():
                if 'data' in kk: continue
                hh = vv.Clone()
                hh.Divide(stats)

            norm_stack.Draw('hist same')


            line = ROOT.TLine(ratio.GetXaxis().GetXmin(), 1., ratio.GetXaxis().GetXmax(), 1.)
            line.SetLineColor(ROOT.kBlack)
            line.SetLineWidth(1)
            ratio_stats.Draw('E2')
            norm_stack.Draw('hist same')
            ratio_stats.Draw('E2 same')
            line.Draw('same')
            ratio.Draw('EP same')
                
            c1.Modified()
            c1.Update()
                
            c1.SaveAs('plots/%s/%s/pdf/%s.pdf' %(label, ch,k))
            c1.SaveAs('plots/%s/%s/png/%s.png' %(label, ch,k))



dateTimeObj = datetime.now()
print(dateTimeObj.hour, ':', dateTimeObj.minute, ':', dateTimeObj.second, '.', dateTimeObj.microsecond)




