from CloudletSimulator.simulator.model.edge_server import MEC_servers, MEC_server
from CloudletSimulator.simulator.model.device import Device
import math
from math import radians, cos, sin, asin, sqrt, atan2

def mec_compare(device:Device, mec: MEC_server):
    # もし直前に割り当てたMECと今割り当てられるMECが同じ場合
    if device._aggregation_name == mec._aggregation_name:
        return True
    else:
        return False

def mec_index_search(device:Device, mecs: MEC_servers):
    mec_num = len(mecs)
    for m in range(mec_num):
        if device._old_mec_name == mecs[m].name:
            return m
    return False

# ホップ数を計算するメソッド
def hop_calc(device:Device, mecs:MEC_servers, mec: MEC_server, previous_mec_name, time):
    """
    ホップ数を計算するメソッド
    :param device: デバイス
    :param mecs: MECサーバ群
    :param mec: 対象のMECサーバ
    :param previous_mec_name: 以前に割り当てたMECの名前
    :param time: 現在時刻
    """
    # ホップ数計算
    # 最初の割り当て
    if device._first_flag == True:           #first_flag 初期値True
        device._hop = [1]                    #device._hop = [1]で更新
        device._first_flag = False
    #elif mec.name == device.mec_name:
       #keep_hop(device)
    # 切替成功

    #first_flag = Falseのとき
    else:   
        mec.add_reboot_count(time)            #reboot_count[time]をインクリメント

        # 集約局が同一の時
        if mec_compare(device, mec) == False:
            device._three_count = device._three_count + 1      #インクリメント
            # ---

            device._hop.append(3)                           # ホップ数の追加
            previous_mec = search_mec(mecs, previous_mec_name)                                  #以前のMECのオブジェクトを取得
            distance = distance_calc(mec.lat, mec.lon, previous_mec.lat, previous_mec.lon)      #以前のMECと今回割り当てるMECの距離を計算

            # 割り当て距離を追加
            if device._distance is None:
                device._distance = [distance]
            else:
                device._distance.append(distance)

            # 最小割り当て距離の更新
            if device._min_distance > distance and distance != 0:
                device._min_distance = distance

            # 最大割り当て距離の更新
            if device._max_distance < distance:
                device._max_distance = distance

        # 集約局が違う時
        else:
            device._hop.append(5)                              #ホップ数の追加
            previous_mec = search_mec(mecs, device.mec_name)
            distance = distance_calc(mec.lat, mec.lon, previous_mec.lat, previous_mec.lon)

            # 割り当て距離を追加
            if device._distance is None:
                device._distance = [distance]
            else:
                device._distance.append(distance)

            # 最小割り当て距離の計算
            if device._min_distance > distance and distance != 0:
                device._min_distance = distance

            # 最大割り当て距離の計算
            if device._max_distance < distance:
                device._max_distance = distance



# mecの名前からmecオブジェクトを返すメソッド
def search_mec(mecs:MEC_servers, mec_name):
    mec_num = len(mecs)
    for m in range(mec_num):
        if mecs[m].name == mec_name:
            return mecs[m]

# 同じ基地局に割り当てる時（ホップ数１）
def keep_hop(device:Device):
    device._hop.append(1)


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