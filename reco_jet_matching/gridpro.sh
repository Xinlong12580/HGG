#python CondorHelper.py -r run_snapshot.sh -a snapshot_args.txt -i "snapshot.py"
python CondorHelper.py -r gridrun.sh -a snapshot_args.txt -i "snapshot.py Cut.cc Matching.cc HGGConst.cc raw_nano"
