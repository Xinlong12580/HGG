import ROOT
dataset_file = "raw_nano/HToGG_ZToLL_18.txt"
with open( dataset_file , "r") as dataset:
    root_files = [ line.strip() for line in dataset];
print(root_files)

rdf = ROOT.RDataFrame("Runs", root_files)

sumw=rdf.Sum("genEventSumw").GetValue()
print(sumw)

