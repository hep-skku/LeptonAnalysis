import FWCore.ParameterSet.Config as cms
from os import environ
home = environ["HOME"]

from CATTools.LeptonAnalysis.tnp_fit_muon_template_cfg import *
process.tnpTightId = process.tnpTemplate.clone()
process.tnpTightId.InputFileNames = cms.vstring(
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part1.root",
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part2.root",
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part3.root",
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part3.root",
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part5.root",
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part6.root",
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part7.root",

        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunC.root",
)
process.tnpTightId.OutputFileName = cms.string("tnp_fit_TightId_RD.root")
process.tnpTightId.Efficiencies.TightId.EfficiencyCategoryAndState = cms.vstring("cut_TightId", "above")

## Modify parameters as you wish
## Change PDF
#process.tnpTightId.Efficiencies.TightId.BinToPDFmap = cms.vstring("voigtPlusCheb")
## Cut on denominator by adding BinnedVariables
process.tnpTightId.Efficiencies.TightId.BinnedVariables.pair_nJets30 = cms.vdouble(2,999) ## nJet >= 2 for ttbar

process.p = cms.Path(process.tnpTightId)

