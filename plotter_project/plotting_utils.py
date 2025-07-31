import ROOT
from datetime import datetime
from cmsstyle import CMS_lumi
from officialStyle import officialStyle

officialStyle(ROOT.gStyle, ROOT.TGaxis)


def create_canvas_with_pads():
    """
    Creates a ROOT canvas with two pads: a main pad and a ratio pad.
    
    Returns:
        tuple: A tuple containing the canvas, main pad, and ratio pad.
    """
    # Create the canvas
    c1 = ROOT.TCanvas('c1', '', 700, 700)
    c1.Draw()
    
    # Create the main pad
    c1.cd()
    main_pad = ROOT.TPad('main_pad', '', 0., 0.25, 1., 1.)
    main_pad.Draw()
    main_pad.SetTicks(True)
    main_pad.SetBottomMargin(0.)
    
    # Create the ratio pad
    c1.cd()
    ratio_pad = ROOT.TPad('ratio_pad', '', 0., 0., 1., 0.25)
    ratio_pad.Draw()
    ratio_pad.SetTopMargin(0.)
    ratio_pad.SetGridy()
    ratio_pad.SetBottomMargin(0.45)
    
    return c1, main_pad, ratio_pad

def initialize_histograms(histos, samples, ch):
    temp_hists = {}
    for k, v in histos[ch].items():
        temp_hists[k] = {}
        for kk, vv in samples[ch].items():
            branch_name = k

            temp_hists[k][f'{k}_{kk}'] = vv.Histo1D(v[0], branch_name, 'tot_weight')
    return temp_hists


def set_histogram_style(hist, x_title, y_title, fill_color, line_color):
    hist.GetXaxis().SetTitle(x_title)
    hist.GetYaxis().SetTitle(y_title)
    hist.SetFillColor(fill_color)
    hist.SetLineColor(line_color)

def create_legend(temp_hists, samples_for_legend, titles):
    leg = ROOT.TLegend(0.24,.67,.95,.90)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.035)
    leg.SetNColumns(3)
    k = list(temp_hists.keys())[0]
    for kk in samples_for_legend:
        leg.AddEntry(temp_hists[k]['%s_%s' %(k, kk)].GetValue(), titles[kk], 'EP' if 'data' in kk else ('L' if 'bstautau' in kk else 'F'))

    return leg

def compute_ratio_plot(temp_hists, ratio, stats, ratio_pad):
    ratio_pad.cd()
    ratio_stats = stats.Clone()
    ratio_stats.SetName(ratio.GetName()+'_ratiostats')
    ratio_stats.Divide(stats)
    ratio_stats.SetMaximum(1.19999) # avoid displaying 2, that overlaps with 0 in the main_pad
    ratio_stats.SetMinimum(0.79999) # and this is for symmetry
    ratio_stats.GetYaxis().SetTitle('obs/exp')
    ratio_stats.GetYaxis().SetTitleOffset(0.5)
    ratio_stats.GetYaxis().SetNdivisions(405)
    ratio_stats.GetXaxis().SetLabelSize(3.* ratio.GetXaxis().GetLabelSize())
    ratio_stats.GetYaxis().SetLabelSize(3.* ratio.GetYaxis().GetLabelSize())
    ratio_stats.GetXaxis().SetTitleSize(3.* ratio.GetXaxis().GetTitleSize())
    ratio_stats.GetYaxis().SetTitleSize(3.* ratio.GetYaxis().GetTitleSize())
    
    norm_stack = ROOT.THStack('norm_stack', '')
    
    for kk, vv in temp_hists.items():
        if 'data' in kk: continue
        hh = vv.Clone()
        hh.Divide(stats)



    line = ROOT.TLine(ratio.GetXaxis().GetXmin(), 1., ratio.GetXaxis().GetXmax(), 1.)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineWidth(1)
 
    return ratio_stats, norm_stack,line, ratio


def get_data_sample_name(ch):
    return 'data_sm' if ch in ['emu', 'mumu', 'mu'] else 'data_eg'


def get_samples_for_legend(samples, ch, data_smpl):
    return [str(k) for k in samples[ch] if 'data' not in k and 'ext' not in k] + [data_smpl]


def style_histograms(temp_hists, k, v, colours):
    maxima, maxima_data = [], []
    for key, ihist in temp_hists[k].items():
        sample_name = key.split(k + '_')[1]
        is_data = f'{k}_data' in key
        color = ROOT.kWhite if is_data else colours.get(sample_name, ROOT.kBlack)
        set_histogram_style(ihist, v[1], 'events', color, color)
        if not is_data:
            maxima.append(ihist.GetMaximum())
        else:
            maxima_data.append(ihist.GetMaximum())
    return maxima, maxima_data


def create_histogram_stacks(temp_hists, k, maxima_data, maxima):
    """Crates histogram stacks for the given channel, both data and MC."""
    ths1 = ROOT.THStack('stack', '')
    data_ths = ROOT.THStack('data_stack', '')

    max_data = max(maxima_data) if maxima_data else 1
    max_total = 1.6 * max(max(maxima), max_data) if maxima else 1.6 * max_data

    for key, ihist in temp_hists[k].items():
        if f'{k}_data' in key:
            continue
        ihist.SetMaximum(1.6 * max_data)
        ihist.Draw('hist same')
        if "bstautau" not in key:
            ths1.Add(ihist.GetValue())

    ths1.SetMaximum(max(max_total,temp_hists[k][f'{k}_bstautau'].GetValue().GetMaximum()))
    ths1.SetMinimum(0.0001)

    for key, ihist in temp_hists[k].items():
        if f'{k}_data' not in key:
            continue
        ihist.Draw('hist same')
        ihist.SetLineWidth(0)
        data_ths.Add(ihist.GetValue())

    return ths1, data_ths


def draw_stat(ths1):

    stats = ths1.GetStack().Last().Clone()
    stats.SetLineColor(0)
    stats.SetFillColor(ROOT.kGray + 1)
    stats.SetFillStyle(3344)
    stats.SetMarkerSize(0)
    stats.Draw('E2 SAME')

    return stats


def style_and_draw_bstautau(temp_hists, k, data_ths, colours):
    hist = temp_hists[k][f'{k}_bstautau']
    hist.SetFillColor(0)
    hist.SetLineColor(colours['bstautau'])
    hist.SetMarkerColor(colours['bstautau'])
    print("BsTauTau histogram integral:", hist.Integral())
    scale_factor = data_ths.GetStack().Last().Integral() / hist.Integral()
    hist.Scale(scale_factor)
    hist.Draw("hist same")
    hist.Draw("EP same")


def process_histograms(histos, temp_hists, samples, ch, colours, label, titles, main_pad, ratio_pad, c1):
    for k, v in histos[ch].items():
        c1.cd()
        data_smpl = get_data_sample_name(ch)
        samples_for_legend = get_samples_for_legend(samples, ch, data_smpl)
        leg = create_legend(temp_hists, samples_for_legend, titles)


        ## plotting main pad
        main_pad.cd()
        main_pad.SetLogy(False)

        maxima, maxima_data = style_histograms(temp_hists, k, v, colours)

        ths1, data_ths = create_histogram_stacks(temp_hists, k, maxima_data, maxima)

        ths1.Draw('hist')
        ths1.GetXaxis().SetTitle(v[1])
        ths1.GetYaxis().SetTitle('events')

        stats = draw_stat(ths1)

        data_ths.GetStack().Last().SetLineColor(ROOT.kBlack)
        data_ths.GetStack().Last().Draw('EP same')

        leg.AddEntry(stats, 'stat. unc.', 'F')
        leg.Draw('same')

        style_and_draw_bstautau(temp_hists, k, data_ths, colours)

        CMS_lumi(main_pad, 4, 0, cmsText='CMS', extraText=' Preliminary', lumi_13TeV='L = 59.7 fb^{-1}')
        main_pad.cd()

        ratio = data_ths.GetStack().Last().Clone()
        ratio.Divide(stats)

        ratio_stats, norm_stack,line, ratio= compute_ratio_plot(temp_hists[k], ratio, stats, ratio_pad)
        ratio_pad.cd()

        norm_stack.Draw('hist same')
        ratio_stats.Draw('E2')
        norm_stack.Draw('hist same')
        ratio_stats.Draw('E2 same')
        line.Draw('same')
        ratio.Draw('EP same')


        c1.Modified()
        c1.Update()

        c1.SaveAs(f'plots/{label}/{ch}/pdf/{k}.pdf')
        c1.SaveAs(f'plots/{label}/{ch}/png/{k}.png')

