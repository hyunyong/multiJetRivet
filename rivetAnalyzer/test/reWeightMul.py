import multiprocessing
import os, ROOT, array
ROOT.gROOT.SetBatch(1)

path = "/xrootd_user/hyunyong/xrootd/powhegRW/"

def rw(dat):
  tmp = open(dat)
  rw_ = {}
  for x in tmp:
    l = x.split()
    rw_[int(l[0])] = float(l[1])
  return rw_

def makeHist(case, reWList):
  for scale in reWList:
    print case, scale
    if not scale in os.listdir("."): os.mkdir(scale)
    for y in range(1,301):
      rw_ = rw(path+"/"+scale+"/newWeight{:03}.dat".format(y))
      inF = ROOT.TFile("8TeVnom{}/multiJetNom{:03}.root".format(case,y))
      outF = ROOT.TFile(scale+"/rwHist8TeV{:03}_{}.root".format(y,case),"RECREATE")
  
      a = ROOT.TH1D("non_eta_high_pt_sdr_pt3_jet3_pt_jet2_pt", "p_{T3}/p_{T2}", 5, array.array('d',[0.1,0.2,0.3,0.4,0.6,0.9]))
      b = ROOT.TH1D("non_eta_high_pt_ldr_pt3_jet3_pt_jet2_pt", "p_{T3}/p_{T2}", 5, array.array('d',[0.1,0.2,0.3,0.4,0.6,0.9]))
      c = ROOT.TH1D("non_eta_high_pt_dr_lpt3_del_r23", "#Delta R_{23}" ,9 ,0.6 ,1.5)
      d = ROOT.TH1D("non_eta_high_pt_dr_hpt3_del_r23", "#Delta R_{23}" ,9 ,0.6 ,1.5)
  
      tr = inF.Get("multiJetReW") 
      for e in tr:
        if e.dR23 < 1.0: a.Fill(e.pTR, rw_[e.evn])
        if e.dR23 > 1.0: b.Fill(e.pTR, rw_[e.evn])
        if e.pTR < 0.3: c.Fill(e.dR23, rw_[e.evn])
        if e.pTR > 0.6: d.Fill(e.dR23, rw_[e.evn])
      outF.Write()
      outF.Close()


if __name__ == "__main__":
  reWList = ["powheg8TeVPDF{}".format(x) for x in range(1,53)]
  reWList = ["powheg8TeVCase{}".format(x) for x in range(1,7)]
  jobs = []
  for x in reWList:
    if not x in os.listdir("."): os.mkdir(x)
  for x in range(1,8):
    p = multiprocessing.Process(target=makeHist, args=(x,reWList,)) 
    jobs.append(p)
    p.start() 

