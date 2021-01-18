from CloudletSimulator.simulator.model.device import Devices

# 要求リソース量の降順にソートする
def reverse_resource_sort(devices:Devices):
    """
    デバイスの要求リソース量を基準に降順にソートするメソッド
    :param device: デバイス
    :param mec: MECサーバ群
    :param plan_index: デバイスのplanのindex
    :param cover_range: 基地局のカバー範囲
    :param time: 現在時刻t
    :return: 割り当てたans_idをTrueと共に返す, 割り当てられなかった時はFalseを返す
    """
    devices = sorted(devices, key=lambda d:d.use_resource, reverse=True)
    return devices
