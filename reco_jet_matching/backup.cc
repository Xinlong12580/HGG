
ROOT::VecOps::RVec<Int_t> GenHGG(Int_t nGenPart,ROOT::VecOps::RVec<Int_t> GenPart_pdgId, ROOT::VecOps::RVec<Int_t> GenPart_genPartIdxMother) { \
        ROOT::VecOps::RVec<Int_t> GG={-1,-1}; \
        Int_t count=0; \
        for (Int_t i=0;i<nGenPart;i++){ \
            if (GenPart_pdgId[i]==21 && GenPart_genPartIdxMother[i]>=0 && GenPart_pdgId[GenPart_genPartIdxMother[i]]==25){ \
                GG.at(count)=i; \
                count++; \
                if(count==2) break;\
            } \
        } \
        return GG; \
} \

ROOT::VecOps::RVec<Int_t> Jet_match(ROOT::VecOps::RVec<Int_t> GenHGG,Int_t nJet,ROOT::VecOps::RVec<Float_t> Jet_phi, ROOT::VecOps::RVec<Float_t> Jet_eta,ROOT::VecOps::RVec<Float_t> GenPart_phi, ROOT::VecOps::RVec<Float_t> GenPart_eta) { \
	 Float_t R=0.4;\
        ROOT::VecOps::RVec<Int_t> GG={-1,-1}; \
        for(Int_t geni=0;geni<2;geni++){ \
	    if(GenHGG[geni]<0) continue;
            Float_t gen_phi=GenPart_phi[GenHGG[geni]]; \
            Float_t gen_eta=GenPart_eta[GenHGG[geni]];\
            for (Int_t i=0;i<nJet;i++){ \
                Float_t reco_phi=Jet_phi[i];\
                Float_t reco_eta=Jet_eta[i];\
                Float_t diff_phi=std::abs(gen_phi-reco_phi)<3.1415926 ? std::abs(gen_phi-reco_phi) : 2*3.1415926-std::abs(gen_phi-reco_phi);\
                Float_t diff_eta=std::abs(gen_eta-reco_eta);\
                if(diff_eta*diff_eta+diff_phi*diff_phi<=R*R){\
                    GG[geni]=i;\
                    break;\
                } \
            } \
        } \
        return GG; \
} \
ROOT::VecOps::RVec<Int_t> GenRelevantPart(Int_t nGenPart,ROOT::VecOps::RVec<Int_t> GenPart_pdgId, ROOT::VecOps::RVec<Int_t> GenPart_genPartIdxMother) { 
        ROOT::VecOps::RVec<Int_t> Parts={-1,-1,-1,-1,-1,-1,-1}; //Mother W, Higgs, Gluon, Gluon, Daughter W, Lepton, Neutrino 
        Int_t count=0; 
        for (Int_t i=0;i<nGenPart;i++){ 
            if (GenPart_pdgId[i]==21 && GenPart_genPartIdxMother[i]>=0 && GenPart_pdgId[GenPart_genPartIdxMother[i]]==25){ 
                Parts.at(count+2)=i;
	        Parts.at(1)=GenPart_genPartIdxMother[i];	
                count++; 
                if(count==2) break;
            } 
        }
       	if(Parts.at(1)>0){
			Parts.at(0)=GenPart_genPartIdxMother[Parts.at(1)];
			if(Parts.at(0)>0){
				for (Int_t i=0;i<nGenPart;i++){
					if (GenPart_pdgId[i]==-24 && GenPart_genPartIdxMother[i]==Parts.at(0)){
						Parts.at(4)=i;
					 	for (Int_t j=0;j<nGenPart;j++){
							if (GenPart_genPartIdxMother[j]==Parts.at(4)){
								 if(GenPart_pdgId[j]==11 || GenPart_pdgId[j]==13 || GenPart_pdgId[j]==15)
									 Parts.at(5)=j;
							 if(GenPart_pdgId[j]==-12 || GenPart_pdgId[j]==-14 || GenPart_pdgId[j]==-16)
								 Parts.at(6)=j;
						 }
					 }
					 break;
				}
			}
		}

	}	
        return Parts; 
} 
Int_t FatJetMatching_deltaR(RVec<Int_t> GenHGG, RVec<Float_t> GenPart_phi, RVec<Float_t> GenPart_eta, Int_t nFatJet, RVec<Float_t> FatJet_phi, RVec<Float_t> FatJet_eta,  Float_t R=0.8) { 
        ROOT::VecOps::RVec<Int_t> GG={-1}; 
	if(GenHGG[0]<0 || GenHGG[1]<0) return GG;
        for (Int_t i=0;i<nJet;i++){ 
	    int matched=1;
            for(Int_t geni=0;geni<2;geni++){ 
            	Float_t gen_phi=GenPart_phi[GenHGG[geni]]; 
            	Float_t gen_eta=GenPart_eta[GenHGG[geni]];
                Float_t reco_phi=Jet_phi[i];
                Float_t reco_eta=Jet_eta[i];
                Float_t diff_phi=std::abs(gen_phi-reco_phi)<3.1415926 ? std::abs(gen_phi-reco_phi) : 2*3.1415926-std::abs(gen_phi-reco_phi);
                Float_t diff_eta=std::abs(gen_eta-reco_eta);
                if(diff_eta*diff_eta+diff_phi*diff_phi>R*R)
                    matched=0; 
            } 
	    if (matched==1){
		    GG.at(0)=i;
		    break;
	    }
        } 
        return GG; 
} 
