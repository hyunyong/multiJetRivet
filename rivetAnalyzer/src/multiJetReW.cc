#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"

#include <vector>
#include <TFile.h>
#include <TTree.h>
namespace Rivet {


  class multiJetReW : public Analysis {
  public:

    multiJetReW()
      : Analysis("multiJetReW")
    {    }
    float jr = 0.5; 
    int drBin = 9;
    void init() {
      const FastJets jets(FinalState(-10, 10, 0.0*GeV), FastJets::ANTIKT, jr);
      addProjection(jets, "Jets");
      std::vector<double> ptrBin;
      ptrBin.push_back(0.1);ptrBin.push_back(0.2);ptrBin.push_back(0.3);ptrBin.push_back(0.4);ptrBin.push_back(0.6);ptrBin.push_back(0.9);
      _h1 = bookHisto1D("non_eta_high_pt_sdr_pt3_jet3_pt_jet2_pt", ptrBin);
      _h2 = bookHisto1D("non_eta_high_pt_ldr_pt3_jet3_pt_jet2_pt", ptrBin);
      _h3 = bookHisto1D("non_eta_high_pt_dr_lpt3_del_r23", drBin,jr+0.1,1.5);
      _h4 = bookHisto1D("non_eta_high_pt_dr_hpt3_del_r23", drBin,jr+0.1,1.5);
      rootOut = new TFile("multiJetNom.root", "RECREATE");
      tr = new TTree("multiJetReW", "multiJetReW");
      tr->Branch("evn", &evn, "evn/I");
      tr->Branch("dR23", &dR23, "dR23/F");
      tr->Branch("pTR", &pTR, "pTR/F");

    }
    void analyze(const Event& event) {
      const Jets& jets = applyProjection<FastJets>(event, "Jets").jetsByPt(30.0*GeV);

      if (jets.size() < 3) vetoEvent;

      const FourMomentum jet1 = jets[0].momentum();
      const FourMomentum jet2 = jets[1].momentum();
      const FourMomentum jet3 = jets[2].momentum();

      if (!inRange(jet1.pT(), 510*GeV,2500*GeV)) vetoEvent;
      if (jet1.absrapidity() > 2.5 || jet2.absrapidity() > 2.5) vetoEvent;

      double jet3_pt_jet2_pt = jet3.pT()/jet2.pT();
      if (jet3_pt_jet2_pt > 0.9) vetoEvent;
      if (jet3_pt_jet2_pt < 0.1) vetoEvent;

      double del_phi12 = mapAngleMPiToPi(jet2.phi() - jet1.phi());
      if (abs(abs(del_phi12) - M_PI) > 1.0) vetoEvent;

      double del_phi23 = mapAngleMPiToPi(jet3.phi() -  jet2.phi());
      double del_eta23 = sign(jet2.rapidity())*(jet3.rapidity() - jet2.rapidity());
      const double del_r23 = add_quad(del_eta23, del_phi23);
      if (!inRange(del_r23, jr+0.1, 1.5)) vetoEvent;

      double w = event.weight();
      evn = event.genEvent()->event_number();
      dR23 = del_r23;
      pTR = jet3_pt_jet2_pt;
      tr->Fill();
      if (inRange(del_r23, jr+0.1,1.0)) _h1->fill(jet3_pt_jet2_pt, w);
      if (inRange(del_r23, 1.0,1.5)) _h2->fill(jet3_pt_jet2_pt, w);
      if (inRange(jet3_pt_jet2_pt, 0.1, 0.3)) _h3->fill(del_r23, w);
      if (inRange(jet3_pt_jet2_pt, 0.6, 0.9)) _h4->fill(del_r23, w);
    }


    void finalize() {
      tr->Write();
      rootOut->Write();
      rootOut->Close();
    }

  private:
    int evn;
    float dR23, pTR;
    TFile *rootOut;
    TTree *tr; 
    Histo1DPtr  _h1;
    Histo1DPtr  _h2;
    Histo1DPtr  _h3;
    Histo1DPtr  _h4;

  };

  DECLARE_RIVET_PLUGIN(multiJetReW);

}
