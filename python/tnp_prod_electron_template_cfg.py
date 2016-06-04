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
process.baseElectrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("slimmedElectrons"),
    cut = cms.string(
         "gsfTrack.isNonnull && superCluster.isNonnull"
       + "&& pt >= 10 && abs(superCluster.eta) <= 2.5"
    )
)
process.twoBaseElectrons = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("baseElectrons"),
    minNumber = cms.uint32(2)
)
process.matchElectronTriggers = cms.EDProducer("PATTriggerMatcherDRLessByR",
    src     = cms.InputTag("baseElectrons"),
    matched = cms.InputTag("unpackedPatTrigger"),
    #matchedCuts = cms.string("type('TriggerElectron')"),
    matchedCuts = cms.string("path('HLT_Ele*') || path('HLT_Mu*')"),
    maxDeltaR = cms.double(0.5),
    resolveAmbiguities    = cms.bool( True ),
    resolveByMatchQuality = cms.bool( True ),
)
process.patElectronsWithTrigger = cms.EDProducer("PATTriggerMatchElectronEmbedder",
    src = cms.InputTag("baseElectrons"),
    matches = cms.VInputTag(cms.InputTag("matchElectronTriggers")),
)

process.patElectronSequence = cms.Sequence(
    process.baseElectrons + process.twoBaseElectrons
  + process.unpackedPatTrigger + process.matchElectronTriggers
  + process.patElectronsWithTrigger
)

## Build tags and probes
process.tagElectrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("patElectronsWithTrigger"),
    cut = cms.string(
        "pt >= 25"
      + "&& !(1.4442<=abs(superCluster.eta) && abs(superCluster.eta)<=1.566)"
      + "&& !triggerObjectMatchesByPath('HLT_Ele23_WPLoose_Gsf_v*').empty()"
    ),
)
process.oneTag  = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tagElectrons"), minNumber = cms.uint32(1))
process.probeElectrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("patElectronsWithTrigger"),
    cut = cms.string(
        "ecalEnergy*sin(superClusterPosition.theta)>10.0"
    ),
)
process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string('60 < mass && mass < 140 && abs(daughter(0).vz - daughter(1).vz) < 4'),
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
process.load("CATTools.CatProducer.pileupWeight_cff")
process.load("CATTools.CatProducer.genWeight_cff")
process.load("CATTools.CatAnalyzer.flatGenWeights_cfi")
process.productOfAllWeights = cms.EDProducer("CandToWeightProductProducer",
    src = cms.InputTag("tpPairs"),
    weights = cms.VInputTag(cms.InputTag("flatGenWeights"), cms.InputTag("pileupWeight")),
)
process.productOfAllWeightsPUUp = process.productOfAllWeights.clone(
    weights = cms.VInputTag(cms.InputTag("flatGenWeights"), cms.InputTag("pileupWeight:up")),
)
process.productOfAllWeightsPUDn = process.productOfAllWeights.clone(
    weights = cms.VInputTag(cms.InputTag("flatGenWeights"), cms.InputTag("pileupWeight:dn")),
)

## Tree producer
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
    flags = cms.PSet(
        HLT_Ele23_WPLoose = cms.string("!triggerObjectMatchesByPath('HLT_Ele23_WPLoose_Gsf_v*').empty()"),

        ## SingleElectron path
        HLT_SingleEl = cms.string("!triggerObjectMatchesByPath('HLT_Ele22_eta2p1_WP75_Gsf_v*').empty()"
                                 + "|| !triggerObjectMatchesByPath('HLT_Ele22_eta2p1_WPLoose_Gsf_v*').empty()"),

        ## DoubleEG paths
        ## ElEl : HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*
        ##   hltEle17Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg*Filter comes together in a single sequence
        ##   hltEle17Ele12CaloIdLTrackIdLIsoVLDZFilter comes after the leg1/leg2 filter sequence
        HLT_ElEl_leg1 = cms.string("!triggerObjectMatchesByFilter('hltEle17Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg1Filter').empty()"),
        HLT_ElEl_leg2 = cms.string("!triggerObjectMatchesByFilter('hltEle17Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg2Filter').empty()"),
        HLT_ElEl_DZ   = cms.string("!triggerObjectMatchesByFilter('hltEle17Ele12CaloIdLTrackIdLIsoVLDZFilter').empty()"),

        ## MuEG paths:
        ##   HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v* :
        ##     hltMu17TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter comes after the Mu17 sequence
        ##   HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v* :
        ##     hltMu8TrkIsoVVLEle17CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter comes after the Mu8 sequence
        HLT_MuEl_path1 = cms.string("!triggerObjectMatchesByFilter('hltMu17TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter').empty()"),
        HLT_MuEl_path2 = cms.string("!triggerObjectMatchesByFilter('hltMu8TrkIsoVVLEle17CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter').empty()"),
    ),
    tagVariables = cms.PSet(
        nvertices = cms.InputTag("nverticesModule"),
    ),
    tagFlags = cms.PSet(),
    pairVariables = cms.PSet(
        weight = cms.InputTag("productOfAllWeights"),
        weightPUUp = cms.InputTag("productOfAllWeightsPUUp"),
        weightPUDn = cms.InputTag("productOfAllWeightsPUDn"),
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
  + process.pileupWeight + process.flatGenWeights
  + process.productOfAllWeights + process.productOfAllWeightsPUUp + process.productOfAllWeightsPUDn
  + process.tpTree
)

process.tagAndProbe = cms.Path(
    process.eventFilters
  + process.patElectronSequence
  + process.tnpSimpleSequence
)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tnp.root"))

