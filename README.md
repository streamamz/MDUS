# MESSENGER's Data Using System (MDUS)
MESSENGERでの観測データを容易に利用できることを目的としたライブラリです

## 依存ライブラリ/Pythonバージョン
以下の環境で正常に動作することを確認しています

* Python 3.10.12
* astropy 6.1.7
* astroquery 0.4.9.post1
* matplotlib 3.5.1
* numpy 1.26.4
* pandas 2.2.2

## 対応データ
以下のデータに対応しています．引用についてはPDSにて確認してください

* [MESSENGER MAG Time-Averaged Calibrated MSO Coordinates Science Data Collection](https://pds-ppi.igpp.ucla.edu/collection/urn:nasa:pds:mess-mag-calibrated:data-mso-avg)      
  * 1，5，10，60秒平均データに対応しています．生データには対応していません
  
今後，FIPS_CDR_SCANデータ等に対応予定です

## 使用方法
```sample.ipynb```を参照してください