# multiJetRivet

```
scram p -n rivet CMSSW CMSSW_11_0_1
cd rivet/src
git clone git@github.com:hyunyong/multiJetRivet.git -b CMSSW_11_0_1
scram b -j8
cd multiJetRivet/rivetAnalyzer/test
cmsRun QCD_TuneCUETP8M1_13TeV_pythia8_rivet.py 100000 1 250 2500
```
