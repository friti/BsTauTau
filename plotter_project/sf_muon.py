# sf_muon.py

import ROOT

def load_muon_sf():
    ROOT.gInterpreter.Declare('auto csetMu = correction::CorrectionSet::from_file("sfs/muon_Z.json");')
    ROOT.gInterpreter.Declare('auto csetMu_id = csetMu->at("NUM_TightID_DEN_genTracks");')
    ROOT.gInterpreter.Declare('auto csetMu_iso = csetMu->at("NUM_TightRelIso_DEN_TightIDandIPCut");')
    ROOT.gInterpreter.Declare('auto csetMu_trg = csetMu->at("NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight");')

def apply_muon_sf(samples, ch, k):
    if ch == 'emu' or ch == 'mu' or ch == 'mumu':
        samples[ch][k] = samples[ch][k].Filter("mu1_pt > 20")
        samples[ch][k] = samples[ch][k].Define("mu1_idsf", 'csetMu_id->evaluate({std::abs(mu1_eta), mu1_pt,"nominal"})')
        samples[ch][k] = samples[ch][k].Define("mu1_isosf", 'csetMu_iso->evaluate({std::abs(mu1_eta), mu1_pt,"nominal"})')

        if ch != 'mumu':
            samples[ch][k] = samples[ch][k].Define('mu_sf_weight', 'mu1_idsf * mu1_isosf')

    if ch == 'mumu':
        samples[ch][k] = samples[ch][k].Filter("mu2_pt > 20")
        samples[ch][k] = samples[ch][k].Define("mu2_idsf", 'csetMu_id->evaluate({std::abs(mu2_eta), mu2_pt,"nominal"})')
        samples[ch][k] = samples[ch][k].Define("mu2_isosf", 'csetMu_iso->evaluate({std::abs(mu2_eta), mu2_pt,"nominal"})')

        samples[ch][k] = samples[ch][k].Define('mu_sf_weight', 'mu1_idsf * mu1_isosf * mu2_idsf * mu2_isosf')

def load_trigger_sf():
    # Muon trigger SFs
    ROOT.gInterpreter.Declare("""
    TFile* mumu_trg_sf_file = nullptr;
    TH2F* sfshisto_mumu = nullptr;

    void load_sfshistomumu() {
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
            load_sfshistomumu();
        }

        int bin_x = sfshisto_mumu->GetXaxis()->FindBin(e1_pt);
        int bin_y = sfshisto_mumu->GetYaxis()->FindBin(mu1_pt);
        return sfshisto_mumu->GetBinContent(bin_x, bin_y);
    }
    """)

def apply_muon_trigger_sf(samples, ch, k):
    if ch == 'mu':
        samples[ch][k] = samples[ch][k].Filter("mu1_pt > 25")
        samples[ch][k] = samples[ch][k].Define("mu1_trgsf", 'csetMu_trg->evaluate({std::abs(mu1_eta), mu1_pt,"nominal"})')
        samples[ch][k] = samples[ch][k].Define('tot_sf_weight', 'mu_sf_weight * mu1_trgsf')

    elif ch == 'mumu':
        samples[ch][k] = samples[ch][k].Define("trg_sf_weight", "get_mumu_trigger_sf(mu1_pt, mu2_pt)")
        samples[ch][k] = samples[ch][k].Define('tot_sf_weight', 'mu_sf_weight * trg_sf_weight')
