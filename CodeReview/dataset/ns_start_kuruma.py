from CloudletSimulator.simulator.model.edge_server import MEC_server
from CloudletSimulator.simulator.model.device import Device
from CloudletSimulator.simulator.allocation.new_congestion import traffic_congestion
from CloudletSimulator.dataset.delete_MEC import delete_mec
from CloudletSimulator.simulator.model.point import Point3D
import pandas as pd
import pickle
import random
import copy


#MECサーバの選択方法


# テスト用デバイスデータ
device_flag = False
# バイナリデータを読み込み
d = open('/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/dataset/device.congestion_binaryfile', 'rb')
devices = pickle.load(d)
device_num = len(devices)
print("デバイスのMAX数", len(devices))
num = len(devices)

new_devices = None

#500秒以降に初めて生成されたモバイル端末のみを取り出す
for d in range(num):
    startup_time = float(devices[d].startup_time)
    if 500 <= startup_time:
        if new_devices is None:
            new_devices = [devices[d]]
        else:
            new_devices.append(devices[d])

num = len(new_devices)
for d in range(num):
    new_plan = None
    plan_num = len(new_devices[d].plan)
    for p in range(plan_num):
        pivot_time = float(new_devices[d].plan[p].time)
        if new_plan is None:
            new_plan = [Point3D(new_devices[d].plan[p].x, new_devices[d].plan[p].y, float(pivot_time - 500.00))]
        else:
            new_plan.append(Point3D(new_devices[d].plan[p].x, new_devices[d].plan[p].y, float(pivot_time - 500.00)))
    new_devices[d].plan = new_plan

for i in range(num):
    new_devices[i].startup_time = float(new_devices[i].plan[0].time) # 各デバイスの起動時間を設定する

new_devices = sorted(new_devices, key=lambda d: d.startup_time, reverse=False)

num = len(new_devices)
for d in range(num):
    print(d, new_devices[d].startup_time, new_devices[d].plan[0].time)

f = open('/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/dataset/device.ns_start_binaryfile', 'wb')
pickle.dump(new_devices, f)
