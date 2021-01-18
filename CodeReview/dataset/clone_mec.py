from CloudletSimulator.simulator.model.edge_server import MEC_server
from CloudletSimulator.simulator.model.device import Device
from CloudletSimulator.simulator.allocation.new_congestion import traffic_congestion
from CloudletSimulator.dataset.delete_MEC import delete_mec
from CloudletSimulator.simulator.model.point import Point3D
import pandas as pd
import pickle
import random
import copy


#MECサーバの選択(モバイル機器の複製)



# テスト用デバイスデータ
device_flag = False
# バイナリデータを読み込み
d = open('/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/dataset/device.ns_start_binaryfile', 'rb')
devices = pickle.load(d)
device_num = len(devices)
print("デバイスのMAX数", len(devices))

device = devices
num = len(devices)

new_devices = None
new_device = copy.deepcopy(devices[0])
for n in range(800): #渋滞を起こすために一台目のモバイル機器を800台生成
    device[0].name = n
    if new_devices is None:
        new_devices = [copy.deepcopy(devices[0])]
    else:
        new_devices.append(copy.deepcopy(devices[0]))

for d in range(200):
    new_devices.append(devices[d]) #元のデバイスを200台追加

num = len(new_devices) #合計1000台

for d in range(750): #750台修正
    if d < 250:
        random_value = random.randint(0, 25)
    elif d < 500:
        random_value = random.randint(70, 100)
    elif d < 750:
        random_value = random.randint(300, 350)

    #random_value = random.randint(0, 100)

    new_plan = None
    plan_num = len(new_devices[d].plan)
    startup_time = float(new_devices[d].startup_time)
    for p in range(plan_num):
        pivot_time = float(new_devices[d].plan[p].time)
        if new_plan is None:
            new_plan = [Point3D(new_devices[d].plan[p].x, new_devices[d].plan[p].y, float(pivot_time - startup_time + random_value))]
        else:
            new_plan.append(Point3D(new_devices[d].plan[p].x, new_devices[d].plan[p].y, float(pivot_time - startup_time + random_value)))
    new_devices[d].plan = new_plan

for i in range(num):
    new_devices[i].startup_time = float(new_devices[i].plan[0].time) # 各デバイスの起動時間を設定する


new_devices = sorted(new_devices, key=lambda d: d.startup_time, reverse=False)

num = len(new_devices)
for d in range(num):
    print(d, new_devices[d].startup_time, new_devices[d].plan[0].time)

#221秒間ある
f = open('/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/dataset/device.clone_binaryfile', 'wb')
pickle.dump(new_devices, f)
