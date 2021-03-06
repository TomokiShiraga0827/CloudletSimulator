from CloudletSimulator.simulator.model.device import Device, Devices
from CloudletSimulator.simulator.model.application import Application
from CloudletSimulator.simulator.model.point import Point, Point3D, point3d_to_point
from CloudletSimulator.simulator.model.angle import Mec_name
from typing import List
import math
from math import radians, cos, sin, asin, sqrt, atan2
import collections
import numpy as np
from geopy.distance import vincenty

class MEC_server:
    num = 0                   #クラス変数
    cong_pri_app = [0, 0, 0]
    def __init__(self, resource: int, name: int, server_type: str, lon: float, lat:float, range:float, system_end_time:int):
        """
        コンストラクタ
        :param r: 所有リソース
        :param devices: 予約デバイス
        :param name: エッジサーバ名
        """
        """
        if name is None:
            Cloudlet.num += 1
            self._name = "c" + str(Cloudlet.num)
        else:
            self._name = name
        """
       
        """
        if devices is None:
            self._devices = []  # type: Devices
        else:
            self._devices = devices     # type: Devices
        self._point = point
        """
        
        self._resource = resource
        self._name = name
        self._server_type = server_type
        self._lon = lon
        self._lat = lat
        self._range = range
        self._system_end_time = system_end_time



        self._apps = []
        self._test = 0



        # ---
        #Allocated_device = namedlist('Allocated_device', ['time','device_name'])
        #Allocated_device = namedlist('Allocated_device', [('device_name', [])])
        #self._having_devices = [[namedlist('Allocated_device', [('device_name', [])])] * system_time

        self._having_devices = [None] * system_end_time      #割り当てているデバイス
        self._having_devices_count = [0] * system_end_time   #割り当てているデバイス数
        self._congestion_status = [None] * system_end_time   #
        self._congestion_flag = [None] * system_end_time     #
        self._mode = "add"           #
        self._cnt = 0                #
        self._resource_per_second =[self._resource] * system_end_time    #
        self._congestion_map = [0] * system_end_time                     #
        self._allocation_count = [0] * system_end_time       #割り当て回数
        self._reboot_count = [0] * system_end_time           #再起動回数
        self._device_distance = 0        #
        self._aggregation_name = None    #集約局(1,2,3,4)
        self._keep_count = 0             #
        self._sorted_flag = False        #

        self._app_ver = []               #実行可能なAPの種類を格納する配列

        # ----




    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value

    @property
    def point3d(self) -> Point3D:
        return self._point

    @property
    def point(self) -> Point:
        return point3d_to_point(self._point)

    @property
    def resource(self) -> int:
        return self._resource

    @resource.setter
    def resource(self, value: int) -> None:
        self._resource = value

    @property
    def devices(self) -> Devices:
        new_devices = []  # type: Devices
        for device in self._devices:
            new_devices.append(device)
        return new_devices

    @property
    def used_resource(self) -> int:
        used_resource = 0
        for device in self._devices:
            used_resource = used_resource + device.use_resource
        return used_resource

    @property
    def empty_resource(self) -> int:
        return self.resource - self.used_resource

    @property
    def apps(self) -> List[Application]:
        ret = []  # type: List[Application]
        for app in self._apps:
            ret.append(app)
        return ret

    @property
    def server_type(self) -> str:
        return self._server_type

    @property
    def lon(self) -> float:
        return self._lon

    @property
    def lat(self) -> float:
        return self._lat

    @property
    def range(self) -> float:
        return self._range

    @property
    def aggregation_station(self):
        return self._aggregation_name


    def set_aggregation_station(self, value):    #集約局をセット(1 or 2 or 3 or 4)
        self._aggregation_name = value

    #アプリケーション--------------------------------------
    @property
    def app_ver(self) -> int:
        return self._app_ver
    
    @app_ver.setter
    def app_ver(self, value) -> None :
        self.app_ver = value
    #----------------------------------------------------




    def check_resource(self, app_resource):
        """"
        リソース残量をチェックする
        :param app_resource: アプリケーションの使用リソース量
        :return: true -> 実行可能, false -> 実行不可能
        """
        if self.resource - app_resource >= 0:
            return True
        else:
            return False

    def mode_adjustment(self, device: Device, plan_index, time):
        """
        デバイスのリソースを調整するモードを返すメソッド
        ・新規でデバイスを割り当てるaddモード
        ・t-1秒に割り当てれたMECとt秒に割り当てるMECが同じ時に割り当て続けるkeepモード
        ・t-1秒に割り当てれたMECとt秒に割り当てるMECが違う時のdecreaseモード
        :param device: デバイス
        :param plan_index: デバイスのplanのindex
        :param mode:　リソース割り当てのモード
        :param old_id: t-1秒に割り当てたMECの名前
        :param time: 現在時刻t
        :return: mode
        """
        plan_index = device.plan_index
        if (self.resource > 0) or ((self.resource - device.use_resource) >= 0):
            old_distance = distance_calc(float(device.plan[plan_index-1].y),
                                     float(device.plan[plan_index-1].x), self.lat, self.lon)
            current_distance = distance_calc(float(device.plan[plan_index].y),
                                     float(device.plan[plan_index].x), self.lat, self.lon)
            current_id, device_flag = self.custom_cover_range_search(device, plan_index)

            #ここのアルゴリズムが間違えてる
            #同じIDを割り当て続ける場合
            if (device_flag == True and current_id == device.mec_name):
                print("MEC", self.name, "KEEP",", plan_index[",device.name, "]:", plan_index)
                print(device.plan[plan_index], current_distance)
                self._mode = "keep"
                device.set_mode = "keep"
                device.mec_name = self.name
                self.add_having_device(time)
                self.save_resource(time)
                device.switch_lost_flag = False

            elif device_flag == True and current_id != device.mec_name and check_add_device(device, time) == False:
                print("DECREASE")
                self._mode = "decrease"
                device.set_mode = "decrease"
                self.resource_adjustment(device)
                self._mode = "add"
                device.set_mode = "add"


                # リソースを増やす
                device.set_mode = "decrease"
                mec[device.mec_name - 1].custom_resource_adjustment(device, time)
                device.add_hop_count()
                #device.hop_calc(self)
                mec[device.mec_name - 1].save_resource(time)
                print("DECREASE")

                # リソースを減らす
                device.set_mode = "add"
                mec[ans_id].custom_resource_adjustment(device, time)
                device.add_hop_count()
                device.mec_name = mec[ans_id].name
                mec[ans_id].add_having_device(time)
                mec[ans_id].add_reboot_count(time)
                mec[ans_id].save_resource(time)
                device.switch_lost_flag = False
            else:
                self._mode = "add"
                device.set_mode = "add"

    def resource_adjustment(self, device: Device):
        """
        MECのカバー範囲内のデバイスを探すメソッド
        :param device: デバイス
        :param plan_index: デバイスの計画表（plan）のリストのインデックス
        :return memo: 発見したデバイスのID, self.resource: MECの保有リソース量, boolean:発見できたかどうかの判定
        """
        #if mode == "add":
        if device.mode == "add":
            self.resource = self.resource - device.use_resource
            #割り当てたMECをデバイスに保存
            device._mec_name = self.name
            #ホップ数カウント
            device.add_hop_count()
            print("MEC", self._name, "に","デバイス", device.name ,"追加", self.resource)
            self._test = self._test + 1
        #elif mode == "decrease":
        elif device.mode == "decrease":
            self.resource = self.resource + device.use_resource
            device.add_hop_count()
            print("デバイス移動")
            self._test = self._test - 1
        else:
            self.resource = self.resource
            print("MEC", self._name, "に", "デバイス", device.name, "KEEP", self.resource)



    def custom_resource_adjustment(self, device: Device, time):
        """
        MECのカバー範囲内のデバイスを探すメソッド
        :param device: デバイス
        :param plan_index: デバイスの計画表（plan）のリストのインデックス
        :return memo: 発見したデバイスのID, self.resource: MECの保有リソース量, boolean:発見できたかどうかの判定
        """
        #if mode == "add":
        if device.mode == "add":
            self.resource = self.resource - device.use_resource    #MECのリソース量を減らす
            if self.name == 11 and time == 98:
                print("77777")
                print(self.name, self.resource, device.use_resource)
            #self.append_having_device(device, time)
            device._allocation_check = device._allocation_check + 1   #device._allocation_checkをインクリメント　初期値0
            #割り当てたMECをデバイスに保存
            device._mec_name = self.name
            #ホップ数カウント
            #device.add_hop_count()
            print("MEC", self._name, "に","デバイス", device.name ,"追加", self.resource)
            self.add_allocation_count(time)                          #時間timeにおけるdeviceの割り当て回数をインクリメント
            self._test = self._test + 1                              #testをインクリメント 初期値0

        #elif mode == "decrease":
        elif device.mode == "decrease":
            self.resource = self.resource + device.use_resource      #MECのリソース量を増やす(戻す)
            #self.decrease_having_device(time)
            device._allocation_check = device._allocation_check - 1  #device._allocation_checkをデクリメント
            #device.add_hop_count()
            print("デバイス移動")
            self._test = self._test - 1                              #testをデクリメント
            
        #else mode == "keep":
        else:
            self.resource = self.resource
            print("MEC", self._name, "に", "デバイス", device.name, "KEEP", self.resource)



    def cover_range_search(self, device: Device, plan_index, time):
        """
        MECのカバー範囲内のデバイスを探すメソッド
        :param device: デバイス
        :param plan_index: デバイスの計画表（plan）のリストのインデックス
        :return memo: 発見したデバイスのID, self.resource: MECの保有リソース量, boolean:発見できたかどうかの判定
        """
        memo = 0
        #if mode == "add":
        if (self.resource > 0) or ((self.resource - device.use_resource) >= 0):
            distance = distance_calc(float(device.plan[plan_index].y),
                                     float(device.plan[plan_index].x), self.lat, self.lon)
            #print(self.name, device.name, distance)
            if distance <= self.range:
                memo = int(self.name)
                #print("ADD")
                #print("main",memo, distance)
                #リソース割り当て
                #self.resource_adjustment(device, mode)

                if device.mode == "add":
                    # リソースを減らす
                    device.add_hop_count()
                    device.mec_name = self.name
                    self.add_having_device(time)
                    if device._lost_flag == True and device.startup_time != time:
                        self.add_reboot_count(time)
                    # リソース割り当て
                    self.custom_resource_adjustment(device, time)
                    self.save_resource(time)
                    device.switch_lost_flag = False
                else:
                    self._cnt = self._cnt + 1
                return memo, True

            else:
                return memo, False
        else:
            return memo, False



    def custom_cover_range_search(self, device: Device, plan_index):
        """
        MECのカバー範囲内のデバイスを探すメソッド
        :param device: デバイス
        :param plan_index: デバイスの計画表（plan）のリストのインデックス
        :return memo: 発見したデバイスのID, self.resource: MECの保有リソース量, boolean:発見できたかどうかの判定
        """
        memo = 0

        if (self.resource > 0) or ((self.resource - device.use_resource) >= 0):
            distance = distance_calc(float(device.plan[plan_index].y),
                                     float(device.plan[plan_index].x), self.lat, self.lon)
            mec_name = int(self.name)
            return mec_name, True
        return 1, False


    def allocated_devices_count(self, original_resource, devices_resource):
        """
        MECに割り当てれているデバイス数を計算するメソッド
        :param original_resource: 初期設定されたMECのリソース量
        :param devices_resource: アプリケーションの使用リソース量(デバイス)
        :return MECに割り当てれているデバイス数
        """
        count = (original_resource - self.resource) / devices_resource
        return count

    def save_resource(self, time):
        """
        ある時刻tのリソース状態を保存するメソッド
        :param time: ある時刻t
        """
        self._resource_per_second[time] = self.resource

    def check_resource_adjustment(self, devices:Devices, original_resource, time):
        sum = 0
        num = self._having_devices_count
        for i in range (num):
            print()
            # 持っているデバイスのリストからデバイスの名前と同じものデバイスを呼び出す
            # 呼び出しデバイスのリソース量を加算して合計sumを作成
            # self._having_devices[i]
        #元々のリソースから合計リソースを引いた値が同じなら
        if self.resource != (original_resource - devices):
          try:
              raise ZeroDivisionError
          except:
              print("リソース量が間違っています")

    #@having_devices.setter
    def append_having_devices(self, time, value):
        self._having_devices[time] = value

    def decrease_having_device(self, time):
        self._having_devices_count[time] = self._having_devices_count[time] - 1
        #self._having_devices.pop(-1)

    #@having_device.setter
    def add_having_device(self, time):
        self._having_devices_count[time] = self._having_devices_count[time] + 1

    def add_allocation_count(self, time):
        self._allocation_count[time] = self._allocation_count[time] + 1

    def add_reboot_count(self, time):
        self._reboot_count[time] = self._reboot_count[time] + 1

    def modify_resource(self, original_resource, used_resource, time):
        if self._resource != original_resource -(self._having_devices_count[time] * used_resource):
            if(original_resource -(self._having_devices_count[time] * used_resource)) < self.resource:
                self._resource = self._resource + 1

            else:
                self._resource = self._resource - 1
            self.save_resource(time)

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

def check_between_time(device:Device, current_time):
    """
    現在時刻tがデバイスの起動時間と終了時間内か判定するメソッド
    :param device:　デバイス
    :param current_time: 現在時刻t
    :return : 判定結果
    """
    if(device.startup_time <= current_time and current_time <= device.shutdown_time):
        return True
    else:
        return False

def check_add_device(device:Device, time):
    """
    あるデバイスが新規の追加なのか他のMECから移動なのかを判定
    :param device: デバイス
    :param time: 現在時刻t
    :return True: 新規の追加なら真, Falseなら他のMECからの移動なら偽
    """
    #新規の追加か移動なのかの判定が必要
    if device.startup_time == time:
        return True
    else:
        return False

def check_plan_index(current_plan_index, moving_time_length):
    """
    ある時刻のplan_indexが指しているindexがデバイスの稼働時間を超えているか判定するメソッド
    :param current_plan_index: 今指しているplanのindex
    :param moving_time_length: あるデバイスの稼働時間の長さ
    :return True: 指しているindexが稼働時間を超えてなければ真, False: 稼働時間を超えているなら偽
    """
    if current_plan_index < moving_time_length:
        True
    else:
        False

def check_allocation(time, mec_num, mec_resource, having_device_resource_sum, mec_resource_sum):
    """
    ある時刻tのMECへのリソース割り当てができているかチェックするメソッド
    :param time: ある時刻t
    :param mec_num: MECの数
    :param mec_resource: MECの１つの元々のリソース量
    :param having_device_resource_sum: あるMECに割り当てられているデバイスの要求リソース量
    :param mec_resource_sum: ある時刻tのMECの合計残存リソース量
    """
    original_resource = mec_resource * mec_num
    numerical_goal = original_resource - having_device_resource_sum
    if numerical_goal == mec_resource_sum:
        print("time:",time, " correct")
    else:
        print("time:", time, " error")



MEC_servers = List[MEC_server]







def copy_to_mec(mecs:MEC_servers, save_devices, time):
    """
    ある時刻tのMECに一時的に保存していた割り当てたデバイスをコピーするメソッド
    :param mecs: MECサーバ群
    :param save_devices: ある時刻tに一時的に保存していたMEC群へ割り当てたデバイスのリスト
    :param time: ある時刻t
    """
    mec_num = len(mecs)
    for index in range(mec_num):
        if save_devices[index] is not None:
            # print("save_devices:", save_devices[index], ", MEC_ID:", mecs[index].name)
            mecs[index].append_having_devices(time, save_devices[index])



def application_reboot_rate(mecs: MEC_servers, system_end_time):
    """
    AP起動処理発生率の合計
    :param mecs: MECサーバ群
    :param system_end_time: システムの終了時間
    :return  シミュレーション中のAP起動処理発生率の合計
    """
    #アプリケーションの再起動発生率計算
    allocation_sum = allocation_count_sum(mecs,system_end_time)         #割り当て回数
    reboot_sum = reboot_count_sum(mecs, system_end_time)                #サーバの切替回数
    reboot_rate = reboot_sum / allocation_sum
    print("reboot_sum", reboot_sum, "allocation_sum",allocation_sum)
    return reboot_rate
    print()

def allocation_count_sum(mecs: MEC_servers, system_end_time):
    """
    デバイスをMECへ割り当てた合計回数を計算するメソッド
    :param mecs: MECサーバ群
    :param system_end_time: システムの終了時間
    :return  シミュレーション中の割り当て回数の合計
    """
    sum = 0
    mec_num = len(mecs)
    keep = 0
    for t in range(system_end_time):
        for index in range(mec_num):
            sum = sum + mecs[index]._allocation_count[t]     #allocation_count:割り当て回数
    for index in range(mec_num):
        keep = keep + mecs[index]._keep_count
    print("KEEP_COUNT", keep)
    return sum

def reboot_count_sum(mecs: MEC_servers, system_end_time):
    """
    サーバの切替回数の合計
    :param mecs: MECサーバ群
    :param system_end_time: システムの終了時間
    :return  シミュレーション中のサーバの切替回数の合計
    """
    #アプリケーションの起動回数計算
    sum = 0
    mec_num = len(mecs)
    for t in range(system_end_time):
        for index in range(mec_num):
            sum = sum + mecs[index]._reboot_count[t]     #reboot_count:サーバの切替回数
    return sum





def monitoring_resource(mecs:MEC_servers, MEC_resource, used_resource,time):
    mec_num = len(mecs)
    for m in range(mec_num):
        if (MEC_resource - (mecs[m]._having_devices[time] * used_resource)) != mecs[m]._resource_per_second[time]:
            sys.exit()
