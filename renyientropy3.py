# Import necessary libraries
import pandas as pd
import numpy as np
from collections import Counter

# Load the udp.csv dataset
df = pd.read_csv('collect traffic.csv')

# Select 'Destination IP' feature as input
X = df['DestinationIP'].values

# Define detection window size and alpha order
window_size = 500
alpha_order = 0.5

# Define function to calculate alpha order Renyi entropy
def renyi_entropy(alpha, counts, total):
    prob = counts / float(total)
    return 1.0 / (1.0 - alpha) * np.log2(np.sum(prob ** alpha))

# Define function to detect DDoS attacks
def detect_ddos(X, window_size, alpha_order, threshold):
    # Define variables for counting packets and attacks
    packets = Counter()
    attacks = Counter()

    # Iterate through all packets
    for i in range(len(X)):
        ip = X[i]

        # Add current packet to counter
        packets[ip] += 1

        # Check if detection window is reached
        if i >= window_size:
            # Remove oldest packet from counter
            oldest_ip = X[i - window_size]
            packets[oldest_ip] -= 1
            if packets[oldest_ip] == 0:
                del packets[oldest_ip]

            # Calculate alpha order Renyi entropy for current window
            counts = np.array(list(packets.values()))
            total = counts.sum()
            renyi = renyi_entropy(alpha_order, counts, total)

            # If Renyi entropy exceeds threshold, mark as attack
            if renyi > threshold:
                attacks[ip] += 1

    # Return list of attacked IPs
    return list(attacks.keys())

# Define threshold for detecting DDoS attacks
threshold = 1.4

# Detect DDoS attacks using alpha order Renyi entropy model
attacked_ips = detect_ddos(X, window_size, alpha_order, threshold)

# Evaluate performance of the model using confusion matrix, accuracy, recall, precision, and F1 score
true_positives = len(attacked_ips)
false_positives = len(set(attacked_ips) - set(df['DestinationIP'].unique()))
false_negatives = len(df['DestinationIP'].unique()) - true_positives
true_negatives = len(df) - (true_positives + false_positives + false_negatives)

accuracy = (true_positives + true_negatives) / len(df)
recall = true_positives / (true_positives + false_negatives)
precision = true_positives / (true_positives + false_positives)
f1_score = 2 * (precision * recall) / (precision + recall)

confusion_matrix = pd.DataFrame({
    'Actual Attack': [true_positives, false_negatives],
    'Actual Normal': [false_positives, true_negatives]
}, index=['Predicted Attack', 'Predicted Normal'])

print('Confusion Matrix:')
print(confusion_matrix)
print('Accuracy:', accuracy)
print('Recall:', recall)
print('Precision:', precision)
print('F1 Score:', f1_score)