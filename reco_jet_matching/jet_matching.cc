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


ROOT::VecOps::RVec<Int_t> RecoHGG(ROOT::VecOps::RVec<Int_t> GenHGG,Int_t nJet,ROOT::VecOps::RVec<Float_t> Jet_phi, ROOT::VecOps::RVec<Float_t> Jet_eta,ROOT::VecOps::RVec<Float_t> GenPart_phi, ROOT::VecOps::RVec<Float_t> GenPart_eta) { \
        ROOT::VecOps::RVec<Int_t> GG={-1,-1}; \
        for(Int_t geni=0;geni<2;geni++){ \
            Float_t gen_phi=GenPart_phi[GenHGG[geni]]; \
            Float_t gen_eta=GenPart_eta[GenHGG[geni]];\
            for (Int_t i=0;i<nJet;i++){ \
                Float_t reco_phi=Jet_phi[i];\
                Float_t reco_eta=Jet_eta[i];\
                Float_t diff_phi=std::abs(gen_phi-reco_phi)<3.1415926 ? std::abs(gen_phi-reco_phi) : 2*3.1415926-std::abs(gen_phi-reco_phi);\
                Float_t diff_eta=std::abs(gen_eta-reco_eta);\
                Float_t R=0.4;\
                if(diff_eta*diff_eta+diff_phi*diff_phi<=R*R){\
                    GG[geni]=i;\
                    break;\
                } \
            } \
        } \
        return GG; \
} \

