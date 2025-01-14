import ROOT
from TIMBER.Analyzer import analyzer
from TIMBER.Tools.Common import CompileCpp

CompileCpp("jet_matching.cc")

files=["BF3F0C2F-BEC9-0D41-8391-1E309CBEFB4C.root"]

ana=analyzer(files)
ana.Define("GenHGGJets","GenHGG(nGenPart,GenPart_pdgId,GenPart_genPartIdxMother)")
ana.Cut("Jet","nJet>=2 || nFatJet>=1")
ana.Define("Matched_RecoJets","RecoHGG(GenHGGJets,nJet,Jet_phi,Jet_eta,GenPart_phi,GenPart_eta)")
columns=["GenHGGJets","Matched_RecoJets"]
ana.Snapshot(columns,"matching.root","Events")
