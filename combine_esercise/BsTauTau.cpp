#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"

using namespace std;

int main() {
  //! [part1]
  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/shapes/";

  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  // Here we will just define two categories for an 13TeV analysis. Each entry in
  // the vector below specifies a bin name and corresponding bin_id.

  ch::Categories cats = {
      {1, "e_tauetaumu"},
      {2, "e_tauetauh"},
      {3, "e_tauhtauh"},
      {4, "mu_tauetaumu"},
      {5, "mu_tauetauh"},
      {6, "mu_tauhtauh"},
      {7, "ee_tauetaumu"},
      {8, "ee_tauetauh"},
      {9, "ee_tauhtauh"},
      {10, "emu_tauetaumu"},
      {11, "emu_tauetauh"},
      {12, "emu_tauhtauh"},
      {13, "mumu_tauetaumu"},
      {14, "mumu_tauetauh"},
      {15, "mumu_tauhtauh"}
    };

  vector<string> masses = {""};

  cb.AddObservations({"*"}, {"bs"}, {"13TeV"}, {"tautau"}, cats);

  vector<string> bkg_procs = {"tt_fullylep","tt_semilep","tt_had","ww","wz","zz","st_s","st_antit","st_tw","st_antitw","w","wext","dy"};
  cb.AddProcesses({"*"}, {"bs"}, {"13TeV"}, {"tautau"}, bkg_procs, cats, false);

  vector<string> sig_procs = {"bstautau"};
  cb.AddProcesses(masses, {"bs"}, {"13TeV"}, {"tautau"}, sig_procs, cats, true);


  //Some of the code for this is in a nested namespace, so
  // we'll make some using declarations first to simplify things a bit.
  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;


  //! [part5]

  //! [part6]
  cb.cp().signals().AddSyst(cb, "signal_norm", "lnN", SystMap<>::init(1.01));
  cb.cp().process(ch::JoinStr({sig_procs, {"tt_fullylep","tt_semilep","tt_had","ww","wz","zz","st_s","st_antit","st_tw","st_antitw","w","wext","dy"}})).AddSyst(cb, "lumi_2018", "lnN", SystMap<>::init(1.026));

  // 2% uncertainty per muon
  cb.cp().bin({"mu_tauetaumu","mu_tauetauh","mu_tauhtauh"}).process(ch::JoinStr({sig_procs, {"tt_fullylep","tt_semilep","tt_had","ww","wz","zz","st_s","st_antit","st_tw","st_antitw","w","wext","dy"}})).AddSyst(cb, "mu_eff", "lnN", SystMap<>::init(1.010));
  cb.cp().bin({"emu_tauetaumu","emu_tauetauh","emu_tauhtauh"}).process(ch::JoinStr({sig_procs, {"tt_fullylep","tt_semilep","tt_had","ww","wz","zz","st_s","st_antit","st_tw","st_antitw","w","wext","dy"}})).AddSyst(cb, "emu_eff", "lnN", SystMap<>::init(1.010));
  cb.cp().bin({"mumu_tauetaumu","mumu_tauetauh","mumu_tauhtauh"}).process(ch::JoinStr({sig_procs, {"tt_fullylep","tt_semilep","tt_had","ww","wz","zz","st_s","st_antit","st_tw","st_antitw","w","wext","dy"}})).AddSyst(cb, "mumu_eff", "lnN", SystMap<>::init(1.020));

  //cb.cp().bin({"stub4_bx1234"}).process({"Fake"}).AddSyst(cb, "CMS_EXO25010_normFake_stub4_bx1234", "rateParam", SystMap<>::init(1.0)); // example of rateParam
  //cb.cp().bin({"stub4_bx1234"}).process({"Fake"}).AddSyst(cb, "CMS_EXO25010_shape_stub4_bx1234", "shape", SystMap<>::init(1.00)); // example of shape uncertainty


  //! [part7]
  cb.cp().backgrounds().ExtractShapes(
      aux_shapes + "bstautau.root",
      "$BIN/$PROCESS",
      "$BIN/$PROCESS_$SYSTEMATIC");
  cb.cp().signals().ExtractShapes(
      aux_shapes + "bstautau.root", 
      "$BIN/$PROCESS$MASS",
      "$BIN/$PROCESS$MASS_$SYSTEMATIC");
  //! [part7]

  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the bs analyses
  ch::SetStandardBinNames(cb);
  //! [part8]

  //! [part9]
  // First we generate a set of bin names:
  set<string> bins = cb.bin_set();
  // This method will produce a set of unique bin names by considering all
  // Observation, Process and Systematic entries in the CombineHarvester
  // instance.

  // We create the output root file that will contain all the shapes.
  TFile output("bs_tautau.input.root", "RECREATE");

  // Finally we iterate through each bin,mass combination and write a
  // datacard.
  for (auto b : bins) {
    for (auto m : masses) {
      cout << ">> Writing datacard for bin: " << b << " and mass: " << m
           << "\n";
      // We need to filter on both the mass and the mass hypothesis,
      // where we must remember to include the "*" mass entry to get
      // all the data and backgrounds.
      cb.cp().bin({b}).mass({m, "*"}).WriteDatacard(
          b + "_" + m + ".txt", output);
    }
  }
  //! [part9]

}
