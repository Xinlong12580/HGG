HToGG_WminusToLNu_16="file dataset=/WminusH_HToGluGlu_WToLNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v2/NANOAODSIM"
HToGG_WminusToLNu_16APV="file dataset=/WminusH_HToGluGlu_WToLNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"
HToGG_WminusToLNu_17="file dataset=/WminusH_HToGluGlu_WToLNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"
HToGG_WminusToLNu_18="file dataset=/WminusH_HToGluGlu_WToLNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM"
HToGG_WplusToLNu_16="file dataset=/WplusH_HToGluGlu_WToLNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v2/NANOAODSIM"
HToGG_WplusToLNu_16APV="file dataset=/WplusH_HToGluGlu_WToLNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"
HToGG_WplusToLNu_17="file dataset=/WplusH_HToGluGlu_WToLNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"
HToGG_WplusToLNu_18="file dataset=/WplusH_HToGluGlu_WToLNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"
HToGG_ZToLL_16="file dataset=/ZH_HToGluGlu_ZToLL_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v2/NANOAODSIM"
HToGG_ZToLL_16APV="file dataset=/ZH_HToGluGlu_ZToLL_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"
HToGG_ZToLL_17="file dataset=/ZH_HToGluGlu_ZToLL_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"
HToGG_ZToLL_18="file dataset=/ZH_HToGluGlu_ZToLL_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM"
HToGG_ZToNuNu_16="file dataset=/ZH_HToGluGlu_ZToNuNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v2/NANOAODSIM"
HToGG_ZToNuNu_16APV="file dataset=/ZH_HToGluGlu_ZToNuNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"
HToGG_ZToNuNu_17="file dataset=/ZH_HToGluGlu_ZToNuNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"
HToGG_ZToNuNu_18="file dataset=/ZH_HToGluGlu_ZToNuNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM"
all_data_name=(HToGG_WminusToLNu_16 HToGG_WminusToLNu_16APV HToGG_WminusToLNu_17 HToGG_WminusToLNu_18 HToGG_WplusToLNu_16 HToGG_WplusToLNu_16APV HToGG_WplusToLNu_17 HToGG_WplusToLNu_18 HToGG_ZToLL_16 HToGG_ZToLL_16APV HToGG_ZToLL_17 HToGG_ZToLL_18 HToGG_ZToNuNu_16 HToGG_ZToNuNu_16APV HToGG_ZToNuNu_17 HToGG_ZToNuNu_18)
for data_name in "${all_data_name[@]}"; do
	data=${!data_name}
	echo $data
	echo dasgoclient -query "$data"
	dasgoclient -query "$data" | tee "$data_name"_tmp.txt
	sed 's@^@root://cmsxrootd.fnal.gov/@' "$data_name"_tmp.txt > "$data_name".txt
	rm "$data_name"_tmp.txt
done
