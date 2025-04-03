## FIles are on TAPE!

from CRABClient.UserUtilities import config, ClientException
import yaml
import datetime
from fnmatch import fnmatch
from argparse import ArgumentParser


config = config()
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.workArea = 'crab_jobs/TEMPLATE_DATASET_TEMPLATE_DATE'

config.section_('Data')
config.Data.publication = False
config.Data.outLFNDirBase = '/store/group/cmst3/group/bpark/friti/bstautau/nano_with_part_TEMPLATE_DATE/TEMPLATE_DATASET_TEMPLATE_CONDITIONS'
config.Data.inputDBS = 'global'

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'TEMPLATE_PRODUCER'
config.JobType.maxMemoryMB = 5000
config.JobType.inputFiles = ["CMSSW_13_0_10/src/data"]

config.section_('User')
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'

if __name__ == '__main__':

  from CRABAPI.RawCommand import crabCommand
  from CRABClient.ClientExceptions import ClientException
  from multiprocessing import Process

  def submit(config):
          crabCommand('submit', config = config)



config.Data.inputDataset = 'TEMPLATE_INPUT'
config.General.requestName = 'TEMPLATE_DATASET'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = TEMPLATE_UNITSPERJOB
globaltag = 'TEMPLATE_GT'

config.JobType.outputFiles = ['step5.root']

print(config)
#submit(config)
