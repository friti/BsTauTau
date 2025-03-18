# Run NanoAODs adding our parT branch

## Setup environment
```
cmssw-el8
SCRAM_ARCH=el8_amd64_gcc11
cmsrel CMSSW_13_0_10
cd CMSSW_13_0_10/src/
cmsenv
git cms-init
git cms-addpkg PhysicsTools/NanoAOD
git cms-addpkg PhysicsTools/PatAlgos
git cms-addpkg RecoBTag

## changes with new parT branches
git cms-merge-topic -u friti:myParT

scram b -j8 
```

Now we need to copy the model in the right directory
```
cp <path_model>.onnx /afs/cern.ch/work/f/friti/BsTauTau/make_samples/nano_with_part_branch/CMSSW_13_0_10/model/.
cp <path_json>.json /afs/cern.ch/work/f/friti/BsTauTau/make_samples/nano_with_part_branch/CMSSW_13_0_10/model/.
```

## Send jobs on CRAB
Use the `multisubmitter_crab.py` and `submit_on_crab_template.py`.
Since these are many and big jobs, crab is better.

## Send jobs on CONDOR
Use the `MultiSubmit.py` and `production_2024.sh`.