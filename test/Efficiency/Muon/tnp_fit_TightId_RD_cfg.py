import FWCore.ParameterSet.Config as cms

from CATTools.LeptonAnalysis.tnp_fit_muon_template_cfg import *
process.tnpTightId = process.tnpTemplate.clone()
process.tnpTightId.OutputFileName = cms.string("tnp_fit_TightId_RD.root")
process.tnpTightId.Efficiencies.TightId.EfficiencyCategoryAndState = cms.vstring("cut_TightId", "above")

## Modify parameters as you wish
## Change PDF
#process.BinToPDFmap = cms.vstring("voigtPlusCheb")
## Cut on denominator by adding BinnedVariables
#process.BinnedVariables.pair_nJets30 = cms.vdouble(2,999) ## nJet >= 2 for ttbar

process.p = cms.Path(process.tnpTightId)

