# Created by mk_runs.py
# NGC5376 [19, 19, 33, 33, 34] vlsr=2080.2
set -x
rm -rf NGC5376
./reduce.py -g -m mask_NGC5376_Havfield_v1.fits 19 NGC5376
./reduce.py -g -m mask_NGC5376_Havfield_v1.fits 33,34 -f 2 NGC5376
./plots.sh NGC5376 _12CO_rebase5_smooth1.3_hanning2.fits 2080.2
