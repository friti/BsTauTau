# sf_trigger_dilepton.py

import ROOT

def load_trigger_sf():
    ROOT.gInterpreter.Declare("""
    TFile* dilepton_trg_sf_file = nullptr;
    TH2F* sfshisto_dilepton = nullptr;

    void load_sfshisto_dilepton() {
        if (dilepton_trg_sf_file == nullptr) {
            dilepton_trg_sf_file = TFile::Open("sfs/dilepton_trigger_sfs_2018.root", "READ");
            if (!dilepton_trg_sf_file || !dilepton_trg_sf_file->IsOpen()) {
                std::cerr << "Error: File not found or unable to open!" << std::endl;
            }
            sfshisto_dilepton = (TH2F*)dilepton_trg_sf_file->Get("h2D_SF_dilepton_lepABpt_FullError");
            if (!sfshisto_dilepton) {
                std::cerr << "Error: Histogram not found!" << std::endl;
            }
        }
    }

    double get_dilepton_trigger_sf(double e1_pt, double e2_pt) {
        if (sfshisto_dilepton == nullptr) {
            load_sfshisto_dilepton();
        }

        int bin_x = sfshisto_dilepton->GetXaxis()->FindBin(e1_pt);
        int bin_y = sfshisto_dilepton->GetYaxis()->FindBin(e2_pt);
        return sfshisto_dilepton->GetBinContent(bin_x, bin_y);
    }
    """)

def apply_dilepton_trigger_sf(samples, ch, k):
    if ch == 'ee':
        samples[ch][k] = samples[ch][k].Define("trg_sf_weight", "get_dilepton_trigger_sf(e1_pt, e2_pt)")
        samples[ch][k] = samples[ch][k].Define('tot_sf_weight', 'e_sf_weight * trg_sf_weight')
    
    elif ch == 'mumu':
        samples[ch][k] = samples[ch][k].Define("trg_sf_weight", "get_dilepton_trigger_sf(mu1_pt, mu2_pt)")
        samples[ch][k] = samples[ch][k].Define('tot_sf_weight', 'mu_sf_weight * trg_sf_weight')
