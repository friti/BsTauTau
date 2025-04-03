############### Code to simultaneously submit 
############### Original Author: George Karathanasis, CERN
#### usage: configure necessairy options  & run with "python multisubmit_v4.py" 


import os, subprocess
import datetime
import random
import math

######################### configuration ###############################

input_datasets={
  #"w":"/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  #"wext":"/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/MINIAODSIM",
  #"dy":"/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM",
  #"dyext":"/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1_ext1-v1/MINIAODSIM",
  "tt_semilep":"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM",
  #"tt_fullylep":"/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  #"tt_had":"/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  #"ww":"/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  #"wz":"/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  #"zz":"/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM",
  #"st_s":"/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  #"st_antit":"/ST_t-channel_antitop_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  #"st_t":"ST_t-channel_top_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  #"st_antitw":"/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  #"st_tw":"/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  #"bstautau":"/ttbarToBsToTauTau_BsFilter_TauTauFilter_TuneCP5_13TeV-pythia8-evtgen/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"
}


#samples_path = '/store/cmst3/group/bpark/friti/bstautau/nano_with_part_v1/'
Run="Run18" 
global_tag = '106X_upgrade2018_realistic_v16_L1v1'

step5_producer = "Run18_106X_step5Nano_13010_cfg.py"
conditions="106X" #133X or 140X
RAM="2500"
tag="Run2018"
slc='el8'

units_per_job = 1

###############################################################################
###############################################################################

date=datetime.date.today().strftime('%Y%b%d')

      
if __name__ == '__main__':

  os.makedirs("sent_to_crab", exist_ok=True)

  template = "submit_on_crab_template.py"


  # Path for the check script
  check_script = "check_crab_status.sh"
  with open(check_script, "w") as script:
    script.write("#!/bin/bash\n\n")


  print(f"Shell script to check CRAB status saved at: {check_script}")
  print("Run it using: ./modified_files/check_crab_status.sh")

  for dataset in input_datasets.keys():
      print('run dataset',dataset)

      output = "sent_to_crab/"+dataset+"_crab_cfg.py"
      
      with open(template, "r") as infile, open(output, "w") as outfile:
        for line in infile:
          newline = line
          if "TEMPLATE_DATASET" in line:
            newline = newline.replace("TEMPLATE_DATASET", dataset)  
          if "TEMPLATE_CONDITIONS" in line:
            newline = newline.replace("TEMPLATE_CONDITIONS", conditions)
          if "TEMPLATE_PRODUCER" in line:
            newline = newline.replace("TEMPLATE_PRODUCER", step5_producer)
          if "TEMPLATE_INPUT" in line:
            newline = newline.replace("TEMPLATE_INPUT", input_datasets[dataset])
          if "TEMPLATE_UNITSPERJOB" in line:
            newline = newline.replace("TEMPLATE_UNITSPERJOB", str(units_per_job))
          if "TEMPLATE_DATE" in line:
            newline = newline.replace("TEMPLATE_DATE", str(date))
          if "TEMPLATE_GT" in line:
            newline = newline.replace("TEMPLATE_GT", global_tag)
          
          outfile.write(newline)


      try:
        subprocess.run(["python3", output], check=True)
        print(f"Successfully executed {output}")
      except subprocess.CalledProcessError as e:
        print(f"Error executing {output}: {e}")
      
      
      # Write the shell script to check CRAB statuses
      with open(check_script, "a") as script:
        script.write(f"crab status -d crab_jobs/{dataset}_{date}/crab_{dataset} \n")  # Add status check for each job

  # Make the script executable
  os.chmod(check_script, 0o755)

   

