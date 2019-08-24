#!/usr/bin/env python
import os, sys
path = sys.argv[1]

tmpList = [x for x in os.listdir(path) if x.endswith(".tar")]
if len(tmpList) != 300: 
  print "job has not been finished"
  exit()
for f in tmpList:
  if os.path.getsize(path+"/"+f) < 10000:
    print f+" has not been finished"
    exit()

newPath = path.split("_")[0]+"nom"+path.split("_")[1][1:]
os.system("mv "+path+" "+newPath)
os.chdir(newPath)
tList = [x for x in os.listdir(".") if x.endswith(".tar")]
os.system("rm *.sh")
os.system("rm *.sub")
os.system("rm *.log")
os.system("rm *.err")
os.system("rm *.out")

for x in tList:
  print x
  os.system("tar xf "+x)
  os.system("mv multiJetNom.root multiJetNom{:03}.root".format(int(x[3:6])))
  os.system("rm "+x)
os.system("rm *.yoda")
