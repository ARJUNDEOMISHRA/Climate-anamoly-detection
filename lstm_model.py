import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# Train LSTM model
def train_lstm(df):
    # Use temperature data
    data = df["temperature"].values.reshape(-1, 1)

    # Normalize data
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    # Create sequences
    X, y = [], []
    seq_length = 10

    for i in range(len(data_scaled) - seq_length):
        X.append(data_scaled[i:i + seq_length])
        y.append(data_scaled[i + seq_length])

    X, y = np.array(X), np.array(y)

    # Build LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=False, input_shape=(seq_length, 1)))
    model.add(Dense(1))

    # Compile model
    model.compile(optimizer="adam", loss="mse")

    # Train model
    model.fit(X, y, epochs=5, batch_size=16, verbose=0)

    return model, scaler, seq_length


# Predict future values
def predict_future(model, scaler, df, seq_length):
    data = df["temperature"].values.reshape(-1, 1)
    data_scaled = scaler.transform(data)

    # Take last sequence
    last_sequence = data_scaled[-seq_length:]

    predictions = []

    # Predict next 10 days
    for _ in range(10):
        pred = model.predict(last_sequence.reshape(1, seq_length, 1), verbose=0)
        predictions.append(pred[0][0])

        # Update sequence
        last_sequence = np.append(last_sequence[1:], pred, axis=0)

    # Convert back to original scale
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    return predictions.flatten()