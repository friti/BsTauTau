import ROOT
from samples import data_samples_names
from plotting_utils import set_histogram_style, CMS_lumi, compute_ratio_plot, officialStyle, draw_stat, style_and_draw_bstautau

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
    maxima, maxima_data = [], []
    
    for key, ihist in temp_hists[k].items():
        flavor_name = key.replace(f"{k}_", "")
        is_data = 'data' in flavor_name
        
        # At this point, all histograms should be actual histogram objects
        color = flavor_colors.get(flavor_name.replace('_masked', ''), ROOT.kBlack)
        set_histogram_style(ihist, v[1], 'events', color, color)
        
        if not is_data:
            maxima.append(ihist.GetMaximum())
        else:
            maxima_data.append(ihist.GetMaximum())
    
    return maxima, maxima_data

def create_flavor_histogram_stacks(temp_hists, k, maxima_data, maxima):
    """Create histogram stacks for flavor-based histograms - OPTIMIZED VERSION."""
    ths1 = ROOT.THStack('flavor_stack', '')
    data_ths = ROOT.THStack('data_stack', '')
    
    max_data = max(maxima_data) if maxima_data else 1
    max_total = 1.6 * max(max(maxima), max_data) if maxima else 1.6 * max_data
    
    # Add flavor histograms to stack
    for flavor in ['b_jets', 'c_jets', 'tau_jets', 'other_jets']:
        key = f'{k}_{flavor}'
        if key in temp_hists[k]:
            ihist = temp_hists[k][key]
            # At this point it should already be a histogram, not a lazy object
            ihist.SetMaximum(max_total)
            ths1.Add(ihist)
    
    ths1.SetMaximum(max_total)
    ths1.SetMinimum(0.0001)
    
    # Add data histograms
    for key, ihist in temp_hists[k].items():
        if 'data' not in key:
            continue
        if hasattr(ihist, 'GetValue'):
            ihist = ihist.GetValue()
        ihist.SetLineWidth(2)
        ihist.SetMarkerStyle(20)
        data_ths.Add(ihist)
    
    return ths1, data_ths

def style_and_draw_bstautau(temp_hists, k, data_ths, colours):
    """Handle bstautau histogram styling with proper error checking."""
    bstautau_key = None
    for key in temp_hists[k].keys():
        if 'bstautau' in key:
            bstautau_key = key
            break
    
    if bstautau_key and data_ths.GetStack() and data_ths.GetStack().Last():
        hist = temp_hists[k][bstautau_key]
        if hasattr(hist, 'GetValue'):
            hist = hist.GetValue()
        
        hist.SetFillColor(0)
        hist.SetLineColor(colours['bstautau'])
        hist.SetMarkerColor(colours['bstautau'])
        
        data_integral = data_ths.GetStack().Last().Integral()
        bstautau_integral = hist.Integral()
        
        if bstautau_integral > 0:
            scale_factor = data_integral / bstautau_integral
            hist.Scale(scale_factor)
            hist.Draw("hist same")
            hist.Draw("EP same")

def process_flavor_histograms(histos, temp_hists, ch, label, main_pad, ratio_pad, c1, colours):
    """Process and save flavor-based histograms - OPTIMIZED."""
    
    # Pre-compute all histograms at once to minimize RDataFrame overhead
    print(f"Computing all flavor histograms for channel {ch}...")
    computed_histos = {}
    for k, v in histos[ch].items():
        computed_histos[k] = compute_and_combine_flavor_histograms(temp_hists, k)
    
    # Now process each histogram for plotting
    for k, v in histos[ch].items():
        print(f"Plotting flavor histogram {k} for channel {ch}")
        
        c1.cd()
        main_pad.cd()
        main_pad.SetLogy(False)
        
        # Style histograms - now they are all pre-computed
        maxima, maxima_data = style_flavor_histograms(temp_hists, k, v)
        
        # Create legend after histograms are computed
        leg = create_flavor_legend(temp_hists, ch)
        
        ths1, data_ths = create_flavor_histogram_stacks(temp_hists, k, maxima_data, maxima)
        ths1.Draw('hist')
        ths1.GetXaxis().SetTitle(v[1])
        ths1.GetYaxis().SetTitle('events')
    
        # Only call bstautau styling if we have bstautau data
        if any('bstautau' in key for key in temp_hists[k].keys()):
            style_and_draw_bstautau(temp_hists, k, data_ths, colours)

        stats = draw_stat(ths1)
        
        if data_ths.GetStack() and data_ths.GetStack().Last():
            data_ths.GetStack().Last().SetLineColor(ROOT.kBlack)
            data_ths.GetStack().Last().Draw('EP same')
        
        leg.AddEntry(stats, 'stat. unc.', 'F')
        leg.Draw('same')
        
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
        
        c1.SaveAs(f'plots/{label}/{ch}/flavor/pdf/{k}_flavor.pdf')
        c1.SaveAs(f'plots/{label}/{ch}/flavor/png/{k}_flavor.png')
