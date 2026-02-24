# HistData変換スクリプト

https://www.histdata.com
からDLしてきたM1のCSVデータをM15に変換するスクリプト

`data`配下にシンボル名のフォルダを置き、その中に各M1 CSVを置いて使用

Ex: `data/usdjpy/DAT_ASCII_USDJPY_M1_2021.csv`

## How to use
```bash
docker compose up -d --build
```

```bash
# data/ 配下の全ファイル一括変換
docker compose exec converter python src/converter.py
# シンボル名を指定して変換(複数可)
docker compose exec converter python src/converter.py data/eurjpy data/eurusd
```
