import ROOT
import math
from TIMBER.Analyzer import analyzer
from TIMBER.Tools.Common import CompileCpp
from argparse import ArgumentParser
ROOT.gROOT.SetBatch(True)

parser=ArgumentParser()
parser.add_argument('-n', type=int, dest='n_jobs',action='store', required=True)
parser.add_argument('-i', type=int, dest='i_job',action='store', required=True)
args=parser.parse_args()
CompileCpp("jet_matching.cc")

files=[]
file_name="raw_nano/HToGG_WminusToLNu_16.txt"

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
ana.Cut("Jet","nJet>=2 || nFatJet>=1")

ana.Define("GenRelevantPartIdx","GenRelevantPartMatching_HGGWLNu(nGenPart,GenPart_pdgId,GenPart_genPartIdxMother)")
#ana.Define("GenHGGJetsIdx","GenHGG(nGenPart,GenPart_pdgId,GenPart_genPartIdxMother)")
ana.Define("GenHGGJetsIdx","RVec<Int_t>({GenRelevantPartIdx.at(2),GenRelevantPartIdx.at(3)})")
ana.Define("GenHIdx","RVec<Int_t>({GenRelevantPartIdx.at(1)})")
ana.Define("GenLIdx","RVec<Int_t>({GenRelevantPartIdx.at(5)})")
ana.Define("Gen_JetsInvMass","InvMass_PtEtaPhiM(FQuantityMatching(GenHGGJetsIdx,GenPart_pt),FQuantityMatching(GenHGGJetsIdx,GenPart_eta),FQuantityMatching(GenHGGJetsIdx,GenPart_phi),FQuantityMatching(GenHGGJetsIdx,GenPart_mass))") 


ana.Define("Matched_JetsIdx","RecoPartMatching_deltaR(GenHGGJetsIdx,GenPart_eta,GenPart_phi,Jet_eta,Jet_phi,0.4)")

ana.Define("Reco_JetsInvMass","InvMass_PtEtaPhiM(FQuantityMatching(Matched_JetsIdx,Jet_pt),FQuantityMatching(Matched_JetsIdx,Jet_eta),FQuantityMatching(Matched_JetsIdx,Jet_phi),FQuantityMatching(Matched_JetsIdx,Jet_mass))") 


ana.Define("Matched_FatJetsIdx","RecoPartMatching_deltaR(GenHIdx,GenPart_eta,GenPart_phi,FatJet_eta,FatJet_phi,0.8)")


ana.Define("Reco_FatJetsMass","FQuantityMatching({Matched_FatJetsIdx},FatJet_mass)") 

ana.Define("MatchedwithGG_FatJetsIdx","FatJetMatching_deltaR(GenHGGJetsIdx,GenPart_eta,GenPart_phi,FatJet_eta,FatJet_phi,0.8)")

ana.Define("RecowithGG_FatJetsMass","FQuantityMatching({MatchedwithGG_FatJetsIdx},FatJet_mass)") 


ana.Define("Matched_ElectronIdx","RecoPartMatching_deltaR(GenLIdx,GenPart_eta,GenPart_phi,Electron_eta,Electron_phi,0.4)")
ana.Define("Matched_MuonIdx","RecoPartMatching_deltaR(GenLIdx,GenPart_eta,GenPart_phi,Muon_eta,Muon_phi,0.4)")
ana.Define("Matched_TauIdx","RecoPartMatching_deltaR(GenLIdx,GenPart_eta,GenPart_phi,Tau_eta,Tau_phi,0.4)")
#columns=["nGenPart","GenPart_eta","GenPart_phi","GenPart_pt","nJet","Jet_eta","Jet_phi","Jet_pt","nFatJet","FatJet_eta","FatJet_phi","FatJet_pt","FatJet_mass","GenHGGJetsIdx","Matched_JetsIdx","Matched_FatJetsIdx"]

columns=["GenRelevantPartIdx","GenHGGJetsIdx","GenHIdx","GenLIdx","Gen_JetsInvMass","Matched_JetsIdx","Reco_JetsInvMass","Matched_FatJetsIdx","Reco_FatJetsMass","MatchedwithGG_FatJetsIdx","RecowithGG_FatJetsMass","Matched_ElectronIdx","Matched_MuonIdx","Matched_TauIdx"]
ana.Snapshot(columns,f"result_{args.n_jobs}_{args.i_job}.root","Events")
