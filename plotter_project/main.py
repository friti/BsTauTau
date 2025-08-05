from datetime import datetime
from io_utils import *
from samples import *
from selection import *
from weights import *
from sf_electron import *
from sf_muon import *
from sf_trigger_dilepton import *
from sf_computation import *
from utils import *
from plotting_utils import *
from histos_baseline import *
from histos_part import histos_combined_scores, histos_max_scores
from part_scores_functions import *
from plotting_flavourbased_utils import *

import argparse
import os
import correctionlib
correctionlib.register_pyroot_binding()

nevents = None  # Set to None to process all events, or specify a number for a limited range

ROOT.gROOT.SetBatch()   
ROOT.gStyle.SetOptStat(0)

# Silence ROOT's verbose output messages
ROOT.gErrorIgnoreLevel = ROOT.kWarning  # Suppresses Info messages, keeps Warning and Error

# Enable ROOT multithreading for performance (only if processing all events)
if nevents is None:
    import multiprocessing
    n_threads = multiprocessing.cpu_count()
    print(f"Enabling ROOT multithreading with {n_threads} threads")
    ROOT.EnableImplicitMT(n_threads)
    
    # Optimize ROOT for performance
    ROOT.gEnv.SetValue("TFile.AsyncPrefetching", "1")  # Enable async prefetching
    ROOT.gEnv.SetValue("TTreeCache.Size", "50000000")  # 50MB cache
    ROOT.gEnv.SetValue("TFile.MaxPrefetchCacheSize", "100000000")  # 100MB prefetch
    ROOT.gEnv.SetValue("RDataFrame.DefaultNSlots", str(n_threads))  # Force RDataFrame to use all cores
else:
    print(f"Multithreading disabled because nevents is limited to {nevents}")
    print("ROOT multithreading doesn't work well with limited event processing")

def parse_arguments():
    parser = argparse.ArgumentParser(description="BsTauTau Plotter")
    parser.add_argument('--channels', nargs='+', default=['emu'], help='Channels to process')
    parser.add_argument('--flavor', action='store_true', default=False, help='Enable flavor-based histograms')
    parser.add_argument('--make_histos', action='store_true', default=False, help='Enable sample-based histograms')
    parser.add_argument('--noblinding', action='store_true', default=False, help='Disable blinding')
    parser.add_argument('--not_part_samples', action='store_true', default=False, help='Disable part samples (if you want to plot with old Cecile samples)')
    parser.add_argument('--no_sfs', action='store_true', default=False, help='Disable scale factors')
    parser.add_argument('--compute_sfs', action='store_true', default=False, help='Save snapshots with scale factors (run again for plotting)')
    parser.add_argument('--compute_btag_sfs', action='store_true', default=False, help='Save snapshots with b-tag scale factors (run again for plotting)')
    parser.add_argument('--use_ntuples_with_sfs', action='store_true', default=False, help='Use ntuples with scale factors')
    parser.add_argument('--use_ntuples_with_btag_sfs', action='store_true', default=False, help='Use ntuples with b-tag scale factors')
    return parser.parse_args()

tau_scores = ['ParTRawTauhtauh', 'ParTRawTauhtaumu', 'ParTRawTauhtaue']
bkg_scores = ['ParTRawB', 'ParTRawC', 'ParTRawOther', 'ParTRawSingletau']
parT_scores = tau_scores + bkg_scores

declare_sfs_cpp_functions()


def main():

    label = '%s'%(datetime.now().strftime('%d%b%Y_%Hh%Mm%Ss'))
    print("#### Plotting label:", label)
    args = parse_arguments()
    channels = args.channels
    channels = channels[0].split(',')
    print("---- Processing channels: ", channels)
    no_sfs = args.no_sfs
    compute_sfs = args.compute_sfs #Compute lepton SFs
    compute_btag_sfs = args.compute_btag_sfs # Compute btagging SFs (lep SFs required)
    use_ntuples_with_sfs = args.use_ntuples_with_sfs ##Plot only with lep SFs
    use_ntuples_with_btag_sfs = args.use_ntuples_with_btag_sfs ## Plot with lep Sfs and btagging SFs
    flavor = args.flavor
    make_histos = args.make_histos
    blinding = not args.noblinding
    part_samples = not args.not_part_samples

    # Create plot directories
    make_directories_for_plots(label, channels)

    samples = dict()
    tree_name = 'Events'

    load_invmass()
    load_sorting_functions()
    for ch in channels:
        print("=============================")
        print(f"========= Channel {ch} ========")
        print("=============================")

        #tree_dir_data = '/eos/cms/store/cmst3/group/bpark/ccaillol/ntuples_emu_2018_ParT/'
        if not part_samples:
            tree_dir = '/eos/cms/store/cmst3/group/bpark/ccaillol/ntuples_%s_2018'%(ch)
            tree_dir_wsfs= None
            tree_dir_btag_sfs = None
            files_names['tt_semilep'] = 'TTToSemiLeptonic'
            files_names['st_tw'] = 'ST_tW_top'
            # Remove 'bstautau' from mc_samples_names if present
            used_mc_samples_names = [name for name in mc_samples_names if name != 'bstautau']
            
        else:
            tree_dir = '/eos/cms/store/cmst3/group/bpark/friti/bstautau/flat_ntuples/ntuples_%s_2018_ParT'%(ch)
            tree_dir_wsfs = '/eos/cms/store/cmst3/group/bpark/friti/bstautau/flat_ntuples/ntuples_%s_2018_ParT/wsfs_snapshots'%(ch)
            tree_dir_btag_sfs = '/eos/cms/store/cmst3/group/bpark/friti/bstautau/flat_ntuples/ntuples_%s_2018_ParT/btag_sfs_snapshots'%(ch)
            used_mc_samples_names = mc_samples_names  # Use all MC samples including 'bstautau'

        samples[ch] = dict()

        # Handle MC samples
        print("====== Loading MC Samples ======")
        mc_samples = load_mc_samples(ch, used_mc_samples_names, files_names, tree_name, tree_dir, tree_dir_wsfs, tree_dir_btag_sfs, luminosity_2018, cross_sections, trigger_selections, use_ntuples_with_sfs, compute_btag_sfs, use_ntuples_with_btag_sfs, part_samples, nevents)
        samples[ch].update(mc_samples)

        # Handle data samples
        print("====== Loading Data Samples ======")
        data_samples, chains = load_data_samples(ch, data_samples_names, files_names, tree_name, tree_dir, trigger_selections, trigger_exclusions, eras_2018, nevents)
        samples[ch].update(data_samples)

        for k, v in samples[ch].items():

            minimum_jet_conditions = '(j_pt > 20 & abs(j_eta)< 2.5 & j_jetid>=2)' # jet pt >20 for btagging SFs

            if 'bstautau' in k:
                bstautau_conditions = {
                    "general": "SigJetMask",
                    "tauhtauh": "SigJetMaskTauhtauh",
                    "tauhtaue": "SigJetMaskTauhtaue",
                    "tauhtaumu": "SigJetMaskTauhtaumu"
                }
            else:
                bstautau_conditions = None

            #!!!!! MC snapshots already saved and these branches already defined. Be careful if changing jet selections this needs to rerun!!!
            if (not compute_btag_sfs and not use_ntuples_with_sfs and not use_ntuples_with_btag_sfs) or 'data' in k: 

                samples[ch][k] = define_invariant_mass_and_mt(samples[ch][k],ch)

                # Define jet branches
                samples[ch][k] = define_jets_with_minimum_selection(samples[ch][k],minimum_jet_conditions, part_samples)

                ## define bstautau mask
                if 'bstautau' in k:
                    samples[ch][k] = define_bstautau_mask(samples[ch][k])

                # Define jets with minimum selection for histograms
                samples[ch][k] = define_jets_with_minimum_selection_for_histos(samples[ch][k], is_bstautau='bstautau' in k, bstautau_conditions=bstautau_conditions, part_samples=part_samples)

                # Define b-tagging conditions
                samples[ch][k] = define_jets_with_btagging_selection(samples[ch][k], part_samples=part_samples)


                ## define bstautau mask for different tau decay modes
                if 'bstautau' in k:
                    samples[ch][k] = define_bstautau_taudecaymodes_mask(samples[ch][k])


                # Define Filtering conditions (used in selections)
                samples[ch][k] = define_btagging_conditions(samples[ch][k], ch)
                samples[ch][k] = define_jet_conditions(samples[ch][k], ch,minimum_jet_conditions)

                # Filter the samples
                filter = preselection[ch]
                samples[ch][k] = samples[ch][k].Filter(filter)

                samples[ch][k] = samples[ch][k].Filter(f"ROOT::VecOps::Any({minimum_jet_conditions})")
                if 'bstautau' in k:
                    samples[ch][k] = samples[ch][k].Filter(f"ROOT::VecOps::Any({bstautau_conditions['general']})")


            # First compute Sfs, after rerun to compute btagging SFs, after rerun for plotting
            # Compute Scale Factors if requested
            if compute_sfs and 'data' not in k:
                print(f"Computing scale factors for sample {k} in channel {ch}")
                samples[ch][k] = compute_all_scale_factors(samples[ch][k], ch, k, files_names)

                ## Specify a custom output directory for saving snapshots
                output_dir = f"{tree_dir}/wsfs_snapshots/"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                save_samples_with_sfs(samples[ch][k], ch, k, files_names, output_dir=output_dir)

            # Compute B-tagging Scale Factors separately if requested
            if compute_btag_sfs and 'data' not in k:
                print(f"Computing b-tagging scale factors for sample {k} in channel {ch}")
                samples[ch][k] = compute_btagging_scale_factors(samples[ch][k], ch)
                samples[ch][k] = compute_btagging_event_weight(samples[ch][k], ch)

                ## Specify a custom output directory for saving snapshots
                output_dir = f"{tree_dir}/btag_sfs_snapshots/"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                #plot_event_weight_2d(samples[ch][k], 'sfs_plots/')
                save_samples_with_btagging_sfs(samples[ch][k], ch, k, files_names, output_dir=output_dir)


            if 'data' not in k:
                weight_str = build_weight_string(k, files_names, args)
                #print(f"Applying weights to {k}: {weight_str}")
                samples[ch][k] = samples[ch][k].Define('tot_weight', weight_str)


            if part_samples:
                histos[ch].update(histos_jets_part)
                histos[ch].update(histos_interesting_jets_part)


                ## Define combined scores histograms
                samples[ch][k] = define_combined_scores(samples[ch][k], tau_scores, parT_scores, bkg_scores, 'bstautau' in k, bstautau_conditions)
                histos[ch].update(histos_combined_scores)
                
                if flavor:
                    histos_flavor[ch].update(histos_interesting_jets_part)
                    histos_flavor[ch].update(histos_combined_scores)



                ## define MAX scores
                samples[ch][k] = define_max_scores(samples[ch][k], parT_scores, 'bstautau' in k, bstautau_conditions)
                histos[ch].update(histos_max_scores)
                #histos_flavor[ch].update(histos_max_scores) Not really easy to do because they are filtered in a weird way and I would need to define also hadronFlavor with the same filter

        print("##### Creating Histogram Definitions #####")
        # Initialize all histogram definitions BEFORE processing (lazy setup)
        temp_hists = None
        temp_flavor_hists = None
        
        if make_histos:
            print("Setting up sample-based histograms...")
            temp_hists = initialize_histograms(histos, samples, ch)
        
        if flavor:
            print("Setting up flavor-based histograms...")
            temp_flavor_hists = initialize_flavor_histograms(histos_flavor, samples, ch)

        print("##### Plotting Histograms #####")
        c1, main_pad, ratio_pad = create_canvas_with_pads()
        
        if make_histos and temp_hists:
            print("Processing sample-based histograms...")
            process_histograms(histos, temp_hists, samples, ch, colours, label, titles, main_pad, ratio_pad, c1, blinding)

        if flavor and temp_flavor_hists:
            print("Processing flavor-based histograms...")
            process_flavor_histograms(histos_flavor, temp_flavor_hists, ch, label, main_pad, ratio_pad, c1, colours, blinding)

        print("#### Plotting label:", label)
        print("End channel ", ch, "script at ", datetime.now().strftime('%d%b%Y_%Hh%Mm%Ss'))

    print("#### Plotting label:", label)
    print("End of script at ", datetime.now().strftime('%d%b%Y_%Hh%Mm%Ss'))
if __name__ == '__main__':
    main()
