import FWCore.ParameterSet.Config as cms

puppiCentral = cms.VPSet(
                 cms.PSet(
                  algoId           = cms.untracked.int32(5),  #0 is default Puppi
                  useCharged       = cms.untracked.bool(True),
                  applyLowPUCorr   = cms.untracked.bool(True),
                  combOpt          = cms.untracked.int32(0),
                  cone             = cms.untracked.double(0.3),
                  rmsPtMin         = cms.untracked.double(0.1),
                  rmsScaleFactor   = cms.untracked.double(1.0)
                 )
                )

puppiForward = cms.VPSet(
                cms.PSet(
                 algoId         = cms.untracked.int32(5),  #0 is default Puppi
                 useCharged     = cms.untracked.bool(False),
                 applyLowPUCorr = cms.untracked.bool(True),
                 combOpt        = cms.untracked.int32(0),
                 cone           = cms.untracked.double(0.3),
                 rmsPtMin       = cms.untracked.double(0.1),
                 rmsScaleFactor = cms.untracked.double(1.0)
                 )
                )

puppi = cms.EDProducer("PuppiProducer",#cms.PSet(#"PuppiProducer",
                       PuppiName      = cms.untracked.string("Puppi"),
                       UseDeltaZCut   = cms.untracked.bool  (False),
                       DeltaZCut      = cms.untracked.double(0.3),
                       candName       = cms.untracked.string('particleFlow'),
                       PFcandName     = cms.InputTag('particleFlow'),
                       vertexName     = cms.untracked.string('offlinePrimaryVertices'),
                       applyCHS       = cms.untracked.bool  (True),
                       useExp         = cms.untracked.bool  (False),
                       MinNeutralPt   = cms.untracked.double(0.2),
                       MinNeutralPtSlope   = cms.untracked.double(0.015),
                       MinPuppiWeight = cms.untracked.double(0.01),
                       algos          = cms.VPSet(
                        cms.PSet(
                         etaMin = cms.untracked.double(-2.5),
                         etaMax = cms.untracked.double( 1.5),
                         ptMin  = cms.untracked.double(0.0),
                         MinNeutralPt   = cms.untracked.double(0.2),
                         MinNeutralPtSlope   = cms.untracked.double(0.015),
                         puppiAlgos = puppiCentral
                        ),
                        cms.PSet(
                         etaMin = cms.untracked.double(1.5),
                         etaMax = cms.untracked.double(3.8),
                         ptMin  = cms.untracked.double(0.5),
                         MinNeutralPt   = cms.untracked.double(0.2),
                         MinNeutralPtSlope   = cms.untracked.double(0.015),
                         puppiAlgos = puppiCentral
                        ),
                        cms.PSet(
                         etaMin = cms.untracked.double(3.8),
                         etaMax = cms.untracked.double(5.0),
                         ptMin  = cms.untracked.double(4.0),
                         MinNeutralPt   = cms.untracked.double(0.2),
                         MinNeutralPtSlope   = cms.untracked.double(0.015),
                         puppiAlgos = puppiForward
                        )
                      )
)
