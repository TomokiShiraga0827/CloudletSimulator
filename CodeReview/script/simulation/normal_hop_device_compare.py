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

#LINE_notify("リソース順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/resource_device100.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1, path_w, how_compare)

#LINE_notify("混雑度順")
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_device100.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)



device_num = 500

#LINE_notify("到着順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/arrival_device500.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)

#LINE_notify("リソース順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/resource_device500.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1, path_w, how_compare)

#LINE_notify("混雑度順")
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_device500.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)



device_num = 1000

#LINE_notify("到着順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/arrival_device1000.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)

#LINE_notify("リソース順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/resource_device1000.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1, path_w, how_compare)

#LINE_notify("混雑度順")
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_device1000.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)





#MECサーバの所要リソース量が変化する場合
system_time = 500
search_distance = 500
device_num = 1000
how_compare = "hop"


MEC_resource = 25

#LINE_notify("到着順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/arrival_mec25.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)

#LINE_notify("リソース順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/resource_mec25.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1, path_w, how_compare)

#LINE_notify("混雑度順")
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_mec25.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)



MEC_resource = 50

#LINE_notify("到着順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/arrival_mec50.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)

#LINE_notify("リソース順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/resource_mec50.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1, path_w, how_compare)

#LINE_notify("混雑度順")
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_mec50.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)



MEC_resource = 100

#LINE_notify("到着順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/arrival_mec100.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)

#LINE_notify("リソース順")
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/resource_mec100.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1, path_w, how_compare)

#LINE_notify("混雑度順")
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_mec100.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)





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

search_distance = 1000
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_distance1000.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)

search_distance = 1500
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_distance1500.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)

search_distance = 2000
make_congestion_binary2(system_time, device_num, MEC_resource, search_distance)
path_w = "/home/tomokishiraga/PycharmProjects/simulation/CloudletSimulator/simulation_result/hop/congestion_distance2000.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
