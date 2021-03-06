import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")
process.load("FWCore.MessageLogger.MessageLogger_cfi")

#-------------
# DQM services
#-------------

# process.load("DQMServices.Core.DQM_cfg")
process.load("CondCore.DBCommon.CondDBCommon_cfi")
process.load("CondCore.DBCommon.CondDBSetup_cfi")

#-----------------------------
# Magnetic Field
#-----------------------------

process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')

#-------------------------------------------------
# GEOMETRY
#-------------------------------------------------

process.load("Configuration.StandardSequences.Geometry_cff")


#-------------------------------------------------
# GLOBALTAG
#-------------------------------------------------

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "GR_E_V25::All"


#-------------------------
#  Reconstruction Modules
#-------------------------

#process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
##process.load("Configuration.StandardSequences.ReconstructionCosmics_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("RecoVertex.BeamSpotProducer.BeamSpot_cff")

# Real data raw to digi
# process.load("EventFilter.SiPixelRawToDigi.SiPixelRawToDigi_cfi")
# process.siPixelDigis.InputLabel = 'source'
# process.siPixelDigis.IncludeErrors = True

# Local Reconstruction
process.load("RecoLocalTracker.SiPixelRecHits.PixelCPEESProducers_cff")
# process.load("RecoLocalTracker.SiPixelClusterizer.SiPixelClusterizer_cfi")
# process.load("EventFilter.SiStripRawToDigi.SiStripRawToDigis_standard_cff")
# process.siStripDigis.ProductLabel = 'source'

# process.load("RecoLocalTracker.SiStripClusterizer.SiStripClusterizer_cfi")
# process.load("RecoLocalTracker.SiStripRecHitConverter.SiStripRecHitConverter_cfi")
# process.load("RecoLocalTracker.SiStripRecHitConverter.SiStripRecHitMatcher_cfi")
# process.load("RecoLocalTracker.SiStripRecHitConverter.StripCPEfromTrackAngle_cfi")
# process.load("RecoLocalTracker.SiStripZeroSuppression.SiStripZeroSuppression_cfi")

##
## Needed when running on RAW:
##
# change strip cluster threshold to reduce noise effects
##process.siStripClusters.Clusterizer.ClusterThreshold = 9
##process.siStripClusters.Clusterizer.SeedThreshold = 6
##process.siStripClusters.Clusterizer.ChannelThreshold = 4

##
## Needed when running on RECO:
##
## Fitter-smoother: loosen outlier rejection as for first data-taking with LHC "collisions"
#process.KFFittingSmootherWithOutliersRejectionAndRK.BreakTrajWith2ConsecutiveMissing =False
#process.KFFittingSmootherWithOutliersRejectionAndRK.EstimateCut = 1000
#process.KFFittingSmootherWithOutliersRejectionAndRK.NoInvalidHitsBeginEnd = False
#process.KFFittingSmootherWithOutliersRejectionAndRK.LogPixelProbabilityCut =  -16.0


#-------------------------
#  Track Refitter
#-------------------------

process.load("RecoTracker.TrackProducer.TrackRefitters_cff")

process.ctfRefitter = process.TrackRefitterP5.clone()
process.ctfRefitter.src = 'ctfWithMaterialTracksP5'
process.ctfRefitter.TrajectoryInEvent = True

process.ckfRefitter = process.TrackRefitter.clone()
process.ckfRefitter.src = 'generalTracks'
process.ckfRefitter.TrajectoryInEvent = True

process.pixlessRefitter = process.TrackRefitter.clone()
process.pixlessRefitter.src = 'ctfPixelLess'
process.pixlessRefitter.TrajectoryInEvent = True

process.load("RecoTracker.TransientTrackingRecHit.TransientTrackingRecHitBuilderWithoutRefit_cfi")

#--------------------------------------------------
#  Load and Configure Offline Validation - needed?
#--------------------------------------------------

process.load("Alignment.OfflineValidation.TrackerOfflineValidation_cfi")

## #-------------
## #  HLT Trigger
## #-------------

## import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
## # accept if 'path_1' succeeds
## process.hltfilter = hlt.hltHighLevel.clone(
## # Min-Bias
## #   HLTPaths = ['HLT_L1Tech_BSC_minBias'],
# ---->    HLTPaths = ['HLT_L1Tech_BSC_minBias_OR'],
## #    HLTPaths = ['HLT_L1Tech_BSC_halo_forPhysicsBackground'],
## #    HLTPaths = ['HLT_L1Tech_BSC_HighMultiplicity'],
## #    HLTPaths = #['HLT_L1Tech_BSC_minBias','HLT_L1Tech_BSC_minBias_OR','HLT_L1Tech
## #_BSC_HighMultiplicity'],
## # Zero-Bias
## #    HLTPaths = #['HLT_L1_BPTX','HLT_ZeroBias','HLT_L1_BPTX_MinusOnly','HLT_L1_BP
## #TX_PlusOnly'],
## #    HLTPaths = ['HLT_L1_BPTX'],
## #    HLTPaths = ['HLT_ZeroBias'],
## #    HLTPaths = ['HLT_L1_BPTX_MinusOnly'],
## #    HLTPaths = ['HLT_L1_BPTX_PlusOnly'],
## # Commissioning: HLT_L1_BptxXOR_BscMinBiasOR
## #    HLTPaths = ['HLT_L1_BptxXOR_BscMinBiasOR'],
## #
## #    HLTPaths = ['p*'],
## #    HLTPaths = ['path_?'],
##    andOr = True,  # False = and, True=or
##    throw = False
##    )
## 
## # to select PhysicsBit
## process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
## process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'

# Trigger filter
process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff')
process.load('HLTrigger/HLTfilters/hltLevel1GTSeed_cfi')
process.hltLevel1GTSeed.L1TechTriggerSeeding = cms.bool(True)
process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string('(40 OR 41) AND ( NOT 36) AND ( NOT 37) AND ( NOT 38) AND ( NOT 39) AND 0 AND ( ( 42 AND 43) OR ( NOT 42 AND ( NOT 43) ) )')

#-------------------------
#  Ntuplizer code
#-------------------------

process.TimingStudy = cms.EDAnalyzer("TimingStudy",
                                     trajectoryInput = cms.string('TrackRefitter'),
                                     fileName = cms.string("EP_FEVT.root"),
                                     extrapolateFrom = cms.int32(2),
                                     extrapolateTo = cms.int32(1),
                                     keepOriginalMissingHit = cms.bool(False),
                                     usePixelCPE= cms.bool(True),
                                     minNStripHits = cms.int32(0),
                                     triggerNames=cms.vstring("HLT_ZeroBias",
                                                              "HLT_Physics",
                                                              "HLT_Random",
                                                              "HLT_PixelTracks_Multiplicity100",
                                                              "HLT_PixelTracks_Multiplicity80",
                                                              "HLT_PixelTracks_Multiplicity125",
                                                              "HLT_PixelTracks_Multiplicity110",
                                                              "HLT_PixelTracks_Multiplicity85",
                                                              "HLT_PixelTracks_Multiplicity70",
                                                              "HLT_PixelTracks_Multiplicity40",
                                                              "HLT_L1Tech_BSC_HighMultiplicity",
                                                              "HLT_JetE30_NoBPTX",
                                                              "HLT_JetE30_NoBPTX_NoHalo",
                                                              "HLT_JetE30_NoBPTX3BX_NoHalo",
                                                              "HLT_JetE50_NoBPTX3BX_NoHalo",
                                                              "HLT_60Jet10",
                                                              "HLT_70Jet10",
                                                              "HLT_70Jet13",
                                                              "HLT_L1Tech_BSC_minBias",
                                                              "HLT_MinBias")#Any MinBias triggers starting like this
)

# For the three cases:
process.ctfNtuple = process.TimingStudy.clone()
process.ctfNtuple.trajectoryInput = 'ctfRefitter'

process.ckfNtuple = process.TimingStudy.clone()
process.ckfNtuple.trajectoryInput = 'ckfRefitter'

process.pixlessNtuple = process.TimingStudy.clone()
process.pixlessNtuple.trajectoryInput = 'pixlessRefitter'


#-------------------------------------------------
# Configure output ntuple file using TFileService
#-------------------------------------------------

##process.TFileService = cms.Service("TFileService", 
##                                   ___file_Name___ = cms.string("test.root"),
##                                   closeFileFast = cms.untracked.bool(True)
##                                   )

#-------------------------------------------------
# Input files:
#-------------------------------------------------

process.source = cms.Source("PoolSource",
                            # replace with your files
                            #lastRun = cms.untracked.uint32(64789),
                            #timetype = cms.string('runnumber'),
                            #firstRun = cms.untracked.uint32(64108),
                            #interval = cms.uint32(1),
    fileNames = cms.untracked.vstring(
)
)


#-------------------------------------------------
# Number of events
#-------------------------------------------------

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1))


#-------------------------------------------------
# Path
#-------------------------------------------------

process.p = cms.Path(
    # Trigger selection:
    #process.hltLevel1GTSeed*
    #process.hltPhysicsDeclared*
    #process.hltfilter*
    # Reco:
    #process.siPixelDigis*process.siStripDigis*
    #//process.RawToDigi*process.reconstructionCosmics*
    # Beamspot:
    process.offlineBeamSpot*
    # Track reco:
    #process.trackerlocalreco*process.recopixelvertexing*process.ckftracks_plus_pixelless*
    # Refitters:
#    process.ctfRefitter*
    process.ckfRefitter*
#    process.pixlessRefitter*
    # Ntuplizers
#    process.ctfNtuple
    process.ckfNtuple
#    process.pixlessNtuple
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.MessageLogger.cerr.threshold = 'INFO'
process.TrackerDigiGeometryESModule.applyAlignment = True
