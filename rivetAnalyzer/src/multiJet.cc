#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"

#include <vector>
namespace Rivet {


  class multiJet : public Analysis {
  public:

    multiJet() : Analysis("multiJet") { }

    double jr = 0.4; //8 Tev: 0.5, 13 TeV: 0.4 
    double min_pT_cut = 30.0;
    double j1_min_pT_cut = 510.0;
    double j1_max_pT_cut = 2500.0;
    double j1_2_y_cut = 2.5;
    double min_dR = jr+0.1;
    double max_dR = 1.5;
    double min_pTR = 0.1;
    double max_pTR = 0.9;
    double dR_cut = 1.0;
    double low_pTR_cut = 0.3;
    double high_pTR_cut = 0.6;

    void init() {
      const FastJets jets(FinalState(), FastJets::ANTIKT, jr);
      declare(jets, "jets");
      // hist book
      std::vector<double> ptrBin = {0.1, 0.2, 0.3, 0.4, 0.6, 0.9};
      int drBin = int((max_dR-min_dR)*10.0);
      book(_h1, "non_eta_high_pt_sdr_pt3_jet3_pt_jet2_pt", ptrBin);
      book(_h2, "non_eta_high_pt_ldr_pt3_jet3_pt_jet2_pt", ptrBin);
      book(_h3, "non_eta_high_pt_dr_lpt3_del_r23", drBin,min_dR,max_dR);
      book(_h4, "non_eta_high_pt_dr_hpt3_del_r23", drBin,min_dR,max_dR);
    }
    void analyze(const Event& event) {
      const Jets& jets = apply<JetAlg>(event, "jets").jetsByPt(Cuts::absrap < j1_2_y_cut+max_dR  && Cuts::pT > min_pT_cut*GeV);
      if (jets.size() < 3) vetoEvent;
      const FourMomentum jet1 = jets[0].momentum();
      const FourMomentum jet2 = jets[1].momentum();
      const FourMomentum jet3 = jets[2].momentum();
      
      if (!inRange(jet1.pT(), j1_min_pT_cut*GeV, j1_max_pT_cut*GeV)) vetoEvent;
      if (jet1.absrapidity() > j1_2_y_cut || jet2.absrapidity() > j1_2_y_cut) vetoEvent;
      double del_phi12 = mapAngleMPiToPi(jet2.phi() - jet1.phi());
      if (abs(abs(del_phi12) - M_PI) > 1.0) vetoEvent;

      double jet3_pt_jet2_pt = jet3.pT()/jet2.pT();
      if (!inRange(jet3_pt_jet2_pt, min_pTR, max_pTR)) vetoEvent;

      double del_phi23 = mapAngleMPiToPi(jet3.phi() -  jet2.phi());
      double del_eta23 = sign(jet2.rapidity())*(jet3.rapidity() - jet2.rapidity());
      const double del_r23 = add_quad(del_eta23, del_phi23);
      if (!inRange(del_r23, min_dR, max_dR)) vetoEvent;

      if (inRange(del_r23, min_dR, dR_cut)) _h1->fill(jet3_pt_jet2_pt);
      if (inRange(del_r23, dR_cut, max_dR)) _h2->fill(jet3_pt_jet2_pt);
      if (inRange(jet3_pt_jet2_pt, min_pTR, low_pTR_cut)) _h3->fill(del_r23);
      if (inRange(jet3_pt_jet2_pt, high_pTR_cut, max_pTR)) _h4->fill(del_r23);
    }


    void finalize() {
      scale(_h1, 1.0/_h1->numEntries());
      scale(_h2, 1.0/_h2->numEntries());
      scale(_h3, 1.0/_h3->numEntries());
      scale(_h4, 1.0/_h4->numEntries());
    }

  private:

    Histo1DPtr  _h1;
    Histo1DPtr  _h2;
    Histo1DPtr  _h3;
    Histo1DPtr  _h4;

  };

  DECLARE_RIVET_PLUGIN(multiJet);

}
