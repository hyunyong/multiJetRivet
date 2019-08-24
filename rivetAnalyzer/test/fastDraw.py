import os, sys, ROOT
ROOT.gROOT.SetBatch(1)
def normHist(hist):
  intg = hist.Integral()
  hist.Scale(1.0/intg)
  for x in xrange(hist.GetNbinsX()):
    binW = hist.GetBinWidth(x+1)
    binC = hist.GetBinContent(x+1)
    binE = hist.GetBinError(x+1)
    hist.SetBinContent(x+1, binC/binW)
    hist.SetBinError(x+1, binE/binW)

rf = ROOT.TFile(sys.argv[1])
os.chdir("sys_draw")
c = ROOT.TCanvas("","",700,800)
key = rf.GetListOfKeys()
for x in key:
   print x.GetName()
   h = rf.Get(x.GetName())
   h.Sumw2()
   normHist(h)
   h.Draw("colz")
   c.SaveAs(sys.argv[1].replace(".root","_")+x.GetName()+".png")

