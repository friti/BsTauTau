# How to run the combine fit

## Install Combine and Combine Harvester
```
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv
git -c advice.detachedHead=false clone --depth 1 --branch v10.2.1 https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
scramv1 b clean; scramv1 b

##CombineHarvester
cd ../../
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
cd CombineHarvester
git checkout v3.0.0
scram b
```

## Install BsTauTau command

```
cp BsTauTau.cpp CombineHarvester/CombineTools/bin/.
```
Add `<bin file="BsTauTau.cpp" name="BsTauTau"></bin>` to `CombineHarvester/CombineTools/bin/BuildFile.xml` file

```
scram b -j 8
cmsenv
```

## Prepare histograms and run the fit
```
python3 prepare_histograms.py 12Aug2025_11h48m43s #folder name output of the plotter script
```
This should copy the datacard into `auxiliaries/shapes/bstautau.root`, if not, copyt it there.
```
BsTauTau # should dave .txt datacards into datacards fodler
combine_and_fit.sh
```
