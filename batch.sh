set -e
git pull
cd scripts
python 02_convertTei2Curation.py
python 12_convertTei2GSheets.py
cd ../
git add .
git commit -a -m "update"
git push origin master
