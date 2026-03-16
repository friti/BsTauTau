# histos definition for sequential cuts - 6 total histograms
import ROOT

# Sequential cuts histograms - explicit list like histos_part.py
histos_part_selections = dict()

## Exclusive categories - 3 mutually exclusive regions (original binning for plotting)
#histos_part_selections['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_general_exclusive'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_general_exclusive', '', 20, 0, 1), 'ParT #tau_{h}#tau_{e} frac (exclusive: tauhtaumu < 0.6 & tauhtaue > 0.4)', [0, 1])
#histos_part_selections['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_general_exclusive'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_general_exclusive', '', 20, 0, 1), 'ParT #tau_{h}#tau_{h} frac (exclusive: tauhtaumu < 0.6 & tauhtaue < 0.4)', [0, 1])
#histos_part_selections['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_general_exclusive'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_general_exclusive', '', 20, 0, 1), 'ParT #tau_{h}#tau_{#mu} frac (exclusive: tauhtaumu > 0.6)', [0, 1])

## Exclusive categories - OPTIMIZED BINNING FOR FITTING
histos_part_selections['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_general_exclusive'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_general_exclusive', '', 10, 0.4, 1.0), 'ParT #tau_{h}#tau_{e} frac (exclusive fit: tauhtaumu < 0.6 & tauhtaue > 0.4)', [0.4, 1.0])
histos_part_selections['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_general_exclusive'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_general_exclusive', '', 10, 0.0, 0.6), 'ParT #tau_{h}#tau_{h} frac (exclusive fit: tauhtaumu < 0.6 & tauhtaue < 0.4)', [0.0, 0.6])
histos_part_selections['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_general_exclusive'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_general_exclusive', '', 10, 0.6, 0.9), 'ParT #tau_{h}#tau_{#mu} frac (exclusive fit: tauhtaumu > 0.6)', [0.6, 0.95])

## Simple tauhtaumu cut categories - 3 overlapping regions based only on tauhtaumu (original binning)
histos_part_selections['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_general_onlytaumucut'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_general_onlytaumucut', '', 20, 0, 1), 'ParT #tau_{h}#tau_{e} frac (only tauhtaumu cut: < 0.6)', [0, 1])
histos_part_selections['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_general_onlytaumucut'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_general_onlytaumucut', '', 20, 0, 1), 'ParT #tau_{h}#tau_{h} frac (only tauhtaumu cut: < 0.6)', [0, 1])
histos_part_selections['btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_general_onlytaumucut'] = (ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_general_onlytaumucut', '', 20, 0, 1), 'ParT #tau_{h}#tau_{#mu} frac (only tauhtaumu cut: > 0.6)', [0, 1])

# Jet mass histograms for exclusive selections
histos_part_selections['btagged_loose_jets_pt_above_20_for_histo_m_exclusive_tauhtaumu'] = (
    ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_m_exclusive_tauhtaumu', '', 30, 0, 60),
    'Jet mass (exclusive: tauhtaumu > 0.6)', [0, 60]
)
histos_part_selections['btagged_loose_jets_pt_above_20_for_histo_m_exclusive_tauhtaue'] = (
    ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_m_exclusive_tauhtaue', '', 30, 0, 60),
    'Jet mass (exclusive: tauhtaumu < 0.6 & tauhtaue > 0.4)', [0, 60]
)
histos_part_selections['btagged_loose_jets_pt_above_20_for_histo_m_exclusive_tauhtauh'] = (
    ROOT.RDF.TH1DModel('btagged_loose_jets_pt_above_20_for_histo_m_exclusive_tauhtauh', '', 30, 0, 60),
    'Jet mass (exclusive: tauhtaumu < 0.6 & tauhtaue < 0.4)', [0, 60]
)
