# sf_electron.py

import ROOT

def load_electron_sf():
    ROOT.gInterpreter.Declare('auto csetEl_2018 = correction::CorrectionSet::from_file("sfs/electron.json");')

def apply_electron_sf(samples, ch, k):
    if ch == 'emu' or ch == 'e' or ch == 'ee':
        samples[ch][k] = samples[ch][k].Filter("e1_pt > 20")
        samples[ch][k] = samples[ch][k].Define("e1_recosf", 'csetEl_2018->evaluate({"2018", "sf", "RecoAbove20", std::abs(e1_eta), e1_pt})')
        samples[ch][k] = samples[ch][k].Define("e1_idsf", 'csetEl_2018->evaluate({"2018", "sf", "Tight", std::abs(e1_eta), e1_pt})')

        if ch != 'ee':
            samples[ch][k] = samples[ch][k].Define('e_sf_weight', 'e1_recosf * e1_idsf')

    if ch == 'ee':
        samples[ch][k] = samples[ch][k].Filter("e2_pt > 20")
        samples[ch][k] = samples[ch][k].Define("e2_recosf", 'csetEl_2018->evaluate({"2018", "sf", "RecoAbove20", std::abs(e2_eta), e2_pt})')
        samples[ch][k] = samples[ch][k].Define("e2_idsf", 'csetEl_2018->evaluate({"2018", "sf", "Tight", std::abs(e2_eta), e2_pt})')
        samples[ch][k] = samples[ch][k].Define('e_sf_weight', 'e1_recosf * e1_idsf * e2_recosf * e2_idsf')

def load_trigger_sf():
    # Electron trigger SFs
    ROOT.gInterpreter.Declare("""
    TFile* ee_trg_sf_file = nullptr;
    TH2F* sfshisto_ee = nullptr;

    void load_sfshisto_ee() {
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
            load_sfshisto_ee();
        }

        int bin_x = sfshisto_ee->GetXaxis()->FindBin(e1_pt);
        int bin_y = sfshisto_ee->GetYaxis()->FindBin(e2_pt);
        return sfshisto_ee->GetBinContent(bin_x, bin_y);
    }
    """)

def apply_electron_trigger_sf(samples, ch, k):
    if ch == 'ee':
        samples[ch][k] = samples[ch][k].Define("trg_sf_weight", "get_ee_trigger_sf(e1_pt, e2_pt)")
        samples[ch][k] = samples[ch][k].Define('tot_sf_weight', 'e_sf_weight*trg_sf_weight')
