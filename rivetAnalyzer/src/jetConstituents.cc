#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"

#include <vector>
#include <TFile.h>
#include <TTree.h>

namespace Rivet {

  class jetConstituents : public Analysis {
  public:

    jetConstituents()
      : Analysis("jetConstituents")
    {  }
    float jr = 0.4; 
    void init() {
      const FastJets jets(FinalState(-10, 10, 0.0*GeV), FastJets::ANTIKT, jr);
      addProjection(jets, "Jets");
      rootOut = new TFile("jetConstituents.root", "RECREATE");
      tr = new TTree("jetConstituents", "jetConstituents");
 
      tr->Branch("evn", &evn, "evn/I");
      tr->Branch("pid", &pid);
      tr->Branch("jetPt", &jetPt);
      tr->Branch("jetY", &jetY);
      tr->Branch("jetPhi", &jetPhi);
      tr->Branch("cPt", &cPt);
      tr->Branch("cPhi", &cPhi);
      tr->Branch("cY", &cY);
    }
    void analyze(const Event& event) {
      const Jets& jets = applyProjection<FastJets>(event, "Jets").jetsByPt(30.0*GeV);
      evn = event.genEvent()->event_number();
      //double w = event.weight();
      jetPt.clear();
      jetY.clear();
      jetPhi.clear();
      pid.clear();

      for (auto j:jets){
        jetPt.push_back(j.momentum().pT());
        jetY.push_back(j.momentum().rapidity());
        jetPhi.push_back(j.momentum().phi());
        const Particles& jetConst = j.constituents();
        std::vector<int> tmpPID;
        std::vector<float> tmpPt;
        std::vector<float> tmpPhi;
        std::vector<float> tmpY;
        for (auto p:jetConst){
          tmpPID.push_back(p.pdgId());
          const FourMomentum & pM = p.momentum();
          tmpPt.push_back(pM.pT());
          tmpPhi.push_back(pM.phi());
          tmpY.push_back(pM.rapidity());
      
        }
        pid.push_back(tmpPID);
        cPt.push_back(tmpPt); 
        cPhi.push_back(tmpPhi); 
        cY.push_back(tmpY); 
      }
      tr->Fill();
    }

    void finalize() {
      tr->Write();
      rootOut->Write();
      rootOut->Close();
    }

  private:
    int evn;
    std::vector<float> jetPt, jetPhi, jetY;
    std::vector<std::vector<int>> pid;
    std::vector<std::vector<float>> cPt, cPhi, cY;
    TFile *rootOut;
    TTree *tr; 
  };

  DECLARE_RIVET_PLUGIN(jetConstituents);

}
