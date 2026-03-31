# Plotter BsTauTau

## Setup environment

```
cmsrel CMSSW_13_0_10
cd CMSSW_13_0_10/src/
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools # install nanoaodtools
cd PhysicsTools/NanoAODTools
cmsenv
scram b
cd ../../../../ 
git clone --recursive git@github.com:friti/BsTauTau.git --branch bstautau
cd BsTauTau/plotter_project/
```

## Arguments
General arguments:
- `make_histos`: if enabled it saves the final histograms as png, pdf, root and C files; with lin and log scale; and with the signal scaled to the stack or normalised as LHCb.
- `channels`: choose which ttbar channels to process (sometimes it is useful for testing to just process the `emu` channel, since it is the fastest one). Example: `--channels 'emu','mumu'`
- `flavor`: if enabled, it also creates flavor-based histograms (instead of only sample-based histograms). This is only for jet-based histograms, where the jets are split depending on their flavor rather than the physics process they come from.
- `noblinding`: if enabled, it removes blinding from plots (to be improved)
- `not_part_samples`: it disables all the parts of the framework where the parT score is used. This is useful if you want to run on ntuples without the saved new parT score.
- `plot_all_jets`: As a default, in the jet-based plots [only the two jets](https://github.com/friti/BsTauTau/blob/bstautau/plotter_project/utils.py#L157-L175) with highest pT are included there (this is to reduce the QCD bkg). If this flag is enabled, it plots the jet-based histograms with all the b-tagged jets.
- `plot_part_selections`: [Add to the final histograms](https://github.com/friti/BsTauTau/blob/bstautau/plotter_project/main.py#L248-L256) also [the ones](https://github.com/friti/BsTauTau/blob/bstautau/plotter_project/histos_part_selections.py) used for the final fit: 3 exclusive categories for each ttbar channel, found cutting the parT scores. Also the histogram where only the parT score of tauhtaumu is applied is saved + the histograms of the exclusive categories for the jet mass.
- `save_filtered_data`
- `use_filtered_data`

Scale Factors arguments:
- `no_sfs`: disable scale factors
- `compute_sfs`: it computes the SFs and saves snapshots of the samples with additional branches with the computed SFs. This includes only reco, ID and trigger SFs.
- `compute_btag_sfs`: it computes the b-tagging SFs on top of the ntuples where the other SFs have already been computed and saves snapshots of the samples with additional branches with the computed SFs.
- `use_ntuples_with_sfs`:
- `use_ntuples_with_btag_sfs`

Simplest command to make plots:
`pyhton3 main.py --make_histos --channels 'emu'`
