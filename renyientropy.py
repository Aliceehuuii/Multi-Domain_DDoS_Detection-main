import pandas as pd
import numpy as np
import math
from scapy.all import *



def calculate_renyi_entropy(data, alpha):
    # 计算数据的概率分布
    distribution = data.value_counts() / len(data)

    # 计算α阶Renyi熵
    entropy = 1 / (1 - alpha) * np.log2((distribution ** alpha).sum())

    return entropy


def analyze_pcap(pcap_file, window_size, alpha, output_file):
    # 读取pcap文件
    packets = rdpcap(pcap_file)

    # 创建空DataFrame保存结果
    result_df = pd.DataFrame(columns=['Window Start', 'Window End', 'Renyi Entropy'])

    # 设置滑动窗口的起始和结束索引
    window_start = 0
    window_end = window_size

    while window_end <= len(packets):
        # 提取窗口内的数据包
        window_packets = packets[window_start:window_end]

        # 获取目的IP地址信息
        destination_ips = [pkt[IP].dst for pkt in window_packets if IP in pkt]

        # 计算α阶Renyi熵
        entropy = calculate_renyi_entropy(pd.Series(destination_ips), alpha)

        # 将结果添加到DataFrame中
        result_df = result_df.append({'Window Start': window_start, 'Window End': window_end, 'Renyi Entropy': entropy},
                                     ignore_index=True)

        # 更新窗口索引
        window_start += window_size
        window_end += window_size

    # 导出为.csv文件
    result_df.to_csv(output_file, index=False)


# 示例用法
pcap_file = 'goldeneye.pcap'
window_size = 1000  # 窗口大小
alpha = 2  # α的值
output_file = 'result.csv'

analyze_pcap(pcap_file, window_size, alpha, output_file)