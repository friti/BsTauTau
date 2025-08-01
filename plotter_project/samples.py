import ROOT

eras_2018 = ['A','B','C','D']

data_samples_names = {
    'mu':['data_sm'],
    'e':['data_eg'],
    'emu':['data_sm','data_eg','data_meg'],
    'mumu':['data_sm','data_dm'],
    'ee':['data_eg']}

mc_samples_names = [
    'tt_fullylep',
    'tt_semilep',
    'tt_had',
    'ww',
    'wz',
    'zz',
    'st_s',
    #'st_t',
    'st_antit',
    'st_tw',
    'st_antitw',
    'w',
    'wext',
    'dy',
    'bstautau',
    #'dyext'
]

files_names = dict()
files_names['data_sm'] = 'SingleMuon'
files_names['data_dm'] = 'DoubleMuon'
files_names['data_eg'] = 'EGamma'
files_names['data_meg'] = 'MuonEG'
files_names['tt_fullylep'] = 'TTTo2L2Nu'
files_names['tt_semilep'] = 'TTToSemileptonic'
files_names['tt_had'] = 'TTToHadronic'
files_names['w'] = 'W'
files_names['wext'] = 'W_ext'
files_names['dy'] = 'DY'
files_names['dyext'] = 'DY_ext'
files_names['ww'] = 'WW'
files_names['wz'] = 'WZ'
files_names['zz'] = 'ZZ'
files_names['st_s'] = 'ST_s'
files_names['st_t'] = 'ST_t_top'
files_names['st_antit'] = 'ST_t_antitop'
files_names['st_tw'] = 'ST_tW'
files_names['st_antitw'] = 'ST_tW_antitop'
files_names['bstautau'] = 'ttbarToBsToTauTau'

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/XsdbTutorialSep#TTbar

luminosity_2018 = 59.7 # in fb-1

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
cross_sections = {
    "tt_semilep": 366.29,      # in pb
    "tt_fullylep": 88.51,      # in pb
    "tt_had": 378.93,          # in pb
    "w": 61526,               # in pb
    "wext": 61526,               # in pb
    "dy": 6077,               # in pb
    "dyext": 6077,               # in pb
    "wz": 47.13,               # in pb
    "ww": 115.0,               # in pb  # CHECKKK
    "zz": 16.523,              # in pb
    "st_s": 3.36,              # in pb
    "st_t": 44.33,             # in pb  # CHECKKK
    "st_antit": 26.38,         # in pb  # CHECKKK
    "st_tw": 35.85,            # in pb  # CHECKKK
    "st_antitw": 35.85,        # in pb  # CHECKKK
    "bstautau": 830 * 2 * 0.1 * 6.8 * 0.001 *10,        ## 10 times LHCb
}


## titles
titles = dict()
titles['data_sm'] = 'data'
titles['data_eg'] = 'data'
titles['tt_fullylep'] = 't#bar{t} lep'
titles['tt_semilep'] = 't#bar{t} semi-lep'
titles['tt_had'] = 't#bar{t} had'
titles['ww'] = 'WW'
titles['w'] = 'W+jets'
titles['dy'] = 'DY'
titles['wz'] = 'WZ'
titles['zz'] = 'ZZ'
titles['st_s'] = 'ST_s'
titles['st_t'] = 'ST_t_top'
titles['st_antit'] = 'ST_t_antitop'
titles['st_tw'] = 'ST_tW_top'
titles['st_antitw'] = 'ST_tW_antitop'
titles['bstautau'] = 'B_{s}#rightarrow #tau #tau'


## colours
colours = dict()
colours['data_sm' ] = ROOT.kBlack
colours['data_eg' ] = ROOT.kBlack
colours['data_meg' ] = ROOT.kBlack
colours['tt_fullylep' ] = ROOT.TColor.GetColor("#92dadd")
colours['tt_semilep'  ] = ROOT.TColor.GetColor("#bd1f01")
colours['tt_had' ] = ROOT.TColor.GetColor("#b9ac70")
colours['ww' ] = ROOT.TColor.GetColor("#e76300")
colours['wz'  ] = ROOT.TColor.GetColor("#717581")
colours['zz'] = ROOT.TColor.GetColor("#832db6")
colours['st_s'] = ROOT.TColor.GetColor("#94a4a2")
colours['st_t'] = ROOT.TColor.GetColor("#a96b59")
colours['st_antit'] = ROOT.TColor.GetColor("#ffa90e")
colours['st_tw'] = ROOT.TColor.GetColor("#832db6")
colours['st_antitw'] = ROOT.TColor.GetColor("#94a4a2")
colours['w'] = ROOT.TColor.GetColor("#92dadd")
colours['wext'] = ROOT.TColor.GetColor("#92dadd")
colours['dy'] = ROOT.TColor.GetColor("#e76300")
colours['dyext'] = ROOT.TColor.GetColor("#e76300")
colours['bstautau'] = ROOT.TColor.GetColor("#ffa90e")
