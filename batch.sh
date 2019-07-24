git pull
cd scripts
python convertTei2Curation.py
cd ../
git add .
git commit -a -m "update"
git push origin master