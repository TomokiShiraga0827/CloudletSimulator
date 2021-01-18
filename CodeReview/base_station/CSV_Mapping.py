#マップに読み込んだCSVファイル内の携帯基地局の座標にマーカーを設置したマップを取得

import pandas as pd
import folium
#csvを読み込み
df = pd.read_csv('kddi_okayama_city.csv')
##対象範囲の緯度経度（岡山駅周辺）
LAT = 34.673759
LNG = 133.923437
#対象範囲を指定
m = folium.Map(location=[LAT, LNG])
#マップにマーカを反映
for i, r in df.iterrows():
    if r['radio'] == 'LTE':
        #folium.Marker(location=[r['lat'], r['lon']], icon=folium.Icon('blue'), popup="LTE").add_to(m)
        folium.CircleMarker(location=[r['lat'], r['lon']], radius=1000, color="green", fill_color="green").add_to(m)
    else:
        folium.Marker(location=[r['lat'], r['lon']], icon=folium.Icon('red'), popup="UMTS").add_to(m)
#マップを保存
m.save("mapping_BaseStation_500.html")
