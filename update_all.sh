cd "$(dirname $0)"
#Must be updated manually as there now is cloudflare captcha in fron tof the site ./brasil_rnc.sh
#Must be updated manually as there now is cloudflare captcha in fron tof the site ./brasil_ienc.py > BR_IENC_Catalog.xml || rm BR_IENC_Catalog.xml
./de_ienc.sh
python3 euris_inc.py
#./noaa_mbtiles.sh
# Moved to hourly (update_nl.sh) - ./nl_ienc.sh
./danube_ienc.sh
./at_ienc.sh
mv *.xml ../catalogs/
cd ../catalogs
git fetch --all
git commit -a -m "Automatic catalog update"
git rebase origin/master
git push

