import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.tnpTemplate = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    ## Input, output 
    InputFileNames = cms.vstring(
        "/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part1.root",
        "/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part2.root",
        "/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part3.root",
        "/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part3.root",
        "/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part5.root",
        "/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part6.root",
        "/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part7.root",

        "/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunC.root",
    ),
    OutputFileName = cms.string("tnp_fit.root"),

    InputTreeName = cms.string("fitter_tree"),
    InputDirectoryName = cms.string("tpTree"),

    ## Variables
    Variables = cms.PSet(
        mass    = cms.vstring("Tag-muon Mass", "76", "125", "GeV/c^{2}"),
        pt      = cms.vstring("muon p_{T}", "0", "1000", "GeV/c"),
        eta     = cms.vstring("muon #eta", "-2.5", "2.5", ""),
        abseta  = cms.vstring("muon |#eta|", "0", "2.5", ""),
        absphi  = cms.vstring("muon |#phi|", "0", "3.142", ""),
        pair_dz = cms.vstring("#Deltaz between two muons", "-100", "100", "cm"),
        tag_pt  = cms.vstring("tag muon p_{T}", "0", "1000.", "GeV/c"),
        dB      = cms.vstring("dxy muon", "0", "2", "cm"),
        dzPV    = cms.vstring("dz PV muon", "-5", "5", "cm"),

        pair_nJets30       = cms.vstring("nJets30", "0", "10", ""),
    ),

    ## Flags
    Categories = cms.PSet(
        PF = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        Tight2012 = cms.vstring("Tight2012 muon", "dummy[pass=1,fail=0]"),
        tag_IsoMu20 = cms.vstring("tag_IsoMu20 tag Muon", "dummy[pass=1,fail=0]"),
    ),

    Expressions = cms.PSet(
        Tight_var = cms.vstring("var_Tight", "Tight2012==1 && abs(dB) < 0.2 && abs(dzPV) < 0.5", "Tight2012",  "dB", "dzPV"),
    ),

    ## Cuts : name, variable, cut threshold
    Cuts = cms.PSet(
        Tight_cut = cms.vstring( "Tight_cut", "Tight_var", "0.5"),
    ),

    ## What to fit
    Efficiencies = cms.PSet(
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring("Tight_cut", "above"), ## Numerator definition
        BinnedVariables = cms.PSet(
            ## Binning in continuous variables
            #pt    = cms.vdouble(20, 25, 30, 40, 50, 60, 80, 120, 200),
            #eta   = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4),
            pt     = cms.vdouble(20, 25, 30, 40, 50, 60, 120),
            abseta = cms.vdouble(0.0, 0.9, 1.2, 2.1, 2.4),
            ## flags and conditions required at the denominator, 
            tag_pt = cms.vdouble(20. , 500.),
            tag_IsoMu20 = cms.vstring("pass"),
            pair_nJets30 = cms.vdouble(0, 999),
        ),
        BinToPDFmap = cms.vstring("voigtPlusExpo"), ## PDF to use, as defined below
    ),

    PDFs = cms.PSet(
        voigtPlusExpo = cms.vstring(
            "Voigtian::signalPass(mass, meanPass[90,80,100], width[2.495], sigmaPass[3,1,20])",
            "Voigtian::signalFail(mass, meanFail[90,80,100], width,        sigmaFail[3,1,20])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        voigtPlusCheb = cms.vstring(
            "Voigtian::signalPass(mass, meanPass[90,80,100], width[2.495], sigmaPass[3,1,20])",
            "Voigtian::signalFail(mass, meanFail[90,80,100], width,        sigmaFail[3,1,20])",
            "RooChebychev::backgroundPass(mass, {p0[0.25,0,0.5], p1[-0.25,-1,0.1],p2[0.,-0.25,0.25]})",
            "RooChebychev::backgroundFail(mass, {b0[0.25,0,0.5], b1[-0.25,-1,0.1],b2[0.,-0.25,0.25]})",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),

        ## How to do the fit
        binnedFit = cms.bool(True),
        binsForFit = cms.uint32(40),
        saveDistributionsPlot = cms.bool(False),
        NumCPU = cms.uint32(1),
        SaveWorkspace = cms.bool(False),
    ),
)

