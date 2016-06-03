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

## Trigger matching
process.load("PhysicsTools.PatAlgos.slimming.unpackedPatTrigger_cfi")
process.matchElectronTriggers = cms.EDProducer("PATTriggerMatcherDRLessByR",
    src     = cms.InputTag("slimmedElectrons"),
    matched = cms.InputTag("unpackedPatTrigger"),
    matchedCuts = cms.string("type('TriggerElectron')"),
    maxDeltaR = cms.double(0.5),
    resolveAmbiguities    = cms.bool( True ),
    resolveByMatchQuality = cms.bool( True ),
)
process.patElectronsWithTrigger = cms.EDProducer("PATTriggerMatchElectronEmbedder",
    src = cms.InputTag("slimmedElectrons"),
    matches = cms.VInputTag(cms.InputTag("matchElectronTriggers")),
)

process.patElectronSequence = cms.Sequence(
    process.unpackedPatTrigger + process.matchElectronTriggers
  + process.patElectronsWithTrigger
)

## Build tags and probes
process.tagElectrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("patElectronsWithTrigger"),
    cut = cms.string(
        "gsfTrack.isNonnull && superCluster.isNonnull"
      + "&& pt >= 25 && abs(superCluster.eta) <= 2.5"
      + "&& !(1.4442<=abs(superCluster.eta)<=1.566)"
#      + "&& !triggerObjectMatchesByFilter('hltEle23WPLooseGsfTrackIsoFilter').empty()"
#      + "&& !triggerObjectMatchesByPath('HLT_Ele23_WPLoose_Gsf_v*').empty()"
    ),
)
process.oneTag  = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tagElectrons"), minNumber = cms.uint32(1))
process.probeElectrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("patElectronsWithTrigger"),
    cut = cms.string(
        "gsfTrack.isNonnull && superCluster.isNonnull"
      + "&& abs(superCluster.eta)<=2.5 && (ecalEnergy*sin(superClusterPosition.theta)>10.0)"
    ),
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
    objects = cms.InputTag("offlineSlimmedPrimaryVertices"),
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

        idCutBasedLoose  = cms.string("electronID('cutBasedElectronID-Spring15-25ns-V1-standalone-loose')"),
        idCutBasedMedium = cms.string("electronID('cutBasedElectronID-Spring15-25ns-V1-standalone-medium')"),
        idCutBasedTight  = cms.string("electronID('cutBasedElectronID-Spring15-25ns-V1-standalone-tight')"),

        idMvaWp80 = cms.string("electronID('mvaEleID-Spring15-25ns-Trig-V1-wp80')"),
        idMvaWp90 = cms.string("electronID('mvaEleID-Spring15-25ns-Trig-V1-wp90')"),
    ),
    flags = cms.PSet(),
    tagVariables = cms.PSet(
        nvertices = cms.InputTag("nverticesModule"),
    ),
    tagFlags = cms.PSet(),
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
  + process.patElectronSequence
  + process.tnpSimpleSequence
)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tnp.root"))

