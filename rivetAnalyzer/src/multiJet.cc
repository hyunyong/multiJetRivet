#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"

#include <vector>
#include <string>
#include <TFile.h>
#include <TTree.h>
namespace Rivet {


  class multiJet : public Analysis {
  public:

    multiJet()
      : Analysis("multiJet")
    {    }
    float jr = 0.5; 
    int drBin = int(1.5-jr)*10;
    void init() {
      const FastJets jets(FinalState(-10, 10, 0.0*GeV), FastJets::ANTIKT, jr);
      addProjection(jets, "Jets");
      std::vector<double> ptrBin;
      ptrBin.push_back(0.0);ptrBin.push_back(0.1);ptrBin.push_back(0.2);ptrBin.push_back(0.3);ptrBin.push_back(0.4);ptrBin.push_back(0.6);ptrBin.push_back(0.9);
      _h1 = bookHisto1D("non_eta_high_pt_sdr_pt3_jet3_pt_jet2_pt", ptrBin);
      _h2 = bookHisto1D("non_eta_high_pt_ldr_pt3_jet3_pt_jet2_pt", ptrBin);
      _h3 = bookHisto1D("non_eta_high_pt_dr_lpt3_del_r23", drBin,jr,1.5);
      _h4 = bookHisto1D("non_eta_high_pt_dr_hpt3_del_r23", drBin,jr,1.5);
    }
    void analyze(const Event& event) {
      const Jets& jets = applyProjection<FastJets>(event, "Jets").jetsByPt(30.0*GeV);
      if (jets.size() < 3) vetoEvent;
      const FourMomentum jet1 = jets[0].momentum();
      const FourMomentum jet2 = jets[1].momentum();
      const FourMomentum jet3 = jets[2].momentum();
      

      if (jet1.pT() < 500*GeV) vetoEvent;
      if (jet1.absrapidity() > 2.5 || jet2.absrapidity() > 2.5) vetoEvent;

      const FourMomentum diJet = jet1 + jet2;
      if (diJet.mass() < 220*GeV) vetoEvent;


      double jet3_pt_jet2_pt = jet3.pT()/jet2.pT();
      if (jet3_pt_jet2_pt > 0.9) vetoEvent;

      double del_phi12 = mapAngleMPiToPi(jet2.phi() - jet1.phi());
      if (abs(abs(del_phi12) - M_PI) > 1.0) vetoEvent;

      double del_phi23 = mapAngleMPiToPi(jet3.phi() -  jet2.phi());
      double del_eta23 = sign(jet2.rapidity())*(jet3.rapidity() - jet2.rapidity());
      const double del_r23 = add_quad(del_eta23, del_phi23);
      if (!inRange(del_r23, jr, 1.5)) vetoEvent;

      double w = event.weight();
      if (inRange(jet1.pT(), 510*GeV,2500*GeV)){
         if (inRange(jet2.absrapidity(), 0, 2.5)){
           if (inRange(del_r23, jr,1.0)) _h1->fill(jet3_pt_jet2_pt, w);
           if (inRange(del_r23, 1.0,1.5)) _h2->fill(jet3_pt_jet2_pt, w);
           if (inRange(jet3_pt_jet2_pt, 0.0, 0.3)) _h3->fill(del_r23, w);
           if (inRange(jet3_pt_jet2_pt, 0.6, 0.9)) _h4->fill(del_r23, w);
         }
      }
    }


    void finalize() {

    }

  private:

    Histo1DPtr  _h1;
    Histo1DPtr  _h2;
    Histo1DPtr  _h3;
    Histo1DPtr  _h4;

  };

  DECLARE_RIVET_PLUGIN(multiJet);

}
