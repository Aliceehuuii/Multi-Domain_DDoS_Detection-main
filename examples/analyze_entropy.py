import sys
from collections import Counter
import math

def calculate_entropy(data):
    total_packets = len(data)
    ip_counter = Counter(data)

    entropy = 0.0
    for count in ip_counter.values():
        probability = float(count) / total_packets
        entropy -= probability * math.log2(probability)

    return entropy

def analyze_entropy(pcap_file):
    ip_addresses = []
    
    with open(pcap_file, 'r') as file:
        for line in file:
            ip = line.strip()
            ip_addresses.append(ip)

    entropy = calculate_entropy(ip_addresses)
    print("Renyi Entropy: {}".format(entropy))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python analyze_entropy.py <pcap_file>")
        sys.exit(1)

    pcap_file = sys.argv[1]
    analyze_entropy(pcap_file)

