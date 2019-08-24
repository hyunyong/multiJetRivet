import os, ROOT, array
ROOT.gROOT.SetBatch(1)

#inF = ROOT.TFile("powheg8TeVnomNtuple.root")
inF = ROOT.TFile("testNom.root")
outF = ROOT.TFile("powheg8TeVnom.root","RECREATE")

a = ROOT.TH1D("non_eta_high_pt_sdr_pt3_jet3_pt_jet2_pt", "p_{T3}/p_{T2}", 5, array.array('d',[0.1,0.2,0.3,0.4,0.6,0.9]))
b = ROOT.TH1D("non_eta_high_pt_ldr_pt3_jet3_pt_jet2_pt", "p_{T3}/p_{T2}", 5, array.array('d',[0.1,0.2,0.3,0.4,0.6,0.9]))
c = ROOT.TH1D("non_eta_high_pt_dr_lpt3_del_r23", "#Delta R_{23}" ,9 ,0.6 ,1.5)
d = ROOT.TH1D("non_eta_high_pt_dr_hpt3_del_r23", "#Delta R_{23}" ,9 ,0.6 ,1.5)
tr = inF.Get("multiJetReW") 
for e in tr:
  if e.dR23 < 0.6: print e.evn, e.dR23, e.pTR
  if e.dR23 < 1.0: a.Fill(e.pTR)
  if e.dR23 > 1.0: b.Fill(e.pTR)
  if e.pTR < 0.3: c.Fill(e.dR23)
  if e.pTR > 0.6: d.Fill(e.dR23)
outF.Write()
outF.Close()
