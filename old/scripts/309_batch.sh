set -e
# TEI/XMLの日付の修正
python 200_convertDate.py

# 分割
python 306_splitFiles.py


python 302_convertTei2Json.py
python 303_convertJson2Curation.py
python 304_convertCuration2Csv.py

# 漏れているtypeのリストアップ
python 501_mergetMissingTypes.py
# 統合用の辞書の修正
python 502_div1.py