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

ana.Define("GenRelevantPartIdx","GenRelevantPart_v2(nGenPart,GenPart_pdgId,GenPart_genPartIdxMother)")
'''
#ana.Define("GenHGGJetsIdx","GenHGG(nGenPart,GenPart_pdgId,GenPart_genPartIdxMother)")
ana.Define("GenHGGJetsIdx","ROOT::VecOps::RVec<Float_t>({GenRelevantPartIdx.at(2),GenRelevantPartIdx,at(3)})")
ana.Define("GenHIdx","ROOT::VecOps::RVec<Float_t>({GenRelevantPartIdx.at(1)})")
ana.Define("GenLIdx","ROOT::VecOps::RVec<Float_t>({GenRelevantPartIdx.at(5)})")

ana.Define("Gen_JetsPt","FQuantity_match(GenHGGJetsIdx,GenPart_pt)")
ana.Define("Gen_JetsPhi","FQuantity_match(GenHGGJetsIdx,GenPart_phi)")
ana.Define("Gen_JetsEta","FQuantity_match(GenHGGJetsIdx,GenPart_eta)")
ana.Define("Gen_JetsMass","FQuantity_match(GenHGGJetsIdx,GenPart_mass)")
ana.Define("Gen_JetsInvMass","InvMass(Gen_JetsPt,Gen_JetsEta,Gen_JetsPhi,Gen_JetsMass)")

ana.Define("Gen_HPt","FQuantity_match(GenHIdx,GenPart_pt)")
ana.Define("Gen_HPhi","FQuantity_match(GenHIdx,GenPart_phi)")
ana.Define("Gen_HEta","FQuantity_match(GenHIdx,GenPart_eta)")
ana.Define("Gen_HMass","FQuantity_match(GenHIdx,GenPart_mass)")

ana.Define("Gen_LPt","FQuantity_match(GenLIdx,GenPart_pt)")
ana.Define("Gen_LPhi","FQuantity_match(GenLIdx,GenPart_phi)")
ana.Define("Gen_LEta","FQuantity_match(GenLIdx,GenPart_eta)")
ana.Define("Gen_LMass","FQuantity_match(GenLIdx,GenPart_mass)")

ana.Define("Matched_JetsIdx","Jet_match(GenHGGJetsIdx,nJet,Jet_phi,Jet_eta,GenPart_phi,GenPart_eta)")

ana.Define("Matched_JetsPt","FQuantity_match(Matched_JetsIdx,Jet_pt)")
ana.Define("Matched_JetsPhi","FQuantity_match(Matched_JetsIdx,Jet_phi)")
ana.Define("Matched_JetsEta","FQuantity_match(Matched_JetsIdx,Jet_eta)")
ana.Define("Matched_JetsMass","FQuantity_match(Matched_JetsIdx,Jet_mass)")
ana.Define("Matched_JetsInvMass","InvMass(Matched_JetsPt,Matched_JetsEta,Matched_JetsPhi,Matched_JetsMass)")

ana.Define("Matched_FatJetsIdx","FatJet_match(GenHGGJetsIdx,nFatJet,FatJet_phi,FatJet_eta,GenPart_phi,GenPart_eta)")

ana.Define("Matched_FatJetsPt","FQuantity_match(Matched_FatJetsIdx,FatJet_pt)")
ana.Define("Matched_FatJetsPhi","FQuantity_match(Matched_FatJetsIdx,FatJet_phi)")
ana.Define("Matched_FatJetsEta","FQuantity_match(Matched_FatJetsIdx,FatJet_eta)")
ana.Define("Matched_FatJetsMass","FQuantity_match(Matched_FatJetsIdx,FatJet_mass)")

ana.Define("Matched_FatJetsMassf","Matched_FatJetsMass.at(0)")
'''
'''
c_gen=ROOT.TCanvas("c","c")
c_gen.cd()
h_gen=ana.DataFrame.Filter("Gen_JetsInvMass>0").Histo1D( ('Gen_InvMass','Gen_InvMass',20,80,170), 'Gen_JetsInvMass') 
h_gen.Draw()
c_gen.Print("gen.pdf")

c_jet=ROOT.TCanvas("c","c")
c_jet.cd()
h_jet=ana.DataFrame.Filter("Matched_JetsInvMass>0").Histo1D( ('MatchedJets_InvMass','MatchedJets_InvMass',20,80,170), 'Matched_JetsInvMass') 
h_jet.Draw()
c_jet.Print("jet.pdf")

c_fatjet=ROOT.TCanvas("c","c")
c_fatjet.cd()
h_fatjet=ana.DataFrame.Filter("Matched_FatJetsMassf>0").Histo1D( ('MatchedFatJets_InvMass','MatchedFatJets_InvMass',20,80,170), 'Matched_FatJetsMassf') 
h_fatjet.Draw()
c_fatjet.Print("fatjet.pdf")

exit()
'''
#columns=["nGenPart","GenPart_eta","GenPart_phi","GenPart_pt","nJet","Jet_eta","Jet_phi","Jet_pt","nFatJet","FatJet_eta","FatJet_phi","FatJet_pt","FatJet_mass","GenHGGJetsIdx","Matched_JetsIdx","Matched_FatJetsIdx"]
#columns=["GenHGGJetsIdx","Matched_JetsIdx","Matched_FatJetsIdx"]
#columns=["nGenPart","GenPart_eta","GenPart_phi","GenPart_pt","nJet","Jet_eta","Jet_phi","Jet_pt","nFatJet","FatJet_eta","FatJet_phi","FatJet_pt","FatJet_mass","nCorrT1METJet","nSoftActivityJet","nSubJet"]
#columns=["GenHGGJetsIdx","Gen_JetsPt","Gen_JetsEta","Gen_JetsPhi","Gen_JetsMass","Gen_JetsInvMass","Matched_JetsIdx","Matched_JetsPt","Matched_JetsEta","Matched_JetsPhi","Matched_JetsMass","Matched_JetsInvMass","Matched_FatJetsIdx","Matched_FatJetsPt","Matched_FatJetsEta","Matched_FatJetsPhi","Matched_FatJetsMass"]
columns=["GenRelevantPartIdx"]
ana.Snapshot(columns,f"result_{args.n_jobs}_{args.i_job}.root","Events")
