import FWCore.ParameterSet.Config as cms

from CATTools.LeptonAnalysis.tnp_fit_muon_template_cfg import *
process.tnpTightIso = process.tnpTemplate.clone()
process.tnpTightIso.Efficiencies.TightIso = process.tnpTightIso.Efficiencies.TightId
process.tnpTightIso.OutputFileName = cms.string("tnp_fit_TightIso_RD.root")
delattr(process.tnpTightIso.Efficiencies, 'TightId')
process.tnpTightIso.Efficiencies.TightIso.EfficiencyCategoryAndState = cms.vstring("cut_TightIso", "below")
#process.tnpTightIso.OutputFileName = cms.string("tnp_fit_TightIso03_RD.root")
#process.tnpTightIso.Efficiencies.TightIso.EfficiencyCategoryAndState = cms.vstring("cut_TightIso03", "below")

## Modify parameters as you wish
## Change PDF
#process.BinToPDFmap = cms.vstring("voigtPlusCheb")
## Cut on denominator by adding BinnedVariables
#process.BinnedVariables.pair_nJets30 = cms.vdouble(2,999) ## nJet >= 2 for ttbar

process.p = cms.Path(process.tnpTightIso)

