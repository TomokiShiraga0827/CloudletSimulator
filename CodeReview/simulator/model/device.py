from CloudletSimulator.simulator.model.application import Application
from CloudletSimulator.simulator.model.route import Route, create_route
from CloudletSimulator.simulator.model.point import Point,Point3D, random_two_point
from CloudletSimulator.simulator.model.angle import Angle, Speed, Mec_name
from typing import List
from tqdm import tqdm
import math
import collections


class Device:

    num = 0  # type: int

    def __init__(self, name: str=None, startup_time: int=0, resource: int=0,plan: Route=None,
                 apps: List[Application]=None, angle: List[Angle]=None, speed: List[Speed]=None, mec_name: List[Mec_name]=None, system_time: int=0):
        if name is None:
            Device.num += 1
            self._name = "d" + str(Device.num)
        else:
            Device.num += 1
            self._name = name

        self._startup_time = startup_time

        if resource is None:
            self._resource = 1
        else:
            self._resource = resource

        if plan is None:
            self._plan = []
            self._allocation_plan = []
        else:
            self._plan = plan
            self._allocation_plan = [None for i in range(len(self._plan))]  # type: List[Point]

        if apps is None:
            self._apps = []   # type: List[Application]
        else:
            self._apps = apps

        if angle is None:
            self._angle = []
        else:
            self._angle = angle

        if speed is None:
            self._speed = []
        else:
            self._speed = speed

        if mec_name is None:
            self._mec_name = [] #type: List[Mec_name]
        else:
            self._mec_name = mec_name

        self._system_time = system_time

        # 毎秒ごとの混雑度を保存するためのリスト
        #if system_time == 0:
            #self._system_time = []
        #else:

        self._plan_index = 0
        #self._congestion_status = [0] * 200
        self._congestion_status = [0]
        self._hop_count = 0
        self._mode = "add"
        self._lost_flag = False
        self._allocation_check = 0
        self._continue_count = 0
        self._MEC_distance = 0
        self._old_mec_name = None
        self._hop = None           #後に配列で定義
        self._first_flag = True
        self._aggregation_name = None
        self._allocation_plan = None
        self._three_count = 0
        self._five_count = 0
        self._min_distance = 10000000
        self._max_distance = 0
        self._distance = None
        self._added_distance = None  #後に配列で定義

        self._app_ver = None






    @property  #直接getterの処理を行う
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def startup_time(self) -> int:
        return self._startup_time

    @startup_time.setter
    def startup_time(self, value: int) -> None:
        self._startup_time = value

    @property
    def use_resource(self) -> int:
        return self._resource

    @use_resource.setter
    def use_resource(self, value) -> None:
        self._resource = value

    #アプリケーション--------------------------------------
    @property
    def app_ver(self) -> int:
        return self._app_ver
    
    @app_ver.setter
    def app_ver(self, value) -> None :
        self.app_ver = value
    #----------------------------------------------------

    @property
    def moving_time(self) -> int:
        return len(self._plan)

    @property
    def shutdown_time(self) -> int:
        return self.startup_time + self.moving_time - 1

    @property
    def plan(self) -> Route:
        return self._plan.copy()

    @property
    def angle(self) -> Angle:
        return self._angle.copy()

    @property
    def speed(self) -> Speed:
        return self._speed.copy()

    @speed.setter
    def speed(self, value: Speed) -> None:
        self._speed = value

    @angle.setter
    def angle(self, value: Angle) -> None:
        self._angle = value

    @plan.setter
    def plan(self, value: Route) -> None:
        self._plan = value

    @property
    def mec_name(self) -> List[Mec_name]:
        return self._mec_name

    @mec_name.setter
    def mec_name(self, Value: List[Mec_name]) -> None:
        self._mec_name = Value

    @property
    def apps(self) -> List[Application]:
        ret = []    # type: List[Application]
        for app in self._apps:
            ret.append(app)
        return ret

    @apps.setter
    def apps(self, value: List[Application]):
        self._apps = value

    @property
    def system_time(self) -> int:
        return self._system_time

    @name.setter
    def system_time(self, value: int) -> None:
        self._system_time = value

    @property
    def hop_count(self) -> int:
        return self._hop_count

    @property
    def hop(self):
        return self._hop


    @property
    def mode(self) -> str:
        return self._mode

    @mode.setter
    def set_mode(self, value) -> str:
        self._mode = value

    @property
    def plan_index(self) -> int:
        return self._plan_index

    @plan_index.setter
    def add_plan_index(self) -> int:
        self._plan_index = self._plan_index + 1

    @property
    def lost_flag(self) -> bool:
        return self._lost_flag

    @lost_flag.setter
    def switch_lost_flag(self, value:bool) -> bool:
        self._lost_flag = value



    def add_hop_count(self) -> int:
        if self._mode == "add":
            if self._hop_count == 0:
                self._hop_count = self._hop_count + 1 # 新規割り当て
            else:
                self._hop_count = self._hop_count + 2  # 切替（割り振った後）時
        elif self._mode == "decrease":
            self._hop_count = self._hop_count + 2 #切替（割り振り前）
        else:
            self._hop_count = self._hop_count


    def check_allocation(self):
        if self._allocation_check == 1 or self._allocation_check == 0:
            print("OK")
        else:
            try:
                raise ZeroDivisionError
            except:
                print("リソース量が間違っています")

    def set_congestion_status(self, system_time):
        self._congestion_status = [0] * system_time

    #Deviceのインスタンスに情報を追加するappendメソッド
    def append_plan(self, value:Point3D) -> None:
        self._plan.append(value)
    def append_mec(self, value: Mec_name) -> None:
        self._mec_name.append(value)
    def append_angle(self, value:Angle) -> None:
        self._angle.append(value)
    def append_speed(self, value:Speed) -> None:
        self._speed.append(value)
    def append_app(self, app: Application) -> None:
        self._apps.append(app)


    def remove_app(self, app: Application) -> None:
        del self._apps[self._apps.index(app)]

    def appret(self, namestr: str) -> bool:
        for app in self._apps:
            if app.name != namestr:
                return False
        return True

    def app_name(self):
        for app in self._apps:
            apn = app.name
        return apn

    def is_poweron(self, time: int) -> bool:
        if self.startup_time <= time < self.shutdown_time:
            return True
        else:
            return False

    def get_pos(self, time: int) -> Point:
        return self.plan[time - self.startup_time]

    def get_allocation_point(self, time: int) -> Point:
        p = self._allocation_plan[time - self.startup_time]
        return p

    def set_allocation_point(self, time: int, pos: Point):
        self._allocation_plan[time - self.startup_time] = pos

    def ret_ds_pri(self) -> int:
        return self.ds_pri

    def set_ds_pri(self, value: int):
        self.ds_pri = value

    def add_ds_pri(self, value: int):
        self.ds_pri += value

    def set_continue_count(self, value: str):
        if value == "add":
            self._continue_count = self._continue_count + 1
        else:
            self._continue_count = 0
    def set_MEC_distance(self, value: int):
        self._MEC_distance = [100000000000000] * value
        
#    @property
    #def continue_count(self):
        #return self._continue_count







#Devices
Devices = List[Device]








def max_distance_search(devices: Devices):
    """
    デバイス群から最大割り当て距離を計算するメソッド
    :param devices: ある時刻tのデバイス群
    :return maximum: 最小割り当て距離, devices[].name: その割り当て距離を持つデバイスの名前
    """
    device_num = len(devices)
    maximum = 0
    for d in range(device_num):
        if devices[d]._max_distance is not None:
            if maximum < devices[d]._max_distance:
                maximum = devices[d]._max_distance
    return maximum

def min_distance_search(devices: Devices):
    """
    デバイス群から最小割り当て距離を計算するメソッド
    :param devices: ある時刻tのデバイス群
    :return maximum: 最小割り当て距離, devices[].name: その割り当て距離を持つデバイスの名前
    """
    device_num = len(devices)
    minimum = 10000000
    for d in range(device_num):
        if devices[d]._min_distance is not None:
            if minimum > devices[d]._min_distance:
                minimum = devices[d]._min_distance
            #index = d
    return minimum

def average_distance_calc(devices: Devices):
    """
    デバイス群から平均割り当て距離を計算するメソッド
    :param devices: ある時刻tのデバイス群
    :return average: 平均ホップ数
    """
    device_num = len(devices)
    cnt = 0
    sum = 0
    average = 0
    for d in range(device_num):
        if devices[d]._distance is not None:
            for distance in devices[d]._distance:
                if distance > 0:
                    sum = sum + distance
                    cnt = cnt + 1
    if cnt != 0:
        average = sum / cnt
    return average

def max_hop_search(devices: Devices):
    """
    デバイス群から最大ホップ数（最大割り当て距離）を計算するメソッド
    :param devices: ある時刻tのデバイス群
    :return maximum: 最大ホップ数, devices[].name: そのホップ数を持つデバイスの名前
    """
    device_num = len(devices)
    maximum = 0
    for d in range(device_num):
        if devices[d].hop is not None:
            if maximum < max(devices[d].hop):
                maximum = max(devices[d].hop)
    return maximum

def min_hop_search(devices: Devices):
    """
    デバイス群から最小ホップ数（最小割り当て距離）を計算するメソッド
    :param devices: ある時刻tのデバイス群
    :return maximum: 最小ホップ数, devices[].name: そのホップ数を持つデバイスの名前
    """
    device_num = len(devices)
    minimum = 10000000
    for d in range(device_num):
        if devices[d].hop is not None:
            if minimum > min(devices[d].hop):
                minimum = min(devices[d].hop)
            #index = d
    return minimum

def average_hop_calc(devices: Devices):
    """
    デバイス群から平均ホップ数（平均割り当て距離）を計算するメソッド
    :param devices: ある時刻tのデバイス群
    :return average: 平均ホップ数
    """
    device_num = len(devices)
    cnt = 0
    sum = 0
    average = 0
    for d in range(device_num):
        if devices[d].hop is not None:
            for h in devices[d].hop:
                sum = sum + h
                cnt = cnt + 1
    if cnt != 0:
        average = sum / cnt
    return average

def device_index_search(devices:Devices, device_names):
    """
    MECの持っているデバイスの名前からデバイスのインデックスを探すメソッド
    :param devices: ある時刻tのデバイス群
    :param device_names: MECの持っているデバイスの名前群
    :return device_index: MECの持っているデバイスのインデックス群
    """
    device_num = len(devices)
    tmp_names = [None]
    for d in range(device_num):                  #デバイス名が全て入った比較用の配列を用意
        if tmp_names is None:
            tmp_names = [devices[d].name]
        else:
            tmp_names.append(devices[d].name)

    #----------------------------------------
    length = len(tmp_names)
    for i in range(length):
        if tmp_names[0] is None:
            tmp_names.pop(0)
    #----------------------------------------

    device_index = [None]
    for name in device_names:             #tmp_namesの配列から目的のデバイス名を探してそのインデックスを格納していく(時刻tにおけるsorted_deviceのインデックス)
        if device_index is None:
            device_index = [tmp_names.index(name)]
        else:
            device_index.append(tmp_names.index(name))

    #----------------------------------------
    length = len(device_index)
    for i in range(length):
        if device_index[0] is None:
            device_index.pop(0)
    #----------------------------------------

    return device_index

def device_resource_calc(devices:Devices, device_index):
    """
    ある時刻tのMECの持っているデバイスの総要求リソース量を計算するメソッド
    :param devices: ある時刻tのデバイス群
    :param  MECの持っているデバイスのインデックス群
    :return average: 平均ホップ数
    """
    sum = 0
    for d_index in device_index:
        #print(d_index)
        if d_index is not None:
            sum = sum + devices[d_index].use_resource   #device_indexのデバイスの要求リソース量を追加
    return sum


