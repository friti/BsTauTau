############### Code to simultaneously submit 
############### Original Author: George Karathanasis, CERN
#### usage: configure necessairy options  & run with "python multisubmit_v4.py" 

import os, subprocess
import datetime
import random
import math

######################### configuration ###############################

input_datasets={
  "w":"/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  "wext":"/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/MINIAODSIM",
  "dy":"/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM",
  "dyext":"/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1_ext1-v1/MINIAODSIM",
  "tt_semilep":"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM",
  "tt_fullylep":"/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  "tt_had":"/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  "ww":"/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  "wz":"/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  "zz":"/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM",
  "st_s":"/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  "st_antit":"/ST_t-channel_antitop_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  "st_t":"ST_t-channel_top_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  "st_antitw":"/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  "st_tw":"/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
  "bstautau":"/ttbarToBsToTauTau_BsFilter_TauTauFilter_TuneCP5_13TeV-pythia8-evtgen/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"
}

njobs = -1
nevts_per_job = 500000

Production="production_2024.sh"

date=datetime.date.today().strftime('%Y%b%d')

samples_path = f'/store/cmst3/group/bpark/friti/bstautau/nano_with_part_{date}/'
Run="Run18" 

Conditions="106X" #133X or 140X
flavor="nextweek"
RAM="2500"
tag="Run2018"
slc='el8'

###############################################################################
###############################################################################

cmsswnano = 'CMSSW_13_0_10/src'

def check_for_folder(path):
  if os.path.isdir(path):
    print (path+" exists")
    os.system('rm -I -r '+path)

import os
import subprocess

import os
import subprocess


def get_total_events(dataset_path):
    """Query DAS to get the total number of events in a dataset."""
    query = f"dasgoclient -query='summary dataset={dataset_path}'"
    try:
        result = subprocess.run(query, shell=True, capture_output=True, text=True, check=True)
        for line in result.stdout.split("\n"):
            if "nevents" in line:
              return int(line.split('"nevents":')[1].split(",")[0].strip())
    except subprocess.CalledProcessError as e:
        print(f"Error querying DAS for {dataset}: {e}")
    return 0

'''
def fetch_dataset_files(dataset_name, dataset_path, output_dir="bkg_files_lists"):
    """
    Fetches a list of dataset files using dasgoclient and writes them to a Python file.
    If the file already exists, it skips querying DAS.

    Parameters:
        dataset_name (str): The key name for the dataset (e.g., "dy", "qcd", "ttbar").
        dataset_path (str): The dataset path in DAS.
        output_dir (str): Directory to save the output file (default: "bkg_files_lists").
    """

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Define output Python file path
    output_file = os.path.join(output_dir, f"{dataset_name}.py")

    # If the file already exists, skip querying DAS
    if os.path.exists(output_file):
        print(f"File {output_file} already exists. Skipping DAS query.")
        return

    print(f"Querying DAS for dataset: {dataset_path}...")

    # DAS query to get file list
    das_query = f'dasgoclient -query="file dataset={dataset_path} status=VALID | grep file.name"'

    try:
        # Execute the command and capture output
        result = subprocess.run(das_query, shell=True, check=True, capture_output=True, text=True)

        # Parse the file list
        file_list = result.stdout.strip().split("\n")

        # Check if files were found
        if not file_list or file_list == [""]:
            print(f"Warning: No files found for {dataset_path}. Skipping.")
            return

        # Format file paths with XRootD prefix
        formatted_files = [f'"root://cms-xrd-global.cern.ch/{file}"' for file in file_list]

        # Write to Python file
        with open(output_file, "w") as f:
            f.write("files = [\n")
            f.write(",\n".join(formatted_files))
            f.write("\n]\n")

        print(f"Saved {len(file_list)} files to {output_file}.")

    except subprocess.CalledProcessError as e:
        print(f"Error querying DAS for {dataset_path}: {e}")

'''
import os
import subprocess

import os
import subprocess

import os
import subprocess

def fetch_dataset_files(dataset_name, dataset_path, output_dir="bkg_files_lists"):
    """
    Fetches a list of dataset files from valid T1/T2 sites using dasgoclient.
    Ensures all valid files are written to a single Python file, avoiding duplicates.

    Parameters:
        dataset_name (str): The key name for the dataset (e.g., "dy", "qcd", "ttbar").
        dataset_path (str): The dataset path in DAS.
        output_dir (str): Directory to save the output file (default: "bkg_files_lists").
    """

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{dataset_name}.py")

    # List of allowed sites (excluding T0)
    sites = [
        "T1_DE_KIT_Disk", "T1_ES_PIC_Disk", "T1_FR_CCIN2P3_Disk", "T1_IT_CNAF_Disk", "T1_UK_RAL_Disk", "T1_US_FNAL_Disk",
        "T2_AT_Vienna", "T2_BE_IIHE", "T2_BE_UCL", "T2_CH_CERN", "T2_CH_CSCS", "T2_DE_DESY", "T2_DE_RWTH", "T2_ES_CIEMAT", 
        "T2_ES_IFCA", "T2_FR_GRIF", "T2_FR_IPHC", "T2_IT_Bari", "T2_IT_Legnaro", "T2_IT_Pisa", "T2_IT_Rome", "T2_UK_London_Brunel", 
        "T2_UK_London_IC", "T2_UK_SGrid_RALPP", "T2_US_Caltech", "T2_US_Florida", "T2_US_MIT","T2_US_Purdue", 
        "T2_US_UCSD", "T2_US_Vanderbilt", "T2_US_Wisconsin"
    ] # T2_US_Nebraska 

    #sites = ["T1_US_FNAL_Disk",""]
    # Load existing files if the output file already exists
    valid_files = set()

    # Loop through each site and collect unique files
    for site in sites:
        print(f"Checking dataset at {site}...")
        das_query = f'dasgoclient -query="file dataset={dataset_path} site={site}"'

        try:
            result = subprocess.run(das_query, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                new_files = set()
                
                for line in result.stdout.split("\n"):
                  file_path = line.strip()
                  full_path = f'"root://cms-xrd-global.cern.ch/{file_path}"'  # This is what we store

                  if file_path and full_path not in valid_files:  # Ensure consistent format for checking
                    new_files.add(full_path)  # Add only unique files                    file_path = line.strip()
                  elif file_path and full_path in valid_files:
                    print("This file is in 2 sites!!! ",file_path, site)
                if new_files:
                    valid_files.update(new_files)  # Add only unique files
                    print(new_files)
                    print(f" -> Added {len(new_files)} new files from {site}.")
                else:
                    print(f" -> No new files found at {site}.")
            else:
                print(f"Warning: No valid files found for {dataset_path} at {site}.")
        except Exception as e:
            print(f"Error querying DAS for {dataset_path} at {site}: {e}")

    # If no new files, do not overwrite
    if len(valid_files) == 0:
        print(f"No files found. Skipping writing to {output_file}.")
        return

    # Write the updated list of files to the Python file
    with open(output_file, "w") as f:
        f.write("files = [\n")
        f.write(",\n".join(sorted(valid_files)))  # Sort for consistency
        f.write("\n]\n")

    print(f"Saved {len(valid_files)} unique files to {output_file}.")
    
def load_dataset_files(dataset_name, input_dir="bkg_files_lists"):
    """
    Reads the dataset file list from a .txt file and adds the XRootD redirector before each path.

    Parameters:
        dataset_name (str): The key name for the dataset (e.g., "dy", "qcd", "ttbar").
        input_dir (str): Directory where the .txt files are stored (default: "qcd_files_lists").

    Returns:
        list: A list of file paths with the XRootD redirector.
    """

    # Construct file path
    file_path = os.path.join(input_dir, f"{dataset_name}.txt")

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found!")
        return []

    # Read file paths and add the redirector
    redirector = "root://cms-xrd-global.cern.ch/"
    with open(file_path, "r") as f:
        files = [redirector + line.strip() for line in f if line.strip()]

    print(f"Loaded {len(files)} files for {dataset_name}.")
    return files
  
  
def load_grid():
   os.system("rm grid_val.txt")
   txt='#!/usr/bin/env bash\n'
   txt='PWD=`pwd`\n'
   txt+="export X509_USER_PROXY=${PWD}/proxy\n"
   txt+="voms-proxy-init --voms cms\n"
   txt+="grid-proxy-info >> grid_val.txt\n"
   with open('act_proxy.sh','w') as fl:
      fl.write(txt)
   os.system('. ./act_proxy.sh')
   kill = False
   with open('grid_val.txt','r') as fl2:
     lines = fl2.readlines()
     for line in lines:
       if "ERROR" in line.split(): 
           kill = True
   if kill:
      print ("wrong grid authentication")
      exit()


      
if __name__ == '__main__':
  #load_grid()
  num = int(random.random()*10000)

   
  for dataset in input_datasets.keys():
      print('run dataset',dataset)

      output_file = f"bkg_files_lists/{dataset}.py"

      # Check if the file already exists
      if os.path.exists(output_file):
        print(f"Skipping {dataset}, file already exists: {output_file}")

      else:
        ## check if we already have list of AOD files from DAS
        fetch_dataset_files(dataset, input_datasets[dataset], output_dir="bkg_files_lists")
        #file_py = 'bkg_files_lists/'+dataset
      
      ## condor logs folder
      name = dataset+"_"+Conditions+"_"+tag
      if not os.path.isdir("condor_logs//"+name+"_"+date):
        os.mkdir("condor_logs/"+name+"_"+date)

      ## all input files
      files = 'bkg_files_lists/'+dataset+'.py'


      ## total number o of jobs?
      if njobs == -1:
        total_events = get_total_events(input_datasets[dataset])
        if total_events > 0:
          num_jobs = math.ceil(total_events / nevts_per_job)

      else:
        num_jobs = njobs  

      print("submitting ",num_jobs," jobs!!")

      ## make condor .sub file
      line="universe = vanilla\n"
      line+='MY.WantOS = "'+slc+'"\n'
      line+='getenv = True\n'
      line+="executable = "+Production+"\n"
      line+="arguments = {path} {cmsswnano} {filespy} --events {nevts} $(Step) {outdir} \n".format(path=os.getcwd(), cmsswnano=cmsswnano, filespy=files, nevts=nevts_per_job, outdir=samples_path+"/"+name)
      line+="request_memory = "+RAM+"\n"
      line+='output = condor_logs/{name}_{date}/job.$(ClusterId).$(Step).out\n'.format(name=name,date=date)
      line+='error = condor_logs/{name}_{date}/job.$(ClusterId).$(Step).err\n'.format(name=name,date=date)
      line+='log = condor_logs/{name}_{date}/job.$(ClusterId).$(Step).log\n'.format(name=name,date=date)
      line+="Proxy_filename          = x509up_u121632\n"
      line+="Proxy_path              = /afs/cern.ch/user/f/friti/$(Proxy_filename)\n"
      line+="x509userproxy           = $(Proxy_path)\n"
      line+="use_x509userproxy       = true\n"
      line+='should_transfer_files   = YES\n'
      line+='when_to_transfer_output = ON_EXIT\n'
      line+='transfer_output_files   = ""\n'
      line+='+AccountingGroup = "group_u_CMST3.all"\n'
      line+='+JobFlavour = \"{flavor}\" \n'.format(flavor=flavor)
      line+="queue {num_jobs}\n".format(num_jobs=num_jobs)
      with open("condor_temp.sub",'w') as out:
        out.write(line);
        out.close()
        os.system('condor_submit condor_temp.sub ')
      

   

