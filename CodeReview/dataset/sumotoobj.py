#MECサーバの選択方法

import csv
from CloudletSimulator.simulator.model.device import Device
from CloudletSimulator.simulator.model.point import Point3D
from CloudletSimulator.simulator.model.angle import Angle,Speed
from typing import List
import pickle
import random

#deviceの作成
with open('sumoTrace.csv', newline='') as csvfile:
	#csvの読み込み
	reader = csv.DictReader(csvfile)
	devices = [] # type:List[Device]
	dflag = 0
	num = 0

	for row in reader:

		d_name = row['vehicle_id']
		d_time = row['timestep_time']
		d_lon = row['vehicle_x']
		d_lat = row['vehicle_y']
		d_angle = Angle(d_time, row['vehicle_angle'])
		d_speed = Speed(d_time, row['vehicle_speed'])
		d_plan = Point3D(d_lon, d_lat, d_time)
		dflag = 0

		for d in devices:


			#情報の追加
			if d.name == d_name:
				d.append_speed(d_speed)
				d.append_plan(d_plan)
				d.append_angle(d_angle)
				dflag = 1
				break

		if dflag == 0:
			d = Device(name=d_name)
			d.startup_time = d_time
			d.append_plan(d_plan)
			d.append_speed(d_speed)
			d.append_angle(d_angle)
			d._system_time = 500                
			d.set_congestion_status(500) 
			d.use_resource = 1
			d._app_ver = random.randint(1,3)    #利用するAPの情報を付与
			devices.append(d)
			num += 1

	device_num = len(devices)

	f = open('device.congestion_binaryfile', 'wb')
	pickle.dump(devices, f)
	f.close
