import ROOT
def declare_sfs_cpp_functions():
    ROOT.gInterpreter.Declare('auto csetEl = correction::CorrectionSet::from_file("sfs/electron.json");')
    ROOT.gInterpreter.Declare('auto csetEl_2018 = csetEl->at("UL-Electron-ID-SF");')
    ROOT.gInterpreter.Declare('auto csetMu = correction::CorrectionSet::from_file("sfs/muon_Z.json");')
    ROOT.gInterpreter.Declare('auto csetMu_id = csetMu->at("NUM_TightID_DEN_genTracks");')
    ROOT.gInterpreter.Declare('auto csetMu_iso = csetMu->at("NUM_TightRelIso_DEN_TightIDandIPCut");')
    ROOT.gInterpreter.Declare('auto csetMu_trg = csetMu->at("NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight");')

    ROOT.gInterpreter.Declare('auto csetBtag = correction::CorrectionSet::from_file("sfs/btagging.json");')
    ROOT.gInterpreter.Declare('auto csetBtag_mujets = csetBtag->at("deepJet_mujets");')
    ROOT.gInterpreter.Declare('auto csetBtag_incl = csetBtag->at("deepJet_incl");')



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

    ROOT.gInterpreter.Declare("""
        TFile* emu_trg_sf_file = nullptr;
        TH2F* sfshisto_emu = nullptr;

        void load_sfshisto() {
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
                load_sfshisto();
            }
            int bin_x = sfshisto_emu->GetXaxis()->FindBin(e1_pt);
            int bin_y = sfshisto_emu->GetYaxis()->FindBin(mu1_pt);
            return sfshisto_emu->GetBinContent(bin_x, bin_y);
        }
    """)
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
    ROOT.gInterpreter.Declare("""
        TFile* single_e_trg_sf_file = nullptr;
        TH2F* sfshisto_single_e = nullptr;

        void load_sfshisto_single_e() {
            if (single_e_trg_sf_file == nullptr) {
                single_e_trg_sf_file = TFile::Open("sfs/electron_trigger_2018.root", "READ");
                if (!single_e_trg_sf_file || !single_e_trg_sf_file->IsOpen()) {
                    std::cerr << "Error: File not found or unable to open!" << std::endl;
                }
                sfshisto_single_e = (TH2F*)single_e_trg_sf_file->Get("EGamma_SF2D");
                if (!sfshisto_single_e) {
                    std::cerr << "Error: Histogram not found!" << std::endl;
                }
            }
        }

        double get_single_e_trigger_sf(double e1_pt, double e1_eta) {
            if (sfshisto_single_e == nullptr) {
                load_sfshisto_single_e();
            }
            int bin_x = sfshisto_single_e->GetXaxis()->FindBin(e1_eta);
            int bin_y = sfshisto_single_e->GetYaxis()->FindBin(e1_pt);
            return sfshisto_single_e->GetBinContent(bin_x, bin_y);
        }
    """)
    ROOT.gInterpreter.Declare("""
        float top_ptweight(ROOT::RVecF genPart_pt, ROOT::RVecI genPart_pdgId) {
            float gentoppt = -1.0, genantitoppt = -1.0;
            float maxtoppt = 500.0;
            float weight = 1.0;
            int top_count = 0, antitop_count = 0;
            for (size_t i = 0; i < genPart_pdgId.size(); i++) {
                if (genPart_pdgId[i] == 6) {
                    top_count++;
                    if (top_count == 2) gentoppt = genPart_pt[i];
                }
                if (genPart_pdgId[i] == -6) {
                    antitop_count++;
                    if (antitop_count == 2) genantitoppt = genPart_pt[i];
                }
            }
            if (gentoppt > 0 && genantitoppt > 0) {
                float w1 = exp(0.0615 - 0.0005 * std::min(gentoppt, maxtoppt));
                float w2 = exp(0.0615 - 0.0005 * std::min(genantitoppt, maxtoppt));
                weight = sqrt(w1 * w2);
            }
            return weight;
        }
    """)


    ## FIXME ME, rerun the lep SFS to have the correct selection on ETA
    ## function to evaluate b-tagging scale factors
    ROOT.gInterpreter.Declare("""
    #include <correction.h>
    #include <vector>
    #include <cmath>

    // Loop over jets, evaluate SF per jet, return vector of SFs
    std::vector<float> evaluate_btag_mujets_sf(const ROOT::VecOps::RVec<int>& flav,
                                        const ROOT::VecOps::RVec<float>& eta,
                                        const ROOT::VecOps::RVec<float>& pt,
                                        const std::string& wp = "L") {
        std::vector<float> result;
        result.reserve(pt.size());
        for (size_t i = 0; i < pt.size(); ++i) {
            float eta_val = std::abs(eta[i]);
            if (eta_val >= 2.5f) {
                eta_val = 2.499f;
            }
            double pt_val = static_cast<double>(pt[i]);
            if (pt_val <= 20.0) pt_val = 20.01;
            else if (pt_val >= 1000.0) pt_val = 999.99;
            float sf = csetBtag_mujets->evaluate({
                "central",            // C-style string literal (const char*)
                wp.c_str(),           // working point, now configurable
                flav[i],              // int
                eta_val,              // double (float promoted to double)
                pt_val
            });
            result.push_back(sf);
        }
        return result;
    }
                              
    std::vector<float> evaluate_btag_incl_sf(const ROOT::VecOps::RVec<int>& flav,
                                        const ROOT::VecOps::RVec<float>& eta,
                                        const ROOT::VecOps::RVec<float>& pt,
                                        const std::string& wp = "L") {
        std::vector<float> result;
        result.reserve(pt.size());
        for (size_t i = 0; i < pt.size(); ++i) {
            float eta_val = std::abs(eta[i]);
            if (eta_val >= 2.5f) {
                eta_val = 2.499f;
            }
            double pt_val = static_cast<double>(pt[i]);
            if (pt_val <= 20.0) pt_val = 20.01;
            else if (pt_val >= 1000.0) pt_val = 999.99;
            float sf = csetBtag_incl->evaluate({
                "central",            // C-style string literal (const char*)
                wp.c_str(),           // working point, now configurable
                flav[i],              // int
                eta_val,              // double (float promoted to double)
                pt_val
            });
            result.push_back(sf);
        }
        return result;
    }
    """)

    ROOT.gInterpreter.Declare("""
    ROOT::VecOps::RVec<float> merge_btag_sfs(const ROOT::VecOps::RVec<int>& flavor,
                                            const ROOT::VecOps::RVec<float>& sf_bc,
                                            const ROOT::VecOps::RVec<float>& sf_light) {
        ROOT::VecOps::RVec<float> combined_sf(flavor.size());
        size_t bc_idx = 0;
        size_t light_idx = 0;
        for (size_t i = 0; i < flavor.size(); ++i) {
            if (flavor[i] != 0) {
                combined_sf[i] = sf_bc[bc_idx++];
            } else {
                combined_sf[i] = sf_light[light_idx++];
            }
        }
                              
        return combined_sf;
    }
    """)


    ROOT.gInterpreter.Declare("""

    TEfficiency* eff_hist_b_L = nullptr;
    TEfficiency* eff_hist_c_L = nullptr;
    TEfficiency* eff_hist_light_L = nullptr;
    TEfficiency* eff_hist_b_M = nullptr;
    TEfficiency* eff_hist_c_M = nullptr;
    TEfficiency* eff_hist_light_M = nullptr;

    TEfficiency* get_eff_hist(int flav, const std::string& wp) {
        static bool loaded = false;
        if (!loaded) {
            TFile* f = TFile::Open("btageff_histos/0520A050-AF68-EF43-AA5B-5AA77C74ED73_out.root");

            eff_hist_b_L = (TEfficiency*)f->Get("h2_LEff_b");
            eff_hist_c_L = (TEfficiency*)f->Get("h2_LEff_c");
            eff_hist_light_L = (TEfficiency*)f->Get("h2_LEff_udsg");

            eff_hist_b_M = (TEfficiency*)f->Get("h2_MEff_b");
            eff_hist_c_M = (TEfficiency*)f->Get("h2_MEff_c");
            eff_hist_light_M = (TEfficiency*)f->Get("h2_MEff_udsg");

            if (!eff_hist_b_L || !eff_hist_c_L || !eff_hist_light_L ||
                !eff_hist_b_M || !eff_hist_c_M || !eff_hist_light_M) {
                std::cerr << "[ERROR] TEfficiency histos not found!" << std::endl;
                f->Close();
                delete f;
                return nullptr;
            }

            f->Close();
            delete f;
            loaded = true;
        }

        if (wp == "L") {
            if (abs(flav) == 5) return eff_hist_b_L;
            else if (abs(flav) == 4) return eff_hist_c_L;
            else return eff_hist_light_L;
        } else if (wp == "M") {
            if (abs(flav) == 5) return eff_hist_b_M;
            else if (abs(flav) == 4) return eff_hist_c_M;
            else return eff_hist_light_M;
        } else {
            std::cerr << "[ERROR] Unknown working point: " << wp << std::endl;
            return nullptr;
        }
    }

    float get_efficiency(int flav, float eta, float pt, const std::string& wp) {
        TEfficiency* h = get_eff_hist(flav, wp);
        if (!h) return 1.0;

        // Clamp pt to [20, 1000]
        float pt_clamped = pt;
        if (pt <= 20.0f) pt_clamped = 20.0f + 1e-2f;
        else if (pt >= 1000.0f) pt_clamped = 1000.0f - 1e-2f;

        int bin = h->FindFixBin(pt_clamped, fabs(eta));
        float eff = h->GetEfficiency(bin);
        return eff;
    }

    float compute_event_weight(
        const ROOT::VecOps::RVec<float>& discr,    // jet btag discriminator (e.g. deepJet score)
        float wp_val,                              // working point threshold
        const ROOT::VecOps::RVec<float>& sf,      // per-jet scale factors
        const ROOT::VecOps::RVec<int>& flav,      // hadron flavour per jet
        const ROOT::VecOps::RVec<float>& eta,
        const ROOT::VecOps::RVec<float>& pt,
        const std::string& wp_str = "L"           // working point string ("L" or "M")
    )
    {
        float weight = 1.0; // per event weight 
        std::vector<std::string> debug_lines;
        for (size_t i = 0; i < discr.size(); ++i) { // loop over the jets
            bool is_btagged = (discr[i] > wp_val);

            float eff = get_efficiency(flav[i], eta[i], pt[i], wp_str);
            float denom = 1.0 - eff;
            if (denom == 0) denom = 1e-6;
            float prev_weight = weight;
            if (is_btagged) {
                weight *= sf[i];
            } else {
                weight *= (1 - (sf[i] * eff)) / denom;
            }

        }
         return weight;
    }
    """)
