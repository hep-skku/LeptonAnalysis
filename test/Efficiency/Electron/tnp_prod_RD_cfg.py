import FWCore.ParameterSet.Config as cms

from CATTools.LeptonAnalysis.tnp_prod_electron_template_cfg import *
process.GlobalTag.globaltag = '76X_dataRun2_v15'

process.source.fileNames = [
    '/store/data/Run2015D/SingleElectron/MINIAOD/16Dec2015-v1/20000/FE1C27B4-1BA7-E511-8E55-0CC47A4D7636.root',
]
