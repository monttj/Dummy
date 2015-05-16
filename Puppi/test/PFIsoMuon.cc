#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "Dummy/Puppi/test/PFIsoMuon.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"

PFIsoMuon::PFIsoMuon(const edm::ParameterSet& iConfig)
{
  inputTagMuons_ = iConfig.getParameter<edm::InputTag>("Muons");

  // not needed at the moment
  inputTagIsoDepMuons_ = iConfig.getParameter< std::vector<edm::InputTag> >("IsoDepMuon");
  inputTagIsoValMuons_   = iConfig.getParameter< std::vector<edm::InputTag> >("IsoValMuon");   

  printMuons_ = iConfig.getParameter<bool>("PrintMuons");

  // Control plots
  TFileDirectory dir = fileservice_->mkdir("PF ISO");
  chargedMuons_    = dir.make<TH1F>("chargedMuons",";Sum pT/pT" ,100,0,4);
  photonMuons_     = dir.make<TH1F>("photonMuons",";Sum pT/pT", 100,0,4);
  neutralMuons_    = dir.make<TH1F>("neutralMuons",";Sum pT/pT", 100,0,4);
  		      
  sumMuons_        = dir.make<TH1F>("allMuons",";Sum pT/pT",100,0,4);

}

PFIsoMuon::~PFIsoMuon(){;}

void 
PFIsoMuon::beginRun(edm::Run const&, edm::EventSetup const& ){;}

void PFIsoMuon::analyze(const edm::Event & iEvent,const edm::EventSetup & c)
{
  edm::Handle<reco::MuonCollection> MuonH;
  bool found = iEvent.getByLabel(inputTagMuons_,MuonH);
  if(!found ) {
    std::ostringstream  err;
    err<<" cannot get Muons: "
       <<inputTagMuons_<<std::endl;
    edm::LogError("PFIsoMuon")<<err.str();
    throw cms::Exception( "MissingProduct", err.str());
  }  

  // get the iso deposits. 3 (charged hadrons, photons, neutral hadrons)
  unsigned nTypes=3;
  IsoDepositMaps electronIsoDep(nTypes);

  for (size_t j = 0; j<inputTagIsoDepMuons_.size(); ++j) {
    iEvent.getByLabel(inputTagIsoDepMuons_[j], electronIsoDep[j]);
  }


  IsoDepositVals electronIsoVal(nTypes);

  // just renaming
  const IsoDepositVals * electronIsoVals = &electronIsoVal;

  for (size_t j = 0; j<inputTagIsoValMuons_.size(); ++j) {
    iEvent.getByLabel(inputTagIsoValMuons_[j], electronIsoVal[j]);
  }

  // Muons - from reco 
  if(printMuons_) {
    unsigned nele=MuonH->size();
    
    for(unsigned iele=0; iele<nele;++iele) {
      reco::MuonRef myMuonRef(MuonH,iele);
      
      double charged =  (*(*electronIsoVals)[0])[myMuonRef];
      double photon = (*(*electronIsoVals)[1])[myMuonRef];
      double neutral = (*(*electronIsoVals)[2])[myMuonRef];
      
      std::cout << "Muon: " << " run " << iEvent.id().run() << " lumi " << iEvent.id().luminosityBlock() << " event " << iEvent.id().event();
      std::cout << " pt " <<  myMuonRef->pt() << " eta " << myMuonRef->eta() << " phi " << myMuonRef->phi() << " charge " << myMuonRef->charge()<< " : ";
      std::cout << " ChargedIso " << charged ;
      std::cout << " PhotonIso " <<  photon ;
      std::cout << " NeutralHadron Iso " << neutral << std::endl;
      
      chargedMuons_ ->Fill(charged/myMuonRef->pt());
      photonMuons_->Fill(photon/myMuonRef->pt());
      neutralMuons_->Fill(neutral/myMuonRef->pt());
      sumMuons_->Fill((charged+photon+neutral)/myMuonRef->pt());
    }
  }

}
  

DEFINE_FWK_MODULE(PFIsoMuon);



