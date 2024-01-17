import numpy as np

from app.model.Features import Features


class FeaturesCalculator:
    def __init__(self, sample, target_ip, sampling_period):
        self.sample = sample
        self.target_ip = target_ip
        self.sampling_period = sampling_period

    def get_features(self):
        return Features(self.__get_sips(), self.__get_appf(), self.__get_abpf(),
                        self.__get_adpf(), self.__get_ppf())

    def __get_sips(self):
        count_src_ips = 0
        for flow in self.sample:
            if flow.get_dst_ip() == self.target_ip:
                count_src_ips += 1
        return count_src_ips / self.sampling_period

    def __get_appf(self):
        packet_count = []
        for flow in self.sample:
            packet_count.append(flow.get_packet_count())
        return np.std(packet_count)

    def __get_abpf(self):
        byte_count = []
        for flow in self.sample:
            byte_count.append(flow.get_byte_count())
        return np.std(byte_count)

    def __get_adpf(self):
        return self.sampling_period / len(self.sample)

    def __get_ppf(self):
        n_int_flows = 0
        for uni_flow in self.sample:
            for bi_flow in self.sample:
                if uni_flow.get_src_ip() == bi_flow.get_dst_ip() and uni_flow.get_dst_ip() == bi_flow.get_src_ip():
                    n_int_flows += 1
        return float(n_int_flows) / len(self.sample)
