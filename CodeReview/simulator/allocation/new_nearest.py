from CloudletSimulator.simulator.model.edge_server import MEC_servers, check_add_device,MEC_server, check_between_time, check_plan_index
from CloudletSimulator.simulator.model.device import Device
from CloudletSimulator.simulator.model.hop_calc import hop_calc,keep_hop
from CloudletSimulator.simulator.allocation.move_plan_priority import search_mec_index
from geopy.distance import vincenty
import math
from math import radians, cos, sin, asin, sqrt, atan2
import sys
import numpy
import collections
from typing import List, Dict

def nearest_search(device:Device, mec:MEC_servers, plan_index, cover_range, time):
    """
    最近傍法のアルゴリズムでリソース割り当てを行うメソッド
    最も近いMECサーバをデバイスに割り当てる
    :param device: デバイス
    :param mec: MECサーバ群
    :param plan_index: デバイスのplanのindex
    :param cover_range: 基地局のカバー範囲
    :param time: 現在時刻t
    :return: 割り当てたans_idをTrueと共に返す, 割り当てられなかった時はFalseを返す
    """
    data = len(mec)
    distance = collections.namedtuple("distance", ("index", "value", "flag"))
    mec_distance = [distance] * data
    cnt = 0 #Falseの回数をカウント
    # 最近傍法を使うために、各MECサーバとの距離を計算
    for m in range(data):
        if mec[m].check_resource(device.use_resource) == True and len(device.plan) > plan_index:
            tmp_distance = distance_calc(float(device.plan[plan_index].y),
                                         float(device.plan[plan_index].x), mec[m].lat, mec[m].lon)
            mec_distance[m] = distance(m, tmp_distance, True)
        else:
            mec_distance[m] = distance(m, 100000000, False)
            cnt = cnt + 1
        #print(distance)

    sorted_distance = sorted(mec_distance, key=lambda m:m.value)  #MECサーバとの距離を近い順にソート
    index_count = 0

    ap_num = 2      #MECで実行可能なAPの種類

    while(True):
        finish_len = len(sorted_distance)        #MECサーバ数
        if index_count == finish_len:
            print("MECのリソース量が少な過ぎます")
            sys.exit()
            return False, mec[0].name

        # 最も距離が近い割り当て可能なMECサーバを選び、その配列のインデックスを取得する
        ans_id = sorted_distance[index_count].index
        
        run_flag = False        #実行可能かどうか判定するためのフラグを初期化

        #取得したインデックスのMECの実行可能APで実行可能かどうか判定する
        for t in range(ap_num):
            if device.app_ver == mec[ans_id].app_ver[t]:
                run_flag = True

        #MECの実行可能APの場合(ダメな場合は次のMECへ)
        if run_flag == True:

            #取得したインデックスのMECのリソース量を確認する(ans_id > 0):ダメなら次のMECへ
            if mec[ans_id].resource > 0:

                #継続割り当ての時
                if mec[ans_id].name == device.mec_name:                    #今回割り当てようとしているMECと前回割り当てたMECが同じ場合
                    device.set_mode = "keep"                               #deviceのmoodをkeepに更新
                    mec[ans_id].custom_resource_adjustment(device, time)   #MECのリソースの調整("keep"なのでMECのリソース量に変化なし)
                    print("KEEP", plan_index)
                    device.mec_name = mec[ans_id].name                     #デバイスに割り当てたMECの名前を保存

                    mec[ans_id].add_having_device(time)                    #having_devices_count[time]をインクリメント
                    mec[ans_id].save_resource(time)                        #ある時刻tのMECのリソース状態を保存するメソッド(resource_per_second[time] = resource)
                    device.switch_lost_flag = False                        #lost_flag = False

                    # 追加項目
                    keep_hop(device)                                             #同じ基地局に割り当てる場合(ホップ数1)
                    print(mec[ans_id].aggregation_station)
                    device._aggregation_name = mec[ans_id].aggregation_station   #deviceの集約局名を割り当てるMECの集約局名に更新
                    mec[ans_id].add_allocation_count(time)                       #add_allocation_count[time]をインクリメント
                    mec[ans_id]._keep_count = mec[ans_id]._keep_count + 1        #keep_countをインクリメント 初期値0

                # 移動する時(新規割り当て以外)
                elif mec[ans_id].name != device.mec_name and mec[ans_id].name != None and device.mec_name != []:
                    #deviceに割り当てていたMECと今回のMECの名前が違い、今回のMECの名前が空ではなく、前回deviceに割り当てたMECの名前の配列の中身がない
                    print("********")
                    print(mec[ans_id].name, device.mec_name)

                    previous_index = search_mec_index(mec, device.mec_name)         #以前にデバイスに割り当てていたMECのインデックスを取得
                    #mec_index = mec_index_search(device, mec)
                    # リソースを増やす
                    device.set_mode = "decrease"

                    print("デバイスの前のMEC:", device.mec_name, "前のMEC", mec[previous_index].name)
                    # 前に割り振ったMECのリソースを回復
                    mec[previous_index].custom_resource_adjustment(device, time)    #以前にデバイスを割り当てていたMECのリソースを調整(増やす)
                    device.add_hop_count()                                          #デバイスのhop_countを更新  hop_count 初期値0
                    #hop_calc(device, mec[device.mec_name - 1])
                    mec[previous_index].save_resource(time)       #ある時刻tのMECのリソース状態を保存するメソッド(resource_per_second[time] = resource):今回の場合は以前に割り当てたMEC
                    print("DECREASE")
                    print("切替", device._aggregation_name, mec[ans_id])
                    previous_mec_name = device.mec_name                             #以前(previous)のMECの名前:ホップ数計算のため

                    # リソースを減らす
                    device.set_mode = "add"
                    hop_calc(device, mec, mec[ans_id], previous_mec_name, time)     #ホップ数の計算
                    mec[ans_id].custom_resource_adjustment(device, time)            #MECサーバのリソース量を調整する
                    device.add_hop_count()                                          #デバイスのhop_countを更新  hop_count 初期値0

                    # 新規追加
                    device._aggregation_name = mec[ans_id].aggregation_station      #deviceの集約局名を割り当てるMECの集約局名に更新
                    device.mec_name = mec[ans_id].name                              #デバイスに割り当てたMECの名前を保存
                    #mec[ans_id].add_allocation_count(time)                         #add_allocation_count[time]をインクリメント

                    mec[ans_id].add_having_device(time)                             #having_devices_count[time]をインクリメント  
                    mec[ans_id].save_resource(time)                                 #ある時刻tのMECのリソース状態を保存するメソッド(resource_per_second[time] = resource)
                    device.switch_lost_flag = False                                 #lost_flag = False
                
                #新規割り当て(初回)
                else:
                    # リソースを減らす
                    device.set_mode = "add"
                    mec[ans_id].custom_resource_adjustment(device, time)          #MECサーバのリソース量を調整するメソッド
                    device.add_hop_count()                                        #デバイスのhop_countを更新  hop_count 初期値0
                    device.mec_name = mec[ans_id].name                            #デバイスに割り当てたMECの名前を保存
                    
                    # 新規追加
                    previous_mec_name = device.mec_name                           #以前(previous)のMECの名前:ホップ数計算のため
                    hop_calc(device, mec, mec[ans_id], previous_mec_name, time)   #ホップ数の計算
                    #keep_hop(device)
                    device._aggregation_name = mec[ans_id].aggregation_station    #deviceの集約局名を割り当てるMECの集約局名に更新
                    #mec[ans_id].add_allocation_count(time)                       #add_allocation_count[time]をインクリメント

                    mec[ans_id].add_having_device(time)                           #having_devices_count[time]をインクリメント
                    mec[ans_id].save_resource(time)                               #ある時刻tのMECのリソース状態を保存するメソッド(resource_per_second[time] = resource)
                    device.switch_lost_flag = False                               #lost_flag = False

                print("MEC_RESOURCE", mec[ans_id].resource)

                return True, mec[ans_id].name                                     #(継続 or 切替 or 継続)の処理が終わったのでTrueとデバイスに割り当てたMECの名前を返す

            index_count = index_count + 1

        #MECで実行可能なAPではなかった場合
        index_count = index_count + 1                                         #次のMECのインデックスにアクセスするためインクリメント
    
    #print(device.name)

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



