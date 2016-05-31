import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.TnP_Muon_ID = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    ## Input, output 
    InputFileNames = cms.vstring(#"root://eoscms//eos/cms/store/cmst3/user/botta/TnPtrees/tnpZ_Data.190456-193557.root",
                                 #"file:tnpZ_MC.root"
"/afs/cern.ch/user/d/dhkim/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part1.root",
"/afs/cern.ch/user/d/dhkim/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part2.root",
"/afs/cern.ch/user/d/dhkim/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part3.root",
"/afs/cern.ch/user/d/dhkim/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part3.root",
"/afs/cern.ch/user/d/dhkim/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part5.root",
"/afs/cern.ch/user/d/dhkim/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part6.root",
"/afs/cern.ch/user/d/dhkim/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunD_part7.root",

"/afs/cern.ch/user/d/dhkim/eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/TnPTree_v41_76X_RunC.root",
),


#				 "file:tnpZ_Data.root"), ## can put more than one
## copy locally to be faster: xrdcp root://eoscms//eos/cms/store/cmst3/user/botta/TnPtrees/tnpZ_Data.190456-193557.root $PWD/tnpZ_Data.190456-193557.root
    ## and then set InputFileNames = cms.vstring("tnpZ_Data.190456-193557.root"), 

#    OutputFileName = cms.string("/afs/cern.ch/user/d/dhkim/eos/cms/store/user/dhkim/TnP_Muon_ID_Data_voigtPlusExpo.root"),
#    OutputFileName = cms.string("/afs/cern.ch/user/d/dhkim/eos/cms/store/user/dhkim/TnP_Muon_ID_Data_vpvPlusExpo.root"),
    OutputFileName = cms.string("/afs/cern.ch/user/d/dhkim/eos/cms/store/user/dhkim/TnP_Muon_ID_Data_vpvPlusExpoMin70.root"),
#    OutputFileName = cms.string("/afs/cern.ch/user/d/dhkim/eos/cms/store/user/dhkim/TnP_Muon_ID_Data_vpvPlusCheb.root"),

    InputTreeName = cms.string("fitter_tree"), 
    InputDirectoryName = cms.string("tpTree"),  
    ## Variables for binning
    Variables = cms.PSet(
        mass   = cms.vstring("Tag-muon Mass", "76", "125", "GeV/c^{2}"),
        pt     = cms.vstring("muon p_{T}", "0", "1000", "GeV/c"),
        eta = cms.vstring("muon #eta", "-2.5", "2.5", ""),
        abseta = cms.vstring("muon |#eta|", "0", "2.5", ""),
	absphi = cms.vstring("muon |#phi|", "0", "3.142", ""),
        pair_dz = cms.vstring("#Deltaz between two muons", "-100", "100", "cm"),
	tag_pt  = cms.vstring("tag muon p_{T}", "0", "1000.", "GeV/c"),
        dB     = cms.vstring("dxy muon", "0", "2", "cm"),
	dzPV     = cms.vstring("dz PV muon", "-5", "5", "cm"),

    ),
    ## Flags you want to use to define numerator and possibly denominator
    Categories = cms.PSet(
        PF = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        Tight2012 = cms.vstring("Tight2012 muon", "dummy[pass=1,fail=0]"),
        tag_IsoMu20 = cms.vstring("tag_IsoMu20 tag Muon", "dummy[pass=1,fail=0]"),
    ),
    Expressions = cms.PSet(
      Tight_var = cms.vstring( "Tight_var", "Tight2012==1 && abs(dB) < 0.2 && abs(dzPV) < 0.5", "Tight2012",  "dB", "dzPV"),
      ),

    ## Cuts : name, variable, cut threshold
    Cuts = cms.PSet(
      Tight_cut = cms.vstring( "Tight_cut", "Tight_var", "0.5"),
      ),

    ## What to fit
    Efficiencies = cms.PSet(
      Tight_Eta = cms.PSet(
            #UnbinnedVariables = cms.vstring("mass", "weight"),
            UnbinnedVariables = cms.vstring("mass"),
            EfficiencyCategoryAndState = cms.vstring("Tight_cut", "above"), ## Numerator definition
            BinnedVariables = cms.PSet(
                ## Binning in continuous variables
		pt     = cms.vdouble( 20., 500.),
                eta = cms.vdouble( -2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6,  2.1, 2.4),
		## flags and conditions required at the denominator, 
                tag_pt = cms.vdouble(20. , 500.),               
                tag_IsoMu20 = cms.vstring("pass"), 
            ),
#        BinToPDFmap = cms.vstring("voigtPlusExpo"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
	BinToPDFmap = cms.vstring("vpvPlusExpoMin70"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusCheb"), ## PDF to use, as defined below
        ),
    
      Tight_Pt_AllEta = cms.PSet(
	#UnbinnedVariables = cms.vstring("mass", "weight"),
	UnbinnedVariables = cms.vstring("mass"),
	EfficiencyCategoryAndState = cms.vstring("Tight_cut", "above"), ## Numerator definition
	BinnedVariables = cms.PSet(
	  ## Binning in continuous variables
	  pt     = cms.vdouble( 20, 25, 30, 40, 50, 60, 80, 120, 200 ),
          abseta = cms.vdouble( 0.0, 2.4),
	  ## flags and conditions required at the denominator,
	  tag_pt = cms.vdouble(20. , 500.),
	  tag_IsoMu20 = cms.vstring("pass"),
	  ),
#	BinToPDFmap = cms.vstring("voigtPlusExpo"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
	BinToPDFmap = cms.vstring("vpvPlusExpoMin70"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusCheb"), ## PDF to use, as defined below
	),

      Tight_Pt_Eta = cms.PSet(
	#UnbinnedVariables = cms.vstring("mass", "weight"),
	UnbinnedVariables = cms.vstring("mass"),
	EfficiencyCategoryAndState = cms.vstring("Tight_cut", "above"), ## Numerator definition
	BinnedVariables = cms.PSet(
	  ## Binning in continuous variables
	  pt     = cms.vdouble( 20, 25, 30, 40, 50, 60, 120),
	  abseta = cms.vdouble( 0.0, 0.9, 1.2, 2.1,  2.4),
	  ## flags and conditions required at the denominator,
	  tag_pt = cms.vdouble(20. , 500.),
	  tag_IsoMu20 = cms.vstring("pass"),
	  ),
#	BinToPDFmap = cms.vstring("voigtPlusExpo"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
	BinToPDFmap = cms.vstring("vpvPlusExpoMin70"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusCheb"), ## PDF to use, as defined below
	),

      ),

    ## PDF for signal and background (double voigtian + exponential background)
    PDFs = cms.PSet(
#	vpvPlusExpo = cms.vstring(
#	  "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
#	  "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,2,10])",
#	  "SUM::signal(vFrac[0.8,0,1]*signal1, signal2)",
#	  "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
#	  "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])",
#	  "efficiency[0.9,0,1]",
#	  "signalFractionInPassing[0.9]"
#	  ),

	voigtPlusExpo = cms.vstring(
	  "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])",
	  "Exponential::backgroundPass(mass, lp[0,-5,5])",
	  "Exponential::backgroundFail(mass, lf[0,-5,5])",
	  "efficiency[0.9,0,1]",
	  "signalFractionInPassing[0.9]"
	  ),
	vpvPlusExpo = cms.vstring(
	  "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
	  "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,2,10])",
	  "SUM::signal(vFrac[0.8,0,1]*signal1, signal2)",
	  "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
	  "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])",
	  "efficiency[0.9,0,1]",
	  "signalFractionInPassing[0.9]"
	  ),
	vpvPlusExpoMin70 = cms.vstring(
	  "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
	  "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])",
	  "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
	  "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
	  "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])",
	  "efficiency[0.9,0.7,1]",
	  "signalFractionInPassing[0.9]"
	  ),
	vpvPlusCheb = cms.vstring(
	  "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
	  "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])",
	  "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
	  #par3
	  "RooChebychev::backgroundPass(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})",
	  "RooChebychev::backgroundFail(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})",
	  "efficiency[0.9,0.7,1]",
	  "signalFractionInPassing[0.9]"
	  )



    ),

    ## How to do the fit
    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(40),
    saveDistributionsPlot = cms.bool(False),
    NumCPU = cms.uint32(1), ## leave to 1 for now, RooFit gives funny results otherwise
    SaveWorkspace = cms.bool(False),
)

#### Slighly different configuration for isolation, where the "passing" is defined by a cut
process.TnP_Muon_Iso = process.TnP_Muon_ID.clone(
    OutputFileName = cms.string("/afs/cern.ch/user/d/dhkim/eos/cms/store/user/dhkim/TnP_Muon_Iso_Data_vpvPlusExpoMin70.root"),
    ## More variables
    Variables = process.TnP_Muon_ID.Variables.clone(
      combRelIsoPF04dBeta = cms.vstring("PF Combined Relative Iso", "-100", "99999", ""),
      tag_combRelIsoPF04dBeta = cms.vstring("PF Combined Relative Tag Iso", "-100", "99999", ""),
      ),
    Expressions = cms.PSet(
      Tight_Iso_var = cms.vstring( "Tight_Iso_var", "combRelIsoPF04dBeta < 0.15", "combRelIsoPF04dBeta"),
      ),
    ## Cuts: name, variable, cut threshold
    Cuts = cms.PSet(
      PFIsoLoose = cms.vstring("PFIsoLoose" ,"combRelIsoPF04dBeta", "0.20"),
      PFIsoTight = cms.vstring("PFIsoTight" ,"combRelIsoPF04dBeta", "0.15"),
      Tight_Iso_cut = cms.vstring("Tight_Iso_cut" ,"Tight_Iso_var", "0.5"),
      ),
    ## What to fit
    Efficiencies = cms.PSet(

      Tight_Iso_Eta = cms.PSet(
	#UnbinnedVariables = cms.vstring("mass","weight"),
	UnbinnedVariables = cms.vstring("mass"),
	EfficiencyCategoryAndState = cms.vstring("Tight_Iso_cut", "above"),
	BinnedVariables = cms.PSet(
	  pt     = cms.vdouble( 20., 500.),
	  eta = cms.vdouble( -2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6,  2.1, 2.4),
	  Tight2012 = cms.vstring("pass"),
          dB   = cms.vdouble( 0.0, 2.0),
	  dzPV = cms.vdouble(-0.5, 0.5),

	  ## flags and conditions required at the denominator,
	  tag_pt = cms.vdouble(20. , 500.),
	  tag_IsoMu20 = cms.vstring("pass"),
	  tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
	  ),
#	BinToPDFmap = cms.vstring("voigtPlusExpo"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
	BinToPDFmap = cms.vstring("vpvPlusExpoMin70"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusCheb"), ## PDF to use, as defined below
	),

      PFTight_Iso_Eta = cms.PSet(
	#UnbinnedVariables = cms.vstring("mass","weight"),
	UnbinnedVariables = cms.vstring("mass"),
	EfficiencyCategoryAndState = cms.vstring("PFIsoTight", "below"),
	BinnedVariables = cms.PSet(
	  pt     = cms.vdouble( 20., 500.),
	  eta = cms.vdouble( -2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6,  2.1, 2.4),
	  Tight2012 = cms.vstring("pass"),
	  dB   = cms.vdouble( 0.0, 2.0),
	  dzPV = cms.vdouble(-0.5, 0.5),

	  ## flags and conditions required at the denominator,
          PF = cms.vstring("pass"),
	  tag_pt = cms.vdouble(20. , 500.),
	  tag_IsoMu20 = cms.vstring("pass"),
	  tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
	  ),
#	BinToPDFmap = cms.vstring("voigtPlusExpo"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
	BinToPDFmap = cms.vstring("vpvPlusExpoMin70"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusCheb"), ## PDF to use, as defined below
	),

      Tight_Iso_Pt_AllEta = cms.PSet(
	#UnbinnedVariables = cms.vstring("mass","weight"),
	UnbinnedVariables = cms.vstring("mass"),
	EfficiencyCategoryAndState = cms.vstring("Tight_Iso_cut", "above"),
	BinnedVariables = cms.PSet(
	  pt     = cms.vdouble( 20, 25, 30, 40, 50, 60, 80, 120, 200 ),
	  abseta = cms.vdouble( 0.0, 2.4),
	  Tight2012 = cms.vstring("pass"),
	  dB   = cms.vdouble( 0.0, 2.0),
	  dzPV = cms.vdouble(-0.5, 0.5),

	  ## flags and conditions required at the denominator,
	  tag_pt = cms.vdouble(20. , 500.),
	  tag_IsoMu20 = cms.vstring("pass"),
	  tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
	  ),
#	BinToPDFmap = cms.vstring("voigtPlusExpo"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
	BinToPDFmap = cms.vstring("vpvPlusExpoMin70"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusCheb"), ## PDF to use, as defined below
	),

      PFTight_Iso_Pt_AllEta = cms.PSet(
	  #UnbinnedVariables = cms.vstring("mass","weight"),
	  UnbinnedVariables = cms.vstring("mass"),
	  EfficiencyCategoryAndState = cms.vstring("PFIsoTight", "below"),
	  BinnedVariables = cms.PSet(
	    pt     = cms.vdouble( 20, 25, 30, 40, 50, 60, 80, 120, 200 ),
	    abseta = cms.vdouble( 0.0, 2.4),
	    Tight2012 = cms.vstring("pass"),
	    dB   = cms.vdouble( 0.0, 2.0),
	    dzPV = cms.vdouble(-0.5, 0.5),

	    ## flags and conditions required at the denominator,
	    PF = cms.vstring("pass"),
	    tag_pt = cms.vdouble(20. , 500.),
	    tag_IsoMu20 = cms.vstring("pass"),
	    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
	    ),
#	BinToPDFmap = cms.vstring("voigtPlusExpo"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
	BinToPDFmap = cms.vstring("vpvPlusExpoMin70"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusCheb"), ## PDF to use, as defined below
	  ),

      Tight_Iso_Pt_Eta = cms.PSet(
	  #UnbinnedVariables = cms.vstring("mass","weight"),
	  UnbinnedVariables = cms.vstring("mass"),
	  EfficiencyCategoryAndState = cms.vstring("Tight_Iso_cut", "above"),
	  BinnedVariables = cms.PSet(
	    pt     = cms.vdouble( 20, 25, 30, 40, 50, 60, 120),
	    abseta = cms.vdouble( 0.0, 0.9, 1.2, 2.1,  2.4),
	    Tight2012 = cms.vstring("pass"),
	    dB   = cms.vdouble( 0.0, 2.0),
	    dzPV = cms.vdouble(-0.5, 0.5),

	    ## flags and conditions required at the denominator,
	    tag_pt = cms.vdouble(20. , 500.),
	    tag_IsoMu20 = cms.vstring("pass"),
	    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
	    ),
#	BinToPDFmap = cms.vstring("voigtPlusExpo"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
	BinToPDFmap = cms.vstring("vpvPlusExpoMin70"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusCheb"), ## PDF to use, as defined below
	  ),

      PFTight_Iso_Pt_Eta = cms.PSet(
	  #UnbinnedVariables = cms.vstring("mass","weight"),
	  UnbinnedVariables = cms.vstring("mass"),
	  EfficiencyCategoryAndState = cms.vstring("PFIsoTight", "below"),
	  BinnedVariables = cms.PSet(
	    pt     = cms.vdouble( 20, 25, 30, 40, 50, 60, 120),
	    abseta = cms.vdouble( 0.0, 0.9, 1.2, 2.1,  2.4),
	    Tight2012 = cms.vstring("pass"),
	    dB   = cms.vdouble( 0.0, 2.0),
	    dzPV = cms.vdouble(-0.5, 0.5),

	    ## flags and conditions required at the denominator,
	    PF = cms.vstring("pass"),
	    tag_pt = cms.vdouble(20. , 500.),
	    tag_IsoMu20 = cms.vstring("pass"),
	    tag_combRelIsoPF04dBeta = cms.vdouble(-0.5, 0.2),
	    ),
#	BinToPDFmap = cms.vstring("voigtPlusExpo"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
	BinToPDFmap = cms.vstring("vpvPlusExpoMin70"), ## PDF to use, as defined below
#	BinToPDFmap = cms.vstring("vpvPlusCheb"), ## PDF to use, as defined below
	  ),
      ),
    )
#
process.p1 = cms.Path(process.TnP_Muon_ID)
process.p2 = cms.Path(process.TnP_Muon_Iso)
