# histos definition
import ROOT

histos = dict()

## common branches
histos_general = dict()
'''
histos_general['nj'] = (ROOT.RDF.TH1DModel('nj'     , '',20,     0,     20), 'N jets'         , 1)
histos_general['j_pt'] = (ROOT.RDF.TH1DModel('j_pt', '', 50, 0, 200), 'Jet pT', 1)
histos_general['j_eta'] = (ROOT.RDF.TH1DModel('j_eta', '', 50, -2.5, 2.5), 'Jet eta', 1)
histos_general['j_phi'] = (ROOT.RDF.TH1DModel('j_phi', '', 50, -3.14, 3.14), 'Jet phi', 1)
histos_general['j_m'] = (ROOT.RDF.TH1DModel('j_m', '', 50, 0, 200), 'Jet mass', 1)
histos_general['j_puid'] = (ROOT.RDF.TH1DModel('j_puid', '', 5, 0, 5), 'Jet PUID', 1)
histos_general['j_jetid'] = (ROOT.RDF.TH1DModel('j_jetid', '', 5, 0, 5), 'Jet ID', 1)
histos_general['j_deepflavB'] = (ROOT.RDF.TH1DModel('j_deepflavB', '', 50, 0, 1), 'Jet DeepFlavB', 1)
histos_general['j_hadronFlavour'] = (ROOT.RDF.TH1DModel('j_hadronFlavour', '', 10, -5, 5), 'Jet Hadron Flavour', 1)
'''

histos_general['selected_njets'] = (ROOT.RDF.TH1DModel('selected_njets', '', 10, 0, 10), 'N jets (pT > min_jet_pt)', 1)
histos_general['selected_jets_pt'] = (ROOT.RDF.TH1DModel('selected_jets_pt', '', 50, 0, 200), 'Jet pT (pT > min_jet_pt)', 1)
histos_general['selected_jets_eta'] = (ROOT.RDF.TH1DModel('selected_jets_eta', '', 50, -2.5, 2.5), 'Jet eta (pT > min_jet_pt)', 1)
histos_general['selected_jets_phi'] = (ROOT.RDF.TH1DModel('selected_jets_phi', '', 50, -3.14, 3.14), 'Jet phi (pT > min_jet_pt)', 1)
histos_general['selected_jets_mass'] = (ROOT.RDF.TH1DModel('selected_jets_mass', '', 50, 0, 50), 'Jet mass (pT > min_jet_pt)', 1)
histos_general['selected_jets_puid'] = (ROOT.RDF.TH1DModel('selected_jets_puid', '', 5, 0, 5), 'Jet PUID (pT > min_jet_pt)', 1)
histos_general['selected_jets_jetid'] = (ROOT.RDF.TH1DModel('selected_jets_jetid', '', 5, 0, 5), 'Jet ID (pT > min_jet_pt)', 1)
histos_general['selected_jets_deepflavB'] = (ROOT.RDF.TH1DModel('selected_jets_deepflavB', '', 50, 0, 1), 'Jet DeepFlavB (pT > min_jet_pt)', 1)
histos_general['selected_jets_ht'] = (ROOT.RDF.TH1DModel('selected_jets_ht', '', 30, 20, 500), 'HT', 1)
#histos_general['selected_jets_hadronFlavour'] = (ROOT.RDF.TH1DModel('selected_jets_hadronFlavour', '', 10, -5, 5), 'Jet Hadron Flavour (pT > min_jet_pt)', 1)


histos_general['MET_phi'] = (ROOT.RDF.TH1DModel('MET_phi', '', 20, -3.14, 3.14), 'MET phi', 1)
histos_general['MET_pt'] = (ROOT.RDF.TH1DModel('MET_pt', '', 30, 0, 200), 'MET pt', 1)


histos['mu'] = dict()
histos['e'] = dict()
histos['emu'] = dict()
histos['mumu'] = dict()
histos['ee'] = dict()

##common branches for electrons
histos_general_e = dict()
histos_general_e['e1_pt'] = (ROOT.RDF.TH1DModel('e1_pt', '', 20, 0, 200), 'Electron 1 pt', 1)
histos_general_e['e1_eta'] = (ROOT.RDF.TH1DModel('e1_eta', '', 20, -2.5, 2.5), 'Electron 1 eta', 1)
histos_general_e['e1_phi'] = (ROOT.RDF.TH1DModel('e1_phi', '', 20, -3.14, 3.14), 'Electron 1 phi', 1)
histos_general_e['e1_dxy'] = (ROOT.RDF.TH1DModel('e1_dxy', '', 20, 0, 0.05), 'Electron 1 dxy', 1)
histos_general_e['e1_dz'] = (ROOT.RDF.TH1DModel('e1_dz', '', 20, 0, 0.1), 'Electron 1 dz', 1)
histos_general_e['e1_charge'] = (ROOT.RDF.TH1DModel('e1_charge', '',3, -1.5, 1.5), 'Electron 1 charge', 1)

## common branches for muons
histos_general_mu = dict()
histos_general_mu['mu1_pt'] = (ROOT.RDF.TH1DModel('mu1_pt', '', 50, 0, 200), 'Muon 1 pT', 1)
histos_general_mu['mu1_eta'] = (ROOT.RDF.TH1DModel('mu1_eta', '', 50, -2.5, 2.5), 'Muon 1 eta', 1)
histos_general_mu['mu1_phi'] = (ROOT.RDF.TH1DModel('mu1_phi', '', 50, -3.14, 3.14), 'Muon 1 phi', 1)
histos_general_mu['mu1_dxy'] = (ROOT.RDF.TH1DModel('mu1_dxy', '', 50, -0.5, 0.5), 'Muon 1 dxy', 1)
histos_general_mu['mu1_dz'] = (ROOT.RDF.TH1DModel('mu1_dz', '', 50, -0.5, 0.5), 'Muon 1 dz', 1)
histos_general_mu['mu1_charge'] = (ROOT.RDF.TH1DModel('mu1_charge', '', 3, -1.5, 1.5), 'Muon 1 charge', 1)

                                                  

histos['mu'].update(histos_general)
histos['e'].update(histos_general)
histos['emu'].update(histos_general)
histos['mumu'].update(histos_general)
histos['ee'].update(histos_general)


histos['mu'].update(histos_general_mu)
histos['e'].update(histos_general_e)
histos['emu'].update(histos_general_e)
histos['emu'].update(histos_general_mu)
histos['mumu'].update(histos_general_mu)
histos['ee'].update(histos_general_e)

## add second lepton

histos['ee']['e2_pt'] = (ROOT.RDF.TH1DModel('e2_pt', '', 20, 0, 500), 'Electron 1 pt', 1)
histos['ee']['e2_eta'] = (ROOT.RDF.TH1DModel('e2_eta', '', 20, -2.5, 2.5), 'Electron 1 eta', 1)
histos['ee']['e2_phi'] = (ROOT.RDF.TH1DModel('e2_phi', '', 20, -3.14, 3.14), 'Electron 1 phi', 1)
histos['ee']['e2_dxy'] = (ROOT.RDF.TH1DModel('e2_dxy', '', 20, 0, 1), 'Electron 1 dxy', 1)
histos['ee']['e2_dz'] = (ROOT.RDF.TH1DModel('e2_dz', '', 20, 0, 1), 'Electron 1 dz', 1)
histos['ee']['e2_charge'] = (ROOT.RDF.TH1DModel('e2_charge', '',3, -1.5, 1.5), 'Electron 1 charge', 1)

histos['mumu']['mu2_pt'] = (ROOT.RDF.TH1DModel('mu2_pt', '', 50, 0, 200), 'Muon 1 pT', 1)
histos['mumu']['mu2_eta'] = (ROOT.RDF.TH1DModel('mu2_eta', '', 50, -2.5, 2.5), 'Muon 1 eta', 1)
histos['mumu']['mu2_phi'] = (ROOT.RDF.TH1DModel('mu2_phi', '', 50, -3.14, 3.14), 'Muon 1 phi', 1)
histos['mumu']['mu2_dxy'] = (ROOT.RDF.TH1DModel('mu2_dxy', '', 50, -0.5, 0.5), 'Muon 1 dxy', 1)
histos['mumu']['mu2_dz'] = (ROOT.RDF.TH1DModel('mu2_dz', '', 50, -0.5, 0.5), 'Muon 1 dz', 1)
histos['mumu']['mu2_charge'] = (ROOT.RDF.TH1DModel('mu2_charge', '', 3, -1.5, 1.5), 'Muon 1 charge', 1)
histos['mumu']['inv_mass'] = (ROOT.RDF.TH1DModel('inv_mass', '', 40, 40, 200), 'inv mass', 1)
#histos['mumu']['inv_mass'] = (ROOT.RDF.TH1DModel('inv_mass', '', 40, 0, 80), 'inv mass', 1)

histos['emu']['inv_mass'] = (ROOT.RDF.TH1DModel('inv_mass', '', 50, 10, 200), 'inv mass', 1)
histos['ee']['inv_mass'] = (ROOT.RDF.TH1DModel('inv_mass', '', 50, 10, 200), 'inv mass', 1)

