#ifndef PFISOREADERDEMO_H
#define PFISOREADERDEMO_H
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include <iostream>
#include <string>
#include <map>

#include "TH2F.h"


class PFIsoMuon : public edm::EDAnalyzer
{
 public:
  explicit PFIsoMuon(const edm::ParameterSet&);
  ~PFIsoMuon();
  virtual void beginRun(edm::Run const&, edm::EventSetup const& );
  virtual void analyze(const edm::Event & iEvent,const edm::EventSetup & c);

  typedef std::vector< edm::Handle< edm::ValueMap<reco::IsoDeposit> > > IsoDepositMaps;
  typedef std::vector< edm::Handle< edm::ValueMap<double> > > IsoDepositVals;

 private:
  
  bool printMuons_;
  
  void plotIsoDeposits(const IsoDepositMaps & depmap, const reco::MuonRef & ref,
		       double&, double&, double&) ;
  
 //This analyzer produces a file with a tree so we need,
  edm::Service<TFileService> fileservice_;

  edm::InputTag inputTagMuons_;
  std::vector<edm::InputTag> inputTagIsoDepMuons_;
  std::vector<edm::InputTag> inputTagIsoValMuons_;   

  // Control histos
  TH1F* chargedMuons_  ; 
  TH1F* photonMuons_   ; 
  TH1F* neutralMuons_  ; 
  TH1F* sumMuons_      ;

};
#endif

