#include "TIMBER/Framework/include/common.h"

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

ROOT::VecOps::RVec<Int_t> FatJet_match(ROOT::VecOps::RVec<Int_t> GenHGG,Int_t nJet,ROOT::VecOps::RVec<Float_t> Jet_phi, ROOT::VecOps::RVec<Float_t> Jet_eta,ROOT::VecOps::RVec<Float_t> GenPart_phi, ROOT::VecOps::RVec<Float_t> GenPart_eta) { 
	Float_t R=0.8;
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

ROOT::VecOps::RVec<Float_t> FQuantity_match(ROOT::VecOps::RVec<Int_t> Idx, ROOT::VecOps::RVec<Float_t> Val){
	ROOT::VecOps::RVec<Float_t> matched_val={};
	for (int i = 0; i< Idx.size(); i++){
		if(Idx.at(i)<0) matched_val.push_back(-999999.0);
		else matched_val.push_back(Val.at(Idx.at(i)));
	}
	return matched_val;
}

float InvMass(ROOT::VecOps::RVec<Float_t> Pt, ROOT::VecOps::RVec<Float_t> Eta,  ROOT::VecOps::RVec<Float_t> Phi, ROOT::VecOps::RVec<Float_t> Mass){
	float inv_mass=-999999.0;
	ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> vectors={};
	
	for(int i=0; i<Pt.size();i++){
		if(Pt.at(i)<-99999.0 ||  Eta.at(i)<-99999.0 || Phi.at(i)<-99999.0 || Mass.at(i)<-99999.0){
			inv_mass=-999999.0;
			return inv_mass;
		}
		
		ROOT::Math::PtEtaPhiMVector vector(Pt.at(i),Eta.at(i),Phi.at(i),Mass.at(i));
		vectors.push_back(vector);
	}
	inv_mass=hardware::InvariantMass(vectors);
	return inv_mass;
}
