import FWCore.ParameterSet.Config as cms

from CATTools.LeptonAnalysis.tnp_prod_electron_template_cfg import *
process.GlobalTag.globaltag = '76X_mcRun2_asymptotic_v12'

process.source.fileNames = [
    "/store/mc/RunIIFall15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU25nsData2015v1_HCALDebug_76X_mcRun2_asymptotic_v12-v1/00000/FC1A95F8-CEB8-E511-9138-02163E017703.root"
]

