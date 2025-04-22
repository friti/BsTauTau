# Run NanoAODs adding our parT branch

## Setup environment
`ssh lxplus8` or access the singularity with `cmssw-el8`
```
git clone --recursive git@github.com:friti/BsTauTau.git
cd BsTauTau/make_samples/nano_with_part_branch

SCRAM_ARCH=el8_amd64_gcc11
cmsrel CMSSW_13_0_10
cd CMSSW_13_0_10/src/
cmsenv
git cms-init
git cms-addpkg PhysicsTools/NanoAOD
git cms-addpkg PhysicsTools/PatAlgos
git cms-addpkg RecoBTag

## changes with new parT branches
git cms-merge-topic -u friti:myPart

scram b -j8

cd ../..
```

Now we need to copy the model in the right directory
```
mkdir CMSSW_13_0_10/src/data
cp model_6026222.onnx CMSSW_13_0_10/src/data/.
cp preprocess.json CMSSW_13_0_10/src/data/.
```
To test it locally
```
cmsRun Run18_106X_step5Nano_13010_cfg.py
```

## Send jobs on CRAB (RECOMMENDED)
Use the `multisubmitter_crab_data.py` and `multisubmitter_crab_mc.py` `submit_on_crab_template.py`.
Since these are many and big jobs, crab is better.

## Send jobs on CONDOR
Use the `MultiSubmit.py` and `production_2024.sh`.
