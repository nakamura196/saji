cd scripts
python 02_convertTei2Curation.py
python 12_convertTei2GSheets.py
cd ../
git commit -a -m "update sheets"
git push origin master