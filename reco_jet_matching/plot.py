import ROOT
ROOT.gROOT.SetBatch(True)
rdf=ROOT.RDataFrame("Events","result_60_0.root")

c_gen=ROOT.TCanvas("c","c")
c_gen.cd()
h_gen=rdf.Filter("Gen_JetsInvMass>0").Histo1D( ('Gen_InvMass','Gen_InvMass',50,0,200), 'Gen_JetsInvMass') 
h_gen.Draw()
c_gen.Print("gen.pdf")

c_jet=ROOT.TCanvas("c","c")
c_jet.cd()
h_jet=rdf.Filter("Reco_JetsInvMass>0").Histo1D( ('MatchedJets_InvMass','MatchedJets_InvMass',50,0,200), 'Reco_JetsInvMass') 
h_jet.Draw()
c_jet.Print("jet.pdf")

c_fatjet=ROOT.TCanvas("c","c")
c_fatjet.cd()
h_fatjet=rdf.Filter("Reco_FatJetsMass.at(0)>0").Histo1D( ('MatchedFatJets_InvMass','MatchedFatJets_InvMass',50,0,200), 'Reco_FatJetsMass') 
h_fatjet.Draw()
c_fatjet.Print("fatjet.pdf")

c_fatjetGG=ROOT.TCanvas("c","c")
c_fatjetGG.cd()
h_fatjetGG=rdf.Filter("RecowithGG_FatJetsMass.at(0)>0").Histo1D( ('MatchedFatJets_InvMass','MatchedFatJets_InvMass',50,0,200), 'RecowithGG_FatJetsMass') 
h_fatjetGG.Draw()
c_fatjetGG.Print("fatjetGG.pdf")
exit()
