# アプリケーション

- 検索・一覧
  - [Google Sheets](https://docs.google.com/spreadsheets/d/1W2akkXwfDENiC78Cbx1qs3rx39RvIz4ZEGMio0ZMRYs/edit?usp=sharing)

- 分析：Google データポータル
  - [文書（アイテム）別](https://datastudio.google.com/u/0/reporting/1zQUZX8ZQwhI5hU_OH5t9hvt1HB9pcwiZ/page/yjjFB)
  - [構成要素（Div1）別](https://datastudio.google.com/u/0/reporting/17i24MCcKJ3P5GQLIcWHCQhB13uNg4YkP/page/EVtFB)

- 画像切り出し
  - [IIIF Curation Viewer](http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?curation=https://nakamura196.github.io/saji/data/curation.json)
  - [IIIF Curation Comparison](https://nakamura196.github.io/icc2/?u=https://nakamura196.github.io/saji/data/curation.json)

# ファイルのアップロード方法
- D:\一次史料\Kreševo\saji で右クリックして、GIT Bash Here をクリックし、以下を貼り付ける
- sh batch.sh

# 【OLD】アプリケーション
- 可視化
  - [集計](https://nakamura196.github.io/min3/vis.html?u=https://nakamura196.github.io/saji/data/data.json)
    - [例: typeとfond](https://nakamura196.github.io/min3/vis?field=http%3A%2F%2Fdiyhistory.org%2Fpublic%2Fphr2%2Fns%2Fsaji%2Ffond&u=https%3A%2F%2Fnakamura196.github.io%2Fsaji%2Fdata%2Fdata.json&dispField=&max=10&sort=Numbers)
    - [第一階層毎の文書数](https://nakamura196.github.io/min3/vis.html?filter_field_1=http%3A%2F%2Fdiyhistory.org%2Fpublic%2Fphr2%2Fns%2Fsaji%2Ftype0&filter_values_1=buyuruldu%2CEMIN%2Cferm%C4%81n%2Cfetv%C4%81%2Ch%C3%BCccet%2Ci%CA%BFl%C4%81m%2Ckass%C4%81m%2Cm%C3%BCr%C4%81sele%2Ctapu%2Ctemess%C3%BCk%2Ctezkire%2Cunknown%2C%CA%BFarz-%C4%B1_h%C4%81l%2C%CA%BFilm%C3%BChaber&filter_field_2=http%3A%2F%2Fdiyhistory.org%2Fpublic%2Fphr2%2Fns%2Fsaji%2Ffond&filter_values_2=Tursko%2B1%2CTursko%2B2&y_axis_field=&u=https%3A%2F%2Fnakamura196.github.io%2Fsaji%2Fdata%2Fdata.json&dispField=http%3A%2F%2Fdiyhistory.org%2Fpublic%2Fphr2%2Fns%2Fsaji%2Ftype0&max=10&sort=Numbers)
    - [第一階層毎のフォルダ別文書数](https://nakamura196.github.io/min3/vis.html?filter_field_1=http%3A%2F%2Fdiyhistory.org%2Fpublic%2Fphr2%2Fns%2Fsaji%2Ftype0&filter_values_1=buyuruldu%2CEMIN%2Cferm%C4%81n%2Cfetv%C4%81%2Ch%C3%BCccet%2Ci%CA%BFl%C4%81m%2Ckass%C4%81m%2Cm%C3%BCr%C4%81sele%2Ctapu%2Ctemess%C3%BCk%2Ctezkire%2Cunknown%2C%CA%BFarz-%C4%B1_h%C4%81l%2C%CA%BFilm%C3%BChaber&filter_field_2=http%3A%2F%2Fdiyhistory.org%2Fpublic%2Fphr2%2Fns%2Fsaji%2Ffond&filter_values_2=Tursko%2B1%2CTursko%2B2&y_axis_field=http%3A%2F%2Fdiyhistory.org%2Fpublic%2Fphr2%2Fns%2Fsaji%2Ffond&u=https%3A%2F%2Fnakamura196.github.io%2Fsaji%2Fdata%2Fdata.json&dispField=http%3A%2F%2Fdiyhistory.org%2Fpublic%2Fphr2%2Fns%2Fsaji%2Ftype0&max=10&sort=Numbers)
    - [フォルダ毎の第一階層別文書数](https://nakamura196.github.io/min3/vis.html?filter_field_1=http%3A%2F%2Fdiyhistory.org%2Fpublic%2Fphr2%2Fns%2Fsaji%2Ftype0&filter_values_1=buyuruldu%2CEMIN%2Cferm%C4%81n%2Cfetv%C4%81%2Ch%C3%BCccet%2Ci%CA%BFl%C4%81m%2Ckass%C4%81m%2Cm%C3%BCr%C4%81sele%2Ctapu%2Ctemess%C3%BCk%2Ctezkire%2Cunknown%2C%CA%BFarz-%C4%B1_h%C4%81l%2C%CA%BFilm%C3%BChaber&filter_field_2=http%3A%2F%2Fdiyhistory.org%2Fpublic%2Fphr2%2Fns%2Fsaji%2Ffond&filter_values_2=Tursko%2B1%2CTursko%2B2&y_axis_field=http%3A%2F%2Fdiyhistory.org%2Fpublic%2Fphr2%2Fns%2Fsaji%2Ftype0&u=https%3A%2F%2Fnakamura196.github.io%2Fsaji%2Fdata%2Fdata.json&dispField=http%3A%2F%2Fdiyhistory.org%2Fpublic%2Fphr2%2Fns%2Fsaji%2Ffond&max=10&sort=Numbers)
  - [タイムライン](https://nakamura196.github.io/min3/input)
