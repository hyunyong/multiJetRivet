from ROOT import *
gROOT.SetBatch(1)
gStyle.SetOptStat(0)

tf = TFile("jetConstituents.root")
tr = tf.Get("jetConstituents")

pidList = {}
nConst = TH1D("numberOfJetConstituents", "Number Of Jet Constituents",100,0,100)
for e in tr:
  for cons in e.pid:
    nConst.Fill(len(cons))
    for p in  cons:
      if abs(p) in  pidList:
        pidList[abs(p)] += 1
      else:  pidList[abs(p)] = 1

keys = pidList.keys()
keys.sort()
pdgid = {11:"e", 13:"#mu", 22:"#gamma", 130:"K_{L}", 211:"#pi^{+}", 310:"K_{S}", 321:"K^{+}", 2112:"#eta", 2212:"p", 3112:"#Sigma^{-}", 3122:"#Lambda", 3222:"#Sigma^{+}", 3312:"#Xi^{-}", 3322:"#Xi^{0}", 3334:"#Omega^{-}"}

pidHist = TH1D("PID", "PID", len(keys), 0, len(keys))
for i,x in enumerate(keys):
  #pidHist.GetXaxis().SetBinLabel(i+1, pdgid[x])
  pidHist.GetXaxis().SetBinLabel(i+1, "%d"%x)
  pidHist.SetBinContent(i+1, pidList[x])

c = TCanvas("","",800, 600)
pidHist.SetLineWidth(2)
pidHist.SetLineColor(kRed-4)
pidHist.Draw("HIST")
c.SaveAs("pid.png")
nConst.SetLineWidth(2)
nConst.SetLineColor(kRed-4)
nConst.Draw("HIST")
c.SaveAs("nConst.png")

