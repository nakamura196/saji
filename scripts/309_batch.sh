set -e
python 302_convertTei2Json.py
python 303_convertJson2Curation.py
python 304_convertCuration2Csv.py