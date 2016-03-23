import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.TnP_Muon_ID = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    ## Input, output 
    InputFileNames = cms.vstring(#"root://eoscms//eos/cms/store/cmst3/user/botta/TnPtrees/tnpZ_Data.190456-193557.root",
                                 #"file:tnpZ_MC.root"

				 "file:tnpZ_MC.root"), ## can put more than one
## copy locally to be faster: xrdcp root://eoscms//eos/cms/store/cmst3/user/botta/TnPtrees/tnpZ_Data.190456-193557.root $PWD/tnpZ_Data.190456-193557.root
    ## and then set InputFileNames = cms.vstring("tnpZ_Data.190456-193557.root"), 

    OutputFileName = cms.string("TnP_Muon_ID_PtEta.root"),
    InputTreeName = cms.string("fitter_tree"), 
    InputDirectoryName = cms.string("tpTree"),  
    ##Defined weight
    WeightVariable =cms.string("weight"),
    ## Variables for binning
    Variables = cms.PSet(
        mass   = cms.vstring("Tag-muon Mass", "76", "125", "GeV/c^{2}"),
        pt     = cms.vstring("muon p_{T}", "0", "1000", "GeV/c"),
        eta = cms.vstring("muon #eta", "-2.5", "2.5", ""),
	absphi = cms.vstring("muon |#phi|", "0", "3.142", ""),
        pair_dz = cms.vstring("#Deltaz between two muons", "-100", "100", "cm"),
	tag_pt  = cms.vstring("tag muon p_{T}", "0", "1000.", "GeV/c"),
        dB     = cms.vstring("dxy muon", "0", "2", "cm"),
	dzPV     = cms.vstring("dz PV muon", "-5", "5", "cm"),
	weight  = cms.vstring("weight", "0", "10", ""),

    ),
    ## Flags you want to use to define numerator and possibly denominator
    Categories = cms.PSet(
        PF = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        Tight2012 = cms.vstring("Tight2012 muon", "dummy[pass=1,fail=0]"),
	#        tag_IsoMu24_eta2p1 = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        #tag_IsoMu17_eta2p1 = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        Mu17_IsoTrkVVL = cms.vstring("Mu17_IsoTrkVVL Probe Muon", "dummy[pass=1,fail=0]"),
	tag_Mu17_IsoTrkVVL = cms.vstring("Mu17_IsoTrkVVL Tag Muon", "dummy[pass=1,fail=0]"),
    ),
    Expressions = cms.PSet(
      Tight_tip_var = cms.vstring( "Tight_tip", "Tight2012==1 && abs(dB) < 0.2 && abs(dzPV) < 0.5", "Tight2012", "dB", "dzPV"),
      ),

    ## Cuts : name, variable, cut threshold
    Cuts = cms.PSet(
      Tight_tip = cms.vstring( "Tight_tip", "Tight_tip_var", ""),
      ),

    ## What to fit
    Efficiencies = cms.PSet(
      Tight_ID_PtEta = cms.PSet(
            UnbinnedVariables = cms.vstring("mass", "weight"),
            #UnbinnedVariables = cms.vstring("mass"),
            EfficiencyCategoryAndState = cms.vstring("Tight_tip", ""), ## Numerator definition
            #EfficiencyCategoryAndState = cms.vstring("PF", "pass"), ## Numerator definition
            BinnedVariables = cms.PSet(
                ## Binning in continuous variables
                pt     = cms.vdouble( 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200 ),
                #eta = cms.vdouble( -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5),
                eta = cms.vdouble( -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5),
                #tag_pt = cms.vdouble( 20, 200),
		## flags and conditions required at the denominator, 
                tag_Mu17_IsoTrkVVL = cms.vstring("pass"), 
                tag_pt = cms.vdouble(20 , 200.),               
#		pair_dz = cms.vdouble(-1.,1.)             ## and for which -1.0 < dz < 1.0
            ),
            BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        )
    ),

    ## PDF for signal and background (double voigtian + exponential background)
    PDFs = cms.PSet(
        vpvPlusExpo = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,2,10])",
            "SUM::signal(vFrac[0.8,0,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
            "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
    ),

    ## How to do the fit
    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(40),
    saveDistributionsPlot = cms.bool(False),
    NumCPU = cms.uint32(1), ## leave to 1 for now, RooFit gives funny results otherwise
    SaveWorkspace = cms.bool(False),
)

#
process.p1 = cms.Path(process.TnP_Muon_ID)
#process.p2 = cms.Path(process.TnP_Muon_Iso)
