import FWCore.ParameterSet.Config as cms
from os import environ
home = environ["HOME"]

from CATTools.LeptonAnalysis.tnp_fit_muon_template_cfg import *
process.tnpTightIso = process.tnpTemplate.clone()
process.tnpTightIso.InputFileNames = cms.vstring(
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part1.root",
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part2.root",
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part3.root",
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part3.root",
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part5.root",
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part6.root",
        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part7.root",

        "file:"+home+"/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunC.root",
)
process.tnpTightIso.OutputFileName = cms.string("tnp_fit_TightIso_RD.root")

process.tnpTightIso.Efficiencies.TightIso = process.tnpTightIso.Efficiencies.TightId
delattr(process.tnpTightIso.Efficiencies, 'TightId')
process.tnpTightIso.Efficiencies.TightIso.EfficiencyCategoryAndState = cms.vstring("cut_TightIso", "below")
#process.tnpTightIso.OutputFileName = cms.string("tnp_fit_TightIso03_RD.root")
#process.tnpTightIso.Efficiencies.TightIso.EfficiencyCategoryAndState = cms.vstring("cut_TightIso03", "below")

## Modify parameters as you wish
## Change PDF
#process.tnpTightIso.Efficiencies.TightIso.BinToPDFmap = cms.vstring("voigtPlusCheb")
## Cut on denominator by adding BinnedVariables
process.tnpTightIso.Variables.Tight2012 = cms.vstring("Tight2012 muon", "0", "1", "")
process.tnpTightIso.Efficiencies.TightIso.BinnedVariables.Tight2012 = cms.vdouble(0.5,1.5) ## Tight2012==1
process.tnpTightIso.Efficiencies.TightIso.BinnedVariables.dB = cms.vdouble(-0.2,0.2) ## abs(dB) < 0.2
process.tnpTightIso.Efficiencies.TightIso.BinnedVariables.dzPV = cms.vdouble(-0.5,0.5) ## abs(dzPV) < 0.5
delattr(process.tnpTightIso.Categories, "Tight2012") ## Should be removed to avoid duplicated definition

process.tnpTightIso.Efficiencies.TightIso.BinnedVariables.pair_nJets30 = cms.vdouble(2,999) ## nJet >= 2 for ttbar

process.p = cms.Path(process.tnpTightIso)

