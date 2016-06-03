# Instruction

Start from the standard CATTools.

```
## Initialize work directory
cmsrel CMSSW_7_6_3_patch2
cd CMSSW_7_6_3_patch2/src
cmsenv
git-cms-init

## Add CATTools modification to CMSSW
git remote add vallot https://github.com/vallot/cmssw
git fetch vallot
git checkout cat76x

## Install Muon Tag and Probe additional packages
git cms-addpkg MuonAnalysis
git clone -n https://github.com/cms-analysis/MuonAnalysis-TagAndProbe TagAndProbe
cd TagAndProbe
git checkout 76X

## Install CATTools
cd $CMSSW_BASE/src
git clone -n https://github.com/vallot/CATTools
cd CATTools
git checkout cat76x
git submodule init
git submodule checkout

## Install LeptonAnalysis subpackage
cd $CMSSW_BASE/src/CATTools
git clone https://github.com/hep-skku/LeptonAnalysis

## Build the whole package
cd $CMSSW_BASE/src
scram b -j8
```
