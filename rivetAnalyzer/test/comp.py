import os, ROOT
ROOT.gROOT.SetBatch(1)

#out = open("comp.txt","w")
for y in range(1,301):
  r1 = ROOT.TFile("8TeVnom3/multiJetNom{:03}.root".format(y))
  r2 = ROOT.TFile("8TeVnom5/multiJetNom{:03}.root".format(y))
  tr1 = r1.Get("multiJetReW") 
  tr2 = r2.Get("multiJetReW") 
  a1 = []
  a2 = []
  b1 = [] 
  b2 = []
  c1 = []
  c2 = []
  d1 = []
  d2 = []
  for e in tr1:
    if e.dR23 < 1.0: a1.append(e.evn)
    if e.dR23 > 1.0: b1.append(e.evn)
    if e.pTR < 0.3: c1.append(e.evn)
    if e.pTR > 0.6: d1.append(e.evn)
  for e in tr2:
    if e.dR23 < 1.0: a2.append(e.evn)
    if e.dR23 > 1.0: b2.append(e.evn)
    if e.pTR < 0.3: c2.append(e.evn)
    if e.pTR > 0.6: d2.append(e.evn)
  #out.write("{:03}: a = {0:.2f}, b = {0:.2f}, c = {0:.2f}, d = {0:.2f}".format
  print y, len(set(a1) & set(a2))/float(len(a1))*100., len(set(b1) & set(b2))/float(len(b1))*100., len(set(c1) & set(c2))/float(len(c1))*100., len(set(d1) & set(d2))/float(len(d1))*100.


