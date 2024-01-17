import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, f1_score
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Conv1D, MaxPooling1D, Flatten, Dense
from keras.layers import Conv1D, MaxPooling1D, LSTM, Flatten, Dense, Dropout, ZeroPadding1D
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler

def calc_renyi_entropy(data, alpha):
    # Check for missing values
    data = data.dropna()
    # Convert data to numeric type
    data = pd.to_numeric(data)
    # Calculate the probability distribution of the data
    p = np.histogram(data, bins='auto', density=True)[0]
    # Calculate the alpha order Renyi entropy
    if alpha == 1:
        entropy = -np.sum(np.log2(p) * p)
    else:
        entropy = 1 / (1 - alpha) * np.log2(np.sum(np.power(p, alpha)))
    return entropy
# Encode 'Destination IP' using one-hot encoding
encoded_ips = pd.get_dummies(dataset['Destination IP'])
alpha_order = 5
dest_ip_entropies = []
for ip in dataset['Destination IP']:
    entropy = calc_renyi_entropy(encoded_ips[ip], alpha_order)
    dest_ip_entropies.append(entropy)
dataset['DestIPEntropy'] = dest_ip_entropies

X = dataset[features].values
y = dataset['Label'].values
is_inf = np.isinf(X)  # Find infinite values
is_large = np.abs(X) > np.finfo(np.float64).max  # Find values too large for float64

# Find indices where either condition is True
invalid_indices = np.where(is_inf | is_large)

# Remove rows containing invalid values
X = np.delete(X, invalid_indices, axis=0)
y = np.delete(y, invalid_indices, axis=0)
# Data preprocessing
scaler = StandardScaler()
# scaler = MinMaxScaler()
X = scaler.fit_transform(X)
# X_scaled = scaler.fit_transform(X)
X = np.reshape(X, (X.shape[0], 1, X.shape[1]))
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

dropout_rate = 0.3
optimizer = ['adam', 'rmsprop']
learning_rate = 0.001
batch_size = 50
epochs = 20

def train_model(dropout_rate, optimizer, learning_rate, batch_size):
    model = Sequential()
    model.add(Conv1D(filters=8, kernel_size=2, strides=1, padding="SAME", activation='relu', input_shape=(None, 12)))
    model.add(MaxPooling1D(pool_size=1))
    model.add(ZeroPadding1D(padding=1))
    model.add(Conv1D(filters=16, kernel_size=2, strides=1, padding="SAME", activation='relu'))
    model.add(MaxPooling1D(pool_size=1))
    model.add(ZeroPadding1D(padding=1))
    model.add(Conv1D(filters=32, kernel_size=2, strides=1, padding="SAME", activation='relu'))
    model.add(MaxPooling1D(pool_size=1))
    model.add(Dense(16, activation='relu'))
    model.add(LSTM(16))
    model.add(Dense(units=16, activation='relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(units=1, activation='sigmoid'))
    # Compile the model with specified optimizer and learning rate
    # Get the optimizer
    for optimizer_name in optimizer:
        if optimizer_name == 'adam':
            optimizer = Adam(lr=learning_rate)

    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model with specified batch size
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2)

    y_pred_probs = model.predict(X_test)
    y_pred = (y_pred_probs > 0.5).astype(int)  # Convert probabilities to binary predictions
    confusion_mat = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("Confusion Matrix:")
    print(confusion_mat)
    print("Accuracy:", accuracy)
    print("Recall:", recall)
    print("Precision:", precision)
    print("F1 Score:", f1)

train_model(dropout_rate, optimizer, learning_rate, batch_size)