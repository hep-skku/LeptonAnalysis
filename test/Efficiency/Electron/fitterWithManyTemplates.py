import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import PhysicsTools.TagAndProbe.commonFit as common
#import PhysicsTools.TagAndProbe.parametricTemplatesWP80MC as common

options = VarParsing('analysis')
options.register(
    "isMC",
    #True,
    False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Compute efficiency for MC"
    )

options.register(
    "inputFileName",
#    "/afs/cern.ch/work/i/ishvetso/public/for_Matteo/TnPTree_mc-powheg.root",
    #"TnPTree_mc_DYJets.root",
    "TnPTree_data_2015.root",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Input filename"
    )

options.register(
    "outputFileName",
    "MCTemplate",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Output filename"
    )

options.register(
    "idName",
    "passingMedium",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "ID variable name as in the fitter_tree"
    )

options.register(
    "dirName",
    "GsfElectronToRECO",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Folder name containing the fitter_tree"
    )

options.register(
    "doCutAndCount",
    False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Do not compute fitting, just cut and count"
    )
options.parseArguments()

process = cms.Process("TagProbe")
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

################################################

InputFileName = options.inputFileName
OutputFile = "efficiency-mc-"+options.idName
if (not options.isMC):
    OutputFile = "efficiency-data-"+options.idName

if (options.outputFileName != ""):
    OutputFile = OutputFile+"-"+options.outputFileName+".root"
else:
    OutputFile = OutputFile+".root"

################################################

#specifies the binning of parameters
EfficiencyBins = cms.PSet(
    probe_Ele_pt = cms.vdouble(10.0, 20.0 , 30.0, 40.0, 50.0, 2000.0),
    probe_Ele_eta = cms.vdouble(-2.5, -2.0, -1.566, -1.4442, -1.0, 0.0, 1.0, 1.4442, 1.566, 2.0, 2.5),
    )

DataBinningSpecification = cms.PSet(
    UnbinnedVariables = cms.vstring("mass"),
    BinnedVariables = cms.PSet(EfficiencyBins),
    BinToPDFmap = cms.vstring(
        "pdf_10p0To20p0_m2p5Tom2p0",
        "*pt_bin0*eta_bin0*","pdf_10p0To20p0_m2p5Tom2p0",
        "*pt_bin1*eta_bin0*","pdf_20p0To30p0_m2p5Tom2p0",
        "*pt_bin2*eta_bin0*","pdf_30p0To40p0_m2p5Tom2p0",
        "*pt_bin3*eta_bin0*","pdf_40p0To50p0_m2p5Tom2p0",
        "*pt_bin4*eta_bin0*","pdf_50p0To2000p0_m2p5Tom2p0",
  
        "*pt_bin0*eta_bin1*","pdf_10p0To20p0_m2p0Tom1p566",
        "*pt_bin1*eta_bin1*","pdf_20p0To30p0_m2p0Tom1p566",
        "*pt_bin2*eta_bin1*","pdf_30p0To40p0_m2p0Tom1p566",
        "*pt_bin3*eta_bin1*","pdf_40p0To50p0_m2p0Tom1p566",
        "*pt_bin4*eta_bin1*","pdf_50p0To2000p0_m2p0Tom1p566",

        "*pt_bin0*eta_bin2*","pdf_10p0To20p0_m1p566Tom1p4442",
        "*pt_bin1*eta_bin2*","pdf_20p0To30p0_m1p566Tom1p4442",
        "*pt_bin2*eta_bin2*","pdf_30p0To40p0_m1p566Tom1p4442",
        "*pt_bin3*eta_bin2*","pdf_40p0To50p0_m1p566Tom1p4442",
        "*pt_bin4*eta_bin2*","pdf_50p0To2000p0_m1p566Tom1p4442",

        "*pt_bin0*eta_bin3*","pdf_10p0To20p0_m1p4442Tom1p0",
        "*pt_bin1*eta_bin3*","pdf_20p0To30p0_m1p4442Tom1p0",
        "*pt_bin2*eta_bin3*","pdf_30p0To40p0_m1p4442Tom1p0",
        "*pt_bin3*eta_bin3*","pdf_40p0To50p0_m1p4442Tom1p0",
        "*pt_bin4*eta_bin3*","pdf_50p0To2000p0_m1p4442Tom1p0",

        "*pt_bin0*eta_bin4*","pdf_10p0To20p0_m1p0To0p0",
        "*pt_bin1*eta_bin4*","pdf_20p0To30p0_m1p0To0p0",
        "*pt_bin2*eta_bin4*","pdf_30p0To40p0_m1p0To0p0",
        "*pt_bin3*eta_bin4*","pdf_40p0To50p0_m1p0To0p0",
        "*pt_bin4*eta_bin4*","pdf_50p0To2000p0_m1p0To0p0",

        "*pt_bin0*eta_bin5*","pdf_10p0To20p0_0p0To1p0",
        "*pt_bin1*eta_bin5*","pdf_20p0To30p0_0p0To1p0",
        "*pt_bin2*eta_bin5*","pdf_30p0To40p0_0p0To1p0",
        "*pt_bin3*eta_bin5*","pdf_40p0To50p0_0p0To1p0",
        "*pt_bin4*eta_bin5*","pdf_50p0To2000p0_0p0To1p0",

        "*pt_bin0*eta_bin6*","pdf_10p0To20p0_1p0To1p4442",
        "*pt_bin1*eta_bin6*","pdf_20p0To30p0_1p0To1p4442",
        "*pt_bin2*eta_bin6*","pdf_30p0To40p0_1p0To1p4442",
        "*pt_bin3*eta_bin6*","pdf_40p0To50p0_1p0To1p4442",
        "*pt_bin4*eta_bin6*","pdf_50p0To2000p0_1p0To1p4442",

        "*pt_bin0*eta_bin7*","pdf_10p0To20p0_1p4442To1p566",
        "*pt_bin1*eta_bin7*","pdf_20p0To30p0_1p4442To1p566",
        "*pt_bin2*eta_bin7*","pdf_30p0To40p0_1p4442To1p566",
        "*pt_bin3*eta_bin7*","pdf_40p0To50p0_1p4442To1p566",
        "*pt_bin4*eta_bin7*","pdf_50p0To2000p0_1p4442To1p566",

        "*pt_bin0*eta_bin8*","pdf_10p0To20p0_1p566To2p0",
        "*pt_bin1*eta_bin8*","pdf_20p0To30p0_1p566To2p0",
        "*pt_bin2*eta_bin8*","pdf_30p0To40p0_1p566To2p0",
        "*pt_bin3*eta_bin8*","pdf_40p0To50p0_1p566To2p0",
        "*pt_bin4*eta_bin8*","pdf_50p0To2000p0_1p566To2p0",

        "*pt_bin0*eta_bin9*","pdf_10p0To20p0_2p0To2p5",
        "*pt_bin1*eta_bin9*","pdf_20p0To30p0_2p0To2p5",
        "*pt_bin2*eta_bin9*","pdf_30p0To40p0_2p0To2p5",
        "*pt_bin3*eta_bin9*","pdf_40p0To50p0_2p0To2p5",
        "*pt_bin4*eta_bin9*","pdf_50p0To2000p0_2p0To2p5",

        )
    )

McBinningSpecification = cms.PSet(
    UnbinnedVariables = cms.vstring("mass", "totWeight"),
    BinnedVariables = cms.PSet(EfficiencyBins, mcTrue = cms.vstring("true")),
    BinToPDFmap = cms.vstring(
        "pdf_10p0To20p0_m2p5Tom2p0",
        "*pt_bin0*eta_bin0*","pdf_10p0To20p0_m2p5Tom2p0",
        "*pt_bin1*eta_bin0*","pdf_20p0To30p0_m2p5Tom2p0",
        "*pt_bin2*eta_bin0*","pdf_30p0To40p0_m2p5Tom2p0",
        "*pt_bin3*eta_bin0*","pdf_40p0To50p0_m2p5Tom2p0",
        "*pt_bin4*eta_bin0*","pdf_50p0To2000p0_m2p5Tom2p0",
  
        "*pt_bin0*eta_bin1*","pdf_10p0To20p0_m2p0Tom1p566",
        "*pt_bin1*eta_bin1*","pdf_20p0To30p0_m2p0Tom1p566",
        "*pt_bin2*eta_bin1*","pdf_30p0To40p0_m2p0Tom1p566",
        "*pt_bin3*eta_bin1*","pdf_40p0To50p0_m2p0Tom1p566",
        "*pt_bin4*eta_bin1*","pdf_50p0To2000p0_m2p0Tom1p566",

        "*pt_bin0*eta_bin2*","pdf_10p0To20p0_m1p566Tom1p4442",
        "*pt_bin1*eta_bin2*","pdf_20p0To30p0_m1p566Tom1p4442",
        "*pt_bin2*eta_bin2*","pdf_30p0To40p0_m1p566Tom1p4442",
        "*pt_bin3*eta_bin2*","pdf_40p0To50p0_m1p566Tom1p4442",
        "*pt_bin4*eta_bin2*","pdf_50p0To2000p0_m1p566Tom1p4442",

        "*pt_bin0*eta_bin3*","pdf_10p0To20p0_m1p4442Tom1p0",
        "*pt_bin1*eta_bin3*","pdf_20p0To30p0_m1p4442Tom1p0",
        "*pt_bin2*eta_bin3*","pdf_30p0To40p0_m1p4442Tom1p0",
        "*pt_bin3*eta_bin3*","pdf_40p0To50p0_m1p4442Tom1p0",
        "*pt_bin4*eta_bin3*","pdf_50p0To2000p0_m1p4442Tom1p0",

        "*pt_bin0*eta_bin4*","pdf_10p0To20p0_m1p0To0p0",
        "*pt_bin1*eta_bin4*","pdf_20p0To30p0_m1p0To0p0",
        "*pt_bin2*eta_bin4*","pdf_30p0To40p0_m1p0To0p0",
        "*pt_bin3*eta_bin4*","pdf_40p0To50p0_m1p0To0p0",
        "*pt_bin4*eta_bin4*","pdf_50p0To2000p0_m1p0To0p0",

        "*pt_bin0*eta_bin5*","pdf_10p0To20p0_0p0To1p0",
        "*pt_bin1*eta_bin5*","pdf_20p0To30p0_0p0To1p0",
        "*pt_bin2*eta_bin5*","pdf_30p0To40p0_0p0To1p0",
        "*pt_bin3*eta_bin5*","pdf_40p0To50p0_0p0To1p0",
        "*pt_bin4*eta_bin5*","pdf_50p0To2000p0_0p0To1p0",

        "*pt_bin0*eta_bin6*","pdf_10p0To20p0_1p0To1p4442",
        "*pt_bin1*eta_bin6*","pdf_20p0To30p0_1p0To1p4442",
        "*pt_bin2*eta_bin6*","pdf_30p0To40p0_1p0To1p4442",
        "*pt_bin3*eta_bin6*","pdf_40p0To50p0_1p0To1p4442",
        "*pt_bin4*eta_bin6*","pdf_50p0To2000p0_1p0To1p4442",

        "*pt_bin0*eta_bin7*","pdf_10p0To20p0_1p4442To1p566",
        "*pt_bin1*eta_bin7*","pdf_20p0To30p0_1p4442To1p566",
        "*pt_bin2*eta_bin7*","pdf_30p0To40p0_1p4442To1p566",
        "*pt_bin3*eta_bin7*","pdf_40p0To50p0_1p4442To1p566",
        "*pt_bin4*eta_bin7*","pdf_50p0To2000p0_1p4442To1p566",

        "*pt_bin0*eta_bin8*","pdf_10p0To20p0_1p566To2p0",
        "*pt_bin1*eta_bin8*","pdf_20p0To30p0_1p566To2p0",
        "*pt_bin2*eta_bin8*","pdf_30p0To40p0_1p566To2p0",
        "*pt_bin3*eta_bin8*","pdf_40p0To50p0_1p566To2p0",
        "*pt_bin4*eta_bin8*","pdf_50p0To2000p0_1p566To2p0",

        "*pt_bin0*eta_bin9*","pdf_10p0To20p0_2p0To2p5",
        "*pt_bin1*eta_bin9*","pdf_20p0To30p0_2p0To2p5",
        "*pt_bin2*eta_bin9*","pdf_30p0To40p0_2p0To2p5",
        "*pt_bin3*eta_bin9*","pdf_40p0To50p0_2p0To2p5",
        "*pt_bin4*eta_bin9*","pdf_50p0To2000p0_2p0To2p5",

        )
)

########################

process.TnPMeasurement = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
                                        InputFileNames = cms.vstring(InputFileName),
                                        InputDirectoryName = cms.string(options.dirName),
                                        InputTreeName = cms.string("fitter_tree"), 
                                        OutputFileName = cms.string(OutputFile),
                                        NumCPU = cms.uint32(8),
                                        SaveWorkspace = cms.bool(False), #VERY TIME CONSUMING FOR MC
                                        doCutAndCount = cms.bool(options.doCutAndCount),
                                        floatShapeParameters = cms.bool(True),
                                        binnedFit = cms.bool(True),
                                        binsForFit = cms.uint32(60),
                                        WeightVariable = cms.string("totWeight"),
                                        # defines all the real variables of the probes available in the input tree and intended for use in the efficiencies
                                        Variables = cms.PSet(
        mass = cms.vstring("Tag-Probe Mass", "60.0", "120.0", "GeV/c^{2}"),
        #probe_Ele_et = cms.vstring("Probe E_{T}", "0", "100", "GeV/c"),
        #probe_sc_eta = cms.vstring("Probe #eta", "-2.5", "2.5", ""), 
	probe_Ele_pt = cms.vstring("Probe P_{T}", "0.0", "2000.0", "GeV/c"),
	probe_Ele_eta = cms.vstring("Probe #eta", "-2.5", "2.5", ""),
        totWeight = cms.vstring("totWeight", "-1000000", "100000000", ""),
        ),
                                        
                                        # defines all the discrete variables of the probes available in the input tree and intended for use in the efficiency calculation
                                        Expressions = cms.PSet(),
                                        Categories = cms.PSet(),
                                        PDFs = common.all_pdfs,
                                        Efficiencies = cms.PSet()
                                        )

setattr(process.TnPMeasurement.Categories, options.idName, cms.vstring(options.idName, "dummy[pass=1,fail=0]"))
setattr(process.TnPMeasurement.Categories, "mcTrue", cms.vstring("MC true", "dummy[true=1,false=0]"))

if (not options.isMC):
    delattr(process.TnPMeasurement, "WeightVariable")
    process.TnPMeasurement.Variables = cms.PSet(
        mass = cms.vstring("Tag-Probe Mass", "60.0", "120.0", "GeV/c^{2}"),
        probe_Ele_pt = cms.vstring("Probe P_{T}", "10", "2000", "GeV/c"),
        probe_Ele_eta = cms.vstring("Probe #eta", "-2.5", "2.5", ""), 
        )
    for pdf in process.TnPMeasurement.PDFs.__dict__:
        param =  process.TnPMeasurement.PDFs.getParameter(pdf)
        if (type(param) is not cms.vstring):
            continue
        for i, l in enumerate(getattr(process.TnPMeasurement.PDFs, pdf)):
            if l.find("signalFractionInPassing") != -1:
                getattr(process.TnPMeasurement.PDFs, pdf)[i] = l.replace("[1.0]","[0.5,0.,1.]")

    setattr(process.TnPMeasurement.Efficiencies, options.idName, DataBinningSpecification)    
    setattr(getattr(process.TnPMeasurement.Efficiencies, options.idName) , "EfficiencyCategoryAndState", cms.vstring(options.idName, "pass"))
else:   
    setattr(process.TnPMeasurement.Efficiencies, "MCtruth_" + options.idName, McBinningSpecification)    
    setattr(getattr(process.TnPMeasurement.Efficiencies, "MCtruth_" + options.idName), "EfficiencyCategoryAndState", cms.vstring(options.idName, "pass"))

    for pdf in process.TnPMeasurement.PDFs.__dict__:
        param =  process.TnPMeasurement.PDFs.getParameter(pdf)
        if (type(param) is not cms.vstring):
            continue
        for i, l in enumerate(getattr(process.TnPMeasurement.PDFs, pdf)):
            if l.find("backgroundPass") != -1:
                #getattr(process.TnPMeasurement.PDFs, pdf)[i] = "RooPolynomial::backgroundPass(mass, a[0.0, -10, 10], b[0.0, -10, 10], c[0.0, -10, 10])"
                getattr(process.TnPMeasurement.PDFs, pdf)[i] = "RooPolynomial::backgroundPass(mass, a[0.0, -10, 10])"
            if l.find("backgroundFail") != -1:
                #getattr(process.TnPMeasurement.PDFs, pdf)[i] = "RooPolynomial::backgroundFail(mass, a[0.0, -10, 10], b[0.0, -10, 10], c[0.0, -10, 10])"
                getattr(process.TnPMeasurement.PDFs, pdf)[i] = "RooPolynomial::backgroundFail(mass, a[0.0, -10, 10])"

process.fit = cms.Path(
    process.TnPMeasurement  
    )


