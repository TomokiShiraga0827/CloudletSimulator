# edege_serverのテスト用プログラム
# 全体時間を考慮している

from CloudletSimulator.simulator.model.edge_server import MEC_server
from CloudletSimulator.simulator.model.device import Device
from CloudletSimulator.simulator.allocation.new_congestion import traffic_ap_congestion
from CloudletSimulator.dataset.delete_MEC import delete_mec
import pandas as pd
import pickle

def make_congestion_binary2(system_end_time, device_num, MEC_resource, search_distance):
    # SUMO全体の計算時間
    #system_end_time = 4736
    #system_end_time = 100
    # CSV読み込み
    df = pd.read_csv("/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/base_station/okayama_kddi.csv",
                     dtype={'lon': 'float', 'lat': 'float'})
    # 基地局の種類を設定
    server_type = "LTE"

    # 基地局のカバー範囲を設定(メートル)
    cover_range = 500
    # CSVの行数を取得（基地局の数）
    n = len(df)
    print("Number of MEC server:", n)
    # 基地局の数のオブジェクト用リストを作成
    mec = [MEC_server(0, 00, " ", 00.00, 00.00, 0, 0)] * n

    # テスト用デバイスデータ
    device_flag = False
    # バイナリデータを読み込み
    d = open('/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/dataset/device.clone_binaryfile2', 'rb')

    devices = pickle.load(d)
    print("デバイスのMAX数", len(devices))
    devices = devices[0:device_num]


    """
    for i in range(3):
        devices2 = devices
        num = len(devices2)
        for d in range(num):
            devices2[d].name = num + d
        devices.extend(devices2)
    """

    #for i in range(2):
        #devices.extend(devices)

    num = len(devices)
    for i in range(num):
        devices[i].startup_time = float(devices[i].plan[0].time) # 各デバイスの起動時間を設定する
        devices[i].set_congestion_status(system_end_time)
        devices[i].set_MEC_distance(len(df))
        devices[i]._first_flag = True
        devices[i]._allocation_plan = [None] * system_end_time
        #devices[i].use_resource = random.randint(1, 5)

    # MECインスタンスをCSVを元に生成
    data_length = len(df)
    #data_length = 100
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


    # 時間をセット
    #devices[i].startup_time = float(devices[i].plan[0].time) # 各デバイスの起動時間を設定する(コメントアウト)

    # 事前に作成しておいたバイナリデータからデバイスインスタンスを作成
    traffic_ap_congestion(mec, devices, system_end_time, search_distance)

    f = open('/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/script/normal/device_compare/congestion_checked_devices2.binaryfile', 'wb')
    pickle.dump(devices, f)
    f.close