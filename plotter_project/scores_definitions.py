def define_combined_scores(samples, ch, k, tau_scores, parT_scores, bkg_scores):
    tau_sum_expr = ' + '.join([f"btagged_loose_jets_pt_above_20_for_histo_{s}" for s in tau_scores])
    total_sum_expr = ' + '.join([f"btagged_loose_jets_pt_above_20_for_histo_{s}" for s in parT_scores])
    bkg_sum_expr = ' + '.join([f"btagged_loose_jets_pt_above_20_for_histo_{s}" for s in bkg_scores])

    samples[ch][k] = samples[ch][k].Define("btagged_loose_jets_pt_above_20_for_histo_sig_sum", tau_sum_expr)
    samples[ch][k] = samples[ch][k].Define("btagged_loose_jets_pt_above_20_for_histo_total_sum", total_sum_expr)
    samples[ch][k] = samples[ch][k].Define("btagged_loose_jets_pt_above_20_for_histo_sig_frac", 
                                           "btagged_loose_jets_pt_above_20_for_histo_sig_sum / btagged_loose_jets_pt_above_20_for_histo_total_sum")

    samples[ch][k] = samples[ch][k].Define("btagged_loose_jets_pt_above_20_for_histo_bkg_sum", bkg_sum_expr)
    return samples


def define_histos_for_combined_scores(samples, histos, ch, k, bkg_scores):
    ## Partial scores
    for bkg in bkg_scores:
        samples[ch][k] = samples[ch][k].Define(
            f"part_sigsum_over_{bkg}",
            f"(btagged_loose_jets_pt_above_20_for_histo_sig_sum) / (btagged_loose_jets_pt_above_20_for_histo_sig_sum + btagged_loose_jets_pt_above_20_for_histo_{bkg})"
        )
        histos[ch][f'part_sigsum_over_{bkg}'] = (
            ROOT.RDF.TH1DModel(f'part_sigsum_over_{bkg}', '', 30, 0, 1),
            f"sig over {bkg} on b-jets with pt>20 GeV",
            1
        )

    histos[ch][f'histo_btagged_l_jets_20gev_sig_frac'] = (ROOT.RDF.TH1DModel(f'histo_btagged_l_jets_20gev_sig_frac', '', 20, 0, 1),f"sig frac", 1 )

    return samples, histos

def create_histograms_for_scores(samples, histos, ch, k, tau_scores, bkg_scores, bstautau_conditions):
    for tau in tau_scores:
        samples[ch][k] = samples[ch][k].Define(
            f"histo_btagged_l_jets_20gev_{tau}_frac",
            f"histo_btagged_l_jets_20gev_{tau} / (histo_btagged_l_jets_20gev_{tau} + histo_btagged_l_jets_20gev_bkg_sum)"
        )
        histo_name = f"histo_btagged_l_jets_20gev_{tau}_frac"

        if k == "bstautau":
            mask = bstautau_conditions.get(tau, None)
            if mask:
                expr = f"{histo_name}[{mask}]"
            else:
                expr = histo_name
        else:
            expr = histo_name

        samples[ch][k] = samples[ch][k].Define(
            f"histo_btagged_l_jets_20gev_{tau}_frac_masked", expr
        )

        histos[ch][f"histo_btagged_l_jets_20gev_{tau}_frac_masked"] = (
            ROOT.RDF.TH1DModel(f"histo_btagged_l_jets_20gev_{tau}_frac_masked", "", 20, 0, 1),
            expr,
            1
        )
    return samples, histos



def save_histograms(samples, histos, ch, k, tau_scores, parT_scores, bkg_scores, bstautau_conditions):
    samples = define_combined_scores(samples, ch, k, tau_scores, parT_scores, bkg_scores)
    samples, histos = create_histograms_for_scores(samples, histos, ch, k, tau_scores, bkg_scores, bstautau_conditions)
    samples, histos = create_combined_histograms(samples, histos, ch, k, bkg_scores)
    return samples, histos