import argparse
import os
import ROOT
from weights import *



def make_directories_for_plots(label, channels):
    """Create directories for storing plots in multiple formats and versions."""
    for ch in channels:
        # Sample-based plots
        ## BsTauTau scaled
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_scaled/log/png/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_scaled/log/pdf/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_scaled/log/C/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_scaled/log/root/' %(label,ch))
        
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_scaled/lin/png/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_scaled/lin/pdf/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_scaled/lin/C/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_scaled/lin/root/' %(label,ch))
        
        ## BsTauTau not scaled
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_not_scaled/log/png/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_not_scaled/log/pdf/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_not_scaled/log/C/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_not_scaled/log/root/' %(label,ch))
        
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_not_scaled/lin/png/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_not_scaled/lin/pdf/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_not_scaled/lin/C/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/samples_based/bstautau_not_scaled/lin/root/' %(label,ch))
        
        # Flavor-based plots
        ## BsTauTau scaled
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_scaled/log/png/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_scaled/log/pdf/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_scaled/log/C/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_scaled/log/root/' %(label,ch))
        
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_scaled/lin/png/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_scaled/lin/pdf/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_scaled/lin/C/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_scaled/lin/root/' %(label,ch))
        
        ## BsTauTau not scaled
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_not_scaled/log/png/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_not_scaled/log/pdf/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_not_scaled/log/C/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_not_scaled/log/root/' %(label,ch))
        
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_not_scaled/lin/png/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_not_scaled/lin/pdf/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_not_scaled/lin/C/' %(label,ch))
        os.system('mkdir -p plots/%s/%s/flavor_based/bstautau_not_scaled/lin/root/' %(label,ch))

def load_mc_samples(ch, mc_samples_names, files_names, tree_name, tree_dir_mc, tree_dir_wsfs, tree_dir_btag_sfs, luminosity_2018, cross_sections, trigger_selections, use_ntuples_with_sfs, compute_btag_sfs, use_ntuples_with_btag_sfs, part_samples, nevents = None):
    """Load MC samples, apply weights, and trigger selections."""
    mc_samples = dict()
    if compute_btag_sfs or use_ntuples_with_sfs:
        print("Computing b-tagging scale factors, loading from:", tree_dir_wsfs)
        tree_dir_mc = tree_dir_wsfs
    if use_ntuples_with_btag_sfs:
        print("Using b-tagging scale factors, loading from:", tree_dir_btag_sfs)
        tree_dir_mc = tree_dir_btag_sfs

    for k in mc_samples_names:
        file_name = files_names[k]
        print(f"Loaded {tree_dir_mc}/{file_name}.root")
        
        # Create RDataFrame for the sample
        if nevents == None:
            mc_samples[k] = ROOT.RDataFrame(tree_name, f'{tree_dir_mc}/{file_name}.root')
        else:
            mc_samples[k] = ROOT.RDataFrame(tree_name, f'{tree_dir_mc}/{file_name}.root').Range(nevents)
        
        # Apply weight normalization if necessary
        if not compute_btag_sfs and not use_ntuples_with_sfs and not use_ntuples_with_btag_sfs:
            norm_weight = luminosity_2018 * cross_sections[k] * 1000 / get_genEventSumw(f'{tree_dir_mc}/{file_name}.root')
            if part_samples:
                mc_samples[k] = mc_samples[k].Define('norm_weight', f'L1PreFiringWeight_Nom*genWeight*puWeight*{norm_weight}')
            else:
                mc_samples[k] = mc_samples[k].Define('norm_weight', f'L1PreFiringWeight_Nom*genWeight*{norm_weight}')

            # Apply trigger selection
            mc_trigger_selection = [trigger_selections[ch][k] for k in trigger_selections[ch]]
            mc_trigger_condition = ' | '.join(mc_trigger_selection)
            print(f"Applying MC trigger selection for {k} in channel {ch}: {mc_trigger_condition}")
            mc_samples[k] = mc_samples[k].Filter(mc_trigger_condition)

    
    return mc_samples

def save_filtered_data_snapshot(sample_rdf, ch, sample_key, files_names, output_dir):
    """
    Save filtered data snapshot with proper handling of eras - SAME FORMAT AS ORIGINAL.
    
    Args:
        sample_rdf: RDataFrame with filtered data
        ch: Channel name
        sample_key: Sample key (e.g., 'data_sm')
        files_names: Dictionary mapping sample keys to file names
        output_dir: Output directory for snapshots
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save each data sample as multiple era files (SAME AS ORIGINAL)
    file_name = files_names[sample_key]
    
    print(f"Saving filtered data snapshot for {sample_key} (channel {ch})")
    
    # Save as multiple era files to match original structure
    from samples import eras_2018
    # Save only once since eras are already mixed in sample_rdf
    output_path = f"{output_dir}/{file_name}.root"
    print(f"Saving filtered data: {output_path}")


    sample_rdf.Snapshot("Events", output_path)
    print(f"Saved filtered data sample: {file_name}")

def load_data_samples(ch, data_samples, files_names, tree_name, tree_dir_data, trigger_selections, trigger_exclusions, eras_2018, nevents = None, use_filtered_data=False, tree_dir_filtered=None):
    """Load data samples and apply trigger selections and exclusions."""
    data_samples_dict = dict()
    chains_dict = dict()  # Store TChain objects to ensure they persist

    # Choose the appropriate directory - ONLY difference when using filtered data
    if use_filtered_data:
        print(f"Using filtered data from: {tree_dir_filtered}")
        data_dir = tree_dir_filtered
    else:
        data_dir = tree_dir_data

    for k in data_samples[ch]:
        print(f"Loading data sample {k} for channel {ch}")
        file_name = files_names[k]
        tmp_chain = ROOT.TChain(tree_name)

        if use_filtered_data:
            # Only one file, no eras
            era_file = f'{data_dir}/{file_name}.root'
            print(f"Loading {era_file}")
            tmp_chain.Add(era_file)
        else:
            # Add the eras for each data sample
            for era in eras_2018:
                era_file = f'{data_dir}/{file_name}{era}.root'
                print(f"Loading {era_file}")
                tmp_chain.Add(era_file)

        if nevents == None:
            tmp_data_rdf = ROOT.RDataFrame(tmp_chain)
        else:
            tmp_data_rdf = ROOT.RDataFrame(tmp_chain).Range(nevents)
        # Debug: print number of events loaded

        # Apply trigger selection and exclusions ONLY if NOT using filtered data
        if not use_filtered_data:
            trigger_selection = trigger_selections[ch][k]
            exclusions = trigger_exclusions[ch][k]
            
            exclusion_filter = ' & '.join([f'!({exclusion})' for exclusion in exclusions]) if exclusions else ''
            final_trigger_filter = f'({trigger_selection}) & ({exclusion_filter})' if exclusion_filter else trigger_selection
            print(f"Applying combined trigger selection and exclusion for {k} in channel {ch}: {final_trigger_filter}")

            filtered_rdf = tmp_data_rdf.Filter(final_trigger_filter)
        else:
            print(f"Using pre-filtered data for {k} - skipping trigger filters")
            filtered_rdf = tmp_data_rdf

        # Normalization for data is just 1
        if not filtered_rdf.HasColumn('tot_weight'):
            filtered_rdf = filtered_rdf.Define('tot_weight', '1')

        # Store both the TChain and the RDataFrame
        data_samples_dict[k] = filtered_rdf
        chains_dict[k] = tmp_chain

    return data_samples_dict, chains_dict
