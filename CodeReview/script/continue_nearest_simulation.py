
from CloudletSimulator.simulator.model.edge_server import MEC_server, check_between_time, check_plan_index, check_allocation, copy_to_mec, application_reboot_rate
from CloudletSimulator.simulator.model.device import max_hop_search, min_hop_search, average_hop_calc,device_index_search, device_resource_calc, max_distance_search, min_distance_search, average_distance_calc
from CloudletSimulator.simulator.allocation.new_congestion import devices_ap_congestion_sort
from CloudletSimulator.simulator.allocation.new_continue import continue_search
from CloudletSimulator.simulator.convenient_function.write_csv import write_csv
from CloudletSimulator.simulator.allocation.new_nearest import nearest_search
from CloudletSimulator.simulator.model.aggregation_station import set_aggregation_station
from CloudletSimulator.simulator.allocation.move_plan_priority import search_mec_index
from CloudletSimulator.simulator.allocation.reverse_resource import reverse_resource_sort
import pandas as pd
import pickle
import random
import sys

def continue_nearest_simulation(system_end_time, MEC_resource, device_num, continue_distance, device_allocation_method, path_w, how_compare):
    df = pd.read_csv("/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/base_station/okayama_kddi.csv",
                     dtype={'lon': 'float', 'lat': 'float'})
    server_type = "LTE"
    cover_range = 500
    n = len(df)
    print("Number of MEC server:", n)
    mec = [MEC_server(0, 00, " ", 00.00, 00.00, 0, 0)] * n


    #MECインスタンスをCSVを元に生成
    data_length = len(df)   

    for index, series in df.iterrows():
        mec[index] = MEC_server(MEC_resource, index + 1, server_type, series["lon"], series["lat"],
                                cover_range, system_end_time)
    #mec = delete_mec(mec)
    

   #MECサーバにAPの情報を付与(乱数を取得し実行可能なAPを設定する)
    count = 1
    for t in range(data_length):
        if count == 1:
            mec[t]._app_ver = [1,2]
            count = 2
        elif count == 2:
            mec[t]._app_ver = [1,3]
            count = 3
        else:
            mec[t]._app_ver = [2,3]
            count = 1
    

    mec_num = len(df)

    # 集約局を対応するMECに設定する
    set_aggregation_station(mec)

    # 到着順
    if device_allocation_method == 0:

        if how_compare == "hop":
            d = open('/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/dataset/device.ns_clone_binaryfile2', 'rb')
        else:
            d = open('/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/dataset/device.ns_clone_binaryfile','rb')
        devices = pickle.load(d)
        devices = devices[0:device_num]
        num = len(devices)
        for i in range(num):
            devices[i].startup_time = float(devices[i].plan[0].time)  # 各デバイスの起動時間を設定する
            devices[i].set_congestion_status(system_end_time)
            devices[i].set_MEC_distance(len(df))
            devices[i]._first_flag = True
            devices[i]._allocation_plan = [None] * system_end_time
        # 順序をシャッフル(各時間ごとに到着順をランダムで決める)
        random.shuffle(devices)
        sorted_devices = [devices] * system_end_time
        for t in range(system_end_time):
            random.shuffle(devices)
            sorted_devices[t] = devices
    # リソース順
    elif device_allocation_method == 1:

        if how_compare == "hop":
            d = open('/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/dataset/device.clone_binaryfile2', 'rb')
        else:
            d = open('/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/dataset/device.clone_binaryfile','rb')
        devices = pickle.load(d)
        devices = devices[0:device_num]
        num = len(devices)
        devices = reverse_resource_sort(devices)
        for i in range(num):
            devices[i].startup_time = float(devices[i].plan[0].time)  # 各デバイスの起動時間を設定する
            devices[i].set_congestion_status(system_end_time)
            devices[i].set_MEC_distance(len(df))
            devices[i]._first_flag = True
        sorted_devices = [devices] * system_end_time               #デバイスをリソース順にソートする
        
    # 混雑度順
    else:
        # 混雑度計算
        # traffic_congestion(mec, devices, system_end_time, 1000)

        if how_compare == "hop":
            cd = open('/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/script/normal/device_compare/congestion_checked_devices2.binaryfile', 'rb')
        else:
            cd = open('/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/script/normal/device_compare/congestion_checked_devices1.binaryfile', 'rb')
        cd = pickle.load(cd)
        devices = cd
        num = len(devices)
        print("device_num", num)

        # 混雑度順で毎秒ごとのdevicesをソートする
        sorted_devices = devices_ap_congestion_sort(devices, system_end_time)



   
    # save_devices = [] * data_length

    # ここからメインの処理----------------------------------------------------------------------------------------

    keep_count = 0

    for t in range(system_end_time):
        #print("[TIME:", t, "]")
        # ある時刻tのMECに割り当てらえたデバイスを一時的に保存する用の変数
        save_devices = [None] * mec_num

        for i in range(num):
            #print("---new device---", sorted_devices[t][i].name)
            # plan_indexがデバイスの稼働時間外なら処理をスキップ
            if (check_plan_index(sorted_devices[t][i].plan_index, len(sorted_devices[t][i].plan)) == False):
                #print("skip")
                continue

            # plan_indexが稼働時間内なら処理開始
            if check_between_time(sorted_devices[t][i], t) == True:
                #print("plan_index", sorted_devices[t][i].plan_index, "max_index", len(sorted_devices[t][i].plan))

                # 継続割り当て
                device_flag, allocation_MEC_name = continue_search(sorted_devices[t][i], mec,
                                                                   sorted_devices[t][i].plan_index, cover_range, t, continue_distance)

                if device_flag == True:
                    # 継続回数
                    keep_count = keep_count + 1

                    # 最近傍選択
                if device_flag == False:
                    device_flag, allocation_MEC_name = nearest_search(sorted_devices[t][i], mec,
                                                                       sorted_devices[t][i].plan_index, cover_range, t)
                # 割り当てが成功したら表示する
                if device_flag == True:
                    # deviceが直前で割り当てたMECのインデックスを取得
                    mec_index = search_mec_index(mec, allocation_MEC_name)

                    # print("device:", sorted_devices[t][i].name, ", use_resource:", sorted_devices[t][i].use_resource, "--->", "MEC_ID:", mec[mec_index].name, ", index:", i)
                    # print(sorted_devices[t][i].mec_name, mec[mec_index].resource)
                    # print(mec_index, len(save_devices))
                    # ---
                    
                    # なぜindexがmec_indexなの？ <- mec用のリストだから
                    if save_devices[mec_index] == None:
                        save_devices[mec_index] = [sorted_devices[t][i].name]            #ある時刻tにMECに割り当てたデバイス名を保存
                    else:
                        save_devices[mec_index].append(sorted_devices[t][i].name)        #デバイス名を追加

                    mec_index = 0         #初期化
                #else:
                    #print("NOT FIND")
                # plan_indexをインクリメント

                sorted_devices[t][i]._plan_index = sorted_devices[t][i]._plan_index + 1   #sorted_devicesのインスタンスのplan_indexをインクリメント
                
            # デバイスの稼働時間を超えた時の処理
            else:
                # もしデバイスの終了時間を超えた時のみ（１回だけ）、デバイスに直前に割り当てたMECのリソースをリカバリーする。
                if sorted_devices[t][i].mec_name != [] and sorted_devices[t][i]._lost_flag == False:
                    #print("DECREASE")
                    sorted_devices[t][i].set_mode = "decrease"                             #移動し終わったデバイスのmodeを変更
                    #print(sorted_devices[t][i].mec_name)
                    mec[sorted_devices[t][i].mec_name - 1].custom_resource_adjustment(sorted_devices[t][i], t)  #MECのリソースを調整(増やす)
                    mec[sorted_devices[t][i].mec_name - 1].save_resource(t)                                     #時刻tにおけるリソースの状態を保存するメソッド:resource_per_second[time]に保存   
                    sorted_devices[t][i].set_mode = "add"                                                       #初期値に更新
                    sorted_devices[t][i]._lost_flag = True                                                      #初期値に更新

        # ある時刻tのMECに一時的に保存していた割り当てたデバイスをコピーする。
        copy_to_mec(mec, save_devices, t)



    #-----
    # リソース消費量がそれぞれで違う時のテスト用関数を作成する
    # 各秒でMECが持っているデバイスのインデックスと数がわかるものとする

    #sum = 0
    #mec_sum = 0
    #having_device_resource_sum = 0
   


    """
    for t in range(system_end_time):
        # print("time:", t)
        for m in range(mec_num):
            # if t == 16:
            # print("MEC_ID:", mec[m].name, ", having devices:", mec[m]._having_devices[t], mec[m]._having_devices_count[t],
            # ", mec_resouce:", mec[m]._resource_per_second[t], ", current time:", t)
            # sum = sum + mec[m]._having_devices_count[t]
            # mec_sum = mec_sum + mec[m]._resource_per_second[t]
            # sum = sum + mec[m]._having_devices_count[t]
            mec_sum = mec_sum + mec[m]._resource_per_second[t]
            if mec[m]._having_devices[t] is not None:
                # print("check", mec[m]._having_devices[t])
                device_index = device_index_search(sorted_devices[t], mec[m]._having_devices[t])
                # print(mec[m]._having_devices[t], device_index)
                having_device_resource_sum = having_device_resource_sum + device_resource_calc(sorted_devices[t],
                                                                                               device_index)
        check_allocation(t, 150, MEC_resource, having_device_resource_sum, mec_sum)
        print((150 * MEC_resource - having_device_resource_sum), mec_sum)
        having_device_resource_sum = 0
        sum = 0
        mec_sum = 0
    """
    # print(sum, (150*100-sum), mec_sum)





    
    num = len(sorted_devices[-1])

    print("system_time: ", system_end_time)
    print("MEC_num: ", mec_num)
    print("device_num: ", num)

    sorted_devices = sorted_devices[0:system_end_time]

    maximum = max_hop_search(sorted_devices[-1])
    print("max_hop: ", maximum)

    minimum = min_hop_search(sorted_devices[-1])
    print("min_hop: ", minimum)

    average_hop = average_hop_calc(sorted_devices[-1])
    print("average_hop: ", average_hop)

    reboot_rate = application_reboot_rate(mec, system_end_time)
    print("AP reboot rate:", reboot_rate)

    max_distance = max_distance_search(sorted_devices[-1])
    print("max_distance:", max_distance)

    min_distance = min_distance_search(sorted_devices[-1])
    print("min_distance:", min_distance)

    average_distance = average_distance_calc(sorted_devices[-1])
    print("average_distance: ", average_distance)


    result = [system_end_time]
    result.append(mec_num)
    result.append(MEC_resource)
    result.append(num)
    result.append(maximum)
    result.append(minimum)
    result.append(average_hop)
    result.append(reboot_rate)
    result.append(max_distance)
    result.append(min_distance)
    result.append(average_distance)

    # pathを動的に変えることで毎回新しいファイルを作成することができる
    write_csv(path_w, result)
    print("finish")

    return average_hop, reboot_rate
