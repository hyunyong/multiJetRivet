# multiJetRivet

```
scram p -n rivet CMSSW CMSSW_8_2_0
cd rivet/src
git clone git@github.com:hyunyong/multiJetRivet.git
scram b -j8
cd multiJetRivet/rivetAnalyzer/test
cmsRun QCD_powheg_v2_ct10_pytia8_cuetp8m1_rivet.py 1
```
