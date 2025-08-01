#!/usr/bin/env python3
"""
Analyze part_all_sig_frac histogram with cut > 0.6 and compute significance S/sqrt(S+B).
Usage: python naive_sensitivity_study.py --input 31Jul2025_17h36m15s --channel emu
"""

import ROOT
import argparse
import sys
from math import sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)  # For headless plotting

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='01Aug2025_14h48m28s', help='Input ROOT file')
    parser.add_argument('--channel', default='emu', help='Channel (emu, mumu, ee, e, mu)')
    args = parser.parse_args()
    
    # Open ROOT file
    f = ROOT.TFile("plots/"+args.input+"/histograms.root", "READ")
    if not f or f.IsZombie():
        print(f"Error: Cannot open {args.input}")
        sys.exit(1)
    
    # Specific histogram to analyze
    hname = "btagged_loose_jets_pt_above_20_for_histo_part_all_sig_frac"
    
    print(f"Analyzing histogram: {hname}")
    print(f"Channel: {args.channel}")
    print(f"Cut: > 0.6")
    print("="*60)
    
    # Get histograms from bstautau_not_scaled folder
    sig = f.Get(f"{args.channel}/{hname}/bstautau_not_scaled/lin/bstautau")
    bkg = f.Get(f"{args.channel}/{hname}/bstautau_not_scaled/lin/mc_total")
    
    if not sig:
        print(f"Error: Cannot find signal histogram at {args.channel}/{hname}/bstautau_not_scaled/lin/bstautau")
        f.Close()
        sys.exit(1)
        
    if not bkg:
        print(f"Error: Cannot find background histogram at {args.channel}/{hname}/bstautau_not_scaled/lin/mc_total")
        f.Close()
        sys.exit(1)
    
    print(f"Signal histogram found: {sig.GetName()}")
    print(f"Background histogram found: {bkg.GetName()}")
    print(f"Signal total integral: {sig.Integral():.1f}")
    print(f"Background total integral: {bkg.Integral():.1f}")
    print()
    
    # Find the bin corresponding to cut > 0.6
    cut_value = 0.6
    n_bins = sig.GetNbinsX()
    cut_bin = -1
    
    # Find the first bin with lower edge >= 0.6
    for i in range(1, n_bins + 1):
        bin_low_edge = sig.GetBinLowEdge(i)
        if bin_low_edge >= cut_value:
            cut_bin = i
            break
    
    if cut_bin == -1:
        print(f"Error: Cannot find bin for cut value {cut_value}")
        f.Close()
        sys.exit(1)
    
    print(f"Cut bin: {cut_bin} (bin low edge: {sig.GetBinLowEdge(cut_bin):.3f})")
    
    # Calculate signal and background after cut (integrate from cut_bin to end)
    S = sig.Integral(cut_bin, n_bins)
    B = bkg.Integral(cut_bin, n_bins)
    
    # Calculate significance S/sqrt(S+B)
    if S + B > 0:
        significance = S / sqrt(S + B)
    else:
        significance = 0
        
    print()
    print("RESULTS:")
    print(f"Signal (S) after cut > {cut_value}: {S:.1f}")
    print(f"Background (B) after cut > {cut_value}: {B:.1f}")
    print(f"Significance S/sqrt(S+B): {significance:.4f}")
    print(f"Signal efficiency: {S/sig.Integral()*100:.1f}%")
    print(f"Background efficiency: {B/bkg.Integral()*100:.1f}%")
    
    # Case with signal divided by 10 (more realistic scenario)
    S_scaled = S / 10.0
    if S_scaled + B > 0:
        significance_scaled = S_scaled / sqrt(S_scaled + B)
    else:
        significance_scaled = 0
        
    print()
    print("RESULTS WITH SIGNAL DIVIDED BY 10:")
    print(f"Signal (S/10) after cut > {cut_value}: {S_scaled:.1f}")
    print(f"Background (B) after cut > {cut_value}: {B:.1f}")
    print(f"Significance S/sqrt(S+B): {significance_scaled:.4f}")
    print(f"Signal efficiency: {S_scaled/(sig.Integral()/10)*100:.1f}%")
    print(f"Background efficiency: {B/bkg.Integral()*100:.1f}%")
    
    f.Close()

if __name__ == "__main__":
    main()
