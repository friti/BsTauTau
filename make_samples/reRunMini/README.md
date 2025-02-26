# Re run miniaod samples

```
cmssw-el7
cmsrel CMSSW_10_6_20
cd CMSSW_10_6_20/src

cmsenv

git cms-init

# Add necessary packages
git cms-addpkg PhysicsTools/NanoAOD
git cms-addpkg PhysicsTools/PatAlgos


git cms-merge-topic -u friti:RelaxedCutsCMSSW10620

scram b -j8 

```