import FWCore.ParameterSet.Config as cms

process = cms.Process('MakingBacon')

# import of standard configurations
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load('Configuration/EventContent/EventContent_cff')
process.load('TrackingTools/TransientTrack/TransientTrackBuilder_cfi')

process.MessageLogger.cerr.FwkReport.reportEvery = 10
process.GlobalTag.globaltag = 'POSTLS170_V6::All'

#process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
process.load("RecoMET.METProducers.PFMET_cfi")
process.pfMetPuppi     = process.pfMet.clone()
#process.pfMetPuppi.src = cms.InputTag('puppi','Puppi')
process.load('RecoJets.Configuration.RecoGenJets_cff')
process.load('RecoJets.JetProducers.ak5PFJets_cfi')

## import custom configurations
#process.load('BaconProd/Ntupler/myJetExtras04_cff')    #include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras05_cff')    #include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras06_cff')    #include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras07_cff')    #include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras08_cff')    #include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras09_cff')    #include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myMETFilters_cff')   # apply MET filters set to tagging mode
#process.load('BaconProd/Ntupler/myMVAMet_cff')

from RecoJets.JetProducers.ak5PFJets_cfi        import ak5PFJets
#for each jet collection run Pruning, subjet b-tagging, quark gluon discrimination,n-subjettiness and subjet quark gluon discrimination
process.AK4PFJets = ak5PFJets.clone(
    rParam = cms.double(0.4),
    jetPtMin = cms.double(20)
    )

process.AK4PFJets.src         = cms.InputTag('puppi','Puppi')
#process.AK4caPFJetsPruned.src = cms.InputTag('puppi','Puppi')
#process.AK5PFJets.src         = cms.InputTag('puppi','Puppi')
#process.AK5caPFJetsPruned.src = cms.InputTag('puppi','Puppi')
#process.AK6PFJets.src         = cms.InputTag('puppi','Puppi')
#process.AK6caPFJetsPruned.src = cms.InputTag('puppi','Puppi')
#process.AK7PFJets.src         = cms.InputTag('puppi','Puppi')
#process.AK7caPFJetsPruned.src = cms.InputTag('puppi','Puppi')
#process.AK8PFJets.src         = cms.InputTag('puppi','Puppi')
#process.AK8caPFJetsPruned.src = cms.InputTag('puppi','Puppi')
#process.AK9PFJets.src         = cms.InputTag('puppi','Puppi')
#process.AK9caPFJetsPruned.src = cms.InputTag('puppi','Puppi')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source("PoolSource",
                            fileNames  = cms.untracked.vstring('file:/data/nbay04/c/benwu/JetMET_TP/SLHC20/QCD_Mark/step3_12235_SLHC20_140PU.root')
                            #fileNames  = cms.untracked.vstring('/store/relval/CMSSW_7_0_0/RelValTTbar_13/GEN-SIM-RECO/PU50ns_POSTLS170_V6_AlcaCSA14-v1/00000/0A982CAD-EFAE-E311-B131-0025905A6132.root')
                            #fileNames  = cms.untracked.vstring('/store/relval/CMSSW_7_1_0_pre5/RelValTTbar_13/GEN-SIM-RECO/PU50ns_POSTLS171_V2-v2/00000/4CCC03AC-BDBC-E311-8597-02163E00EA7F.root')
)
process.source.inputCommands = cms.untracked.vstring("keep *",
                                                     "drop *_MEtoEDMConverter_*_*")
import os
cmssw_base = os.environ['CMSSW_BASE']

process.load('Dummy/Puppi/Puppi_cff')

process.ntupler = cms.EDAnalyzer('NtuplerMod',
  skipOnHLTFail = cms.untracked.bool(False),
  outputName    = cms.untracked.string('Pup_vDZ.root'),
  TriggerFile   = cms.untracked.string(cmssw_base+"/src/BaconAna/DataFormats/data/HLTFile_v0"),

  useGen = cms.untracked.bool(True),
  genEventInfoName = cms.untracked.string('generator'),
  genParticlesName = cms.untracked.string('genParticles'),
  useMETFilters              = cms.untracked.bool(True),
  fillAllGen                 = cms.untracked.bool(False),
  pflowCandidatesName        = cms.untracked.InputTag('puppi','Puppi'),
  primaryVerticesName        = cms.untracked.string('offlinePrimaryVertices'),
  beamspotName               = cms.untracked.string('offlineBeamSpot'),
  pileupInfoName             = cms.untracked.string('addPileupInfo'),
  pflowMETName               = cms.untracked.string('pfMet'),
  rhoForIsolationName        = cms.untracked.string('fixedGridRhoFastjetAll'),
  rhoForJetsName             = cms.untracked.string('fixedGridRhoFastjetAll'),
  electronName               = cms.untracked.string('gedGsfElectrons'),
  muonName                   = cms.untracked.string('muons'),
  applyMuscle                = cms.untracked.bool(False),
  photonName                 = cms.untracked.string('gedPhotons'),
  tauName                    = cms.untracked.string('hpsPFTauProducer'),
  NumCones                   = cms.untracked.int32(6),
  MinCone                    = cms.untracked.double(0.4),
  ConeIter                   = cms.untracked.double(0.1),
  jetName                    = cms.untracked.string('PFJets'),
  genJetName                 = cms.untracked.string('GenJets'),
  jetFlavorName              = cms.untracked.string('byValAlgo'),
  jetFlavorPhysName          = cms.untracked.string('byValPhys'),
  pruneJetName               = cms.untracked.string('caPFJetsPruned'),
  subJetName                 = cms.untracked.string('caPFJetsPruned'),
  rhoName                    = cms.untracked.string('kt6PFJets'),
  csvBTagName                = cms.untracked.string('jetCombinedSecondaryVertexMVABJetTags'),
  csvBTagSubJetName          = cms.untracked.string('jetCombinedSecondaryVertexMVABJetTagsSJ'),
  jettiness                  = cms.untracked.string('Njettiness'),
  QGLikelihood               = cms.untracked.string('QGTagger'),
  QGLikelihoodSubjet         = cms.untracked.string('QGTaggerSubJets'),
  computeFullJetInfo         = cms.untracked.bool(True),
  trackName                  = cms.untracked.string('generalTracks'),
  conversionName             = cms.untracked.string('allConversions'),
  ecalBarrelSuperclusterName = cms.untracked.string('correctedHybridSuperClusters'),
  ecalEndcapSuperclusterName = cms.untracked.string('correctedMulti5x5SuperClustersWithPreshower'),
  ecalBarrelRecHitName       = cms.untracked.string('reducedEcalRecHitsEB'),
  ecalEndcapRecHitName       = cms.untracked.string('reducedEcalRecHitsEE')
)

#process.baconSequence = cms.Sequence(
                                     #process.puppi*
##                                     process.pfMetPuppi)
                                     ##process.metFilters*
                                     ##process.recojetsequence*
                                     ##process.genjetsequence*
                                     ##process.AK4jetsequence*
                                     ##process.AK4genjetsequence*
                                     ##process.AK5jetsequence*
                                     ##process.AK5genjetsequence*
                                     ##process.AK6jetsequence*
                                     ##process.AK6genjetsequence*
                                     ##process.AK7jetsequence*
                                     ##process.AK7genjetsequence*
                                     ##process.AK8jetsequence*
                                     ##process.AK8genjetsequence*
                                     ##process.AK9jetsequence*
                                     ##process.AK9genjetsequence*
##                                     process.recoTauClassicHPSSequence*   ### must come after antiktGenJets otherwise conflict on RecoJets/JetProducers/plugins#
					 #process.ak5PFJets*
                                     ##process.ak5GenJets*
                                     #process.MVAMetSeq)

process.baconSequence2 =  cms.Sequence( process.puppi* process.ak5PFJets* process.AK4PFJets)
                                       #process.ak5GenJets*
                                       #process.MVAMetSeq)

process.p = cms.Path(process.baconSequence2)

process.output = cms.OutputModule("PoolOutputModule",
                                  outputCommands = cms.untracked.vstring('keep *'),
                                  fileName       = cms.untracked.string ("BBB")
)

