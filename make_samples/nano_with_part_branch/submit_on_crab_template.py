## FIles are on TAPE!

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
config.General.workArea = 'crab_jobs/TEMPLATE_DATASET_%s' % production_tag

config.section_('Data')
config.Data.publication = False
config.Data.outLFNDirBase = '/store/group/cmst3/group/bpark/friti/bstautau/nano_with_part_%s/TEMPLATE_DATASET_TEMPLATE_CONDITIONS' % (production_tag)
config.Data.inputDBS = 'global'

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'TEMPLATE_PRODUCER'

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
globaltag = '106X_upgrade2018_realistic_v16_L1v1'

config.JobType.outputFiles = ['nano.root']

print(config)
submit(config)
