# histos definition
import ROOT

histos = dict()

## common branches
histos_combined_scores = dict()
## combined scores
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_part_all_sig_frac'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_part_all_sig_frac', '', 20, 0, 1), 'sig frac', 1)
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_masked', '', 20, 0, 1), ' frac', 1)
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_masked', '', 20, 0, 1), 'frac', 1)
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_masked'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_masked', '', 20, 0, 1), 'frac', 1)
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_part_sig_over_ParTRawB'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_part_sig_over_ParTRawB', '', 20, 0, 1), 'frac', 1)
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_part_sig_over_ParTRawC'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_part_sig_over_ParTRawC', '', 20, 0, 1), 'frac', 1)
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_part_sig_over_ParTRawOther'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_part_sig_over_ParTRawOther', '', 20, 0, 1), 'frac', 1)        
histos_combined_scores['btagged_loose_jets_pt_above_20_for_histo_part_sig_over_ParTRawSingletau'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_part_sig_over_ParTRawSingletau', '', 20, 0, 1), 'frac', 1)        

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