import FWCore.ParameterSet.Config as cms
from os import environ
home = environ["HOME"]

from CATTools.LeptonAnalysis.tnp_fit_muon_template_cfg import *
process.tnpTightIso = process.tnpTemplate.clone()
process.tnpTightIso.Efficiencies.TightIso = process.tnpTightIso.Efficiencies.TightId
process.tnpTightIso.InputFileNames = cms.vstring(
     "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_76X_DYLL_M50_MadGraphMLM_part1.root",
     "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_76X_DYLL_M50_MadGraphMLM_part2.root",
)
process.tnpTightIso.OutputFileName = cms.string("tnp_fit_TightIso_MC.root")
delattr(process.tnpTightIso.Efficiencies, 'TightId')
process.tnpTightIso.Efficiencies.TightIso.EfficiencyCategoryAndState = cms.vstring("cut_TightIso", "below")
#process.tnpTightIso.OutputFileName = cms.string("tnp_fit_TightIso03_RD.root")
#process.tnpTightIso.Efficiencies.TightIso.EfficiencyCategoryAndState = cms.vstring("cut_TightIso03", "below")

## Modify parameters as you wish
## Change PDF
#process.tnpTightIso.Efficiencies.TightIso.BinToPDFmap = cms.vstring("voigtPlusCheb")
## Cut on denominator by adding BinnedVariables
process.tnpTightIso.Efficiencies.TightIso.BinnedVariables.pair_nJets30 = cms.vdouble(2,999) ## nJet >= 2 for ttbar

process.p = cms.Path(process.tnpTightIso)

