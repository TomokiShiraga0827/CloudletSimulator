

#normal_hop_device_compare.pyのシミュレーション

countdown = 33 #シミュレーションの実行回数

from CloudletSimulator.script.normal.nearest_simulation import nearest_simulation
from CloudletSimulator.dataset.congestion_set2 import make_congestion_binary2
from CloudletSimulator.simulator.convenient_function.line_notify import LINE_notify




#モバイル機器数が変化する場合
system_time = 500
search_distance = 500
MEC_resource = 25
how_compare = "hop"


device_num = 100

#LINE_notify("到着順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/arrival_device100.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("リソース順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/resource_device100.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("混雑度順")
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_device100.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)



device_num = 500

#LINE_notify("到着順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/arrival_device500.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("リソース順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/resource_device500.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("混雑度順")
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_device500.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)



device_num = 1000

#LINE_notify("到着順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/arrival_device1000.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("リソース順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/resource_device1000.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("混雑度順")
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_device1000.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)





#MECサーバの所要リソース量が変化する場合
system_time = 500
search_distance = 500
device_num = 1000
how_compare = "hop"


MEC_resource = 25

#LINE_notify("到着順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/arrival_mec25.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("リソース順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/resource_mec25.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("混雑度順")
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_mec25.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)



MEC_resource = 50

#LINE_notify("到着順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/arrival_mec50.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("リソース順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/resource_mec50.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("混雑度順")
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_mec50.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)



MEC_resource = 100

#LINE_notify("到着順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/arrival_mec100.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("リソース順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/resource_mec100.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("混雑度順")
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_mec100.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)



"""

#混雑度順で加算距離を変化させる場合
system_time = 500
device_num = 1000
MEC_resource = 25
how_compare = "hop"


#LINE_notify("混雑度順")
search_distance = 500
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_distance500.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

search_distance = 1000
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_distance1000.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

search_distance = 1500
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_distance1500.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

search_distance = 2000
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_distance2000.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

"""

print("normal_hop_device_compare.pyのシミュレーション完了")


#----------------------------------------------------------------------------------------------------------------------


#normal_ap_reboot_device_compare.pyのシミュレーション

#from CloudletSimulator.script.normal.nearest_simulation import nearest_simulation
from CloudletSimulator.script.normal.continue_priority_simulation import continue_priority_simulation
from CloudletSimulator.script.normal.continue_nearest_simulation import continue_nearest_simulation
from CloudletSimulator.dataset.congestion_set import make_congestion_binary1
from CloudletSimulator.simulator.convenient_function.line_notify import LINE_notify

#モバイル機器数を変化させる場合
system_time = 500
search_distance = 500    #加算距離
MEC_resource = 5
continue_distance = 500  #MECのカバー範囲(継続割り当て距離)
f_time = 200
how_compare = "ap_reboot"


device_num = 100

#LINE_notify("混雑度順＋最近傍")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/nearest_device100.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("混雑度順＋継続割り当て＋最近傍")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/continue_device100.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_nearest_simulation(system_time,  MEC_resource, device_num, continue_distance, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_device100.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)


device_num = 500

#LINE_notify("混雑度順＋最近傍")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/nearest_device500.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("混雑度順＋継続割り当て＋最近傍")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/continue_device500.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_nearest_simulation(system_time,  MEC_resource, device_num, continue_distance, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_device500.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)



device_num=1000

#LINE_notify("混雑度順＋最近傍")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/nearest_device1000.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("混雑度順＋継続割り当て＋最近傍")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/continue_device1000.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_nearest_simulation(system_time,  MEC_resource, device_num, continue_distance, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_device1000.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)





#先読み時間を変化させる場合
system_time = 500
search_distance = 500
device_num = 1000
MEC_resource = 5
continue_distance = 500
how_compare = "ap_reboot"


f_time = 10

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_ftime10.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)



f_time = 50

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_ftime50.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)



f_time = 100

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_ftime100.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)



f_time = 200

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_ftime200.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)



f_time = 300

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_ftime300.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)


f_time = 400

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_ftime400.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)
countdown = countdown - 1
print("残りのシミュレーション回数:",countdown)

print("normal_ap_reboot_device_compare.pyのシミュレーション完了")















