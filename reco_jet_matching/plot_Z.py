import ROOT
ROOT.gROOT.SetBatch(True)
files=[]
with open("files.txt","r") as f:
    files=["root://cmsxrootd.fnal.gov//store/user/xinlong/HGG/"+line.strip() for line in f]

rdf=ROOT.RDataFrame("Events",files)

c_gen=ROOT.TCanvas("c","c")
c_gen.cd()
h_gen=rdf.Filter("Gen_JetsInvMass>0").Histo1D( ('Gen_InvMass','Gen_InvMass',50,0,200), 'Gen_JetsInvMass',"scaledWeight") 
h_gen.Draw()
c_gen.Print("gen_Z.pdf")

c_jet=ROOT.TCanvas("c","c")
c_jet.cd()
h_jet=rdf.Filter("Reco_JetsInvMass>0").Histo1D( ('MatchedJets_InvMass','MatchedJets_InvMass',50,0,200), 'Reco_JetsInvMass',"scaledWeight") 
h_jet.Draw()
c_jet.Print("jet_Z.pdf")

c_fatjet=ROOT.TCanvas("c","c")
c_fatjet.cd()
h_fatjet=rdf.Filter("Reco_FatJetsMass.at(0)>0").Histo1D( ('MatchedFatJets_InvMass','MatchedFatJets_InvMass',50,0,200), 'Reco_FatJetsMass',"scaledWeight") 
h_fatjet.Draw()
c_fatjet.Print("fatjet_Z.pdf")

c_fatjetall=ROOT.TCanvas("c","c")
c_fatjetall.cd()
h_fatjetall=rdf.Histo1D( ('FatJets_InvMass','FatJets_InvMass',50,0,200), 'FatJet_msoftdrop',"scaledWeight") 
h_fatjetall.Draw()
c_fatjetall.Print("fatjet_Zall.pdf")

c_fatjetGG=ROOT.TCanvas("c","c")
c_fatjetGG.cd()
h_fatjetGG=rdf.Filter("RecowithGG_FatJetsMass.at(0)>0").Histo1D( ('MatchedFatJets_InvMass','MatchedFatJets_InvMass',50,0,200), 'RecowithGG_FatJetsMass',"scaledWeight") 
print(rdf.Filter("RecowithGG_FatJetsMass.at(0)>0").Sum("scaledWeight").GetValue())
h_fatjetGG.Draw()
c_fatjetGG.Print("fatjetGG_Z.pdf")

c_Z=ROOT.TCanvas("c","c")
c_Z.cd()
h_EE=rdf.Filter("Reco_EEInvMass>0").Histo1D( ('MatchedZ_InvMass','MatchedZ_InvMass',50,0,200), 'Reco_EEInvMass',"scaledWeight") 
h_MuMu=rdf.Filter("Reco_MuMuInvMass>0").Histo1D( ('MatchedZ_InvMass','MatchedZ_InvMass',50,0,200), 'Reco_MuMuInvMass',"scaledWeight") 
h_TauTau=rdf.Filter("Reco_TauTauInvMass>0").Histo1D( ('MatchedZ_InvMass','MatchedZ_InvMass',50,0,200), 'Reco_TauTauInvMass',"scaledWeight") 
h_Z=h_EE.Clone()
h_Z.Add(h_MuMu.GetPtr())
h_Z.Add(h_TauTau.GetPtr())
h_Z.Draw()
c_Z.Print("ZLL.pdf")

c_ZPt=ROOT.TCanvas("c","c")
c_ZPt.cd()
h_EEPt=rdf.Filter("HighPt_EEInvMass>0").Histo1D( ('MatchedZ_InvMass','MatchedZ_InvMass',50,0,200), 'HighPt_EEInvMass',"scaledWeight") 
h_MuMuPt=rdf.Filter("HighPt_MuMuInvMass>0").Histo1D( ('MatchedZ_InvMass','MatchedZ_InvMass',50,0,200), 'HighPt_MuMuInvMass',"scaledWeight") 
h_TauTauPt=rdf.Filter("HighPt_TauTauInvMass>0").Histo1D( ('MatchedZ_InvMass','MatchedZ_InvMass',50,0,200), 'HighPt_TauTauInvMass',"scaledWeight") 
h_ZPt=h_EEPt.Clone()
h_ZPt.Add(h_MuMuPt.GetPtr())
h_ZPt.Add(h_TauTauPt.GetPtr())
h_ZPt.Draw()
c_ZPt.Print("ZLLPt.pdf")
exit()
