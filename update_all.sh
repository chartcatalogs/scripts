cd "$(dirname $0)"
./brasil_rnc.sh
#./de_ienc.sh
python3 euris_inc.py
#./noaa_mbtiles.sh
./nl_ienc.sh
./danube_ienc.sh
./at_ienc.sh
mv *.xml ../catalogs/
cd ../catalogs
git fetch --all
git commit -a -m "Automatic catalog update"
git rebase origin/master
git push

