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

f_num = int(sys.argv[2])

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(5000)
)

process.source = cms.Source("LHESource",
			    fileNames = cms.untracked.vstring(
			    'file:/xrootd_user/hyunyong/xrootd/POWHEG8TeV/pwgeve_POWHEG2jet001.lhe',
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

process.source.firstRun = cms.untracked.uint32(f_num)
process.RandomNumberGeneratorService.generator.initialSeed = f_num

process.load('GeneratorInterface.RivetInterface.rivetAnalyzer_cfi')
process.rivetAnalyzer.AnalysisNames = cms.vstring('multiJetReW')
process.generation_step+=process.rivetAnalyzer
process.rivetAnalyzer.OutputFile = cms.string('QCD_powheg_ct10_pythia8_cuetp8m1_13TeV_rivet_%03d.yoda'%(f_num))
process.MessageLogger.cerr.FwkReport.reportEvery = 50000