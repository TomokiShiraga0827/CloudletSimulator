#csvファイルから岡山駅周辺のKDDI基地局のデータのみを取得する

import csv

input_file = open("japan.csv","r")       #csvファイルの読み込み
reader = csv.reader(input_file)          #リーダの取得

output_file = open("kurashiki_kddi.csv","w")  #新規ファイルの作成
w = csv.writer(output_file)              #ライタの取得

for row in reader:
    
    if row[0] == "radio":                #1行目の代入処理を飛ばすための比較
        w.writerow([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13]])
        continue

    lon = row[6]
    lat = row[7]

    lon = float(lon)
    lat = float(lat)

    if lon >= 133.726147 and lon <= 133.855253 and lat >= 34.565135 and lat <= 34.619178:
        mnc = row[2]
        if mnc == "50" or mnc == "51" or mnc == "53":
            w.writerow([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13]])

output_file.close()
input_file.close()

