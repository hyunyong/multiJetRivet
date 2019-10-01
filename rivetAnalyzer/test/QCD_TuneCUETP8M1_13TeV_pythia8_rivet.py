import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

process = cms.Process('GEN')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

import sys
maxNum = int(sys.argv[2])
fNum = int(sys.argv[3])
minPt = int(sys.argv[4])
maxPt = int(sys.argv[5])

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(maxNum)
)
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

process.genstepfilter.triggerConditions=cms.vstring("generation_step")
process.generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(
            'HardQCD:all = on',
            #'ParticleDecays:rMax = 1000.0',
            #'ParticleDecays:xyMax = 1000.0',
            #'ParticleDecays:zMax = 500.0',
            #'ParticleDecays:limitRadius = on',
            #'ParticleDecays:tauMax = 1000.0',
            #'ParticleDecays:limitTau = on',
            #'ParticleDecays:limitTau0 = on',
            #'ParticleDecays:tau0Max = 1000.0',
            'PhaseSpace:pTHatMin = %d  '%minPt,
            'PhaseSpace:pTHatMax = %d  '%maxPt
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'processParameters',
                                    )
        )
                         )

process.generation_step = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)

process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step)
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 

process.source.firstRun = cms.untracked.uint32(fNum)
process.RandomNumberGeneratorService.generator.initialSeed = fNum

process.load('GeneratorInterface.RivetInterface.rivetAnalyzer_cfi')
process.rivetAnalyzer.AnalysisNames = cms.vstring('jetConstituents')
#process.rivetAnalyzer.AnalysisNames = cms.vstring('multiJetReW')
process.generation_step+=process.rivetAnalyzer
process.rivetAnalyzer.OutputFile = cms.string('QCD_Pt_%dto%d_TuneCUETP8M1_13TeV_pythia8_rivet_%03d.yoda'%(minPt, maxPt, fNum))
process.MessageLogger.cerr.FwkReport.reportEvery = 50000

