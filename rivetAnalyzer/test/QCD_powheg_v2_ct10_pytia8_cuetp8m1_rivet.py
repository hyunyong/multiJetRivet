import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
import sys

process = cms.Process('GEN')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

fNum = int(sys.argv[2])
seedOffSet = int(sys.argv[3])

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("LHESource",
			    fileNames = cms.untracked.vstring(
			    'file:./pwgeve_POWHEG2jet{:03}.lhe'.format(fNum),
							      )
                           )           

process.options = cms.untracked.PSet(
)

process.genstepfilter.triggerConditions=cms.vstring("generation_step")

pythia8PowhegEmissionVetoSettingsBlock = cms.PSet(
    pythia8PowhegEmissionVetoSettings = cms.vstring(
          'POWHEG:veto = 1',
          'POWHEG:pTdef = 1',
          'POWHEG:emitted = 0',
          'POWHEG:pTemt = 0',
          'POWHEG:pThard = 0',
          'POWHEG:vetoCount = 100',
          'SpaceShower:pTmaxMatch = 2',
          'TimeShower:pTmaxMatch = 2',
    )
)

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(8000.),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        pythia8PowhegEmissionVetoSettingsBlock,      
        processParameters = cms.vstring(
            'POWHEG:nFinal = 2',
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'pythia8PowhegEmissionVetoSettings',
                                    'processParameters'
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
process.RandomNumberGeneratorService.generator.initialSeed = seedOffSet + fNum
#process.RandomNumberGeneratorService.generator.initialSeed = 700+fNum
#process.RandomNumberGeneratorService.generator.initialSeed = 1300+fNum
#process.RandomNumberGeneratorService.generator.initialSeed = 1600+fNum
#process.RandomNumberGeneratorService.generator.initialSeed = 2600+fNum
#process.RandomNumberGeneratorService.generator.initialSeed = 3300+fNum
#process.RandomNumberGeneratorService.generator.initialSeed = 70691+fNum

process.load('GeneratorInterface.RivetInterface.rivetAnalyzer_cfi')
process.rivetAnalyzer.AnalysisNames = cms.vstring('multiJetReW')
process.generation_step+=process.rivetAnalyzer
process.rivetAnalyzer.OutputFile = cms.string('QCD_powheg_ct10_pythia8_cuetp8m1_13TeV_rivet_{:03}.yoda'.format(fNum))
process.MessageLogger.cerr.FwkReport.reportEvery = 50000
