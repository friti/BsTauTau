import ROOT
from samples import data_samples_names
from plotting_utils import set_histogram_style, CMS_lumi, compute_ratio_plot, officialStyle, draw_stat
from blinding_utils import apply_data_blinding_to_histogram, should_apply_blinding

def initialize_flavor_histograms(histos, samples, ch):
    """Initialize histograms categorized by jet flavor - MAXIMUM EFFICIENCY VERSION."""
    temp_hists = {}
    
    # Define flavor categories based on hadronFlavour
    flavor_categories = {
        'b_jets': 'btagged_loose_jets_pt_above_20_for_histo_hadronFlavour == 5',
        'c_jets': 'btagged_loose_jets_pt_above_20_for_histo_hadronFlavour == 4', 
        'tau_jets': 'btagged_loose_jets_pt_above_20_for_histo_hadronFlavour == 15',
        'other_jets': 'btagged_loose_jets_pt_above_20_for_histo_hadronFlavour != 5 && btagged_loose_jets_pt_above_20_for_histo_hadronFlavour != 4 && btagged_loose_jets_pt_above_20_for_histo_hadronFlavour != 15'
    }
    
    # Get all MC samples (excluding data and bstautau) once
    mc_samples = {kk: vv for kk, vv in samples[ch].items() if 'data' not in kk and 'bstautau' not in kk}
    data_samples = {kk: vv for kk, vv in samples[ch].items() if 'data' in kk}
    bstautau_samples = {kk: vv for kk, vv in samples[ch].items() if 'bstautau' in kk}
    
    if not mc_samples:
        return temp_hists
    
    for k, v in histos[ch].items():
        temp_hists[k] = {}
        
        # Create all flavor branches once per sample, then make all histograms
        enhanced_samples = {}
        
        # Add flavor-filtered branches to each MC sample once
        for sample_name, sample_rdf in mc_samples.items():
            enhanced_rdf = sample_rdf
            for flavor_name, flavor_cut in flavor_categories.items():
                filtered_branch = f"{k}_flavor_{flavor_name}"
                enhanced_rdf = enhanced_rdf.Define(
                    filtered_branch,
                    f"{k}[{flavor_cut}]"
                )
            enhanced_samples[sample_name] = enhanced_rdf
        
        # Now create all histograms from the enhanced samples (still lazy)
        for flavor_name in flavor_categories.keys():
            flavor_hists = []
            filtered_branch = f"{k}_flavor_{flavor_name}"
            for sample_name, enhanced_rdf in enhanced_samples.items():
                hist = enhanced_rdf.Histo1D(v[0], filtered_branch, 'tot_weight')
                flavor_hists.append(hist)
            temp_hists[k][f'{k}_{flavor_name}'] = flavor_hists
        
        # Handle data samples - create lazy histograms
        if data_samples:
            data_hists = [sample_rdf.Histo1D(v[0], k, 'tot_weight') for sample_rdf in data_samples.values()]
            temp_hists[k][f'{k}_data'] = data_hists
        
        # Handle bstautau samples - create lazy histograms  
        if bstautau_samples:
            bstautau_hists = [sample_rdf.Histo1D(v[0], k, 'tot_weight') for sample_rdf in bstautau_samples.values()]
            temp_hists[k][f'{k}_bstautau'] = bstautau_hists
    
    return temp_hists

def compute_and_combine_flavor_histograms(temp_hists, k):
    """Compute all lazy histograms and combine flavor histograms - OPTIMIZED."""
    
    # Process all histogram lists in parallel-friendly way
    for key, hist_list in list(temp_hists[k].items()):
        if isinstance(hist_list, list) and hist_list:
            # Compute all histograms first, then combine
            computed_hists = [hist.GetValue() for hist in hist_list]
            
            # Create combined histogram
            combined_hist = computed_hists[0].Clone(key)
            combined_hist.Reset()
            
            # Add all computed histograms
            for computed_hist in computed_hists:
                combined_hist.Add(computed_hist)
            
            # Replace the list with the combined histogram
            temp_hists[k][key] = combined_hist
    
    return temp_hists[k]

def get_flavor_colors():

    """Define colors for different jet flavors."""
    return {
        'b_jets': ROOT.kRed,
        'c_jets': ROOT.kBlue,
        'tau_jets': ROOT.kGreen + 2,
        'other_jets': ROOT.kOrange,
        'data_sm': ROOT.kBlack,
        'data_eg': ROOT.kBlack,
        'bstautau': ROOT.TColor.GetColor("#ffa90e")
    }

def get_flavor_titles():
    """Define titles for different jet flavors."""
    return {
        'b_jets': 'b-jets',
        'c_jets': 'c-jets', 
        'tau_jets': '#tau-jets',
        'other_jets': 'other jets',
        'data': 'Data',
        'bstautau': 'B_{s}#rightarrow #tau #tau'
    }

def create_flavor_legend(temp_hists, ch):
    """Create legend for flavor-based histograms."""
    leg = ROOT.TLegend(0.24,.67,.95,.90)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.035)
    leg.SetNColumns(3)
    
    flavor_titles = get_flavor_titles()
    k = list(temp_hists.keys())[0]
    
    # Add flavor entries - now the histograms should be actual histogram objects
    for flavor in ['b_jets', 'c_jets', 'tau_jets', 'other_jets']:
        if f'{k}_{flavor}' in temp_hists[k].keys():
            hist_obj = temp_hists[k][f'{k}_{flavor}']
            # Make sure it's a histogram object, not a dictionary
            if hasattr(hist_obj, 'GetValue'):
                hist_obj = hist_obj.GetValue()
            leg.AddEntry(hist_obj, flavor_titles[flavor], 'F')

    # Add single data entry
    if f'{k}_data' in temp_hists[k].keys():
        hist_obj = temp_hists[k][f'{k}_data']
        if hasattr(hist_obj, 'GetValue'):
            hist_obj = hist_obj.GetValue()
        leg.AddEntry(hist_obj, flavor_titles['data'], 'EP')

    # Add bstautau entry if present
    for sample_name in temp_hists[k].keys():
        if 'bstautau' in sample_name:
            hist_obj = temp_hists[k][sample_name]
            if hasattr(hist_obj, 'GetValue'):
                hist_obj = hist_obj.GetValue()
            leg.AddEntry(hist_obj, flavor_titles['bstautau'], 'L')
    
    return leg

def style_flavor_histograms(temp_hists, k, v):
    """Style histograms for flavor categorization - AFTER COMPUTATION."""
    flavor_colors = get_flavor_colors()
    
    for key, ihist in temp_hists[k].items():
        flavor_name = key.replace(f"{k}_", "")
        is_data = 'data' in flavor_name
        
        # At this point, all histograms should be actual histogram objects
        color = flavor_colors.get(flavor_name.replace('_masked', ''), ROOT.kBlack)
        set_histogram_style(ihist, v[1], 'events', color, color)

def calculate_flavor_maximum(temp_hists, k):
    """Calculate the maximum Y value considering all scenarios including scaled BsTauTau."""
    maxima, maxima_data = [], []
    
    # Get maxima from flavor histograms and data
    for key, ihist in temp_hists[k].items():
        flavor_name = key.replace(f"{k}_", "")
        is_data = 'data' in flavor_name
        
        if not is_data and 'bstautau' not in flavor_name:
            maxima.append(ihist.GetMaximum())
        elif is_data:
            maxima_data.append(ihist.GetMaximum())
    
    mc_max = max(maxima) if maxima else 1
    data_max = max(maxima_data) if maxima_data else 1
    
    # For BsTauTau plots, calculate max considering both scaled and unscaled versions
    bstautau_key = None
    for key in temp_hists[k].keys():
        if 'bstautau' in key:
            bstautau_key = key
            break
    
    if bstautau_key:
        bstautau_hist = temp_hists[k][bstautau_key]
        if hasattr(bstautau_hist, 'GetValue'):
            bstautau_hist = bstautau_hist.GetValue()
        
        bstautau_unscaled_max = bstautau_hist.GetMaximum()
        
        # Calculate what the scaled max would be (using total MC as reference)
        if maxima:
            total_mc_integral = sum(hist.Integral() for hist in [temp_hists[k][f'{k}_{flavor}'] for flavor in ['b_jets', 'c_jets', 'tau_jets', 'other_jets'] if f'{k}_{flavor}' in temp_hists[k]])
            scale_factor = total_mc_integral / bstautau_hist.Integral() if bstautau_hist.Integral() > 0 else 1
            bstautau_scaled_max = bstautau_unscaled_max * scale_factor
        else:
            bstautau_scaled_max = bstautau_unscaled_max
        
        # Use the maximum of all scenarios
        desired_max = 1.6 * max(mc_max, data_max, bstautau_unscaled_max, bstautau_scaled_max)
    else:
        desired_max = 1.6 * max(mc_max, data_max)
    
    return desired_max

def create_flavor_histogram_stacks(temp_hists, k, desired_max, blinding):
    """Create histogram stacks for flavor-based histograms - OPTIMIZED VERSION."""
    ths1 = ROOT.THStack('flavor_stack', '')
    data_ths = ROOT.THStack('data_stack', '')
    
    # Add flavor histograms to stack
    for flavor in ['b_jets', 'c_jets', 'tau_jets', 'other_jets']:
        key = f'{k}_{flavor}'
        if key in temp_hists[k]:
            ihist = temp_hists[k][key]
            # At this point it should already be a histogram, not a lazy object
            ihist.SetMaximum(desired_max)
            ths1.Add(ihist)
    
    ths1.SetMaximum(desired_max)
    ths1.SetMinimum(0.0001)
    
    # Add data histograms
    for key, ihist in temp_hists[k].items():
        if 'data' not in key:
            continue
        if hasattr(ihist, 'GetValue'):
            ihist = ihist.GetValue()
        
        # Apply blinding to data histograms for ParTRaw plots
        if should_apply_blinding(k) and blinding :
            apply_data_blinding_to_histogram(ihist, k)
        
        ihist.SetLineWidth(2)
        ihist.SetMarkerStyle(20)
        data_ths.Add(ihist)
    
    return ths1, data_ths

def style_and_draw_bstautau(temp_hists, k, ths1, colours):
    """Handle bstautau histogram styling with proper error checking."""
    bstautau_key = None
    for key in temp_hists[k].keys():
        if 'bstautau' in key:
            bstautau_key = key
            break
    
    if bstautau_key and ths1.GetStack() and ths1.GetStack().Last():
        hist = temp_hists[k][bstautau_key]
        if hasattr(hist, 'GetValue'):
            hist = hist.GetValue()
        
        hist.SetFillColor(0)
        hist.SetLineColor(colours['bstautau'])
        hist.SetMarkerColor(colours['bstautau'])
        
        data_integral = ths1.GetStack().Last().Integral()
        bstautau_integral = hist.Integral()
        
        if bstautau_integral > 0:
            scale_factor = data_integral / bstautau_integral
            hist.Scale(scale_factor)
            hist.Draw("hist same")
            hist.Draw("EP same")

def style_and_draw_bstautau_flavor(temp_hists, k, ths1, colours, scale_to_mc=True):
    """Handle bstautau histogram styling with proper scaling control for flavor plots."""
    bstautau_key = None
    for key in temp_hists[k].keys():
        if 'bstautau' in key:
            bstautau_key = key
            break
    
    if bstautau_key and ths1.GetStack() and ths1.GetStack().Last():
        hist = temp_hists[k][bstautau_key]
        hist.SetFillColor(0)
        hist.SetLineColor(colours['bstautau'])
        hist.SetMarkerColor(colours['bstautau'])
        #print("BsTauTau histogram integral:", hist.Integral(),k)
        
        if scale_to_mc:
            scale_factor = ths1.GetStack().Last().Integral() / hist.Integral() if hist.Integral() > 0 else 1
            hist.Scale(scale_factor)
            #print(f"Scaled BsTauTau histogram for total of {hist.Integral()}")

        hist.Draw("hist same")
        hist.Draw("EP same")

def save_flavor_plot_versions(c1, label, ch, k, main_pad, scale_suffix=""):
    """
    Save flavor plots in multiple formats and versions with new directory structure.
    """
    if scale_suffix == "_scaled":
        base_path = f'plots/{label}/{ch}/flavor_based/bstautau_scaled'
    elif scale_suffix == "_unscaled":
        base_path = f'plots/{label}/{ch}/flavor_based/bstautau_not_scaled'
    else:
        # For plots without BsTauTau, use scaled path as default
        base_path = f'plots/{label}/{ch}/flavor_based/bstautau_scaled'
    
    # Linear version
    main_pad.SetLogy(False)
    c1.Modified()
    c1.Update()
    
    # Save linear versions in all formats
    c1.SaveAs(f'{base_path}/lin/pdf/{k}_flavor.pdf')
    c1.SaveAs(f'{base_path}/lin/png/{k}_flavor.png')
    c1.SaveAs(f'{base_path}/lin/C/{k}_flavor.C')
    c1.SaveAs(f'{base_path}/lin/root/{k}_flavor.root')
    
    # Log version - need to adjust maximum to avoid overlap with legend
    main_pad.SetLogy(True)
    
    # Get all drawable objects from the main pad to find the maximum
    current_max = 0
    pad_primitives = main_pad.GetListOfPrimitives()
    for obj in pad_primitives:
        if hasattr(obj, 'GetMaximum'):
            obj_max = obj.GetMaximum()
            if obj_max > current_max:
                current_max = obj_max
        elif hasattr(obj, 'GetStack') and obj.GetStack():
            # For THStack objects
            stack_max = obj.GetStack().Last().GetMaximum()
            if stack_max > current_max:
                current_max = stack_max
    
    # Set maximum to 1000 times the current maximum for log scale
    log_max = current_max * 1000
    for obj in pad_primitives:
        if hasattr(obj, 'SetMaximum'):
            obj.SetMaximum(log_max)
    
    c1.Modified()
    c1.Update()
    
    # Save log versions in all formats
    c1.SaveAs(f'{base_path}/log/pdf/{k}_flavor.pdf')
    c1.SaveAs(f'{base_path}/log/png/{k}_flavor.png')
    c1.SaveAs(f'{base_path}/log/C/{k}_flavor.C')
    c1.SaveAs(f'{base_path}/log/root/{k}_flavor.root')
    
    # Reset to linear for consistency and restore original maximum
    main_pad.SetLogy(False)
    for obj in pad_primitives:
        if hasattr(obj, 'SetMaximum'):
            obj.SetMaximum(current_max)
    
    c1.Modified()
    c1.Update()

def process_flavor_histograms(histos, temp_hists, ch, label, main_pad, ratio_pad, c1, colours, blinding):
    """Process and save flavor-based histograms - OPTIMIZED."""
    
    # Create ROOT file for saving flavor histograms with compression
    root_file_path = f'plots/{label}/histograms_flavor.root'
    root_file = ROOT.TFile(root_file_path, 'UPDATE', "", ROOT.kLZMA)  # Use LZMA compression
    root_file.SetCompressionLevel(1)  # Fast compression
    print(f"Created flavor ROOT file: {root_file_path}")
    
    # Create channel folder in ROOT file
    channel_folder = root_file.mkdir(ch)
    
    # Pre-compute all histograms at once to minimize RDataFrame overhead
    print(f"Computing all flavor histograms for channel {ch}...")
    computed_histos = {}
    for k, v in histos[ch].items():
        computed_histos[k] = compute_and_combine_flavor_histograms(temp_hists, k)
    
    # Now process each histogram for plotting
    for i, (k, v) in enumerate(histos[ch].items()):
        
        c1.cd()
        main_pad.cd()
        main_pad.SetLogy(False)
        
        # Style histograms - now they are all pre-computed
        style_flavor_histograms(temp_hists, k, v)
        
        # Calculate maximum considering all scenarios
        desired_max = calculate_flavor_maximum(temp_hists, k)
        
        # Create legend after histograms are computed
        leg = create_flavor_legend(temp_hists, ch)
        
        ths1, data_ths = create_flavor_histogram_stacks(temp_hists, k, desired_max, blinding)
        
        # Get X-axis range from the histogram
        x_min = ths1.GetXaxis().GetXmin() if ths1.GetStack() and ths1.GetStack().Last() else 0
        x_max = ths1.GetXaxis().GetXmax() if ths1.GetStack() and ths1.GetStack().Last() else 1
        
        # Clear and draw with fixed Y-axis range
        main_pad.Clear()
        
        # Draw frame with desired Y-axis range
        frame = main_pad.DrawFrame(x_min, 0.0001, x_max, desired_max)
        frame.GetXaxis().SetTitle(v[1])
        frame.GetYaxis().SetTitle('events')
        
        # Draw histogram on top of the fixed frame
        ths1.Draw('hist same')

        stats = draw_stat(ths1)
        
        if data_ths.GetStack() and data_ths.GetStack().Last():
            data_ths.GetStack().Last().SetLineColor(ROOT.kBlack)
            data_ths.GetStack().Last().Draw('EP same')
        
        leg.AddEntry(stats, 'stat. unc.', 'F')
        leg.Draw('same')

        # Save histograms to ROOT file BEFORE any scaling
        save_flavor_histograms_to_root_file(channel_folder, k, ths1, data_ths, temp_hists)

        # IMPORTANT: Plot unscaled version FIRST, then scaled version
        
        # Version 1: BsTauTau at original scale (not scaled to data) - PLOT FIRST
        if any('bstautau' in key for key in temp_hists[k].keys()):
            style_and_draw_bstautau_flavor(temp_hists, k, ths1, colours, scale_to_mc=False)

        CMS_lumi(main_pad, 4, 0, cmsText='CMS', extraText=' Preliminary', lumi_13TeV='L = 59.7 fb^{-1}')
        
        # Ratio pad
        if data_ths.GetStack() and data_ths.GetStack().Last():
            ratio = data_ths.GetStack().Last().Clone()
            ratio.Divide(stats)
            
            ratio_stats, norm_stack, line, ratio = compute_ratio_plot(temp_hists[k], ratio, stats, ratio_pad)
            ratio_pad.cd()
            
            ratio_stats.Draw('E2')
            line.Draw('same')
            ratio.Draw('EP same')
        
        c1.Modified()
        c1.Update()
        
        # Save unscaled version in all formats (linear and log)
        save_flavor_plot_versions(c1, label, ch, k, main_pad, scale_suffix="_unscaled")

        # Version 2: BsTauTau scaled to data (current behavior) - PLOT SECOND
        if any('bstautau' in key for key in temp_hists[k].keys()):
            # Clear and redraw everything with scaling
            c1.cd()
            main_pad.cd()
            main_pad.Clear()
            
            # Apply the same frame strategy for the scaled version
            frame = main_pad.DrawFrame(x_min, 0.0001, x_max, desired_max)
            frame.GetXaxis().SetTitle(v[1])
            frame.GetYaxis().SetTitle('events')
            
            # Redraw the main plot components on the fixed frame
            ths1.Draw('hist same')
            stats.Draw('E2 SAME')
            if data_ths.GetStack() and data_ths.GetStack().Last():
                data_ths.GetStack().Last().Draw('EP same')
            leg.Draw('same')
            
            # Draw BsTauTau WITH scaling (using cloned histogram)
            style_and_draw_bstautau_flavor(temp_hists, k, ths1, colours, scale_to_mc=True)
            
            CMS_lumi(main_pad, 4, 0, cmsText='CMS', extraText=' Preliminary', lumi_13TeV='L = 59.7 fb^{-1}')
            
            # Redraw ratio plot (same as before)
            ratio_pad.cd()
            ratio_pad.Clear()
            if data_ths.GetStack() and data_ths.GetStack().Last():
                ratio_stats.Draw('E2')
                line.Draw('same')
                ratio.Draw('EP same')
            
            # Save scaled version in all formats (linear and log)
            save_flavor_plot_versions(c1, label, ch, k, main_pad, scale_suffix="_scaled")

        else:
            # For plots without BsTauTau, just save the regular version
            save_flavor_plot_versions(c1, label, ch, k, main_pad, scale_suffix="")

    # Close the ROOT file
    root_file.Close()
    print(f"Flavor ROOT file saved: {root_file_path}")


def save_flavor_histograms_to_root_file(channel_folder, histogram_name, ths1, data_ths, temp_hists):
    """
    Save flavor-based histograms to ROOT file with proper folder structure.
    
    Args:
        channel_folder: ROOT directory for the channel
        histogram_name: Name of the histogram (k)
        ths1: Flavor stack (combined b, c, tau, other jets)
        data_ths: Data stack
        temp_hists: Dictionary containing all histograms
    """
    # Create subfolder for this histogram
    histo_folder = channel_folder.mkdir(histogram_name)
    histo_folder.cd()
    
    # Save flavor stack (total background)
    if ths1.GetStack() and ths1.GetStack().Last():
        flavor_total = ths1.GetStack().Last().Clone(f"{histogram_name}_flavor_total")
        flavor_total.Write("ths1")
    
    # Save data
    if data_ths.GetStack() and data_ths.GetStack().Last():
        data_hist = data_ths.GetStack().Last().Clone(f"{histogram_name}_data")
        data_hist.Write("data")
    
    # Save bstautau signal if present
    if f'{histogram_name}_bstautau' in temp_hists[histogram_name]:
        bstautau_hist = temp_hists[histogram_name][f'{histogram_name}_bstautau'].Clone(f"{histogram_name}_bstautau")
        bstautau_hist.Write("bstautau")
    
    # Save individual flavor categories
    flavor_categories = ['b_jets', 'c_jets', 'tau_jets', 'other_jets']
    for flavor in flavor_categories:
        key = f'{histogram_name}_{flavor}'
        if key in temp_hists[histogram_name]:
            flavor_hist = temp_hists[histogram_name][key].Clone(f"{histogram_name}_{flavor}")
            flavor_hist.Write(flavor)
        if key in temp_hists[histogram_name]:
            flavor_hist = temp_hists[histogram_name][key].Clone(f"{histogram_name}_{flavor}")
            flavor_hist.Write(flavor)
            flavor_hist = temp_hists[histogram_name][key].Clone(f"{histogram_name}_{flavor}")
            flavor_hist.Write(flavor)
        if key in temp_hists[histogram_name]:
            flavor_hist = temp_hists[histogram_name][key].Clone(f"{histogram_name}_{flavor}")
            flavor_hist.Write(flavor)

