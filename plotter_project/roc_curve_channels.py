import ROOT
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import auc

# Open the ROOT file

root_file = ROOT.TFile("plots/08Aug2025_20h07m39s_allsfs_2highestptbtaggedjets/histograms.root", "READ") #mumu
#root_file = ROOT.TFile("plots/08Aug2025_20h06m25s_allsfs_alljets/histograms.root", "READ") #mumu
#root_file = ROOT.TFile("plots/11Aug2025_15h09m14s/histograms.root", "READ") #mumu


# Signal histogram names and labels

signal_hist_names = {
    "btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_masked": "ParTRawTauhtaumu",
    "btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_masked": "ParTRawTauhtauh",
    "btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_masked": "ParTRawTauhtaue"
}


plt.figure()
marker_coords = {}  # to store (bkg_eff, signal_eff) for the X

# Loop over signal histograms
for hist_name, label in signal_hist_names.items():
    data_hist = root_file.Get(f"emu/{hist_name}/bstautau_scaled/lin/mc_total")
    total_bkg_integral = data_hist.Integral()

    n_bins = data_hist.GetNbinsX()
    signal_hist = root_file.Get(f"emu/{hist_name}/bstautau_scaled/lin/bstautau")
    if not signal_hist:
        print(f"Error: Signal histogram '{hist_name}' not found")
        continue

    total_signal_integral = signal_hist.Integral()
    signal_efficiency = []
    bkg_efficiency = []

    cut_points = np.linspace(0, 1, 50)

    print("Processing ",hist_name)
    #for threshold in range(1, n_bins + 1):
    for cut in cut_points:
        cut_bin_signal = signal_hist.FindBin(cut)
        cut_bin_bkg = data_hist.FindBin(cut)

        signal_above_threshold = signal_hist.Integral(cut_bin_signal, n_bins)
        bkg_above_threshold = data_hist.Integral(cut_bin_bkg, n_bins)

        #print("For cut ",threshold, signal_above_threshold,bkg_above_threshold)
        
        signal_eff = signal_above_threshold / total_signal_integral
        bkg_eff = bkg_above_threshold / total_bkg_integral

        signal_efficiency.append(signal_eff)
        bkg_efficiency.append(bkg_eff)

    line, = plt.plot(bkg_efficiency, signal_efficiency, label=label+f' AUC = {auc(bkg_efficiency, signal_efficiency):.2f}')
    curve_color = line.get_color()

    cut_point = 0.6  # Example cut at 0.8
    cut_bin_signal = signal_hist.FindBin(cut_point)
    cut_bin_bkg = data_hist.FindBin(cut_point)
    
    # Calculate the integrals above the threshold (for signal and background)
    signal_above_threshold = signal_hist.Integral(cut_bin_signal, signal_hist.GetNbinsX())
    bkg_above_threshold = data_hist.Integral(cut_bin_bkg, data_hist.GetNbinsX())
    
    # Calculate efficiencies (normalized integrals)
    signal_eff = signal_above_threshold / total_signal_integral
    bkg_eff = bkg_above_threshold / total_bkg_integral
    
    # Plot the cut at 0.8
    plt.scatter(bkg_eff, signal_eff, color=curve_color, marker='x', s=100)



# Plot random classifier diagonal
plt.plot([0, 1], [0, 1], 'r--', label='Random Classifier')

plt.xlabel("Background Efficiency (False Positive Rate)")
plt.ylabel("Signal Efficiency (True Positive Rate)")
plt.title("ROC Curve: Signal vs Background Efficiency")
plt.legend(loc='lower right')
plt.grid(True)


plt.show()
plt.savefig("roc_curve_multiple_signals_partdef_aftertauhtaumucut.png")
