## Test Fragments locally for Run3

- CMSSW_15_0_2
- Save fragment in `Configuration/GenProduction/python/`
- cmsDriver command
```cmsDriver.py Configuration/GenProduction/python/fragment.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN --conditions 140X_mcRun3_2024_realistic_v26 --beamspot DBrealistic --step GEN --geometry DB:Extended --era Run3_2024 --python_filename GEN-RunIII2024Summer24wmLHEGS-00004_1_cfg.py --fileout file:GEN-RunIII2024Summer24wmLHEGS-00004.root --number 100 --number_out 100 --no_exec --mc --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(592)"```
- run the producer
- test it with the python script