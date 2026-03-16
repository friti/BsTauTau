# histos definition
import ROOT

histos = dict()

## common branches
histos_combined_scores = dict()
## combined scores
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_part_all_sig_frac'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_part_all_sig_frac', '', 20, 0, 1), 'sig frac', 1)

# Decay-mode specific masks (existing)
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_masked', '', 20, 0, 1), 'ParT #tau_{h}#tau_{e} frac (decay-specific)', 1)
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_masked', '', 20, 0, 1), 'ParT #tau_{h}#tau_{h} frac (decay-specific)', 1)
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_masked', '', 20, 0, 1), 'ParT #tau_{h}#tau_{#mu} frac (decay-specific)', 1)

# General masks (NEW - no decay mode diversification)
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_general'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_general', '', 20, 0, 1), 'ParT #tau_{h}#tau_{e} frac (general)', 1)
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_general'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_general', '', 20, 0, 1), 'ParT #tau_{h}#tau_{h} frac (general)', 1)
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_general'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_general', '', 20, 0, 1), 'ParT #tau_{h}#tau_{#mu} frac (general)', 1)

histos_max_scores = dict()
## max scores
histos_max_scores['btagged_loose_jets_pt_above_20_max_tauhtaue_raw_score_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_tauhtaue_raw_score_masked', '', 20, 0, 1), 'raw score', 1)
histos_max_scores['btagged_loose_jets_pt_above_20_max_tauhtaue_ratio_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_tauhtaue_ratio_masked', '', 20, 0, 1), 'ratio', 1)
histos_max_scores['btagged_loose_jets_pt_above_20_max_tauhtauh_raw_score_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_tauhtauh_raw_score_masked', '', 20, 0, 1), 'raw score', 1)
histos_max_scores['btagged_loose_jets_pt_above_20_max_tauhtauh_ratio_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_tauhtauh_ratio_masked', '', 20, 0, 1), 'ratio', 1)
histos_max_scores['btagged_loose_jets_pt_above_20_max_tauhtaumu_raw_score_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_tauhtaumu_raw_score_masked', '', 20, 0, 1), 'raw score', 1)
histos_max_scores['btagged_loose_jets_pt_above_20_max_tauhtaumu_ratio_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_tauhtaumu_ratio_masked', '', 20, 0, 1), 'ratio', 1)
histos_max_scores['btagged_loose_jets_pt_above_20_max_b_raw_score_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_b_raw_score_masked', '', 20, 0, 1), 'raw score', 1)
histos_max_scores['btagged_loose_jets_pt_above_20_max_b_ratio_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_b_ratio_masked', '', 20, 0, 1), 'ratio', 1)
histos_max_scores['btagged_loose_jets_pt_above_20_max_c_raw_score_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_c_raw_score_masked', '', 20, 0, 1), 'raw score', 1)
histos_max_scores['btagged_loose_jets_pt_above_20_max_c_ratio_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_c_ratio_masked', '', 20, 0, 1), 'ratio', 1)
histos_max_scores['btagged_loose_jets_pt_above_20_max_other_raw_score_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_other_raw_score_masked', '', 20, 0, 1), 'raw score', 1)
histos_max_scores['btagged_loose_jets_pt_above_20_max_other_ratio_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_other_ratio_masked', '', 20, 0, 1), 'ratio', 1)
histos_max_scores['btagged_loose_jets_pt_above_20_max_singletau_raw_score_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_singletau_raw_score_masked', '', 20, 0, 1), 'raw score', 1)
histos_max_scores['btagged_loose_jets_pt_above_20_max_singletau_ratio_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_max_singletau_ratio_masked', '', 20, 0, 1), 'ratio', 1)