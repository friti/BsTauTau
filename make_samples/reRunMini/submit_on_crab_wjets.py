from CRABClient.UserUtilities import config, ClientException
import yaml
import datetime
from fnmatch import fnmatch
from argparse import ArgumentParser

production_tag = datetime.date.today().strftime('%Y%b%d')

config = config()
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.workArea = 'crab_jobs/WJetsToLNu_RunIISummer20UL18-106X_%s' % production_tag

config.section_('Data')
config.Data.publication = False
config.Data.outLFNDirBase = '/store/group/cmst3/group/bpark/friti/bstautau/wjets/miniaod_%s' % ('WJetsToLNu_RunIISummer20UL18-106X_' + production_tag)
config.Data.inputDBS = 'global'

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'wjets_miniaodstep_cfg.py'
config.Data.partialDataset = True
#config.JobType.scriptExe = 'crab_script.sh'
#config.JobType.maxJobRuntimeMin = 3000
#config.JobType.allowUndistributedCMSSW = True
#config.Data.allowNonValidInputDataset = True
#config.JobType.numCores = 4
config.JobType.maxMemoryMB = 4000
#config.JobType.maxMemoryMB = 3000
config.section_('User')
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
#config.Data.partialDataset = True  # no partial dataset available!!

if __name__ == '__main__':

  from CRABAPI.RawCommand import crabCommand
  from CRABClient.ClientExceptions import ClientException
  from multiprocessing import Process

  def submit(config):
          crabCommand('submit', config = config)



config.Data.inputDataset = '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM'
config.General.requestName = 'wjets'
config.Data.splitting = 'FileBased' 
config.Data.unitsPerJob = 5
globaltag = '106X_upgrade2018_realistic_v11_L1v1'
                
config.JobType.outputFiles = ['wjets_miniaod.root']
        
print(config)
submit(config)
