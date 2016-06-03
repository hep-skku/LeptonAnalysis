import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
#process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
#process.load('Configuration.StandardSequences.MagneticField_cff')
#process.load("Configuration.StandardSequences.Reconstruction_cff")

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(),
)

## Event Filters
process.load("CATTools.CatProducer.eventCleaning.eventCleaning_cff")
process.load("HLTrigger.HLTfilters.triggerResultsFilter_cfi")
process.primaryVertexFilter.vertexCollection = "offlineSlimmedPrimaryVertices"
#process.eventFilters = cms.Sequence(process.primaryVertexFilter + process.scrapingFilter + process.triggerResultsFilter)
process.eventFilters = cms.Sequence(process.primaryVertexFilter + process.triggerResultsFilter)
process.triggerResultsFilter.triggerConditions = ["HLT_Ele23_WPLoose_Gsf_v*"]
process.triggerResultsFilter.l1tResults = ''
process.triggerResultsFilter.throw = True
process.triggerResultsFilter.hltResults = "TriggerResults::HLT"

## Build tags and probes
process.tagElectrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("slimmedElectrons"),
    cut = cms.string(
        "track.isNonnull && pt >= 25 && abs(superCluster.eta) <= 2.5"
      + "&& !(1.4442<=abs(superCluster.eta)<=1.566)"
### FIXME : trigger matching is not working because the matching information is "packed".
#     + "&& !triggerObjectMatchesByFilter('hltEle23WPLooseGsfTrackIsoFilter').empty()"
      + "&& !triggerObjectMatchesByPath('HLT_Ele23_WPLoose_Gsf_v*').empty()"
    ),
)
process.oneTag  = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tagElectrons"), minNumber = cms.uint32(1))
process.probeElectrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("slimmedElectrons"),
    cut = cms.string("track.isNonnull && abs(superCluster.eta)<=2.5 && (ecalEnergy*sin(superClusterPosition.theta)>10.0)"),
)
process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    #cut = cms.string('60 < mass < 140 && abs(daughter(0).vz - daughter(1).vz) < 4'),
    cut = cms.string('60 < mass && abs(daughter(0).vz - daughter(1).vz) < 4'),
    decay = cms.string('tagElectrons@+ probeElectrons@-'),
)
process.onePair = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tpPairs"), minNumber = cms.uint32(1))

## Event variables associated with tag or Z candidates (from MuonAnalysis/TagAndProbe)
process.nverticesModule = cms.EDProducer("VertexMultiplicityCounter",
    probes = cms.InputTag("tagElectrons"),
    objects = cms.InputTag("offlinePrimaryVertices"),
    objectSelection = cms.string("!isFake && ndof > 4 && abs(z) <= 25 && position.Rho <= 2"),
)
process.njets30Module = cms.EDProducer("CandCleanedMultiplicityCounter",
    pairs   = cms.InputTag("tpPairs"),
    objects = cms.InputTag("slimmedJets"),
    objectSelection = cms.string("abs(eta) < 5 && pt > 30"),
    minTagObjDR   = cms.double(0.3),
    minProbeObjDR = cms.double(0.3),
)
#genWeightInfo = cms.EDProducer("GenWeightInfo",
#    pairTag= cms.InputTag("tpPairs"),
#    genInfoTag= cms.InputTag("generator")
#)
process.load("CATTools.CatProducer.pileupWeight_cff")
process.load("CATTools.CatProducer.genWeight_cff")
process.load("CATTools.CatAnalyzer.flatGenWeights_cfi")
process.productOfAllWeight = cms.EDProducer("CandToWeightProductProducer",
    src = cms.InputTag("tpPairs"),
    weights = cms.VInputTag(
        cms.InputTag("pileupWeight"),
        cms.InputTag("flatGenWeights"),
    ),
)

process.tpTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
    # choice of tag and probe pairs, and arbitration
    tagProbePairs = cms.InputTag("tpPairs"),
    arbitration   = cms.string("None"),
    # probe variables: all useful ones
    variables = cms.PSet(
        pt = cms.string("pt"),
        eta = cms.string("eta"),
        scEta = cms.string("superCluster.eta"),
        phi = cms.string("phi"),
    ),
    flags = cms.PSet(
        idCutBasedMedium = cms.InputTag("probeIdCutBasedMedium"),
    ),
    tagVariables = cms.PSet(
        nvertices = cms.InputTag("nverticesModule"),
    ),
    tagFlags = cms.PSet(
    ),
    pairVariables = cms.PSet(
        weight = cms.InputTag("productOfAllWeights"),
        nJets30 = cms.InputTag("njets30Module"),
        dz      = cms.string("daughter(0).vz - daughter(1).vz"),
        pt      = cms.string("pt"),
        rapidity = cms.string("rapidity"),
        deltaR   = cms.string("deltaR(daughter(0).eta, daughter(0).phi, daughter(1).eta, daughter(1).phi)"),
    ),
    pairFlags = cms.PSet(),
    isMC           = cms.bool(False),
    addRunLumiInfo = cms.bool(False),
)

process.tnpSimpleSequence = cms.Sequence(
    process.tagElectrons + process.oneTag
  + process.probeElectrons
  + process.tpPairs + process.onePair
  + process.nverticesModule + process.njets30Module
  + process.tpTree
)

process.tagAndProbe = cms.Path(
    process.eventFilters
  + process.tnpSimpleSequence
)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tnp.root"))

"""
from FWCore.ParameterSet.VarParsing import VarParsing
import sys

###################################################################
options['SUPERCLUSTER_COLL']       = "reducedEgamma:reducedSuperClusters"

from PhysicsTools.TagAndProbe.treeMakerOptions_cfi import *

if (varOptions.isMC):
    options['HLTFILTERTOMEASURE']  = cms.vstring()#"HLT_Ele23_WPLoose_Gsf_v*")
    #options['HLTFILTERTOMEASURE']  = cms.vstring("HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ")
    #options['HLTFILTERTOMEASURE']  = cms.vstring()#"hltEle23WPLooseGsfTrackIsoFilter")

setModules(process, options)
from PhysicsTools.TagAndProbe.treeContent_cfi import *

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

###################################################################
## ID
###################################################################

from PhysicsTools.TagAndProbe.electronIDModules_cfi import *
setIDs(process, options)

###################################################################
## SEQUENCES
###################################################################

process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag(options['ELECTRON_COLL'])
process.ele_sequence = cms.Sequence(
    process.goodElectrons +
    process.egmGsfElectronIDSequence +
    process.goodElectronsPROBECutBasedVeto +
    process.goodElectronsPROBECutBasedLoose +
    process.goodElectronsPROBECutBasedMedium +
    process.goodElectronsPROBECutBasedTight +
    process.goodElectronsTAGCutBasedVeto +
    process.goodElectronsTAGCutBasedLoose +
    process.goodElectronsTAGCutBasedMedium +
    process.goodElectronsTAGCutBasedTight +
    process.goodElectronsTagHLT +
    process.goodElectronsProbeHLT +
    process.goodElectronsProbeMeasureHLT +
    process.goodElectronsMeasureHLT
    )

process.sc_sequence = cms.Sequence(process.superClusterCands +
                                   process.goodSuperClusters +
                                   process.goodSuperClustersHLT +
                                   process.GsfMatchedSuperClusterCands
                                   )

process.GsfElectronToTrigger = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                              CommonStuffForSuperClusterProbe, mcTruthCommonStuff,
                                              tagProbePairs = cms.InputTag("tagTightHLT"),
                                              arbitration   = cms.string("Random2"),
                                              flags         = cms.PSet(passingHLT    = cms.InputTag("goodElectronsMeasureHLT")
                                                                       ),                                               
				              Jets          = cms.InputTag("slimmedJets"),
                                              allProbes     = cms.InputTag("goodElectronsProbeMeasureHLT"),
                                              )

if (varOptions.isMC):
    #process.GsfElectronToTrigger.probeMatches  = cms.InputTag("McMatchHLT")
    process.GsfElectronToTrigger.eventWeight   = cms.InputTag("generator")
    process.GsfElectronToTrigger.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")

process.GsfElectronToSC = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                         CommonStuffForSuperClusterProbe, mcTruthCommonStuff,
                                         tagProbePairs = cms.InputTag("tagTightSC"),
                                         arbitration   = cms.string("Random2"),
                                         flags         = cms.PSet(passingRECO   = cms.InputTag("GsfMatchedSuperClusterCands", "superclusters"),         
                                                                  ),                                               
                                         allProbes     = cms.InputTag("goodSuperClustersHLT"),
                                         )

if (varOptions.isMC):
    #process.GsfElectronToSC.probeMatches  = cms.InputTag("McMatchSC")
    process.GsfElectronToSC.eventWeight   = cms.InputTag("generator")
    process.GsfElectronToSC.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")

process.GsfElectronToRECO = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                           mcTruthCommonStuff, CommonStuffForGsfElectronProbe,
                                           tagProbePairs = cms.InputTag("tagTightRECO"),
                                           arbitration   = cms.string("Random2"),
                                           flags         = cms.PSet(passingVeto   = cms.InputTag("goodElectronsPROBECutBasedVeto"),
                                                                    passingLoose  = cms.InputTag("goodElectronsPROBECutBasedLoose"),
                                                                    passingMedium = cms.InputTag("goodElectronsPROBECutBasedMedium"),
                                                                    passingTight  = cms.InputTag("goodElectronsPROBECutBasedTight"),
                                                                    ),                                               
                                           allProbes     = cms.InputTag("goodElectronsProbeHLT"),
                                           )

if (varOptions.isMC):
    #process.GsfElectronToRECO.probeMatches  = cms.InputTag("McMatchRECO")
    process.GsfElectronToRECO.eventWeight   = cms.InputTag("generator")
    process.GsfElectronToRECO.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")

if (varOptions.isMC):
    process.p = cms.Path(
        process.sampleInfo +
        process.ele_sequence + 
        process.sc_sequence +
        process.allTagsAndProbes +
        process.pileupReweightingProducer +
        process.mc_sequence +
        process.eleVarHelper +
        process.tree_sequence
        )
else:
    process.p = cms.Path(
        process.sampleInfo +
        process.ele_sequence + 
        process.sc_sequence +
        process.allTagsAndProbes +
        process.mc_sequence +
        process.eleVarHelper +
        process.tree_sequence
        )

"""

