import ROOT
from histos_part import histos_combined_scores, histos_max_scores

def apply_data_blinding_to_histogram(data_histogram, histogram_name, min_blinded_bins=10):
    """
    Apply blinding to data histogram for ParTRaw histograms.
    
    For tau scores (tauhtaumu, tauhtauh, tauhtaue): blind high score bins (last bins)
    For background scores (singletau, other, b, c): blind low score bins (first bins)
    
    Args:
        data_histogram: ROOT histogram object containing data
        histogram_name: Name of the histogram to check if blinding should be applied
        min_blinded_bins: Minimum number of bins to blind
    
    Returns:
        bool: True if blinding was applied, False otherwise
    """
    
    
    # Get the number of bins
    n_bins = data_histogram.GetNbinsX()
    
    # Determine blinding strategy based on histogram name
    is_tau_score = any(tau_name in histogram_name for tau_name in ['ParTRawTauhtauh', 'ParTRawTauhtaumu', 'ParTRawTauhtaue'])
    is_bkg_score = any(bkg_name in histogram_name for bkg_name in ['ParTRawB', 'ParTRawC', 'ParTRawOther', 'ParTRawSingletau'])
    
    if is_tau_score:
        # For tau scores: blind high score bins (last bins)
        
        # Find the last filled bin (working backwards from the end)
        last_filled_bin = n_bins
        for bin_idx in range(n_bins, 0, -1):
            if data_histogram.GetBinContent(bin_idx) > 0:
                last_filled_bin = bin_idx
                break
        
        # Calculate the starting bin for blinding from the end
        blind_start_bin = max(1, last_filled_bin - min_blinded_bins + 1)
        
        # Set the high score bins to zero
        for bin_idx in range(blind_start_bin, n_bins + 1):
            data_histogram.SetBinContent(bin_idx, 0)
            data_histogram.SetBinError(bin_idx, 0)
            
    elif is_bkg_score:
        # For background scores: blind low score bins (first bins)
        
        # Find the first filled bin (working forwards from the start)
        first_filled_bin = 1
        for bin_idx in range(1, n_bins + 1):
            if data_histogram.GetBinContent(bin_idx) > 0:
                first_filled_bin = bin_idx
                break
        
        # Calculate the ending bin for blinding from the start
        blind_end_bin = min(n_bins, first_filled_bin + min_blinded_bins - 1)
        
        # Set the low score bins to zero
        for bin_idx in range(1, blind_end_bin + 1):
            data_histogram.SetBinContent(bin_idx, 0)
            data_histogram.SetBinError(bin_idx, 0)
    
    else:
        # For other ParTRaw histograms, use default behavior (high bins)
        
        # Find the last filled bin
        last_filled_bin = n_bins
        for bin_idx in range(n_bins, 0, -1):
            if data_histogram.GetBinContent(bin_idx) > 0:
                last_filled_bin = bin_idx
                break
        
        # Calculate the starting bin for blinding from the end
        blind_start_bin = max(1, last_filled_bin - min_blinded_bins + 1)
        
        # Set the high score bins to zero
        for bin_idx in range(blind_start_bin, n_bins + 1):
            data_histogram.SetBinContent(bin_idx, 0)
            data_histogram.SetBinError(bin_idx, 0)
    
    return True

def should_apply_blinding(histogram_name):
    """
    Check if a histogram should have blinding applied based on its name or if it is in specific lists.

    Args:
        histogram_name: Name of the histogram

    Returns:
        bool: True if blinding should be applied
    """
    # These should be imported or defined elsewhere in your code

    #if 'ParTRaw' in histogram_name:
    #    return True
    if histogram_name in histos_combined_scores.keys():
        return True
    if histogram_name in histos_max_scores.keys():
        return True
    return False
