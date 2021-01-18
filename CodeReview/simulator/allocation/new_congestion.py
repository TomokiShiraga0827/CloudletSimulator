from CloudletSimulator.simulator.model.edge_server import MEC_servers, check_add_device,MEC_server
from CloudletSimulator.simulator.model.device import Device, Devices, device_index_search
import math
from math import radians, cos, sin, asin, sqrt, atan2
from typing import List



#APの実行環境を考慮した混雑度(モバイル端末の優先度)の計算

def traffic_ap_congestion(mecs:MEC_servers, devices: Devices, system_time, seach_distance):
    
    """
    あるMECのカバー範囲内の要求リソース量の総和を求める計算（混雑度）
    :param mecs: MEC群
    :param devices: デバイス群
    :param system_time: システムのある時間t
    :param search_distance: 加算距離
    """
    
    data_length = len(mecs)



    #(ステップ1)
    #動作中のモバイル機器の取り出し

    #時刻0秒からsystem_time(system_end_time)までループ
    for t in range (system_time):
        print("time:", t, ", ", t/system_time*100, "%")
        priority_not_count = 0

        # ある時刻tの各MECごとの混雑度を計算(1つ目のMECから順に計算)
        for m in range(data_length):
            mecs[m], devices , count = traffic_ap_congestion_calc(mecs, mecs[m], devices, t, seach_distance)
            priority_not_count = priority_not_count + count
        print("time:", t, "優先度計算失敗回数:", priority_not_count)

    num = len(devices)

    for d in range(num):
        devices[d].mec_name = []
    #devices_congestion_sort(devices, system_time)



#各MECサーバごとに混雑度を計算するメソッド
def traffic_ap_congestion_calc(mecs:MEC_servers, mec:MEC_server, devices: Devices, time , search_distance):
   
    """
    あるMECのカバー範囲内の要求リソース量の総和を求める計算（混雑度）
    :param mec: あるMECサーバ
    :param device: デバイス群
    :param time: システムのある時間t
    :param search_distance: 加算距離
    :sum_ap1: ap1の混雑度
    :sum_ap2: ap2の混雑度
    :sum_ap3: ap3の混雑度
    :server_sum1: 利用可能MEC数(AP1)
    :server_sum2: 利用可能MEC数(AP2)
    :server_sum3: 利用可能MEC数(AP3)
    :ap_num: MECが保持する実行可能APの数
    :device_priority: デバイスの優先度
    :return: ある時刻tのときのMECのカバー範囲内の要求リソース量の総和
    """

    cnt = 0
    device_num = len(devices)
    mec_num = len(mecs)
    #sum = 0                                        #デバイスの要求リソース量の総和を保存しておく変数
    save_device = [None]                            #加算距離内のデバイスのインデックスを保存するための変数
    save_mec = [None]                               #加算距離内のMECのインデックスを保存するための変数
    sum_ap1 = 0
    sum_ap2 = 0
    sum_ap3 = 0
    server_sum1 = 0
    server_sum2 = 0
    server_sum3 = 0
    ap_num = 2
    priority_not_count = 0



    #(ステップ2)
    #アプリケーションごとの混雑度の計算

    #時刻tにおけるあるMECサーバに要求されるAPごとの混雑度(要求リソース量の総和)を求める

    for i in range(device_num):
        startup = devices[i].startup_time
        shutdown = devices[i].shutdown_time

        #動作中のデバイス
        if startup <= time and shutdown >= time:
            # デバイスのplanのindex番号を計算(そのデバイスが生成されてからの時間)
            index = int(time) - int(startup)
            if index < (shutdown - startup):
                # デバイスとMECとの距離を計算(引数で渡されたmec[m]の座標を利用):edge_server.py内のメソッド
                distance = distance_calc(float(devices[i].plan[index].y), float(devices[i].plan[index].x), mec.lat,
                                         mec.lon)

                # 探索距離内あるか判定(デバイスとMECの2点間距離<=MECの加算距離)
                # もしあれば追加、なければfor文を抜けて次のデバイスへ
                if distance <= (search_distance):
                    if save_device[0] is None:
                        save_device[0] = i         #デバイスのインデックスをsave_device[0]に保存
                    else:
                        save_device.append(i)      #デバイスの2つ目以降もsave_device[1 ~ device_num-1]に追加していく

                    cnt = cnt + 1                

                    #デバイスの利用APごとに要求リソース量を追加する(あるMECのAPごとの混雑度の計算)
                    if devices[i].app_ver == 1:
                        sum_ap1 = sum_ap1 + devices[i].use_resource

                    elif devices[i].app_ver == 2:
                        sum_ap2 = sum_ap2 + devices[i].use_resource

                    else:
                        sum_ap3 = sum_ap3 + devices[i].use_resource



    #(ステップ3)
    #アプリケーションごとの利用可能MECサーバ数の計算

    #あるMECの加算距離内に存在する全てのMECサーバを取り出す
    for j in range(mec_num):
        distance = distance_calc(mecs[j].lat, mecs[j].lon, mec.lat, mec.lon)

        # 探索距離内あるか判定(MECとMECの2点間距離<=MECの加算距離)
        # もしあれば追加、なければfor文を抜けて次のMECへ
        if distance <= (search_distance):
            if save_mec[0] is None:
                save_mec[0] = j         #MECのインデックスをsave_mec[0]に保存
            else:
                save_mec.append(j)      #MECの2つ目以降もsave_mec[1 ~ mec_num-1]に追加していく

    #あるMECの加算距離内のMECを取り出してsave_mecに保存している状態なので、あるMECの加算距離内のAPごとの利用可能MEC数を計算する
    if save_device[0] != None:

        #AP1の利用可能MEC数の計算
        for save_index in save_mec:
            for k in range(ap_num):
                if mecs[save_index].app_ver[k] == 1:
                    server_sum1 = server_sum1 + 1

        #AP2の利用可能MEC数の計算
        for save_index in save_mec:
            for l in range(ap_num):
                if mecs[save_index].app_ver[l] == 2:
                    server_sum2 = server_sum2 + 1

        #AP3の利用可能MEC数の計算
        for save_index in save_mec:
            for m in range(ap_num):
                if mecs[save_index].app_ver[m] == 3:
                    server_sum3 = server_sum3 + 1




    #(ステップ4)
    #モバイル機器に優先度の付与

    #現時点でモバイル端末の優先度を求めるために用意した変数
    #あるMECにおけるAPごとの混雑度:sum_ap1, sum_ap2, sum_ap3
    #あるMECにおけるAPごとの利用可能MECサーバ数:server_sum1, server_sum2, server_sum3

    #あるMECサーバの加算距離内に存在するモバイル機器の優先度を計算する
    if save_device[0] != None:
        #モバイル機器の優先度が高い場合には優先度を更新する
        for save_index in save_device:

            #モバイル機器が利用するAPごとに場合分けして優先度を計算
            if devices[save_index].app_ver == 1:

                #0除算の対策(可算距離内にAP3を実行可能なサーバ数が0の場合)
                if server_sum1 == 0:
                    print("優先度計算不可")
                    priority_not_count = priority_not_count + 1
                    continue

                #モバイル機器が利用するAP1の優先度を計算
                device_priority = sum_ap1 / server_sum1

                #要求リソースのあるモバイル機器の優先度が初期化後の0のままなら
                if devices[save_index]._congestion_status[time] == 0:                #congestion_status = [0] * system_time
                    devices[save_index]._congestion_status[time] = device_priority   #モバイル機器の優先度を保存
                    devices[save_index].mec_name = mec.name                          #先に計算したMECと比較するために保存
                    
                elif devices[save_index]._congestion_status[time] < device_priority:   #先に計算したモバイル機器の優先度より今回計算したモバイル機器の優先度の方が多い場合
                    devices[save_index]._congestion_status[time] = device_priority     #モバイル機器の優先度が大きい方に値を更新
                    devices[save_index].mec_name = mec.name
                else:
                    # 値が被る時(混雑度を近い方に更新)
                    startup = devices[save_index].startup_time
                    index = int(time) - int(startup)
                    if index < (shutdown - startup):
                        #previous_mec:先に計算したMECのインデックス
                        #previous_distance:先に計算したMECとの距離
                        #current_distance:現在計算したMECとの距離

                        previous_mec = search_mec(mecs, devices[save_index].mec_name)
                        previous_distance = distance_calc(float(devices[save_index].plan[index].y),
                                                        float(devices[save_index].plan[index].x),
                                                        previous_mec.lat, previous_mec.lon)
                        current_distance = distance_calc(float(devices[save_index].plan[index].y),
                                                        float(devices[save_index].plan[index].x), mec.lat, mec.lon)
                        if current_distance < previous_distance:
                            devices[save_index]._congestion_status[time] = device_priority
                            devices[save_index].mec_name = mec.name

            elif devices[save_index].app_ver == 2:

                # 0除算の対策(可算距離内にAP3を実行可能なサーバ数が0の場合)
                if server_sum2 == 0:
                    print("優先度計算不可")
                    priority_not_count = priority_not_count + 1
                    continue

                #モバイル機器が利用するAP2の優先度を計算
                device_priority = sum_ap2 / server_sum2

                #要求リソースのあるモバイル機器の優先度が初期化後の0のままなら
                if devices[save_index]._congestion_status[time] == 0:                #congestion_status = [0] * system_time
                    devices[save_index]._congestion_status[time] = device_priority   #モバイル機器の優先度を保存
                    devices[save_index].mec_name = mec.name                          #先に計算したMECと比較するために保存
                    
                elif devices[save_index]._congestion_status[time] < device_priority:   #先に計算したモバイル機器の優先度より今回計算したモバイル機器の優先度の方が多い場合
                    devices[save_index]._congestion_status[time] = device_priority     #モバイル機器の優先度が大きい方に値を更新
                    devices[save_index].mec_name = mec.name
                else:
                    # 値が被る時(混雑度を近い方に更新)
                    startup = devices[save_index].startup_time
                    index = int(time) - int(startup)
                    if index < (shutdown - startup):
                        #previous_mec:先に計算したMECのインデックス
                        #previous_distance:先に計算したMECとの距離
                        #current_distance:現在計算したMECとの距離

                        previous_mec = search_mec(mecs, devices[save_index].mec_name)
                        previous_distance = distance_calc(float(devices[save_index].plan[index].y),
                                                        float(devices[save_index].plan[index].x),
                                                        previous_mec.lat, previous_mec.lon)
                        current_distance = distance_calc(float(devices[save_index].plan[index].y),
                                                        float(devices[save_index].plan[index].x), mec.lat, mec.lon)
                        if current_distance < previous_distance:
                            devices[save_index]._congestion_status[time] = device_priority
                            devices[save_index].mec_name = mec.name

            else:

                # 0除算の対策(可算距離内にAP3を実行可能なサーバ数が0の場合)
                if server_sum3 == 0:
                    print("優先度計算不可")
                    priority_not_count = priority_not_count + 1
                    continue

                #モバイル機器が利用するAP3の優先度を計算
                device_priority = sum_ap3 / server_sum3

                #要求リソースのあるモバイル機器の優先度が初期化後の0のままなら
                if devices[save_index]._congestion_status[time] == 0:                #congestion_status = [0] * system_time
                    devices[save_index]._congestion_status[time] = device_priority   #モバイル機器の優先度を保存
                    devices[save_index].mec_name = mec.name                          #先に計算したMECと比較するために保存
                    
                elif devices[save_index]._congestion_status[time] < device_priority:   #先に計算したモバイル機器の優先度より今回計算したモバイル機器の優先度の方が多い場合
                    devices[save_index]._congestion_status[time] = device_priority     #モバイル機器の優先度が大きい方に値を更新
                    devices[save_index].mec_name = mec.name
                else:
                    # 値が被る時(混雑度を近い方に更新)
                    startup = devices[save_index].startup_time
                    index = int(time) - int(startup)
                    if index < (shutdown - startup):
                        #previous_mec:先に計算したMECのインデックス
                        #previous_distance:先に計算したMECとの距離
                        #current_distance:現在計算したMECとの距離

                        previous_mec = search_mec(mecs, devices[save_index].mec_name)
                        previous_distance = distance_calc(float(devices[save_index].plan[index].y),
                                                        float(devices[save_index].plan[index].x),
                                                        previous_mec.lat, previous_mec.lon)
                        current_distance = distance_calc(float(devices[save_index].plan[index].y),
                                                        float(devices[save_index].plan[index].x), mec.lat, mec.lon)
                        if current_distance < previous_distance:
                            devices[save_index]._congestion_status[time] = device_priority
                            devices[save_index].mec_name = mec.name




    return mec, devices, priority_not_count



#(ステップ5)
#モバイル機器を優先度順にソート

#APを考慮した割り当てに変更する(モバイル端末に優先度を設定:優先度=APの混雑度/周辺のAPの動作環境数)
#事前にAPの優先度を求めて、このメソッド内で毎秒ごとにモバイル端末の優先度順にソートする
def devices_ap_congestion_sort(devices:Device, system_time):

    """
    デバイス群を毎秒ごとにモバイル端末の優先度順に降順ソートする
    :param devices: あるデバイス
    :param system_time: ある時間
    :d_congestion_status[t]: モバイル機器の優先度
    :return ソート済のデバイス群
    """

    sorted_devices = [Devices] * system_time
    for t in range(system_time):
        sorted_devices[t] = sorted(devices, key=lambda d: d._congestion_status[t], reverse=True)
    return sorted_devices



# ユーグリット距離
def distance_calc(lat1, lon1, lat2, lon2):

    """
    ２点の緯度経度から距離（メートル）を計算するメソッド
    :param lat1 : １点目の　lat
    :param lon1 : １点目の　lot
    :param lat2 : ２点目の　lat
    :param lot2 : ２点目の　lot
    :return : 距離
    """

    # return distance as meter if you want km distance, remove "* 1000"
    radius = 6371 * 1000

    dLat = (lat2 - lat1) * math.pi / 180
    dLot = (lon2 - lon1) * math.pi / 180

    lat1 = lat1 * math.pi / 180
    lat2 = lat2 * math.pi / 180

    val = sin(dLat / 2) * sin(dLat / 2) + sin(dLot / 2) * sin(dLot / 2) * cos(lat1) * cos(lat2)
    ang = 2 * atan2(sqrt(val), sqrt(1 - val))
    return radius * ang  # meter



def search_mec(mecs:MEC_servers, mec_name):
    mec_num = len(mecs)
    for m in range(mec_num):
        if mecs[m].name == mec_name:
            return mecs[m]












#APの実行環境を考慮しない混雑度の計算------------------------------------------------------------------------------------------------------------

def traffic_congestion(mecs:MEC_servers, devices: Devices, system_time, seach_distance):
    """
    あるMECのカバー範囲内の要求リソース量の総和を求める計算（混雑度）
    :param mecs: MEC群
    :param devices: デバイス群
    :param system_time: システムのある時間t
    :param search_distance: 加算距離
    """

    data_length = len(mecs)

    #時刻0秒からsystem_time(system_end_time)までループ
    for t in range (system_time):
        print("time:", t, ", ", t/system_time*100, "%")

        # ある時刻tの各MECごとの混雑度を計算(1つ目のMECから順に計算)
        for m in range(data_length):
            mecs[m], devices = traffic_congestion_calc(mecs, mecs[m], devices, t, seach_distance)

    num = len(devices)

    for d in range(num):
        devices[d].mec_name = []
    #devices_congestion_sort(devices, system_time)


#各MECサーバごとに混雑度を計算するメソッド
def traffic_congestion_calc(mecs:MEC_servers, mec:MEC_server, devices: Devices, time , search_distance):
    """
    あるMECのカバー範囲内の要求リソース量の総和を求める計算（混雑度）
    :param mec: あるMECサーバ
    :param device: デバイス群
    :param time: システムのある時間t
    :param search_distance: 加算距離
    :return ある時刻tのときのMECのカバー範囲内の要求リソース量の総和
    """

    cnt = 0
    device_num = len(devices)
    sum = 0                                  #デバイスの要求リソース量の総和を保存しておく変数
    save = [None]                            #デバイスのインデックスを保存するための変数

    #時刻tにおけるあるMECサーバに要求されるリソース量の総和sumを求める
    for i in range(device_num):
        startup = devices[i].startup_time
        shutdown = devices[i].shutdown_time
        if startup <= time and shutdown >= time:
            # デバイスのplanのindex番号を計算
            index = int(time) - int(startup)
            if index < (shutdown - startup):
                # デバイスとMECとの距離を計算(引数で渡されたmec[m]の座標を利用):edge_server.py内のメソッド
                distance = distance_calc(float(devices[i].plan[index].y), float(devices[i].plan[index].x), mec.lat,
                                         mec.lon)

                # 探索距離内あるか判定(デバイスとMECの2点間距離<=MECの加算距離)
                # もしあれば追加、なければfor文を抜けて次のデバイスへ
                if distance <= (search_distance):
                    if save[0] is None:
                        save[0] = i         #デバイスのインデックスをsave[0]に保存
                    else:
                        save.append(i)      #デバイスの2つ目以降もsave[1~device_num-1]に追加していく

                    cnt = cnt + 1                          #デバイスのインデックスを保存
                    sum = sum + devices[i].use_resource    #デバイスの要求リソース量をsumに追加する
    #print(save)

    mec._congestion_status[time] = sum                     #時刻tにおけるあるMECサーバに要求されるリソース量の総和

    if save[0] != None:
        for save_index in save:
            # 混雑度が多ければ、値を更新する

            #要求リソースのあるデバイスの混雑度が初期化後の0のままなら
            if devices[save_index]._congestion_status[time] == 0:      #congestion_status = [0] * system_time
                devices[save_index]._congestion_status[time] = sum     #MECの要求リソース量を保存

                # 先に計算したMECと比較するために保存
                devices[save_index].mec_name = mec.name                

            elif devices[save_index]._congestion_status[time] < sum:   #先に計算したMECの要求リソース量より今回計算したMECの要求リソース量が多い場合
                devices[save_index]._congestion_status[time] = sum     #MECの要求リソース量の総和が大きい方に値を更新
                devices[save_index].mec_name = mec.name
            else:

            # 値が被る時 or 小さい時?
                startup = devices[save_index].startup_time
                index = int(time) - int(startup)
                if index < (shutdown - startup):
                    previous_mec = search_mec(mecs, devices[save_index].mec_name)
                    previous_distance = distance_calc(float(devices[save_index].plan[index].y),
                                                      float(devices[save_index].plan[index].x),
                                                      previous_mec.lat, previous_mec.lon)
                    current_distance = distance_calc(float(devices[save_index].plan[index].y),
                                                      float(devices[save_index].plan[index].x), mec.lat, mec.lon)
                    if current_distance < previous_distance:
                        devices[save_index]._congestion_status[time] = sum
                        devices[save_index].mec_name = mec.name

    return mec, devices








# デバイスを混雑度順に降順ソートする
def devices_congestion_sort(devices:Device, system_time):

    """
    デバイス群を毎秒ごとに混雑度順に降順ソートする
    :param devices: あるデバイス
    :param system_time: ある時間
    :return ソート済のデバイス群
    """

    sorted_devices = [Devices] * system_time
    for t in range(system_time):
        sorted_devices[t] = sorted(devices, key=lambda d: d._congestion_status[t], reverse=True)
    return sorted_devices



"""
def congestion_map_calc():
    min_lat = 34.632282
    max_lat = 34.652382
    min_lon = 133.87895
    max_lon = 133.92678
    lat_value = (max_lat - min_lat) / 50
    lon_value = (max_lon - min_lon) / 50
    for n in range(250):
        # 格子状の範囲で地図を区切り、混雑度を計算できるようにする。
    print()
"""