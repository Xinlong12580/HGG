import ROOT
import math
from TIMBER.Analyzer import analyzer
from TIMBER.Tools.Common import CompileCpp
from argparse import ArgumentParser
ROOT.gROOT.SetBatch(True)

parser=ArgumentParser()
parser.add_argument('-y', type=str, dest='year',action='store', required=True)
parser.add_argument('-n', type=int, dest='n_jobs',action='store', required=True)
parser.add_argument('-i', type=int, dest='i_job',action='store', required=True)
args=parser.parse_args()
CompileCpp("Matching.cc")
CompileCpp("Cut.cc")
CompileCpp("HGGConst.cc")
files=[]
file_name=""
sumW=0
Nexp=0
if args.year == "16":
    file_name = "raw_nano/HToGG_ZToLL_16.txt"
elif args.year == "16APV":
    file_name = "raw_nano/HToGG_ZToLL_16APV.txt"
if args.year == "17":
    file_name = "raw_nano/HToGG_ZToLL_17.txt"
if args.year == "18":
    file_name = "raw_nano/HToGG_ZToLL_18.txt"

pt_cut=150

with open(file_name,"r") as f:
    all_files=f.readlines()
    all_files=[line.strip() for line in all_files]
    N=len(all_files)
    print(N)
    n_apiece=math.floor(N/args.n_jobs)
    i=args.i_job
    if i<args.n_jobs-1:
        files=all_files[i*n_apiece:(i+1)*n_apiece]
    else:
        files=all_files[i*n_apiece:len(all_files)]
print(len(files))
#exit()
#files=["BF3F0C2F-BEC9-0D41-8391-1E309CBEFB4C.root"]

ana=analyzer(files)
ana.Cut("nJet_Cut","nJet>=2 || nFatJet>=1")


ana.Cut("FatjetPt", f"MaxCut(FatJet_pt, {pt_cut} ,1)")

ana.Define("GenRelevantPartIdx","GenRelevantPartMatching_HGGZLL(nGenPart,GenPart_pdgId,GenPart_genPartIdxMother)")
#ana.Define("GenHGGJetsIdx","GenHGG(nGenPart,GenPart_pdgId,GenPart_genPartIdxMother)")
ana.Define("GenHGGJetsIdx","RVec<Int_t>({GenRelevantPartIdx.at(2),GenRelevantPartIdx.at(3)})")
ana.Define("GenHIdx","RVec<Int_t>({GenRelevantPartIdx.at(1)})")
ana.Define("GenLIdx","RVec<Int_t>({GenRelevantPartIdx.at(5), GenRelevantPartIdx.at(6)})")
ana.Define("Gen_JetsInvMass","InvMass_PtEtaPhiM(FQuantityMatching(GenHGGJetsIdx,GenPart_pt),FQuantityMatching(GenHGGJetsIdx,GenPart_eta),FQuantityMatching(GenHGGJetsIdx,GenPart_phi),FQuantityMatching(GenHGGJetsIdx,GenPart_mass))") 


ana.Define("Matched_JetsIdx","RecoPartMatching_deltaR(GenHGGJetsIdx,GenPart_eta,GenPart_phi,Jet_eta,Jet_phi,0.4)")

ana.Define("Reco_JetsInvMass","InvMass_PtEtaPhiM(FQuantityMatching(Matched_JetsIdx,Jet_pt),FQuantityMatching(Matched_JetsIdx,Jet_eta),FQuantityMatching(Matched_JetsIdx,Jet_phi),FQuantityMatching(Matched_JetsIdx,Jet_mass))") 


ana.Define("Matched_FatJetsIdx","RecoPartMatching_deltaR(GenHIdx,GenPart_eta,GenPart_phi,FatJet_eta,FatJet_phi,0.8)")


#ana.Define("Reco_FatJetsMass","FQuantityMatching({Matched_FatJetsIdx},FatJet_mass)") 
ana.Define("Reco_FatJetsMass","FQuantityMatching({Matched_FatJetsIdx},FatJet_msoftdrop)") 

ana.Define("MatchedwithGG_FatJetsIdx","FatJetMatching_deltaR(GenHGGJetsIdx,GenPart_eta,GenPart_phi,FatJet_eta,FatJet_phi,0.8)")

#ana.Define("RecowithGG_FatJetsMass","FQuantityMatching({MatchedwithGG_FatJetsIdx},FatJet_mass)") 
ana.Define("RecowithGG_FatJetsMass","FQuantityMatching({MatchedwithGG_FatJetsIdx},FatJet_msoftdrop)") 


ana.Define("Matched_ElectronIdx","RecoPartMatching_deltaR(GenLIdx,GenPart_eta,GenPart_phi,Electron_eta,Electron_phi,0.4)")
ana.Define("Matched_MuonIdx","RecoPartMatching_deltaR(GenLIdx,GenPart_eta,GenPart_phi,Muon_eta,Muon_phi,0.4)")
ana.Define("Matched_TauIdx","RecoPartMatching_deltaR(GenLIdx,GenPart_eta,GenPart_phi,Tau_eta,Tau_phi,0.4)")

ana.Define("Reco_EEInvMass","InvMass_PtEtaPhiM(FQuantityMatching(Matched_ElectronIdx,Electron_pt),FQuantityMatching(Matched_ElectronIdx,Electron_eta),FQuantityMatching(Matched_ElectronIdx,Electron_phi),FQuantityMatching(Matched_ElectronIdx,Electron_mass))") 
ana.Define("Reco_MuMuInvMass","InvMass_PtEtaPhiM(FQuantityMatching(Matched_MuonIdx,Muon_pt),FQuantityMatching(Matched_MuonIdx,Muon_eta),FQuantityMatching(Matched_MuonIdx,Muon_phi),FQuantityMatching(Matched_MuonIdx,Muon_mass))") 
ana.Define("Reco_TauTauInvMass","InvMass_PtEtaPhiM(FQuantityMatching(Matched_TauIdx,Tau_pt),FQuantityMatching(Matched_TauIdx,Tau_eta),FQuantityMatching(Matched_TauIdx,Tau_phi),FQuantityMatching(Matched_TauIdx,Tau_mass))") 

#ana.Define("HighPt_ElectronIdx", "FMaxIdxFinding(Electron_pt,2)")
#ana.Define("HighPt_MuonIdx", "FMaxIdxFinding(Muon_pt,2)")
#ana.Define("HighPt_TauIdx", "FMaxIdxFinding(Tau_pt,2)")


ana.Define("HighPt_ElectronIdx", "LeptonPairIdxFinding(Electron_pt,Electron_charge)")
ana.Define("HighPt_MuonIdx", "LeptonPairIdxFinding(Muon_pt,Muon_charge)")
ana.Define("HighPt_TauIdx", "LeptonPairIdxFinding(Tau_pt,Tau_charge)")

ana.Define("test","FQuantityMatching(HighPt_ElectronIdx,Electron_pt)") 
ana.Define("HighPt_EEInvMass","InvMass_PtEtaPhiM(FQuantityMatching(HighPt_ElectronIdx,Electron_pt),FQuantityMatching(HighPt_ElectronIdx,Electron_eta),FQuantityMatching(HighPt_ElectronIdx,Electron_phi),FQuantityMatching(HighPt_ElectronIdx,Electron_mass))") 
ana.Define("HighPt_MuMuInvMass","InvMass_PtEtaPhiM(FQuantityMatching(HighPt_MuonIdx,Muon_pt),FQuantityMatching(HighPt_MuonIdx,Muon_eta),FQuantityMatching(HighPt_MuonIdx,Muon_phi),FQuantityMatching(HighPt_MuonIdx,Muon_mass))") 
ana.Define("HighPt_TauTauInvMass","InvMass_PtEtaPhiM(FQuantityMatching(HighPt_TauIdx,Tau_pt),FQuantityMatching(HighPt_TauIdx,Tau_eta),FQuantityMatching(HighPt_TauIdx,Tau_phi),FQuantityMatching(HighPt_TauIdx,Tau_mass))") 
#columns=["nGenPart","GenPart_eta","GenPart_phi","GenPart_pt","nJet","Jet_eta","Jet_phi","Jet_pt","nFatJet","FatJet_eta","FatJet_phi","FatJet_pt","FatJet_mass","GenHGGJetsIdx","Matched_JetsIdx","Matched_FatJetsIdx"]

if args.year == "16":
    ana.Define("scaledWeight","genWeight * HGGConst::run2Y16Lumi * HGGConst::HZXSec * HGGConst::HGGBR * HGGConst::ZLLBR / HGGConst::HGGZLL16DSSumW")
if args.year == "16APV":
    ana.Define("scaledWeight","genWeight * HGGConst::run2Y16APVLumi * HGGConst::HZXSec * HGGConst::HGGBR * HGGConst::ZLLBR / HGGConst::HGGZLL16APVDSSumW")
if args.year == "17":
    ana.Define("scaledWeight","genWeight * HGGConst::run2Y17Lumi * HGGConst::HZXSec * HGGConst::HGGBR * HGGConst::ZLLBR / HGGConst::HGGZLL17DSSumW")
if args.year == "18":
    ana.Define("scaledWeight","genWeight * HGGConst::run2Y18Lumi * HGGConst::HZXSec * HGGConst::HGGBR * HGGConst::ZLLBR / HGGConst::HGGZLL18DSSumW")
columns=["GenRelevantPartIdx","GenHGGJetsIdx","GenHIdx","GenLIdx","Gen_JetsInvMass","Matched_JetsIdx","Reco_JetsInvMass","Matched_FatJetsIdx","Reco_FatJetsMass","MatchedwithGG_FatJetsIdx","RecowithGG_FatJetsMass","Matched_ElectronIdx","Matched_MuonIdx","Matched_TauIdx","Reco_EEInvMass","Reco_MuMuInvMass","Reco_TauTauInvMass","HighPt_ElectronIdx","HighPt_MuonIdx","HighPt_TauIdx","HighPt_EEInvMass","HighPt_MuMuInvMass","HighPt_TauTauInvMass","FatJet_msoftdrop","nFatJet","test","genWeight","scaledWeight"]
ana.Snapshot(columns,f"result_Z_{args.year}_{args.n_jobs}_{args.i_job}.root","Events")
