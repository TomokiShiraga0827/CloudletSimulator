from CloudletSimulator.simulator.model.edge_server import MEC_servers, MEC_server

def set_aggregation_station(mecs:MEC_servers):
    """
    MECを管理する集約局をセットするメソッド
    中央の緯度経度を元に地図を４個分に均等に分けて集約局を割り振る
    :param mecs: MECサーバ群
    """
    mec_num = len(mecs)
    central_lat = 34.6664535
    central_lon = 133.91122

    #133.885195 34.629142 133.986394 34.714251

    #central_lat = 34.663377
    # 正式
    #central_lat = 34.664405 # 正式 kuruma1
    #central_lat = 34.642504 # kuruma3の時の地図
    #central_lon = 133.917336
    #central_lon = 133.91157 # 正式 kuruma1
    #central_lon = 133.90286 # kuruma3の時の地図
    for m in range(mec_num):
        # 左下
        if mecs[m].lat <= central_lat and mecs[m].lon <= central_lon:
            mecs[m].set_aggregation_station(1)
        # 右下
        elif mecs[m].lat <= central_lat and central_lon <= mecs[m].lon:
            mecs[m].set_aggregation_station(2)
        # 左上
        elif central_lat <= mecs[m].lat and mecs[m].lon <= central_lon:
            mecs[m].set_aggregation_station(3)
        # 右上
        elif central_lat <= mecs[m].lat and central_lon <= mecs[m].lon:
       # else:
            mecs[m].set_aggregation_station(4)
