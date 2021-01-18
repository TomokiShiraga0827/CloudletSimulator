from CloudletSimulator.script.normal.nearest_simulation import nearest_simulation
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

#LINE_notify("混雑度順＋継続割り当て＋最近傍")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/continue_device100.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_nearest_simulation(system_time,  MEC_resource, device_num, continue_distance, 2, path_w, how_compare)

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_device100.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)


device_num = 500

#LINE_notify("混雑度順＋最近傍")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/nearest_device500.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)

#LINE_notify("混雑度順＋継続割り当て＋最近傍")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/continue_device500.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_nearest_simulation(system_time,  MEC_resource, device_num, continue_distance, 2, path_w, how_compare)

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_device500.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)



device_num=1000

#LINE_notify("混雑度順＋最近傍")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/nearest_device1000.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)

#LINE_notify("混雑度順＋継続割り当て＋最近傍")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/continue_device1000.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_nearest_simulation(system_time,  MEC_resource, device_num, continue_distance, 2, path_w, how_compare)

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_device1000.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)





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



f_time = 50

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_ftime50.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)



f_time = 100

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_ftime100.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)



f_time = 200

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_ftime200.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)



f_time = 300

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_ftime300.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)



f_time = 400

#LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/ap_reboot/priority_ftime400.csv"
make_congestion_binary1(system_time, device_num, MEC_resource, search_distance)
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)