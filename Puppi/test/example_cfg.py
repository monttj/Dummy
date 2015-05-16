import FWCore.ParameterSet.Config as cms

### command-line arguments
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('python')

options.register('globalTag', 'auto:startup',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    'Global Tag for Conditions Data'
)

options.register('output', 'test_output.root',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    'Output file name'
)

options.register('n', -1,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    'Maximum number of events to run on'
)

options.parseArguments()
###

process = cms.Process('USER')

### Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, options.globalTag)

### load default PAT sequence
process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff")
process.patseq = cms.Sequence(process.patCandidates * process.selectedPatCandidates)
process.p = cms.Path(process.patseq)

# remove unnecessary PAT modules
process.p.remove(process.makePatElectrons)
process.p.remove(process.makePatPhotons)
process.p.remove(process.makePatJets)
process.p.remove(process.makePatTaus)
process.p.remove(process.makePatMETs)
process.p.remove(process.patCandidateSummary)
process.p.remove(process.selectedPatElectrons)
process.p.remove(process.selectedPatPhotons)
process.p.remove(process.selectedPatJets)
process.p.remove(process.selectedPatTaus)
process.p.remove(process.selectedPatCandidateSummary)

### muon selection
process.selectedPatMuons.cut = 'pt>10 && abs(eta)<2.4'

# load user-defined particle collections (e.g. PUPPI)

# -- PF-Weighted
process.load('CommonTools.ParticleFlow.deltaBetaWeights_cff')

# -- PUPPI
from pfPUPPISequence_cff import *
load_pfPUPPI_sequence(process, 'pfPUPPISequence', algo = 'PUPPI',
  src_puppi = 'pfAllHadronsAndPhotonsForPUPPI',
  cone_puppi_central = 0.5
)

process.p.replace(
  process.pfParticleSelectionSequence,
  process.pfParticleSelectionSequence  *
  process.pfDeltaBetaWeightingSequence *
  process.pfPUPPISequence
)

# load user-defined muon PF-isolation values
muon_src, cone_size = 'selectedPatMuons', 0.4

from MuonPFIsolationSequence_cff import *
load_muonPFiso_sequence(process, 'MuonPFIsoSequenceSTAND', algo = 'R04STAND',
  src = muon_src,
  src_charged_hadron = 'pfAllChargedHadrons',
  src_neutral_hadron = 'pfAllNeutralHadrons',
  src_photon         = 'pfAllPhotons',
  src_charged_pileup = 'pfPileUpAllChargedParticles',
  coneR = cone_size
)

load_muonPFiso_sequence(process, 'MuonPFIsoSequencePFWGT', algo = 'R04PFWGT',
  src = muon_src,
  src_neutral_hadron = 'pfWeightedNeutralHadrons',
  src_photon         = 'pfWeightedPhotons',
  coneR = cone_size
)

load_muonPFiso_sequence(process, 'MuonPFIsoSequencePUPPI', algo = 'R04PUPPI',
  src = muon_src,
  src_charged_hadron = 'pfPUPPIChargedHadrons',
  src_neutral_hadron = 'pfPUPPINeutralHadrons',
  src_photon         = 'pfPUPPIPhotons',
  coneR = cone_size
)

process.MuonPFIsoSequences = cms.Sequence(
  process.MuonPFIsoSequenceSTAND *
  process.MuonPFIsoSequencePFWGT *
  process.MuonPFIsoSequencePUPPI
)

process.p.replace(
  process.selectedPatMuons,
  process.selectedPatMuons *
  process.MuonPFIsoSequences
)

# --- Input Configuration -------------------------------------------------------------
inputfile = ['/store/mc/Spring14dr/DYJetsToLL_M-50_13TeV-madgraph-pythia8/AODSIM/PU_S14_POSTLS170_V6-v1/00000/00E3A144-B2CB-E311-AB91-003048F02D36.root']
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring(inputfile))

# --- Output configuration ------------------------------------------------------------
process.out = cms.OutputModule('PoolOutputModule',
  fileName = cms.untracked.string(options.output),
  ## save only events passing the full path
  #SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
  outputCommands = cms.untracked.vstring([
    'keep *_OfflinePrimaryVertices_*_*',
    'keep *_selectedPatMuons_*_*',
    'keep *_muPFIsoValue*STAND_*_USER',
    'keep *_muPFIsoValue*PFWGT_*_USER',
    'keep *_muPFIsoValue*PUPPI_*_USER'
  ])
)

process.outpath = cms.EndPath(process.out)

### MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1

### Maximum Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.n) )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

